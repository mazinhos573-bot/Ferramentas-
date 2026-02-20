import sys
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QFileDialog
)
from PyQt6.QtGui import QPalette, QColor, QFont, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


class CollaboratorsList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Colaboradores RDC")
        self.resize(1000, 700)

        # Tema matrix/hacker
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            * {
                color: #00ff41;
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                background-color: #0d1a0d;
                border: 1px solid #00cc33;
                padding: 5px;
            }
            QTableWidget {
                background-color: #000000;
                gridline-color: #004d1a;
                alternate-background-color: #0a140a;
                selection-background-color: #004d1a;
            }
            QHeaderView::section {
                background-color: #001a00;
                color: #00ff41;
                border: 1px solid #00cc33;
                padding: 6px;
            }
            QPushButton {
                background-color: #001a00;
                border: 1px solid #00cc33;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #004d1a;
            }
            QLabel#contador {
                color: #00ff88;
                font-size: 15px;
                font-weight: bold;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ── Cabeçalho / Contadores ───────────────────────────────
        header_layout = QHBoxLayout()
        self.label_fixos = QLabel("Fixos: 0")
        self.label_diaristas = QLabel("Diaristas: 0")
        self.label_fixos.setObjectName("contador")
        self.label_diaristas.setObjectName("contador")

        header_layout.addWidget(self.label_fixos)
        header_layout.addStretch()
        header_layout.addWidget(self.label_diaristas)

        main_layout.addLayout(header_layout)

        # ── Formulário de entrada ───────────────────────────────
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        inputs = [
            ("Nome ....................", QLineEdit, "nome"),
            ("Fornecedora AG .........", QComboBox, "fornecedora"),
            ("Fixo / Diarista ........", QComboBox, "tipo"),
            ("OBS .....................", QLineEdit, "obs"),
        ]

        for label_text, widget_class, attr_name in inputs:
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(180)

            if widget_class == QComboBox:
                w = QComboBox()
                if attr_name == "fornecedora":
                    w.addItems(["", "D0", "Polly"])
                else:
                    w.addItems(["", "F", "D"])
            else:
                w = QLineEdit() 

            row.addWidget(label)
            row.addWidget(w, stretch=1)
            form_layout.addLayout(row)

            setattr(self, f"{attr_name}_input", w)

        # Botões
        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("Adicionar / Atualizar")
        self.add_button.clicked.connect(self.add_or_update_collaborator)
        btn_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("Limpar campos")
        self.clear_button.clicked.connect(self.clear_inputs)
        btn_layout.addWidget(self.clear_button)

        form_layout.addLayout(btn_layout)
        main_layout.addLayout(form_layout)

        # ── Tabela ───────────────────────────────────────────────
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nº", "Nome", "Fornecedora AG", "Fixo/Diarista", "OBS"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        # Permite edição ao clicar
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | 
                                  QTableWidget.EditTrigger.AnyKeyPressed)
        self.table.itemChanged.connect(self.on_item_changed)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        main_layout.addWidget(self.table, stretch=1)

        # Botões de ações
        actions_layout = QHBoxLayout()
        self.print_button = QPushButton("Imprimir Lista (A4)")
        self.print_button.clicked.connect(self.print_list)
        actions_layout.addWidget(self.print_button)

        self.save_csv_button = QPushButton("Salvar em CSV")
        self.save_csv_button.clicked.connect(self.save_to_csv)
        actions_layout.addWidget(self.save_csv_button)

        self.load_csv_button = QPushButton("Carregar de CSV")
        self.load_csv_button.clicked.connect(self.load_from_csv)
        actions_layout.addWidget(self.load_csv_button)

        self.report_button = QPushButton("Gerar Relatório PDF")
        self.report_button.clicked.connect(self.generate_pdf_report)
        actions_layout.addWidget(self.report_button)

        main_layout.addLayout(actions_layout)

        # Rodapé
        footer = QLabel("LDC by EricLM  •  2025/2026")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #006600; font-size: 12px;")
        main_layout.addWidget(footer)

        self.next_number = 1
        self.selected_row = -1

    def update_counters(self):
        fixos = 0
        diaristas = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 3)
            if item and item.text() == "F":
                fixos += 1
            elif item and item.text() == "D":
                diaristas += 1
        
        self.label_fixos.setText(f"Fixos: {fixos}")
        self.label_diaristas.setText(f"Diaristas: {diaristas}")

    def clear_inputs(self):
        self.nome_input.clear()
        self.obs_input.clear()
        self.fornecedora_input.setCurrentIndex(0)
        self.tipo_input.setCurrentIndex(0)
        self.nome_input.setFocus()
        self.selected_row = -1
        self.add_button.setText("Adicionar à Lista")

    def add_or_update_collaborator(self):
        nome = self.nome_input.text().strip()
        if not nome:
            QMessageBox.warning(self, "Campo obrigatório", "Preencha o Nome!")
            self.nome_input.setFocus()
            return

        fornecedora = self.fornecedora_input.currentText()
        tipo = self.tipo_input.currentText()
        obs = self.obs_input.text().strip()

        if self.selected_row >= 0:
            # Atualizar linha existente
            self.table.setItem(self.selected_row, 1, QTableWidgetItem(nome))
            self.table.setItem(self.selected_row, 2, QTableWidgetItem(fornecedora))
            self.table.setItem(self.selected_row, 3, QTableWidgetItem(tipo))
            self.table.setItem(self.selected_row, 4, QTableWidgetItem(obs))
            self.clear_inputs()
            self.update_counters()
            return

        # Adicionar novo
        row = self.table.rowCount()
        self.table.insertRow(row)

        items = [
            QTableWidgetItem(str(self.next_number)),
            QTableWidgetItem(nome),
            QTableWidgetItem(fornecedora),
            QTableWidgetItem(tipo),
            QTableWidgetItem(obs)
        ]

        for col, item in enumerate(items):
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, col, item)

        self.next_number += 1
        self.clear_inputs()
        self.update_counters()

    def on_selection_changed(self):
        selected = self.table.selectedItems()
        if not selected:
            self.clear_inputs()
            return

        row = selected[0].row()
        self.selected_row = row
        self.add_button.setText("Atualizar linha selecionada")

        nome = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
        fornec = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
        tipo = self.table.item(row, 3).text() if self.table.item(row, 3) else ""
        obs = self.table.item(row, 4).text() if self.table.item(row, 4) else ""

        self.nome_input.setText(nome)
        self.fornecedora_input.setCurrentText(fornec)
        self.tipo_input.setCurrentText(tipo)
        self.obs_input.setText(obs)

    def on_item_changed(self, item):
        if item.column() == 3:  # só atualiza contadores se mudar Fixo/Diarista
            self.update_counters()

    def save_to_csv(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Lista vazia", "Não há dados para salvar.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar em CSV", "", "CSV Files (*.csv)")
        if not file_name:
            return

        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Nº", "Nome", "Fornecedora AG", "Fixo/Diarista", "OBS"])
            for row in range(self.table.rowCount()):
                data = [self.table.item(row, col).text() for col in range(5)]
                writer.writerow(data)

        QMessageBox.information(self, "Sucesso", "Dados salvos com sucesso!")

    def load_from_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Carregar de CSV", "", "CSV Files (*.csv)")
        if not file_name:
            return

        self.table.setRowCount(0)
        self.next_number = 1

        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Pular cabeçalho
                for row_data in reader:
                    if len(row_data) != 5:
                        continue
                    _, nome, fornecedora, tipo, obs = row_data  # Ignora Nº do CSV e regenera
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    items = [
                        QTableWidgetItem(str(self.next_number)),
                        QTableWidgetItem(nome),
                        QTableWidgetItem(fornecedora),
                        QTableWidgetItem(tipo),
                        QTableWidgetItem(obs)
                    ]
                    for col, item in enumerate(items):
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                        self.table.setItem(row, col, item)
                    self.next_number += 1
            self.update_counters()
            QMessageBox.information(self, "Sucesso", "Dados carregados com sucesso!")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar CSV: {str(e)}")

    def print_list(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Lista vazia", "Não há colaboradores para imprimir.")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        self._draw_report(printer)

    def generate_pdf_report(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Lista vazia", "Não há dados para gerar relatório.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Gerar Relatório PDF", "", "PDF Files (*.pdf)")
        if not file_name:
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_name)

        self._draw_report(printer)

        QMessageBox.information(self, "Sucesso", "Relatório PDF gerado com sucesso!")

    def _draw_report(self, printer):
        painter = QPainter(printer)
        painter.setPen(QColor("#00ff41"))
        font_normal = QFont("Courier New", 10)
        font_title = QFont("Courier New", 14, QFont.Weight.Bold)
        font_sub = QFont("Courier New", 11, QFont.Weight.Bold)

        margin = 80
        line_height = 24
        y = margin
        page_width = printer.width() - 2 * margin

        # Cabeçalho
        painter.setFont(font_title)
        title = "LISTA DE COLABORADORES RDC"
        painter.drawText(margin, y, page_width, 40, Qt.AlignmentFlag.AlignCenter, title)
        y += 45

        # Data
        painter.setFont(font_sub)
        data_str = f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        painter.drawText(margin, y, page_width, 30, Qt.AlignmentFlag.AlignCenter, data_str)
        y += 40

        # Contadores
        fixos = self.label_fixos.text()
        diar = self.label_diaristas.text()
        painter.drawText(margin, y, page_width//2 - 20, 30, Qt.AlignmentFlag.AlignLeft, fixos)
        painter.drawText(margin + page_width//2 + 20, y, page_width//2 - 20, 30, Qt.AlignmentFlag.AlignRight, diar)
        y += 40

        # Linha separadora
        painter.setPen(QColor("#004d1a"))
        painter.drawLine(margin, y, printer.width() - margin, y)
        painter.setPen(QColor("#00ff41"))
        y += 30

        # Cabeçalho da tabela
        painter.setFont(font_sub)
        headers = ["Nº", "Nome", "Fornecedora AG", "Tipo", "Observação"]
        col_widths = [50, 220, 140, 90, page_width - 500]  # ajustado para caber

        x = margin
        for i, hdr in enumerate(headers):
            painter.drawText(x, y, col_widths[i], line_height,
                            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, hdr)
            x += col_widths[i]
        y += line_height + 10

        painter.drawLine(margin, y-8, printer.width() - margin, y-8)
        y += 16

        # Dados
        painter.setFont(font_normal)
        for row in range(self.table.rowCount()):
            if y > printer.height() - margin - 100:
                printer.newPage()
                y = margin + 60
                painter.drawText(margin, y-30, page_width, 30,
                                Qt.AlignmentFlag.AlignCenter, "(continuação da lista)")
                y += 50

            x = margin
            for col in range(5):
                text = self.table.item(row, col).text() if self.table.item(row, col) else ""
                painter.drawText(x, y, col_widths[col], line_height,
                                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
                x += col_widths[col]

            y += line_height

        # Rodapé
        y += 40
        if y > printer.height() - margin - 50:
            printer.newPage()
            y = margin + 60

        painter.setFont(QFont("Courier New", 9))
        painter.drawText(margin, y, "Gerado por LDC — EricLM")
        
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CollaboratorsList()
    window.show()
    sys.exit(app.exec())