import sys
import random
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QSplitter, QMessageBox,
    QFrame, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor, QColor


# ───────────────────────────────────────────────
# SIMULAÇÃO DE DADOS DE CRYPTO
# ───────────────────────────────────────────────
class CryptoSim:
    def __init__(self):
        self.pares = {}
        self.historico = {}
        self.ultimo_update = {}

    def registrar_par(self, par: str):
        par = par.upper()
        if par not in self.pares:
            self.pares[par] = {
                "preco": random.uniform(0.0005, 68000) if "USDT" in par else random.uniform(0.01, 4200),
                "volume_24h": random.uniform(5e6, 4e9),
                "var_5min": 0.0,
                "var_15min": 0.0,
                "rsi_14": random.uniform(38, 72),
                "recomendacao": "NEUTRAL"
            }
            self.historico[par] = []
            self.ultimo_update[par] = datetime.now()

    def tick(self):
        agora = datetime.now()
        for par in list(self.pares.keys()):
            if (agora - self.ultimo_update.get(par, agora)).total_seconds() < 8:
                continue
            data = self.pares[par]
            variacao = random.uniform(-1.8, 2.1) * (1 + random.random() * 0.7 if random.random() < 0.22 else 1)
            data["preco"] *= (1 + variacao / 100)
            data["preco"] = round(data["preco"], 8 if data["preco"] < 1 else 2)
            self.historico[par].append(data["preco"])
            if len(self.historico[par]) > 120:
                self.historico[par].pop(0)

            if len(self.historico[par]) >= 30:
                data["var_5min"] = (data["preco"] / self.historico[par][-30] - 1) * 100
            if len(self.historico[par]) >= 90:
                data["var_15min"] = (data["preco"] / self.historico[par][-90] - 1) * 100

            data["rsi_14"] = max(20, min(85, data["rsi_14"] + random.uniform(-4.2, 5.1)))

            v = data["var_5min"]
            r = data["rsi_14"]
            if v > 1.8 and r < 38:
                data["recomendacao"] = "STRONG BUY"
            elif v > 0.9 and r < 48:
                data["recomendacao"] = "BUY"
            elif v < -1.6 and r > 68:
                data["recomendacao"] = "STRONG SELL"
            elif v < -0.8 and r > 58:
                data["recomendacao"] = "SELL"
            else:
                data["recomendacao"] = "NEUTRAL" if abs(v) < 0.7 else "WATCH"

            self.ultimo_update[par] = agora

    def top_pares(self, quantidade=8):
        ordenados = sorted(
            self.pares.items(),
            key=lambda x: abs(x[1]["var_5min"]),
            reverse=True
        )
        return ordenados[:quantidade]


