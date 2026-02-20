import sys
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QFileDialog
)
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


class CollaboratorsList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Colaboradores RDC")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Contadores
        header = QHBoxLayout()
        self.label_fixos = QLabel("Fixos: 0")
        self.label_diaristas = QLabel("Diaristas: 0")
        header.addWidget(self.label_fixos)
        header.addStretch()
        header.addWidget(self.label_diaristas)
        layout.addLayout(header)

        # Formulário
        form_layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.fornecedora_input = QComboBox()
        self.fornecedora_input.addItems(["", "D0", "Polly"])
        self.tipo_input = QComboBox()
        self.tipo_input.addItems(["", "F", "D"])
        self.obs_input = QLineEdit()

        for label_text, widget in [
            ("Nome", self.nome_input),
            ("Fornecedora AG", self.fornecedora_input),
            ("Fixo / Diarista", self.tipo_input),
            ("OBS", self.obs_input),
        ]:
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(150)
            row.addWidget(label)
            row.addWidget(widget)
            form_layout.addLayout(row)

        layout.addLayout(form_layout)

        # Botão adicionar
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.add_collaborator)
        layout.addWidget(btn_add)

        # Tabela
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["N°", "Nome", "Fornecedora/AG", "Fixo/Diarista", "OBS"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # Botões
        buttons = QHBoxLayout()

        btn_save = QPushButton("Salvar CSV")
        btn_save.clicked.connect(self.save_csv)
        buttons.addWidget(btn_save)

        btn_load = QPushButton("Carregar CSV")
        btn_load.clicked.connect(self.load_csv)
        buttons.addWidget(btn_load)

        btn_print = QPushButton("Imprimir")
        btn_print.clicked.connect(self.print_list)
        buttons.addWidget(btn_print)

        btn_pdf = QPushButton("Gerar PDF")
        btn_pdf.clicked.connect(self.generate_pdf_report)
        buttons.addWidget(btn_pdf)

        layout.addLayout(buttons)

        self.next_number = 1

    # ==========================
    # Funções
    # ==========================

    def update_counters(self):
        fixos = 0
        diaristas = 0

        for row in range(self.table.rowCount()):
            tipo_item = self.table.item(row, 3)
            if tipo_item:
                if tipo_item.text() == "F":
                    fixos += 1
                elif tipo_item.text() == "D":
                    diaristas += 1

        self.label_fixos.setText(f"Fixos: {fixos}")
        self.label_diaristas.setText(f"Diaristas: {diaristas}")

    def add_collaborator(self):
        nome = self.nome_input.text().strip()
        if not nome:
            QMessageBox.warning(self, "Erro", "Preencha o Nome!")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        data = [
            str(self.next_number),
            nome,
            self.fornecedora_input.currentText(),
            self.tipo_input.currentText(),
            self.obs_input.text().strip()
        ]

        for col, value in enumerate(data):
            self.table.setItem(row, col, QTableWidgetItem(value))

        self.next_number += 1
        self.update_counters()

        self.nome_input.clear()
        self.obs_input.clear()

    # ==========================
    # CSV
    # ==========================

    def save_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar CSV", "", "CSV (*.csv)")
        if not file_name:
            return

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["N°", "Nome", "Fornecedora/AG", "Fixo/Diarista", "OBS"])

            for row in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(row, col).text()
                    for col in range(5)
                ])

        QMessageBox.information(self, "Sucesso", "Arquivo salvo!")

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Carregar CSV", "", "CSV (*.csv)")
        if not file_name:
            return

        self.table.setRowCount(0)
        self.next_number = 1

        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row_data in reader:
                row = self.table.rowCount()
                self.table.insertRow(row)

                for col, value in enumerate(row_data):
                    self.table.setItem(row, col, QTableWidgetItem(value))

                self.next_number += 1

        self.update_counters()
        QMessageBox.information(self, "Sucesso", "Arquivo carregado!")

    # ==========================
    # Impressão / PDF
    # ==========================

    def print_list(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.draw_report(printer)

    def generate_pdf_report(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", "", "PDF (*.pdf)")
        if not file_name:
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_name)

        self.draw_report(printer)
        QMessageBox.information(self, "Sucesso", "PDF gerado!")

    def draw_report(self, printer):
        painter = QPainter(printer)

        page_rect = printer.pageRect(QPrinter.Unit.Point)

        painter.fillRect(page_rect, QColor("white"))
        painter.setPen(QColor("black"))

        margin = 60
        y = int(margin)
        line_height = 20

        page_width = int(page_rect.width()) - 2 * margin

        font_title = QFont("Arial", 14, QFont.Weight.Bold)
        font_normal = QFont("Arial", 10)

        painter.setFont(font_title)
        painter.drawText(int(margin), y, int(page_width), 30,
                         Qt.AlignmentFlag.AlignCenter,
                         "Lista de Colaboradores RDC")

        y += 40
        painter.setFont(font_normal)

        for row in range(self.table.rowCount()):
            linha = "   ".join(
                self.table.item(row, col).text()
                for col in range(5)
            )
            painter.drawText(int(margin), int(y), linha)
            y += line_height

        y += 30

        fixos = int(self.label_fixos.text().replace("Fixos: ", ""))
        diaristas = int(self.label_diaristas.text().replace("Diaristas: ", ""))
        total = fixos + diaristas

        painter.drawText(int(margin), int(y), f"Data: {datetime.now().strftime('%d/%m/%Y')}")
        y += 20
        painter.drawText(int(margin), int(y), f"Quantidade Fixo: {fixos}")
        y += 20
        painter.drawText(int(margin), int(y), f"Quantidade Diarista: {diaristas}")
        y += 20
        painter.drawText(int(margin), int(y), f"Total: {total}")

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CollaboratorsList()
    window.show()
    sys.exit(app.exec())