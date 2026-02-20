import sys
import random
import time
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QPlainTextEdit, QSplitter, QMessageBox,
    QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINELA v2.0 – ROOT ACCESS REQUIRED")
        self.setFixedSize(460, 560)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #00050f, stop:1 #001400);
            }
            QLabel { color: #00ff5e; font-family: Consolas; }
            QLineEdit {
                background: #0a1a0a;
                color: #00ff9d;
                border: 1px solid #00ff5e;
                border-radius: 4px;
                padding: 9px;
                font-family: Consolas;
            }
            QPushButton {
                background: #00ff5e;
                color: black;
                font-weight: bold;
                border: none;
                padding: 15px;
                border-radius: 4px;
                font-family: Consolas;
            }
            QPushButton:hover { background: #00cc4d; }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(40)

        logo = QLabel("SENTINELA\nv2.0")
        logo.setFont(QFont("Consolas", 42, QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("color: #00ff5e; letter-spacing: 4px;")
        layout.addWidget(logo)

        form = QVBoxLayout()
        form.setSpacing(20)
        user_label = QLabel("IDENTIFIER:")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("root | Ericlm | ghost")

        pass_label = QLabel("AUTH KEY:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("••••••••••")

        for lbl, widget in [(user_label, self.user_input), (pass_label, self.pass_input)]:
            lbl.setFont(QFont("Consolas", 14))
            form.addWidget(lbl)
            form.addWidget(widget)

        layout.addLayout(form)

        btn = QPushButton("EXECUTE BREACH SEQUENCE")
        btn.clicked.connect(self.verificar_login)
        layout.addWidget(btn)

        self.setLayout(layout)
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

    def verificar_login(self):
        u = self.user_input.text().strip().lower()
        p = self.pass_input.text().strip()
        valid_users = ["root", "ericlm", "admin", "ghost", ""]
        if u in valid_users and p in ["Evo@0101", "sentinela", "darknet", ""]:
            self.accept()
        else:
            QMessageBox.critical(self, "ACCESS DENIED", "[!] INTRUSION ATTEMPT LOGGED [!]")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SENTINELA v3.8 – SHADOW CORE")
        self.resize(1440, 900)
        self.setStyleSheet("QMainWindow { background: #000814; }")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 5)

        # Header
        hdr = QHBoxLayout()
        logo = QLabel("SENTINELA  v3.8")
        logo.setFont(QFont("Consolas", 28, QFont.Weight.Bold))
        logo.setStyleSheet("color: #00ff5e;")
        title = QLabel("DEEP SHADOW MONITORING & ACTIVE DEFENSE")
        title.setFont(QFont("Consolas", 16))
        title.setStyleSheet("color: #88ffaa;")
        hdr.addWidget(logo)
        hdr.addSpacing(40)
        hdr.addWidget(title)
        hdr.addStretch()
        main_layout.addLayout(hdr)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: #00ff5e; width: 3px; }")

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QWidget { background: #0a120a; border-right: 3px solid #00ff5e; }
            QPushButton {
                background: #111911;
                color: #00ff88;
                text-align: left;
                padding: 14px 18px;
                border: none;
                margin: 4px 8px;
                font-family: Consolas;
            }
            QPushButton:hover { background: #00ff5e; color: black; }
        """)
        sb_layout = QVBoxLayout(sidebar)
        actions = [
            ("▶ ACTIVATE SHADOW", self.iniciar_monitoramento),
            ("⏹ DEACTIVATE SHADOW", self.parar_monitoramento),
            ("🛡️ FIREWALL", self.firewall_status_detailed),
            ("🌐 NETSTAT / INTERFACES", self.ifconfig),
            ("🔍 NMAP SCAN", self.nmap_sim),
            ("📊 PROCESSES", self.ps),
            ("📡 PACKET CAPTURE", self.packet_dump_sim),
            ("📜 SHADOW LOGS", self.ver_logs),
            ("⚠️ TOP BLOCKED", self.show_top_blocked_ips),
            ("🚪 TERMINATE SESSION", self.sair),
        ]
        for txt, fn in actions:
            b = QPushButton(txt)
            b.clicked.connect(fn)
            sb_layout.addWidget(b)
        sb_layout.addStretch()
        splitter.addWidget(sidebar)

        # Terminal
        term_frame = QFrame()
        term_frame.setStyleSheet("QFrame { background: #000; border: 3px solid #00ff5e; }")
        term_layout = QVBoxLayout(term_frame)
        term_layout.setContentsMargins(14, 14, 14, 14)

        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QPlainTextEdit {
                background: rgba(0, 20, 0, 0.94);
                color: #00ff88;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
                selection-background-color: #004d1a;
            }
        """)
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.97)
        self.terminal.setGraphicsEffect(opacity)
        term_layout.addWidget(self.terminal)

        cmd_widget = QWidget()
        cmd_layout = QHBoxLayout(cmd_widget)
        self.prompt = QLabel("ghost@sentinela:~/darkpool $ ")
        self.prompt.setStyleSheet("color: #00ffaa; font-family: Consolas; font-size: 14px;")
        self.cmd_input = QLineEdit()
        self.cmd_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #00ffbb;
                border: none;
                font-family: Consolas;
                font-size: 14px;
            }
        """)
        self.cmd_input.returnPressed.connect(self.executar_comando)
        cmd_layout.addWidget(self.prompt)
        cmd_layout.addWidget(self.cmd_input)
        term_layout.addWidget(cmd_widget)

        splitter.addWidget(term_frame)
        splitter.setSizes([260, 1180])
        main_layout.addWidget(splitter, 1)

        # Footer
        self.footer = QLabel("SENTINELA v2.0 | ACTIVE THREATS: 0 | Ericlm – 2026")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer.setStyleSheet("""
            QLabel {
                background: #0a0f0a;
                color: #00cc66;
                padding: 10px;
                font-family: Consolas;
                font-size: 13px;
                border-top: 2px solid #00ff5e;
            }
        """)
        main_layout.addWidget(self.footer)

        # Estado
        self.monitorando = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.log_simulado_avancado)

        # Firewall + stats
        self.firewall_rules = {"127.0.0.1": "allow", "192.168.66.1": "allow", "10.8.0.1": "allow"}
        self.firewall_stats = {}
        self.total_dropped = 0
        self.firewall_mode = "NORMAL"
        self.threat_level = 0

        self.boot_sequence()
        self.mover_cursor_fim()

    def boot_sequence(self):
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║        SENTINELA v2.0  –  SHADOW CORE INITIALIZED            ║",
            "╚══════════════════════════════════════════════════════════════╝",
            f"[BOOT] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "[NET]  eth0  192.168.66.13/24   MAC 00:1c:42:aa:ff:01",
            "[NET]  tun0  10.8.0.6           Mullvad-style exit",
            "[NET]  wlan1mon  CHANNEL 11     monitor mode active",
            "[FW]   Default policy: DROP     Active rules: 3",
            "[SYS]  Kernel: 6.9.x-parrot     Hidden procs: 3",
            "[HONEYPOT] Cowrie/Dionaea   23 traps last 48h",
            "[ALERT] Threat level: LOW       Packets dropped: 0",
            "",
            "Type 'help' for ghost commands.",
            "Welcome back, shadow."
        ]
        for line in lines:
            self.append_terminal(line)

    def append_terminal(self, text: str, alert=False, critical=False):
        prefix = ""
        if critical:
            prefix = "!!! CRITICAL !!! "
        elif alert:
            prefix = "[ALERT] "
        self.terminal.appendPlainText(prefix + text)
        self.mover_cursor_fim()
        self.atualizar_rodape()

    def mover_cursor_fim(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()

    def atualizar_rodape(self):
        nivel = "LOW" if self.threat_level < 3 else "MEDIUM" if self.threat_level < 8 else "HIGH"
        cor = "#00ff88" if self.threat_level < 3 else "#ffaa00" if self.threat_level < 8 else "#ff4444"
        self.footer.setStyleSheet(f"""
            QLabel {{
                background: #0a0f0a;
                color: {cor};
                padding: 10px;
                font-family: Consolas;
                font-size: 13px;
                border-top: 2px solid #00ff5e;
            }}
        """)
        self.footer.setText(f"SENTINELA v2.0 | ACTIVE THREATS: {self.threat_level} | LEVEL: {nivel} | Ericlm – 2026")

    def executar_comando(self):
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        self.append_terminal(f"ghost@sentinela:~/darkpool $ {cmd}")
        self.cmd_input.clear()

        parts = cmd.split()
        base = parts[0].lower()

        if base in ("help", "?"):
            self.show_help()
        elif base in ("status", "sys"):
            self.show_status()
        elif base in ("start", "activate"):
            self.iniciar_monitoramento()
        elif base in ("stop", "deactivate"):
            self.parar_monitoramento()
        elif base in ("fw", "firewall"):
            if len(parts) == 1 or parts[1] in ("status", "show"):
                self.firewall_status_detailed()
            elif len(parts) >= 3:
                sub = parts[1]
                ip = parts[2]
                if sub in ("block", "drop", "deny"):
                    self.firewall_rules[ip] = "block"
                    self.append_terminal(f"[FW] BLOCK added → {ip}")
                elif sub in ("allow", "accept", "permit"):
                    self.firewall_rules[ip] = "allow"
                    self.append_terminal(f"[FW] ALLOW added → {ip}")
                elif sub in ("del", "remove", "delete"):
                    self.firewall_rules.pop(ip, None)
                    self.append_terminal(f"[FW] Rule removed → {ip}")
        elif base in ("fwreset", "resetfw"):
            self.firewall_rules = {"127.0.0.1": "allow", "192.168.66.1": "allow", "10.8.0.1": "allow"}
            self.firewall_stats.clear()
            self.total_dropped = 0
            self.append_terminal("[FW] Resetado para default policy")
        elif base == "topblocked":
            self.show_top_blocked_ips()
        elif base in ("netstat", "ifconfig", "ip", "ip a"):
            self.ifconfig()
        elif base in ("nmap", "scan"):
            self.nmap_sim()
        elif base in ("ps", "processes", "proc"):
            self.ps()
        elif base in ("whoami", "id"):
            self.whoami()
        elif base in ("hashcat", "crack"):
            self.hashcat_sim()
        elif base == "exploit":
            self.exploit_sim()
        elif base == "matrix":
            self.matrix_effect()
        elif base in ("clear", "cls"):
            self.terminal.clear()
            self.append_terminal("[+] Buffer flushed")
        elif base in ("logs", "tail", "dump"):
            self.ver_logs()
        elif base in ("exit", "quit", "logout"):
            self.sair()
        else:
            self.append_terminal(f"[-] Unknown command: {cmd}", alert=True)

    def show_help(self):
        help_text = [
            " ghost commands v2.0 ",
            "─────────────────────",
            " help              →  this menu",
            " status            →  system snapshot",
            " start / stop      →  shadow monitoring",
            " fw status         →  firewall rules + stats",
            " fw block/allow <ip> → manage rules",
            " topblocked        →  most blocked IPs",
            " nmap / scan       →  fake network scan",
            " netstat / ifconfig → interfaces & connections",
            " ps / processes    →  running processes",
            " whoami / id       →  current identity",
            " hashcat <hash>    →  fake hash cracking",
            " exploit           →  load exploit kit (sim)",
            " matrix            →  matrix rain effect",
            " clear             →  clear screen",
            " logs / tail       →  recent logs",
            " exit              →  terminate session",
        ]
        self.append_terminal("═" * 60)
        for line in help_text:
            self.append_terminal(line)
        self.append_terminal("═" * 60)

    def show_status(self):
        lines = [
            f"SHADOW STATUS ─ {datetime.now().strftime('%H:%M:%S')}",
            f"  Uptime           : {random.randint(5, 180)}d {random.randint(0,23):02d}h",
            f"  Public IP        : {random_ip()}  ({random.choice(['NL','DE','SE','US'])} exit)",
            f"  Threat level     : {self.threat_level} ({'LOW' if self.threat_level<3 else 'MEDIUM' if self.threat_level<8 else 'HIGH'})",
            f"  Packets dropped  : {self.total_dropped:,}",
            f"  Active rules     : {len(self.firewall_rules)}",
            f"  Shadow mode      : {'ACTIVE' if self.monitorando else 'DORMANT'}",
        ]
        for line in lines:
            self.append_terminal(line)

    def iniciar_monitoramento(self):
        if self.monitorando:
            self.append_terminal("[!] Shadow already active", alert=True)
            return
        self.monitorando = True
        self.timer.start(random.randint(800, 1800))
        self.append_terminal("[√] SHADOW MONITORING DEPLOYED", alert=True)
        self.threat_level += 1
        self.atualizar_rodape()

    def parar_monitoramento(self):
        if not self.monitorando:
            self.append_terminal("[i] Shadow already dormant")
            return
        self.monitorando = False
        self.timer.stop()
        self.append_terminal("[×] SHADOW CORE HIBERNATED")
        if self.threat_level > 0:
            self.threat_level -= 1
        self.atualizar_rodape()

    def log_simulado_avancado(self):
        if not self.monitorando:
            return

        events = [
            ("[C2]", f"Beacon from {random_ip()} – possible {random.choice(['Cobalt','Sliver','BruteRatel'])}"),
            ("[SCAN]", f"Port scan detected – {random.randint(40,220)} ports from {random_ip()}"),
            ("[BRUTE]", f"RDP/SSH bruteforce – {random.randint(120,800)} attempts – {random_ip()}"),
            ("[EXFIL]", f"DNS tunneling suspected – {random.randint(2,12)} queries/min"),
            ("[HONEY]", f"Cowrie caught: root:{''.join(random.choices('a-z0-9!@#',k=9))}"),
        ]

        event, msg = random.choice(events)
        if random.random() < 0.4:
            self.append_terminal(f"{event} {msg}", alert=True)
            self.threat_level += random.randint(1, 2)
        else:
            self.append_terminal(f"[FW] {event} attempt blocked – {msg}")

        self.atualizar_rodape()

        # Firewall chance
        if random.random() < 0.6:
            ip = random_ip()
            action = self.decide_firewall_action(ip, random.randint(1,65535))
            if action in ("DROP", "REJECT"):
                self.total_dropped += 1
                self.firewall_stats[ip] = self.firewall_stats.get(ip, 0) + 1
                self.append_terminal(f"[FW {action}] {ip} → blocked", alert=True)
                self.threat_level += 1

    def decide_firewall_action(self, ip, port):
        if self.firewall_mode == "DROP_ALL":
            return "DROP"
        if ip in self.firewall_rules:
            return "ALLOW" if self.firewall_rules[ip] == "allow" else "DROP"
        if port in [445, 3389, 22]:
            return "DROP" if random.random() < 0.8 else "ALLOW"
        return "ALLOW"

    def firewall_status_detailed(self):
        self.append_terminal("═" * 70)
        self.append_terminal(" FIREWALL – SENTINELA PF v3.8 ")
        self.append_terminal("═" * 70)
        self.append_terminal(f"Policy mode     : {self.firewall_mode}")
        self.append_terminal(f"Packets dropped : {self.total_dropped:,}")
        self.append_terminal(f"Active rules    : {len(self.firewall_rules)}")
        self.append_terminal("")
        self.append_terminal("Rules:")
        for ip, act in sorted(self.firewall_rules.items()):
            self.append_terminal(f"  {ip:18} → {act.upper()}")
        self.append_terminal("")
        self.show_top_blocked_ips(short=True)
        self.append_terminal("═" * 70)

    def show_top_blocked_ips(self, short=False):
        if not self.firewall_stats:
            self.append_terminal("No blocks recorded yet.")
            return
        top = sorted(self.firewall_stats.items(), key=lambda x: x[1], reverse=True)[:7]
        for ip, cnt in top:
            self.append_terminal(f"  {ip:16} : {cnt:,} drops")
        if not short:
            self.append_terminal(f"Total unique blocked: {len(self.firewall_stats)}")

    def ifconfig(self):
        lines = [
            "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500",
            f"        inet 192.168.66.13  netmask 255.255.255.0  broadcast 192.168.66.255",
            f"        ether 00:1c:42:aa:ff:01  txqueuelen 1000",
            "",
            "tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500",
            f"        inet 10.8.0.6  netmask 255.255.255.255",
            "",
            "wlan1mon: flags=8923<UP,BROADCAST,NOARP,PROMISC,MULTICAST>  mtu 1500",
            "        mode MONITOR"
        ]
        for line in lines:
            self.append_terminal(line)

    def nmap_sim(self):
        self.append_terminal("[nmap -sS -T4 -n 192.168.66.0/24]")
        QTimer.singleShot(800, lambda: self.append_terminal("Starting Nmap 7.95 ( https://nmap.org )"))
        QTimer.singleShot(1800, lambda: self.append_terminal("Nmap scan report for 192.168.66.1"))
        QTimer.singleShot(2200, lambda: self.append_terminal("Host is up (0.0012s latency)."))
        QTimer.singleShot(2800, lambda: self.append_terminal("PORT    STATE SERVICE"))
        QTimer.singleShot(3400, lambda: self.append_terminal("22/tcp  open  ssh"))
        QTimer.singleShot(4000, lambda: self.append_terminal("80/tcp  open  http"))
        QTimer.singleShot(4600, lambda: self.append_terminal("445/tcp open  microsoft-ds"))
        QTimer.singleShot(5200, lambda: self.append_terminal("Nmap done: 256 IP addresses (12 hosts up) scanned in 4.82 seconds"))

    def ps(self):
        procs = [
            "root     1423  0.0  0.1  98765  4321 ?        Ss   02:14   0:00 /usr/sbin/sshd",
            "ghost    5678  4.2  1.8 345678 98765 pts/0    Sl+  03:22   1:45 python3 sentinela.py",
            "root     9012  0.0  0.0  12345  6789 ?        S    04:01   0:00 [kworker/4:1]",
            "???      6666  ??   ??   ?????  ???? ?        ??   ??     hidden process (possible rootkit)",
        ]
        self.append_terminal("[ps aux --sort=-%cpu | head -12]")
        for p in procs + [f"ghost   {random.randint(1000,9999)}  {random.uniform(0.1,8.0):.1f} ..." for _ in range(5)]:
            self.append_terminal(p)

    def whoami(self):
        self.append_terminal("uid=0(root) gid=0(root) groups=0(root),1(daemon),999(ghost)")
        self.append_terminal("Current context: shadow / darkpool")

    def hashcat_sim(self):
        self.append_terminal("[hashcat -m 0 -a 3 target.hash ?a?a?a?a?a?a]")
        self.append_terminal("Session..........: hashcat")
        self.append_terminal("Status...........: Cracked")
        self.append_terminal("Hash.Mode........: 0 (MD5)")
        time.sleep(0.8)  # simula demora
        self.append_terminal("Recovered........: 1/1 (100.00%) Digests")
        self.append_terminal("Progress.........: 100.00%")
        self.append_terminal("Cracked password.: Evo@0101")
        self.append_terminal("[+] Password recovered in simulated time: 0d 1h 42m 19s")

    def exploit_sim(self):
        self.append_terminal("╔════════════════════════════════════╗")
        self.append_terminal("║     EXPLOIT KIT LOADED – v4.2      ║")
        self.append_terminal("║   CVE-2025-XXXX – Zero-day active  ║")
        self.append_terminal("╚════════════════════════════════════╝")
        self.append_terminal("[!] Payload delivery vector: HTTPS")
        self.append_terminal("[!] Target acquired. Awaiting C2 beacon...")
        self.threat_level += 3
        self.atualizar_rodape()

    def matrix_effect(self):
        self.append_terminal("[MATRIX MODE – 5 seconds]")
        chars = "01█▓▒░■□◾◽▪▫"
        for _ in range(8):
            line = "".join(random.choice(chars) for _ in range(80))
            self.append_terminal(line)
            QApplication.processEvents()
            time.sleep(0.15)
        self.append_terminal("[MATRIX sequence terminated]")

    def ver_logs(self):
        self.append_terminal("═" * 70)
        self.append_terminal(" LAST 20 SHADOW ENTRIES ")
        self.append_terminal("═" * 70)
        for i in range(20):
            h = (datetime.now().hour - i - random.randint(0,5)) % 24
            self.append_terminal(f"[{h:02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}] {random.choice(['INFO','WARN','ALERT','CRIT'])} – {random.choice(['connection dropped','C2 heartbeat blocked','bruteforce mitigated','port knock detected','exfil attempt stopped'])}")
        self.append_terminal("═" * 70)

    def sair(self):
        if QMessageBox.question(self, "TERMINATE", "Really kill shadow node?\nAll monitoring will go dark.", 
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.close()

    def packet_dump_sim(self):
        self.append_terminal("[tcpdump -i any -nn -c 10]")
        for _ in range(8):
            QTimer.singleShot(random.randint(400, 2200), lambda: self.append_terminal(
                f"IP {random_ip()} > {random_ip()}: {random.choice(['TCP 443 → 52841 [S]','ICMP echo request','UDP 53 → 49152 DNS query'])}"
            ))

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)