# ───────────────────────────────────────────────
# LOGIN
# ───────────────────────────────────────────────
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINELA v4.0 – CRYPTO SHADOW ROOT")
        self.setFixedSize(480, 580)
        self.setStyleSheet("""
            QDialog { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0a000f, stop:1 #001a00); }
            QLabel { color: #00ff41; font-family: Consolas; }
            QLineEdit { background: #0d1a0d; color: #00ff41; border: 1px solid #00ff41;
                        border-radius: 4px; padding: 10px; font-family: Consolas; }
            QPushButton { background: #00cc33; color: black; font-weight: bold;
                          border: none; padding: 16px; border-radius: 4px; font-family: Consolas; }
            QPushButton:hover { background: #00ff41; }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(45)

        logo = QLabel("SENTINELA\nCRYPTO v4.0")
        logo.setFont(QFont("Consolas", 40, QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("color: #00ff41; letter-spacing: 5px;")
        layout.addWidget(logo)

        form = QVBoxLayout()
        form.setSpacing(22)
        user_label = QLabel("IDENTIFIER:")
        self.user_input = QLineEdit()
        pass_label = QLabel("SHADOW KEY:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        for lbl, w in [(user_label, self.user_input), (pass_label, self.pass_input)]:
            lbl.setFont(QFont("Consolas", 15))
            form.addWidget(lbl)
            form.addWidget(w)

        layout.addLayout(form)

        btn = QPushButton("BREACH & AUTHENTICATE")
        btn.clicked.connect(self.verificar)
        layout.addWidget(btn)

        self.setLayout(layout)

    def verificar(self):
        u = self.user_input.text().strip().lower()
        p = self.pass_input.text().strip()
        if u in ["root", "ghost", "ericlm", "trader", ""] and p in ["sentinela", "darkpool", "Evo@0101", "crypto666", ""]:
            self.accept()
        else:
            QMessageBox.critical(self, "DENIED", "[!] INTRUSION DETECTED – LOGGED [!]")


# ───────────────────────────────────────────────
# JANELA PRINCIPAL
# ───────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINELA v4.0 – CRYPTO SHADOW CORE")
        self.resize(1480, 920)
        self.setStyleSheet("QMainWindow { background: #00050a; }")

        self.crypto = CryptoSim()
        for p in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "1000PEPEUSDT"]:
            self.crypto.registrar_par(p)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 6)

        # Header
        hdr = QHBoxLayout()
        logo = QLabel("SENTINELA CRYPTO v4.0")
        logo.setFont(QFont("Consolas", 30, QFont.Weight.Bold))
        logo.setStyleSheet("color: #00ff41;")
        title = QLabel("LIVE MARKET SHADOW – MOMENTUM DETECTION")
        title.setFont(QFont("Consolas", 15))
        title.setStyleSheet("color: #00cc33;")
        hdr.addWidget(logo)
        hdr.addSpacing(50)
        hdr.addWidget(title)
        hdr.addStretch()
        main_layout.addLayout(hdr)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: #00ff41; width: 4px; }")

        # ─── Sidebar ───
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QWidget { background: #0a140a; border-right: 4px solid #00ff41; }
            QPushButton {
                background: #0f1a0f; color: #00ff41; text-align: left;
                padding: 15px 20px; border: none; margin: 5px 10px;
                font-family: Consolas; font-size: 14px;
            }
            QPushButton:hover { background: #00cc33; color: black; }
        """)
        sb_layout = QVBoxLayout(sidebar)

        botoes = [
            ("▶ ACTIVATE SHADOW", self.iniciar),
            ("⏹ DEACTIVATE SHADOW", self.parar),
            ("₿ CRYPTO TOP", self.mostrar_top),
            ("🔍 WATCH PAIR", self.watch_par),
            ("📡 NETSTAT", self.ifconfig),
            ("🛡️ FIREWALL", self.firewall_status_detailed),
            ("📜 SHADOW LOGS", self.ver_logs),
            ("✖ TERMINATE", self.sair),
        ]
        for txt, fn in botoes:
            b = QPushButton(txt)
            b.clicked.connect(fn)
            sb_layout.addWidget(b)
        sb_layout.addStretch()
        splitter.addWidget(sidebar)

        # ─── Terminal ───
        term_frame = QFrame()
        term_frame.setStyleSheet("QFrame { background: #000; border: 4px solid #00ff41; }")
        term_layout = QVBoxLayout(term_frame)
        term_layout.setContentsMargins(16, 16, 16, 16)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setUndoRedoEnabled(False)
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: rgba(0,12,0,0.96);
                color: #00ff41;
                font-family: 'Consolas', monospace;
                font-size: 15px;
                border: none;
                selection-background-color: #004d1a;
            }
        """)
        term_layout.addWidget(self.terminal)

        cmd_widget = QWidget()
        cmd_layout = QHBoxLayout(cmd_widget)
        self.prompt = QLabel("shadow@sentinela:~/crypto $ ")
        self.prompt.setStyleSheet("color: #00ff41; font-family: Consolas; font-size: 15px;")
        self.cmd_input = QLineEdit()
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #00ff41;
                border: none;
                font-family: Consolas;
                font-size: 15px;
            }
        """)
        self.cmd_input.returnPressed.connect(self.executar_comando)
        cmd_layout.addWidget(self.prompt)
        cmd_layout.addWidget(self.cmd_input)
        term_layout.addWidget(cmd_widget)

        splitter.addWidget(term_frame)
        splitter.setSizes([280, 1200])
        main_layout.addWidget(splitter, 1)

        # Footer
        self.footer = QLabel("SENTINELA CRYPTO v4.0 | ACTIVE | Ericlm – 2026")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer.setStyleSheet("""
            QLabel {
                background: #0a0f0a;
                color: #00ff41;
                padding: 12px;
                font-family: Consolas;
                font-size: 14px;
                border-top: 3px solid #00ff41;
            }
        """)
        main_layout.addWidget(self.footer)

        # Timers
        self.monitor_on = False
        self.timer_crypto = QTimer()
        self.timer_crypto.timeout.connect(self.atualizar_crypto)
        self.timer_crypto.start(2200)

        self.timer_logs = QTimer()
        self.timer_logs.timeout.connect(self.log_simulado)
        self.timer_logs.start(4800)

        self.timer_mining = QTimer()
        self.timer_mining.timeout.connect(self.simulate_mining_transfer)

        self.boot_sequence()
        self.mover_cursor_fim()

    def simulate_mining_transfer(self):
        amount = random.uniform(2, 10)
        attempts = random.randint(1000000, 100000000)
        nonce = random.randint(0, 4294967295)
        hash_prefix = '0000' + ''.join(random.choices('0123456789abcdef', k=60))
        wallet = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlhfe"  

        self.append(f"[MINING] Iniciando computação de hash para novo bloco...", cor="#ffff00")
        self.append(f"[MINING] Taxa de hash: {random.uniform(5, 15):.2f} TH/s", cor="#ffff00")
        self.append(f"[MINING] Tentativas realizadas: {attempts}", cor="#ffff00")
        self.append(f"[MINING] Bloco encontrado! Nonce: {nonce}", cor="#00ff00")
        self.append(f"[MINING] Hash do bloco: {hash_prefix}", cor="#00ff00")
        self.append(f"[MINING] Recompensa minerada: {amount:.2f} USD", cor="#00ff00")
        self.append(f"[MINING] Realizando transferência para carteira Bitcoin: {wallet} valor: {amount:.2f} USD", cor="#00ff00")

    def watch_par(self):
        par, ok = QInputDialog.getText(
            self,
            "WATCH PAIR",
            "Digite o(s) par(es) para monitorar (ex: SOLUSDT TONUSDT):"
        )
        if ok and par.strip():
            pares = [p.strip().upper() for p in par.split() if p.strip()]
            if pares:
                for p in pares:
                    self.crypto.registrar_par(p)
                self.append(f"→ Monitoring added: {' '.join(pares)}", cor="#ffff00")
                self.mostrar_top(live=True)
            else:
                self.append("[i] Nenhum par válido", cor="#888888")
        else:
            self.append("[i] Watch cancelado", cor="#888888")

    def boot_sequence(self):
        lines = [
            "╔══════════════════════════════════════════════╗",
            "║ SENTINELA CRYPTO SHADOW v4.0 BOOTING ║",
            "╚══════════════════════════════════════════════╝",
            f"[INIT] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "[NET] tun0 10.8.0.13 – Mullvad shadow exit",
            "[API] Binance & Bybit shadow feeds connected",
            "[DATA] 8 pairs pre-loaded – sampling every 8s",
            "[MOMENTUM] RSI + Δ5min + volume shadow active",
            "[STATUS] Shadow dormant – type 'start' or click ACTIVATE",
            "",
            "ghost@sentinela:~/crypto $ help → command list"
        ]
        for line in lines:
            self.append(line, cor="#00ff88")

    def append(self, texto: str, cor="#00ff41", alerta=False, forte=False):
        prefix = "!!! " if forte else "[!]" if alerta else ""
        linha = f"{prefix}{texto}"

        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal.setTextCursor(cursor)

        self.terminal.setTextColor(QColor(cor))
        self.terminal.insertPlainText(linha + "\n")
        self.terminal.setTextColor(QColor("#00ff41"))

        self.mover_cursor_fim()

    def mover_cursor_fim(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()

    def executar_comando(self):
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        self.append(f"shadow@sentinela:~/crypto $ {cmd}")
        self.cmd_input.clear()

        parts = cmd.lower().split()
        base = parts[0]

        if base in ("help", "?"):
            self.show_help()
        elif base in ("start", "activate"):
            self.iniciar()
        elif base in ("stop", "deactivate"):
            self.parar()
        elif base in ("top", "rank", "movers"):
            self.mostrar_top()
        elif base == "watch" and len(parts) > 1:
            for p in parts[1:]:
                self.crypto.registrar_par(p.upper())
            self.append(f"→ Monitoring added: {' '.join(parts[1:])}", cor="#ffff00")
        elif base in ("status", "s"):
            self.mostrar_top(5)
        elif base in ("clear", "cls"):
            self.terminal.clear()
            self.append("[+] Buffer limpo")
        elif base in ("exit", "quit"):
            self.sair()
        else:
            self.append(f"[-] comando desconhecido: {cmd}", cor="#ff4444", alerta=True)

    def show_help(self):
        linhas = [
            " crypto shadow commands v4.0 ",
            "──────────────────────────────",
            " start     → ativa atualização agressiva",
            " stop      → hiberna shadow",
            " top       → pares com maior movimento 5min",
            " watch <par> → monitora par (ex: watch SOLUSDT TONUSDT)",
            " status / s → mostra top 5 agora",
            " clear     → limpa tela",
            " help      → este menu",
            " exit      → finaliza sessão",
        ]
        self.append("═" * 50, cor="#00aa33")
        for l in linhas:
            self.append(l, cor="#00ff88")
        self.append("═" * 50, cor="#00aa33")

    def iniciar(self):
        if self.monitor_on:
            self.append("[!] Shadow já ativo", cor="#ffff00", alerta=True)
            return
        self.monitor_on = True
        self.timer_mining.start(120000)  # 2 minutos
        self.append("[√] CRYPTO SHADOW ATIVADO – momentum tracking live", cor="#00ff00", forte=True)
        self.append("[MINING] Simulação de mineração iniciada.", cor="#ffff00")

    def parar(self):
        if not self.monitor_on:
            return
        self.monitor_on = False
        self.timer_mining.stop()
        self.append("[×] CRYPTO SHADOW HIBERNADO", cor="#ff8800")
        self.append("[MINING] Simulação de mineração pausada.", cor="#ff8800")

    def atualizar_crypto(self):
        self.crypto.tick()
        if self.monitor_on:
            self.mostrar_top(live=True)

    def mostrar_top(self, qtd=8, live=False):
        top = self.crypto.top_pares(qtd)
        if not top:
            self.append("nenhum par monitorado ainda.", cor="#888888")
            return

        agora = datetime.now().strftime("%H:%M:%S")
        header = f" TOP MOVERS {qtd} @ {agora} ────── 5min Δ"
        self.append(header, cor="#00ff88")
        self.append("═" * len(header), cor="#004d1a")

        for par, info in top:
            v = info["var_5min"]
            sinal = "BUY " if "BUY" in info["recomendacao"] else "SELL " if "SELL" in info["recomendacao"] else ""
            cor_sinal = "#00ff00" if "BUY" in info["recomendacao"] else "#ff3333" if "SELL" in info["recomendacao"] else "#666666"
            preco_str = f"{info['preco']:,.8f}" if info['preco'] < 1 else f"{info['preco']:,.2f}"
            linha = f" {par:10} {preco_str:>14} {v:>+6.2f}% {sinal}"
            self.append(linha, cor=cor_sinal)

        self.append("═" * len(header), cor="#004d1a")

    def ver_logs(self):
        self.append(" últimas entradas shadow (simuladas) ".center(60, "═"), cor="#00aa33")
        for _ in range(12):
            t = (datetime.now() - timedelta(minutes=random.randint(1,90))).strftime("%H:%M")
            msg = random.choice([
                "BTCUSDT spike +2.4% – momentum BUY trigger",
                "ETHUSDT -1.8% RSI oversold → possible reversal",
                "DOGEUSDT volume 3.1× media → watch breakout",
                "PEPEUSDT whale dump detected – SELL pressure"
            ])
            cor = "#88ff88" if "BUY" in msg else "#ff8888" if "SELL" in msg else "#aaffaa"
            self.append(f"[{t}] {msg}", cor=cor)
        self.append("═" * 60, cor="#004d1a")

    def ifconfig(self):
        self.append(" tun0: shadow exit – 10.8.0.13 ".center(60,"─"), cor="#00cc33")
        self.append(" connected via encrypted tunnel – no leak detected")

    def firewall_status_detailed(self):
        self.append("[FW] Shadow crypto node – DROP-ALL policy (except API endpoints)")

    def sair(self):
        if QMessageBox.question(self, "KILL SESSION", "Realmente finalizar shadow node?") == QMessageBox.StandardButton.Yes:
            self.close()

    def log_simulado(self):
        # Pode implementar logs automáticos aqui no futuro
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)