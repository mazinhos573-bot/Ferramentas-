import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog
)
from PyQt6.QtGui import QPalette, QColor, QFont, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


class CollaboratorsList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Colaboradores RDC")
        self.resize(900, 650)

        # Tema hacker (preto + verde matrix)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            * {
                color: #00ff41;
                font-family: 'Courier New', Courier, monospace;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                background-color: #0d1a0d;
                border: 1px solid #00cc33;
                padding: 4px;
            }
            QTableWidget {
                background-color: #000000;
                gridline-color: #004d1a;
                alternate-background-color: #0a140a;
            }
            QHeaderView::section {
                background-color: #001a00;
                color: #00ff41;
                border: 1px solid #00cc33;
                padding: 4px;
            }
            QPushButton {
                background-color: #001a00;
                border: 1px solid #00cc33;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #004d1a;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ── Formulário de entrada ───────────────────────────────
        form_layout = QVBoxLayout()

        inputs = [
            ("Nome >", QLineEdit, "nome"),
            ("Fornecedora AG >", QComboBox, "fornecedora"),
            ("Fixo / Diarista >", QComboBox, "tipo"),
            ("OBS >", QLineEdit, "obs"),
        ]

        for label_text, widget_class, attr_name in inputs:
            row = QHBoxLayout()
            label = QLabel(label_text)
            if widget_class == QComboBox:
                w = QComboBox()
                if attr_name == "fornecedora":
                    w.addItems(["D0", "Polly"])
                else:
                    w.addItems(["F", "D"])
            else:
                w = QLineEdit()

            row.addWidget(label)
            row.addWidget(w)
            form_layout.addLayout(row)

            setattr(self, f"{attr_name}_input", w)
            setattr(self, f"{attr_name}_label", label)

        # Botão adicionar
        self.add_button = QPushButton("Adicionar à Lista")
        self.add_button.clicked.connect(self.add_collaborator)
        form_layout.addWidget(self.add_button, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(form_layout)

        # ── Tabela ───────────────────────────────────────────────
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nº", "Nome", "Fornecedora AG", "Fixo/Diarista", "OBS"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table, stretch=1)

        # Botão imprimir
        self.print_button = QPushButton("Imprimir Lista")
        self.print_button.clicked.connect(self.print_list)
        main_layout.addWidget(self.print_button)

        # Rodapé
        footer = QLabel("LDC by EricLM")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #006600; font-size: 11px;")
        main_layout.addWidget(footer)

        self.next_number = 1

    def add_collaborator(self):
        nome = self.nome_input.text().strip()
        if not nome:
            QMessageBox.warning(self, "Campo obrigatório", "O campo Nome é obrigatório!")
            self.nome_input.setFocus()
            return

        fornecedora = self.fornecedora_input.currentText()
        tipo = self.tipo_input.currentText()
        obs = self.obs_input.text().strip()

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

        # Limpar campos
        self.nome_input.clear()
        self.obs_input.clear()
        self.nome_input.setFocus()

    def print_list(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Lista vazia", "Não há colaboradores para imprimir.")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        painter = QPainter(printer)
        painter.setPen(QColor("black"))
        font = QFont("Courier New", 10)
        painter.setFont(font)

        page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
        margin = 80
        line_height = 22
        y = margin
        x_start = margin

        # Cabeçalho
        title_font = QFont("Courier New", 14, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.drawText(x_start, y, "LISTA DE COLABORADORES RDC")
        y += 50
        painter.setFont(font)

        headers = ["Nº", "Nome", "Fornecedora AG", "Fixo/Diarista", "OBS"]
        col_widths = [50, 220, 140, 100, 340]   # soma ≈ 850 (A4 ~ 794-900 px)

        # Linha de cabeçalho
        for i, header in enumerate(headers):
            painter.drawText(x_start, y, col_widths[i], line_height,
                            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, header)
            x_start += col_widths[i]
        y += line_height + 8

        painter.drawLine(margin, y-4, printer.width() - margin, y-4)
        y += 12

        # Dados
        x_start = margin
        for row in range(self.table.rowCount()):
            if y > printer.height() - margin - 80:  # quase no fim da página
                printer.newPage()
                y = margin + 40
                painter.drawText(margin, y-30, "(continuação)")
                y += 30

            for col in range(5):
                item = self.table.item(row, col)
                text = item.text() if item else ""
                painter.drawText(x_start, y, col_widths[col], line_height,
                                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
                x_start += col_widths[col]

            y += line_height
            x_start = margin

        # Rodapé
        y += 40
        if y > printer.height() - margin:
            printer.newPage()
            y = margin + 40

        painter.setFont(QFont("Courier New", 9))
        painter.drawText(margin, y, "LDC by EricLM")
        
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CollaboratorsList()
    window.show()
    sys.exit(app.exec())