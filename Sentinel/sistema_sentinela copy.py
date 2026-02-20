import sys
import random
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QPlainTextEdit, QSplitter, QMessageBox,
    QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QTextCursor, QColor, QPalette

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINELA v3.7 - ROOT ACCESS")
        self.setFixedSize(440, 540)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #000814, stop:1 #001a00);
            }
            QLabel { color: #00ff41; }
            QLineEdit {
                background: #0d1a0d;
                color: #00ff9d;
                border: 1px solid #00ff41;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas';
            }
            QPushButton {
                background: #00ff41;
                color: #000;
                font-weight: bold;
                border: none;
                padding: 14px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #00cc33; }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(35)

        logo = QLabel("█▀█ █▀▀ █▀█\n█▀▄ ██▄ █▄█\nSENTINELA")
        logo.setFont(QFont("Consolas", 38, QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("color: #00ff41; letter-spacing: 2px;")
        layout.addWidget(logo)

        form = QVBoxLayout()
        form.setSpacing(18)
        user_label = QLabel("IDENT:")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("root | Ericlm")
        
        pass_label = QLabel("KEY:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("********")

        for lbl, inp in [(user_label, self.user_input), (pass_label, self.pass_input)]:
            lbl.setFont(QFont("Consolas", 13))
            form.addWidget(lbl)
            form.addWidget(inp)

        layout.addLayout(form)

        self.btn = QPushButton("BREACH AUTHORIZATION")
        self.btn.clicked.connect(self.verificar_login)
        layout.addWidget(self.btn)

        self.setLayout(layout)
        self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

    def verificar_login(self):
        u = self.user_input.text().strip()
        p = self.pass_input.text().strip()
        if (u in ["Ericlm", "root", "admin"]) and p == "Evo@0101":
            self.accept()
        else:
            QMessageBox.critical(self, "DENIED", "INVALID CREDENTIALS\n[BRUTEFORCE DETECTED]")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINELA v3.7 – SHADOW NODE")
        self.resize(1360, 880)
        self.setStyleSheet("QMainWindow { background: #00060f; }")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 4)
        main_layout.setSpacing(0)

        # ─── Header ───────────────────────────────────────
        hdr = QHBoxLayout()
        hdr.setContentsMargins(12, 12, 12, 12)
        logo = QLabel("SENTINELA  v3.7")
        logo.setFont(QFont("Consolas", 26, QFont.Weight.Bold))
        logo.setStyleSheet("color: #00ff5e;")
        title = QLabel("DEEP PACKET SHADOW MONITOR")
        title.setFont(QFont("Consolas", 16))
        title.setStyleSheet("color: #88ffaa;")
        hdr.addWidget(logo)
        hdr.addSpacing(30)
        hdr.addWidget(title)
        hdr.addStretch()
        main_layout.addLayout(hdr)

        # ─── Splitter ─────────────────────────────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: #00ff41; width: 3px; }")

        # ── Sidebar ──
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QWidget { background: #0a120a; border-right: 3px solid #00ff41; }
            QPushButton {
                background: #111911;
                color: #00ff88;
                text-align: left;
                padding: 14px 16px;
                border: none;
                margin: 3px 6px;
                font-family: Consolas;
            }
            QPushButton:hover { background: #00ff41; color: black; }
        """)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setSpacing(6)

        actions = [
            ("▶ LAUNCH SHADOW",      self.iniciar_monitoramento),
            ("⏹ KILL SHADOW",        self.parar_monitoramento),
            ("📡 NETSTAT / SOCKS",    self.netstat),
            ("🔍 WHOIS / GEOIP",      self.whois_fake),
            ("🕵️ ARP TABLE",         self.arp_table),
            ("📜 DUMP RECENT",        self.ver_logs),
            ("⚡ PACKET CAPTURE",     self.packet_dump_sim),
            ("🐝 HONEYPOT STATUS",    self.honeypot_status),
            ("🌐 TOR / PROXY CHECK",  self.tor_check),
            ("🚪 TERMINATE SESSION",  self.sair),
        ]
        for txt, fn in actions:
            b = QPushButton(txt)
            b.clicked.connect(fn)
            sb_layout.addWidget(b)
        sb_layout.addStretch()
        splitter.addWidget(sidebar)

        # ── Terminal Area ──
        term_frame = QFrame()
        term_frame.setStyleSheet("QFrame { background: #000; border: 3px solid #00ff41; }")
        term_layout = QVBoxLayout(term_frame)
        term_layout.setContentsMargins(12, 12, 12, 12)

        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QPlainTextEdit {
                background: rgba(3, 12, 3, 0.94);
                color: #00ff5e;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
                selection-background-color: #004d1a;
            }
        """)
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.96)
        self.terminal.setGraphicsEffect(opacity)
        term_layout.addWidget(self.terminal)

        # Prompt + input
        cmd_w = QWidget()
        cmd_l = QHBoxLayout(cmd_w)
        cmd_l.setContentsMargins(0, 6, 0, 0)
        self.prompt = QLabel("shadow@sentinela:~/darknet $ ")
        self.prompt.setStyleSheet("color: #00ff88; font-family: Consolas; font-size: 14px;")
        self.cmd_input = QLineEdit()
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #00ff9d;
                border: none;
                font-family: Consolas;
                font-size: 14px;
            }
        """)
        self.cmd_input.returnPressed.connect(self.executar_comando)
        cmd_l.addWidget(self.prompt)
        cmd_l.addWidget(self.cmd_input)
        term_layout.addWidget(cmd_w)

        splitter.addWidget(term_frame)
        splitter.setSizes([240, 1120])
        main_layout.addWidget(splitter, 1)

        # ─── Footer ───
        foot = QLabel("SENTINELA v3.7 – Ericlm | NO LOGS – NO MERCY – 2026")
        foot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        foot.setStyleSheet("""
            QLabel {
                background: #0a0f0a;
                color: #00cc66;
                padding: 10px;
                font-family: Consolas;
                font-size: 12px;
                border-top: 2px solid #00ff41;
            }
        """)
        main_layout.addWidget(foot)

        # ─── Init state ───
        self.monitorando = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.log_simulado_avancado)

        self.boot_sequence()
        self.mover_cursor_fim()

    def boot_sequence(self):
        lines = [
            "╔═══════════════════════════════════════════════════════════════╗",
            "║        SENTINELA v3.7 – SHADOW NODE – BOOT SEQUENCE           ║",
            "╚═══════════════════════════════════════════════════════════════╝",
            f"[INIT] {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}",
            "[NET]  eth0  UP  192.168.66.13/24  (spoofed MAC: 00:1C:42:aa:bb:cc)",
            "[NET]  tun0  ACTIVE  10.8.0.6  (VPN – Mullvad-like exit)",
            "[NET]  wlan1 MONITOR MODE ENABLED  (channel 6 – injection ready)",
            "[SYS]  Kernel: Linux 6.8.x-parrot  x86_64",
            "[SYS]  Uptime:  13d 17:42:19",
            "[MEM]  38% used  –  11.4 GiB / 31.2 GiB",
            "[PROC] Hidden processes: 4  (possible rootkit activity)",
            "[HONEYPOT]  Cowrie + Dionaea  –  17 connections trapped last 24h",
            "",
            "Type 'help' or press TAB (sim) to see ghost commands.",
            "Welcome back, ghost."
        ]
        for line in lines:
            self.append_terminal(line)

    def append_terminal(self, text: str, alert=False):
        if alert:
            self.append_terminal("!!! ────────────────────────────────────────────── !!!")
            self.append_terminal(text)
            self.append_terminal("!!! ────────────────────────────────────────────── !!!")
        else:
            self.terminal.appendPlainText(text)
        self.mover_cursor_fim()

    def mover_cursor_fim(self):
        cur = self.terminal.textCursor()
        cur.movePosition(QTextCursor.MoveOperation.End)
        self.terminal.setTextCursor(cur)
        self.terminal.ensureCursorVisible()

    def executar_comando(self):
        cmd = self.cmd_input.text().strip()
        if not cmd: return
        self.append_terminal(f"shadow@sentinela:~/darknet $ {cmd}")
        self.cmd_input.clear()

        if cmd in ("help", "?"):
            self.show_help()
        elif cmd == "status":
            self.show_status()
        elif cmd in ("start", "start_monitor"):
            self.iniciar_monitoramento()
        elif cmd in ("stop", "stop_monitor"):
            self.parar_monitoramento()
        elif cmd in ("logs", "dump", "tail"):
            self.ver_logs()
        elif cmd == "netstat":
            self.netstat()
        elif cmd == "arp":
            self.arp_table()
        elif cmd == "whois":
            self.whois_fake()
        elif cmd == "packetdump" or cmd == "tcpdump":
            self.packet_dump_sim()
        elif cmd == "honeypot":
            self.honeypot_status()
        elif cmd == "torcheck":
            self.tor_check()
        elif cmd == "clear" or cmd == "cls":
            self.terminal.clear()
            self.append_terminal("[+] Terminal flushed")
        elif cmd in ("exit", "quit", "q"):
            self.sair()
        else:
            self.append_terminal(f"[-] ghost command not found: {cmd}", alert=True)
            self.append_terminal("try: help")

    def show_help(self):
        cmds = [
            " help              →  this menu",
            " status            →  node snapshot",
            " start / stop      →  shadow monitor toggle",
            " netstat           →  active connections + listeners",
            " arp               →  local ARP cache spoof check",
            " whois <ip>        →  geo / asn lookup (sim)",
            " packetdump        →  fake live packet capture",
            " honeypot          →  trapped bots & scanners",
            " torcheck          →  exit node fingerprint",
            " logs / tail       →  recent shadow log",
            " clear             →  wipe screen",
            " exit              →  ghost out",
        ]
        self.append_terminal("─" * 64)
        self.append_terminal(" GHOST COMMANDS v3.7")
        self.append_terminal("─" * 64)
        for c in cmds:
            self.append_terminal(c)
        self.append_terminal("─" * 64)

    def show_status(self):
        data = [
            f"SHADOW NODE STATUS ─ {datetime.now().strftime('%H:%M:%S')}",
            f"  Uptime       : {random.randint(3,120)}d {random.randint(0,23):02d}h",
            f"  Interfaces   : eth0, tun0, wlan1mon",
            f"  Public IP    : {random.choice(['185.220.101.', '89.234.157.'])}" + f"{random.randint(10,250)}.{random.randint(1,255)}",
            f"  ASN          : AS{random.choice([9009,4826,6079,16276,24940])}",
            f"  Location     : {'NL' if random.random()<0.4 else 'DE' if random.random()<0.7 else 'SE'}/{'Amsterdam' if random.random()<0.5 else 'Frankfurt' if random.random()<0.8 else 'Stockholm'}",
            f"  CPU          : {random.randint(18,87)}%  –  spikes to {random.randint(92,99)}%",
            f"  Connections  : {random.randint(12,340)} active  /  {random.randint(1800,12400)} total 24h",
            f"  Threats      : {random.randint(0,7)} HIGH / {random.randint(11,68)} MEDIUM",
            f"  Shadow Mode  : {'ACTIVE' if self.monitorando else 'SLEEP'}",
        ]
        for line in data:
            self.append_terminal(line)

    def iniciar_monitoramento(self):
        if self.monitorando:
            self.append_terminal("[!] Shadow already running", alert=True)
            return
        self.monitorando = True
        self.timer.start(1200 + random.randint(0, 900))  # ~1.2–2.1s
        self.append_terminal("[√] SHADOW MONITORING DEPLOYED – listening dark pool", alert=True)

    def parar_monitoramento(self):
        if not self.monitorando:
            self.append_terminal("[i] Shadow already dormant")
            return
        self.monitorando = False
        self.timer.stop()
        self.append_terminal("[×] SHADOW TERMINATED – stealth mode restored")

    def log_simulado_avancado(self):
        msgs = [
            f"[C2] Beacon detected – {random.choice(['45.32.123.45','104.244.42.129','185.117.118.'])}:{random.randint(40000,65535)} → potential {random.choice(['Cobalt Strike','Sliver','Brute Ratel'])}",
            f"[SCAN] Incoming horizontal scan – {random.randint(30,180)} ports hit from {random.choice(['185.220.101.','146.70.'])}x.x",
            f"[AUTH] Failed RDP bruteforce – user: administrator – {random.randint(47,340)} attempts – src: {random_ip()}",
            f"[DNS] Suspicious exfil – query: {random.choice(['a','b','c'])}x{random.randint(1000,9999)}.evilcorp[.]onion",
            f"[PROXY] SOCKS5 connection established – {random_ip()} → chain length: {random.randint(2,5)}",
            f"[HONEY] Cowrie caught SSH login attempt – user:root pass:{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789!@#$',k=10))}",
            f"[WARN] Kernel module loaded – possible {random.choice(['Diamorphine','SuckIT','rootfoo'])} rootkit",
            f"[DATA] {random.randint(300,4800)} KB exfiltrated to C&C – protocol: HTTPS/DNS",
            f"[ALERT] Credential stuffing detected –  {random.randint(800,4200)} attempts/min – target: smtp.corp.local",
            f"[INFO] Tor circuit built – exit: {random.choice(['DE','NL','US','FR','RU'])} node",
        ]
        linha = random.choice(msgs)
        if "ALERT" in linha or "C2" in linha or "rootkit" in linha:
            self.append_terminal(linha, alert=True)
        else:
            self.append_terminal(linha)

    def netstat(self):
        self.append_terminal("[netstat -tulnpa --numeric]")
        for _ in range(random.randint(6,18)):
            proto = random.choice(["tcp","udp"])
            local  = f"0.0.0.0:{random.randint(1,65535)}" if random.random()<0.6 else f"127.0.0.1:{random.randint(10000,60000)}"
            foreign = f"{random_ip()}:{random.randint(1,65535)}" if random.random()<0.4 else "0.0.0.0:*"
            state   = random.choice(["LISTEN","ESTABLISHED","TIME_WAIT","CLOSE_WAIT","*"]) if proto=="tcp" else ""
            pid     = random.randint(1,65535) if random.random()<0.7 else "-"
            self.append_terminal(f"{proto:4}  {local:22}  {foreign:22}  {state:12}  {pid}")

    def arp_table(self):
        self.append_terminal("[arp -a]")
        for _ in range(random.randint(4,12)):
            ip   = f"192.168.66.{random.randint(1,254)}"
            mac  = ':'.join(f'{random.randint(0,255):02x}' for _ in range(6))
            self.append_terminal(f"{ip:16}  {mac.upper()}  dynamic")

    def whois_fake(self):
        ip = random_ip()
        self.append_terminal(f"[whois {ip}]")
        self.append_terminal(f"inetnum:        {ip}-{ip}")
        self.append_terminal(f"netname:        {random.choice(['HOSTING','CLOUD','VPN','DATACENTER','PROXY'])}-{random.randint(100,999)}")
        self.append_terminal(f"country:        {random.choice(['NL','DE','US','RU','CN','FR'])}")
        self.append_terminal(f"org-name:       {random.choice(['M247','OVH','HETZNER','CONTABO','VULTR','AWS'])}")
        self.append_terminal(f"abuse-mailbox:  abuse@{random.choice(['example','proton','tutanota'])}.com")

    def packet_dump_sim(self):
        self.append_terminal("[tcpdump -i any -nn -c 12]")
        QTimer.singleShot(600,  lambda: self.append_terminal("listening on any, link-type EN10MB..."))
        for delay, line in [
            (1200,  f"IP {random_ip()} > {random_ip()}: ICMP echo request"),
            (1800,  f"IP {random_ip()}.443 > {random_ip()}.52812: Flags [S]"),
            (2400,  f"IP {random_ip()}.53 > {random_ip()}.49123: 12345 1/0/0 A {random_ip()}"),
            (3200,  f"TCP {random_ip()}.22 > {random_ip()}.54321: Flags [P.]"),
        ]:
            QTimer.singleShot(delay, lambda l=line: self.append_terminal(l))

    def honeypot_status(self):
        self.append_terminal("[HONEYPOT STATUS]")
        self.append_terminal(f"  Cowrie   →  {random.randint(9,84)} sessions today")
        self.append_terminal(f"  Dionaea  →  {random.randint(0,19)} malware samples captured")
        self.append_terminal(f"  Wordpot  →  {random.randint(3,47)} WP vuln probes")

    def tor_check(self):
        self.append_terminal("[TOR EXIT NODE CHECK]")
        if random.random() < 0.7:
            self.append_terminal("Current exit appears clean (no recent blacklists)")
        else:
            self.append_terminal("WARN: Exit node flagged – possible DPI tagging", alert=True)

    def ver_logs(self):
        self.append_terminal("═" * 70)
        self.append_terminal(" LAST 14 SHADOW ENTRIES ")
        self.append_terminal("═" * 70)
        for i in range(14):
            h = (datetime.now().hour - i - random.randint(0,3)) % 24
            m = random.randint(0,59)
            s = random.randint(0,59)
            self.append_terminal(f"[{h:02d}:{m:02d}:{s:02d}] {random.choice(['INFO','WARN','ALERT','CRIT'])} – {random.choice(['connection dropped','port knock detected','exfil blocked','C2 heartbeat','bruteforce mitigated'])}")
        self.append_terminal("═" * 70)

    def sair(self):
        if QMessageBox.question(self, "KILL SESSION", "Terminate shadow node?\nAll monitors will go dark.", 
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.close()

def random_ip():
    return ".".join(str(random.randint(0,255)) for _ in range(4))

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