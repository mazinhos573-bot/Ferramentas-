import sys
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QFrame
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


class CollaboratorsList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RDC – Gestão de Colaboradores")
        self.resize(720, 980)

        # =============================================
        #  TEMA DARK
        # =============================================
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
            }
            QLabel {
                color: #e5e7eb;
            }
            QLineEdit, QComboBox {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 6px;
                padding: 9px 14px;
                font-size: 14px;
                color: #f3f4f6;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox QAbstractItemView {
                background-color: #1f2937;
                color: #f3f4f6;
                selection-background-color: #374151;
            }
            QTableWidget {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 8px;
                gridline-color: #374151;
                color: #e5e7eb;
                font-size: 13.5px;
                alternate-background-color: #111827;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #cbd5e1;
                padding: 10px 12px;
                border: none;
                border-bottom: 1px solid #374151;
                font-weight: 600;
                font-size: 13.5px;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton#danger {
                background-color: #ef4444;
            }
            QPushButton#danger:hover {
                background-color: #dc2626;
            }
            QPushButton#secondary {
                background-color: #4b5563;
            }
            QPushButton#secondary:hover {
                background-color: #374151;
            }
            .card {
                background-color: #1e293b;
                border: 1px solid #374151;
                border-radius: 10px;
                padding: 20px;
            }
            .section-title {
                font-size: 18px;
                font-weight: 600;
                color: #f1f5f9;
            }
            .counter-panel {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 14px 18px;
                font-weight: 500;
                color: #e5e7eb;
                min-width: 160px;
                text-align: center;
            }
            QFrame.separator {
                background-color: #374151;
                max-height: 1px;
            }
            QLabel.footer {
                color: #9ca3af;
                font-size: 12px;
            }
        """)

        # Forçar paleta dark (melhora alguns widgets)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(17, 24, 39))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(243, 244, 246))
        palette.setColor(QPalette.ColorRole.Base, QColor(31, 41, 55))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(17, 24, 39))
        palette.setColor(QPalette.ColorRole.Text, QColor(243, 244, 246))
        palette.setColor(QPalette.ColorRole.Button, QColor(59, 130, 246))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setPalette(palette)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(32, 24, 32, 24)
        main_layout.setSpacing(24)
        central_widget.setLayout(main_layout)

        # Cabeçalho
        header = QVBoxLayout()
        title = QLabel("Gestão de Colaboradores")
        title.setStyleSheet("font-size: 26px; font-weight: 700; color: #f1f5f9;")
        subtitle = QLabel("Controle de alocação – Fixos e Diaristas | RDC")
        subtitle.setStyleSheet("font-size: 14px; color: #9ca3af;")
        header.addWidget(title)
        header.addWidget(subtitle)
        main_layout.addLayout(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(sep)

        # Contadores (card) – formato solicitado
        counters_card = QWidget()
        counters_card.setObjectName("card")
        counters_layout = QVBoxLayout()
        counters_layout.setSpacing(16)
        counters_card.setLayout(counters_layout)

        lbl_counters_title = QLabel("Resumo de Alocação")
        lbl_counters_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #f1f5f9;")
        counters_layout.addWidget(lbl_counters_title)

        # Linha Polly x D0
        row_main = QHBoxLayout()
        row_main.setSpacing(32)

        # Coluna Polly
        polly_col = QVBoxLayout()
        polly_col.setSpacing(8)
        polly_title = QLabel("Polly")
        polly_title.setStyleSheet("font-weight: bold; font-size: 15px; color: #60a5fa;")
        polly_col.addWidget(polly_title)

        self.lbl_polly_fixo     = QLabel("Fixo:         0")
        self.lbl_polly_diarista = QLabel("Diaristas:    0")
        self.lbl_polly_total    = QLabel("Total:        0")

        for lbl in (self.lbl_polly_fixo, self.lbl_polly_diarista, self.lbl_polly_total):
            lbl.setObjectName("counter-panel")
            lbl.setMinimumWidth(180)
            polly_col.addWidget(lbl)

        # Coluna D0
        d0_col = QVBoxLayout()
        d0_col.setSpacing(8)
        d0_title = QLabel("D0")
        d0_title.setStyleSheet("font-weight: bold; font-size: 15px; color: #f87171;")
        d0_col.addWidget(d0_title)

        self.lbl_d0_fixo     = QLabel("Fixo:         0")
        self.lbl_d0_diarista = QLabel("Diaristas:    0")
        self.lbl_d0_total    = QLabel("Total:        0")

        for lbl in (self.lbl_d0_fixo, self.lbl_d0_diarista, self.lbl_d0_total):
            lbl.setObjectName("counter-panel")
            lbl.setMinimumWidth(180)
            d0_col.addWidget(lbl)

        row_main.addLayout(polly_col)
        row_main.addLayout(d0_col)
        row_main.addStretch()

        counters_layout.addLayout(row_main)
        main_layout.addWidget(counters_card)

        # Formulário (card)
        form_card = QWidget()
        form_card.setObjectName("card")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)
        form_card.setLayout(form_layout)

        form_header = QLabel("Adicionar ou Editar Colaborador")
        form_header.setStyleSheet("font-size: 17px; font-weight: 600; color: #f1f5f9;")
        form_layout.addWidget(form_header)

        self.inputs = {}
        form_fields = [
            ("Nome completo",       QLineEdit,   "nome"),
            ("Fornecedora",         QComboBox,   "fornecedora", ["", "D0", "Polly"]),
            ("Tipo de contratação", QComboBox,   "tipo",        ["", "Fixo", "Diarista"]),
            ("Observação / Lotação",QLineEdit,   "obs"),
        ]

        for label_text, w_class, key, *opts in form_fields:
            row = QHBoxLayout()
            row.setSpacing(16)
            lbl = QLabel(label_text)
            lbl.setFixedWidth(190)
            lbl.setStyleSheet("font-weight: 500; color: #d1d5db;")
            if w_class == QComboBox:
                w = QComboBox()
                w.addItems(opts[0] if opts else [""])
            else:
                w = QLineEdit()
            w.setMinimumHeight(38)
            row.addWidget(lbl)
            row.addWidget(w, 1)
            form_layout.addLayout(row)
            self.inputs[key] = w

        btn_row = QHBoxLayout()
        self.btn_save = QPushButton("Salvar Colaborador")
        self.btn_save.clicked.connect(self.add_or_update_collaborator)
        btn_clear = QPushButton("Limpar")
        btn_clear.setObjectName("secondary")
        btn_clear.clicked.connect(self.clear_inputs)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(btn_clear)
        btn_row.addStretch()
        form_layout.addLayout(btn_row)

        main_layout.addWidget(form_card)

        # Tabela – Nome Completo mais largo
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nº", "Nome Completo", "Fornecedora", "Tipo", "Observação / Lotação"])
        
        # Aumentar largura da coluna Nome Completo
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nome expande mais
        self.table.setColumnWidth(1, 280)  # largura inicial maior
        
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)

        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        main_layout.addWidget(self.table, 1)

        # Ações
        actions = QHBoxLayout()
        self.btn_delete = QPushButton("Excluir Selecionado(s)")
        self.btn_delete.setObjectName("danger")
        self.btn_delete.clicked.connect(self.delete_selected)

        btn_print  = QPushButton("Imprimir")
        btn_export = QPushButton("Exportar CSV")
        btn_import = QPushButton("Importar CSV")
        btn_pdf    = QPushButton("Gerar PDF")

        for b in (btn_print, btn_export, btn_import, btn_pdf):
            b.setObjectName("secondary")

        btn_print.clicked.connect(self.print_list)
        btn_export.clicked.connect(self.save_to_csv)
        btn_import.clicked.connect(self.load_from_csv)
        btn_pdf.clicked.connect(self.generate_pdf_report)

        actions.addWidget(self.btn_delete)
        actions.addStretch()
        actions.addWidget(btn_print)
        actions.addWidget(btn_export)
        actions.addWidget(btn_import)
        actions.addWidget(btn_pdf)
        main_layout.addLayout(actions)

        # Rodapé
        footer = QLabel(f"RDC – Gestão de Colaboradores • v1.1 • {datetime.now().year}")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setObjectName("footer")
        main_layout.addWidget(footer)

        self.next_number = 1
        self.selected_row = -1
        self.update_counters()

    def update_counters(self):
        fixos = diaristas = 0
        polly_f = polly_d = d0_f = d0_d = 0

        for r in range(self.table.rowCount()):
            fornec = self.table.item(r, 2).text().strip() if self.table.item(r, 2) else ""
            tipo   = self.table.item(r, 3).text().strip() if self.table.item(r, 3) else ""

            if tipo == "Fixo":
                fixos += 1
                if fornec == "Polly": polly_f += 1
                elif fornec == "D0":  d0_f += 1
            elif tipo == "Diarista":
                diaristas += 1
                if fornec == "Polly": polly_d += 1
                elif fornec == "D0":  d0_d += 1

        # Atualização no formato desejado
        self.lbl_polly_fixo.setText(    f"Fixo:         {polly_f}")
        self.lbl_polly_diarista.setText(f"Diaristas:    {polly_d}")
        self.lbl_polly_total.setText(   f"Total:        {polly_f + polly_d}")

        self.lbl_d0_fixo.setText(     f"Fixo:         {d0_f}")
        self.lbl_d0_diarista.setText( f"Diaristas:    {d0_d}")
        self.lbl_d0_total.setText(    f"Total:        {d0_f + d0_d}")

    # Os demais métodos permanecem iguais
    def clear_inputs(self):
        for w in self.inputs.values():
            if isinstance(w, QLineEdit):
                w.clear()
            elif isinstance(w, QComboBox):
                w.setCurrentIndex(0)
        self.btn_save.setText("Salvar Colaborador")
        self.selected_row = -1
        self.inputs["nome"].setFocus()

    def add_or_update_collaborator(self):
        nome = self.inputs["nome"].text().strip()
        if not nome:
            QMessageBox.warning(self, "Atenção", "O campo Nome completo é obrigatório.")
            return

        fornecedora = self.inputs["fornecedora"].currentText().strip()
        tipo        = self.inputs["tipo"].currentText().strip()
        obs         = self.inputs["obs"].text().strip()

        if self.selected_row >= 0:
            self.table.setItem(self.selected_row, 1, QTableWidgetItem(nome))
            self.table.setItem(self.selected_row, 2, QTableWidgetItem(fornecedora))
            self.table.setItem(self.selected_row, 3, QTableWidgetItem(tipo))
            self.table.setItem(self.selected_row, 4, QTableWidgetItem(obs))
            self.clear_inputs()
            self.update_counters()
            return

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
        if selected:
            row = selected[0].row()
            self.selected_row = row
            self.btn_save.setText("Atualizar Colaborador")

            nome = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            fornec = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            tipo   = self.table.item(row, 3).text() if self.table.item(row, 3) else ""
            obs    = self.table.item(row, 4).text() if self.table.item(row, 4) else ""

            self.inputs["nome"].setText(nome)
            self.inputs["fornecedora"].setCurrentText(fornec)
            self.inputs["tipo"].setCurrentText(tipo)
            self.inputs["obs"].setText(obs)
        else:
            self.clear_inputs()

    def delete_selected(self):
        selected_rows = set(item.row() for item in self.table.selectedItems())
        if not selected_rows:
            QMessageBox.information(self, "Atenção", "Nenhum colaborador selecionado.")
            return

        reply = QMessageBox.question(
            self, "Confirmação",
            f"Deseja realmente excluir {len(selected_rows)} colaborador(es)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            for row in sorted(selected_rows, reverse=True):
                self.table.removeRow(row)
            self.next_number = 1
            for r in range(self.table.rowCount()):
                self.table.setItem(r, 0, QTableWidgetItem(str(self.next_number)))
                self.next_number += 1
            self.clear_inputs()
            self.update_counters()

    def save_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar como CSV", "", "CSV (*.csv)")
        if not file_name: return

        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            writer.writerow(headers)
            for row in range(self.table.rowCount()):
                row_data = [self.table.item(row, col).text() if self.table.item(row, col) else "" for col in range(self.table.columnCount())]
                writer.writerow(row_data)
        QMessageBox.information(self, "Sucesso", "Lista exportada com sucesso!")

    def load_from_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir CSV", "", "CSV (*.csv)")
        if not file_name: return

        self.table.setRowCount(0)
        self.next_number = 1

        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # cabeçalho
            for row_data in reader:
                if len(row_data) < 5: continue
                row = self.table.rowCount()
                self.table.insertRow(row)
                for col, value in enumerate(row_data[:5]):
                    if col == 0:
                        item = QTableWidgetItem(str(self.next_number))
                    else:
                        item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    self.table.setItem(row, col, item)
                self.next_number += 1

        self.update_counters()
        QMessageBox.information(self, "Sucesso", "Dados importados com sucesso!")

    def print_list(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Impressão", "Funcionalidade de impressão em desenvolvimento.")

    def generate_pdf_report(self):
        QMessageBox.information(self, "PDF", "Geração de relatório PDF em desenvolvimento.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = CollaboratorsList()
    window.show()
    sys.exit(app.exec())