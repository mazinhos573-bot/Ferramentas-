import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QScrollArea, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl, QPoint, QSize
from PyQt5.QtGui import QDesktopServices, QFont, QCursor, QColor, QPainter, QBrush

class FloatingButton(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(50, 50)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn = QPushButton("EVO")
        self.btn.setFixedSize(50, 50)
        self.btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #0223f5;
                color: white;
                border-radius: 25px;
                font-weight: bold;
                border: 2px solid rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: #0223f5;
            }
        """)
        self.btn.clicked.connect(self.restore_main_window)
        layout.addWidget(self.btn)

    def restore_main_window(self):
        self.hide()
        self.main_window.show()
        # Centralize a janela principal em torno da posição Y do botão, se possível,

        # ou simplesmente mostre-o onde estava.


class ClickableLabel(QLabel):
    def __init__(self, text, callback=None, parent=None):
        super().__init__(text, parent)
        self.callback = callback
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.callback:
            self.callback()


class MenuItem(QWidget):
    def __init__(self, icon_text, title, url, badge=None):
        super().__init__()
        self.url = url
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(40)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(12)
        
        # Icon
        self.icon_lbl = QLabel(icon_text)
        self.icon_lbl.setFont(QFont("Segoe UI Emoji", 12))
        self.icon_lbl.setStyleSheet("color: #2d3748;")
        layout.addWidget(self.icon_lbl)
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setFont(QFont("Segoe UI", 10))
        self.title_lbl.setStyleSheet("color: #1f2937; font-weight: 500;")
        layout.addWidget(self.title_lbl)
        
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Badge
        if badge:
            self.badge_lbl = QLabel(str(badge))
            self.badge_lbl.setAlignment(Qt.AlignCenter)
            self.badge_lbl.setFixedSize(24, 20)
            self.badge_lbl.setStyleSheet("""
                background-color: #e5e7eb;
                color: #374151;
                border-radius: 10px;
                font-size: 11px;
                font-weight: bold;
            """)
            layout.addWidget(self.badge_lbl)
            
        self.setStyleSheet("""
            MenuItem {
                background-color: transparent;
                border-radius: 8px;
            }
            MenuItem:hover {
                background-color: rgba(243, 244, 246, 0.8);
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            QDesktopServices.openUrl(QUrl(self.url))


class SideMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(320)
        self.setFixedHeight(750)
        
        self.oldPos = self.pos()
        self.floating_btn = FloatingButton(self)
        
        self.initUI()
        self.center_on_screen()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Widget de fundo (para estilização e transparência)
        self.bg_widget = QWidget()
        # Transparência de 20% a 50% solicitada.
        # rgba(255,255,255, 200) tem aproximadamente 20% de transparência, mantendo a legibilidade.

        # Se desejar 50% de transparência, use rgba(255,255,255, 128).
        self.bg_widget.setStyleSheet("""
            QWidget#bg {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 100);
            }
        """)
        self.bg_widget.setObjectName("bg")
        
        # Poderíamos adicionar um efeito de sombra projetada aqui, mas vamos manter simples para otimizar o desempenho.
        bg_layout = QVBoxLayout(self.bg_widget)
        bg_layout.setContentsMargins(16, 20, 16, 20)
        bg_layout.setSpacing(16)
        
        # --- HEADER ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        
        # Bloco de logotipo
        logo_lbl = QLabel("E")
        logo_lbl.setFixedSize(40, 40)
        logo_lbl.setAlignment(Qt.AlignCenter)
        logo_lbl.setStyleSheet("""
            background-color: #0223f5;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            font-size: 20px;
        """)
        header_layout.addWidget(logo_lbl)
        
        # Área de título
        title_vlayout = QVBoxLayout()
        title_vlayout.setSpacing(0)
        title_lbl = QLabel("ERICLM.EVO")
        title_lbl.setStyleSheet("font-weight: 800; font-size: 16px; color: #111827;")
        version_lbl = QLabel("System Menu v1.0")
        version_lbl.setStyleSheet("font-size: 12px; color: #6b7280;")
        title_vlayout.addWidget(title_lbl)
        title_vlayout.addWidget(version_lbl)
        title_vlayout.setAlignment(Qt.AlignVCenter)
        header_layout.addLayout(title_vlayout)
        
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        #Botão Minimizar
        min_btn = QPushButton("—")
        min_btn.setFixedSize(24, 24)
        min_btn.setCursor(QCursor(Qt.PointingHandCursor))
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #9ca3af;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover { color: #374151; }
        """)
        min_btn.clicked.connect(self.minimize_to_float)
        header_layout.addWidget(min_btn, 0, Qt.AlignTop)
        
        bg_layout.addLayout(header_layout)
        
        # --- SEPARADOR ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: 1px solid rgba(0,0,0,0.05);")
        bg_layout.addWidget(line)
        
        # --- ÁREA DE ROLAGEM PARA VER OS LINKS ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)
        
        # Ferramenta auxiliar para adicionar cabeçalhos de seção
        def add_section_header(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #9ca3af; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
            lbl.setContentsMargins(12, 10, 12, 4)
            scroll_layout.addWidget(lbl)

        # SEÇÃO DE ASSISTENTES
        add_section_header("ASSISTENTES")
        scroll_layout.addWidget(MenuItem("🔧", "Code Refine", "https://aistudio.google.com/apps/0103e43f-9e61-4085-af7c-0c2a7737659b?showPreview=true&showAssistant=true&fullscreenApplet=true"))
        scroll_layout.addWidget(MenuItem("💼", "Dev Web/Apps", "https://aistudio.google.com/apps/ab73b8f2-3b87-428c-9b20-5d0c327da43f?showPreview=true&showAssistant=true")) #,badge=2
        scroll_layout.addWidget(MenuItem("🎯", "Código Pro", "https://aistudio.google.com/apps/406331d2-8ebd-4e0f-be63-5f8f916389ee?showPreview=true&showAssistant=true"))
        scroll_layout.addWidget(MenuItem("📐", "Senior Architect", "https://aistudio.google.com/apps/89029522-cb60-44da-9585-92106d39f3c9?showPreview=true&showAssistant=true"))

        # SEÇÃO DE RECURSOS
        add_section_header("RECURSOS")
        scroll_layout.addWidget(MenuItem("🔗", "GitHub", "https://github.com/"))
        scroll_layout.addWidget(MenuItem("🎨", "Font Awesome", "https://fontawesome.com/search"))
        scroll_layout.addWidget(MenuItem("📦", "Gerador de QR Code", "https://qr.io/?gad_source=1&gad_campaignid=11398459434&gbraid=0AAAAAC6IOXJs2vQuR7ohimFZlrhGtMtoG&gclid=CjwKCAjw5s_QBhAdEiwADD_gBksBji0BSGfYE5PGIknysrUbqtgNPTmouMVTiHK-q6XcISWqVGSn8hoCbjYQAvD_BwE"))

        scroll_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        scroll_area.setWidget(scroll_content)
        bg_layout.addWidget(scroll_area)
        
        # --- RODAPÉ (Imagem de perfil) ---
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(12, 10, 12, 0)
        
        # Avatar fictício (usando um círculo colorido com texto)
        avatar_lbl = ClickableLabel("MG", callback=QApplication.instance().quit)
        avatar_lbl.setFixedSize(36, 36)
        avatar_lbl.setAlignment(Qt.AlignCenter)
        avatar_lbl.setToolTip("Fechar o sistema")
        avatar_lbl.setStyleSheet("""
            background-color: #0223f5;
            color: white;
            border-radius: 18px;
            font-weight: bold;
        """)
        footer_layout.addWidget(avatar_lbl)
        
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(0)
        user_name = QLabel("Manoel Guedes")
        user_name.setStyleSheet("font-weight: bold; color: #374151; font-size: 13px;")
        user_email = QLabel("ericlm.evo@gmail.com")
        user_email.setStyleSheet("color: #6b7280; font-size: 11px;")
        user_info_layout.addWidget(user_name)
        user_info_layout.addWidget(user_email)
        
        footer_layout.addLayout(user_info_layout)
        footer_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        bg_layout.addLayout(footer_layout)
        
        main_layout.addWidget(self.bg_widget)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def minimize_to_float(self):
        self.hide()
        screen = QApplication.primaryScreen().geometry()
        # Coloque o botão flutuante na borda central direita.
        btn_x = screen.width() - self.floating_btn.width() - 20
        btn_y = self.pos().y() + (self.height() // 2) - (self.floating_btn.height() // 2)
        self.floating_btn.move(btn_x, btn_y)
        self.floating_btn.show()

    # Lógica de arrastar janelas
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Ativar dimensionamento de DPI alto
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    menu = SideMenu()
    menu.show()
    
    sys.exit(app.exec_())
