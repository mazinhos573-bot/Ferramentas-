import sys
import random
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QPlainTextEdit, QSplitter, QMessageBox,
    QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QTextCursor, QPalette, QColor


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Sentinela - Login")
        self.setFixedSize(420, 520)
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a0a;
            }
            QLabel {
                color: #00ff41;
            }
            QLineEdit {
                background-color: #1a1a1a;
                color: #00ff41;
                border: 2px solid #00ff41;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #00ff41;
                color: black;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00cc33;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # Logo centralizado
        logo = QLabel("🛡️\nSENTINELA")
        logo.setFont(QFont("Arial", 52, QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("color: #00ff41; letter-spacing: 3px;")
        layout.addWidget(logo)

        # Campos de login
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        user_label = QLabel("Login:")
        user_label.setFont(QFont("Arial", 12))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ericlm")
        form_layout.addWidget(user_label)
        form_layout.addWidget(self.user_input)

        pass_label = QLabel("Senha:")
        pass_label.setFont(QFont("Arial", 12))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("Evo@0101")
        form_layout.addWidget(pass_label)
        form_layout.addWidget(self.pass_input)

        layout.addLayout(form_layout)

        # Botão
        self.btn_login = QPushButton("ACESSAR SISTEMA")
        self.btn_login.clicked.connect(self.verificar_login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

        # Centralizar janela na tela
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

    def verificar_login(self):
        if self.user_input.text().strip() == "Ericlm" and self.pass_input.text().strip() == "Evo@0101":
            self.accept()
        else:
            QMessageBox.critical(self, "Acesso Negado", "Login ou senha incorretos!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Sentinela - Painel de Monitoramento")
        self.resize(1280, 820)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a0a;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 5)
        main_layout.setSpacing(0)

        # ==================== HEADER ====================
        header = QHBoxLayout()
        header.setContentsMargins(10, 10, 10, 10)

        logo_header = QLabel("🛡️ SENTINELA")
        logo_header.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        logo_header.setStyleSheet("color: #00ff41;")

        titulo = QLabel("MONITORAMENTO AVANÇADO")
        titulo.setFont(QFont("Arial", 18))
        titulo.setStyleSheet("color: #ffffff;")

        header.addWidget(logo_header)
        header.addWidget(titulo)
        header.addStretch()

        main_layout.addLayout(header)

        # ==================== SPLITTER (Sidebar + Terminal) ====================
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #00ff41; width: 2px; }")

        # --- Sidebar ---
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #111111;
                border-right: 3px solid #00ff41;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #00ff41;
                text-align: left;
                padding: 12px 15px;
                border: none;
                margin: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #00ff41;
                color: black;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(8)

        botoes = [
            ("▶ Iniciar Monitoramento", self.iniciar_monitoramento),
            ("⏹ Parar Monitoramento", self.parar_monitoramento),
            ("📋 Visualizar Logs", self.ver_logs),
            ("📊 Status do Sistema", self.status_sistema),
            ("🔧 Configurações", self.configuracoes),
            ("🚪 Sair do Sistema", self.sair),
        ]

        for texto, funcao in botoes:
            btn = QPushButton(texto)
            btn.clicked.connect(funcao)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        splitter.addWidget(sidebar)

        # --- Terminal (tela preta meio transparente) ---
        terminal_frame = QFrame()
        terminal_frame.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border: 3px solid #00ff41;
            }
        """)

        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.setContentsMargins(10, 10, 10, 10)

        # Área do terminal (preta com opacidade)
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QPlainTextEdit {
                background-color: rgba(0, 0, 0, 0.92);
                color: #00ff41;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: none;
                padding: 8px;
            }
        """)
        # Efeito de semi-transparência
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.95)
        self.terminal.setGraphicsEffect(opacity)

        terminal_layout.addWidget(self.terminal)

        # Linha de comando estilo CMD
        cmd_widget = QWidget()
        cmd_layout = QHBoxLayout(cmd_widget)
        cmd_layout.setContentsMargins(0, 5, 0, 0)

        self.prompt = QLabel("sentinela@monitor:~$ ")
        self.prompt.setStyleSheet("color: #00ff41; font-family: monospace; font-size: 14px;")

        self.cmd_input = QLineEdit()
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: #00ff41;
                border: none;
                font-family: 'Consolas', monospace;
                font-size: 14px;
            }
        """)
        self.cmd_input.returnPressed.connect(self.executar_comando)

        cmd_layout.addWidget(self.prompt)
        cmd_layout.addWidget(self.cmd_input)

        terminal_layout.addWidget(cmd_widget)
        splitter.addWidget(terminal_frame)

        splitter.setSizes([220, 1060])
        main_layout.addWidget(splitter, 1)

        # ==================== RODAPÉ ====================
        rodape = QLabel("Sistema Sentinela © by Ericlm - Todos os direitos reservados")
        rodape.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rodape.setStyleSheet("""
            QLabel {
                background-color: #111111;
                color: #00ff41;
                padding: 12px;
                font-size: 12px;
                border-top: 2px solid #00ff41;
            }
        """)
        main_layout.addWidget(rodape)

        # ==================== INICIALIZAÇÃO ====================
        self.monitorando = False
        self.timer_monitor = QTimer()
        self.timer_monitor.timeout.connect(self.log_simulado)

        self.terminal.appendPlainText("╔══════════════════════════════════════════════════════════════╗")
        self.terminal.appendPlainText("║               SISTEMA SENTINELA v2.1 - INICIALIZADO           ║")
        self.terminal.appendPlainText("╚══════════════════════════════════════════════════════════════╝")
        self.terminal.appendPlainText("Bem-vindo, Ericlm.")
        self.terminal.appendPlainText("Digite 'help' para ver os comandos disponíveis.")
        self.terminal.appendPlainText("")

        # Cursor no final
        self.mover_cursor_fim()

    def mover_cursor_fim(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()

    def append_terminal(self, texto: str):
        self.terminal.appendPlainText(texto)
        self.mover_cursor_fim()

    def executar_comando(self):
        comando = self.cmd_input.text().strip()
        if not comando:
            return

        self.append_terminal(f"sentinela@monitor:~$ {comando}")
        self.cmd_input.clear()

        if comando == "help":
            self.append_terminal("Comandos disponíveis:")
            self.append_terminal("  help               → Esta ajuda")
            self.append_terminal("  status             → Status completo do sistema")
            self.append_terminal("  start_monitor      → Iniciar monitoramento em tempo real")
            self.append_terminal("  stop_monitor       → Parar monitoramento")
            self.append_terminal("  logs               → Exibir logs recentes")
            self.append_terminal("  clear              → Limpar terminal")
            self.append_terminal("  scan               → Simular scan de rede")
            self.append_terminal("  exit               → Sair do sistema")

        elif comando == "status":
            self.append_terminal("STATUS DO SISTEMA - " + datetime.now().strftime("%H:%M:%S"))
            self.append_terminal("  CPU Usage      : 47%")
            self.append_terminal("  RAM Usage      : 4.8 GB / 16 GB")
            self.append_terminal("  Network        : ONLINE (192.168.1.100)")
            self.append_terminal("  Threats        : 0 detected")
            self.append_terminal("  Monitoramento  : " + ("ATIVO" if self.monitorando else "INATIVO"))

        elif comando == "start_monitor":
            self.iniciar_monitoramento()

        elif comando == "stop_monitor":
            self.parar_monitoramento()

        elif comando == "logs":
            self.ver_logs()

        elif comando == "scan":
            self.append_terminal("[SCAN] Iniciando varredura de rede...")
            QTimer.singleShot(800, lambda: self.append_terminal("[SCAN] 127 dispositivos encontrados"))
            QTimer.singleShot(1400, lambda: self.append_terminal("[SCAN] 0 vulnerabilidades críticas"))
            QTimer.singleShot(2100, lambda: self.append_terminal("[SCAN] Concluído com sucesso!"))

        elif comando == "clear":
            self.terminal.clear()
            self.append_terminal("Terminal limpo.")

        elif comando == "exit":
            self.sair()

        else:
            self.append_terminal(f"Comando desconhecido: {comando}")
            self.append_terminal("Digite 'help' para ajuda.")

    def iniciar_monitoramento(self):
        if not self.monitorando:
            self.monitorando = True
            self.timer_monitor.start(1800)  # log a cada 1.8s
            self.append_terminal("[SENTINELA] Monitoramento em tempo real ATIVADO")
        else:
            self.append_terminal("[AVISO] Monitoramento já está ativo.")

    def parar_monitoramento(self):
        if self.monitorando:
            self.monitorando = False
            self.timer_monitor.stop()
            self.append_terminal("[SENTINELA] Monitoramento em tempo real DESATIVADO")
        else:
            self.append_terminal("[AVISO] Monitoramento não está ativo.")

    def log_simulado(self):
        mensagens = [
            "[ALERTA] Tentativa de acesso bloqueada - IP: 45.67.89.12",
            "[INFO] Conexão com servidor secundário OK",
            "[WARN] Temperatura do servidor: 61°C",
            "[SUCCESS] Backup automático realizado",
            f"[DATA] {datetime.now().strftime('%H:%M:%S')} - Pacote de 2453 bytes recebido",
            "[THREAT] Nenhuma ameaça detectada na última varredura",
        ]
        self.append_terminal(random.choice(mensagens))

    def ver_logs(self):
        self.append_terminal("═" * 60)
        self.append_terminal("ÚLTIMOS 10 LOGS DO SISTEMA")
        self.append_terminal("═" * 60)
        for i in range(10):
            hora = (datetime.now().hour - i) % 24
            self.append_terminal(f"[{hora:02d}:{random.randint(10,59):02d}:{random.randint(10,59):02d}] INFO - Operação normal")
        self.append_terminal("═" * 60)

    def status_sistema(self):
        self.append_terminal("Use o comando 'status' no terminal para ver o status completo.")

    def configuracoes(self):
        self.append_terminal("[CONFIG] Abrindo painel de configurações (simulado)")
        self.append_terminal("   • Modo escuro: ATIVADO")
        self.append_terminal("   • Notificações: ATIVADAS")
        self.append_terminal("   • Nível de segurança: MÁXIMO")

    def sair(self):
        resposta = QMessageBox.question(
            self,
            "Encerrar Sistema",
            "Deseja realmente sair do Sistema Sentinela?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Tema moderno

    # Login primeiro
    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        janela = MainWindow()
        janela.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)