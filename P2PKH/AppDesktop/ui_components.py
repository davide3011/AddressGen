from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QPushButton, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Classe principale per l'interfaccia utente
class BitcoinGeneratorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Configurazione finestra principale
        self.setWindowTitle('Bitcoin P2PKH Address Generator')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale con spaziatura
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header dell'applicazione
        self.header_label = QLabel('Bitcoin P2PKH Address Generator')
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        main_layout.addWidget(self.header_label)
        
        # Selettore di rete
        network_layout = QHBoxLayout()
        network_label = QLabel('Network:')
        network_label.setFont(QFont('Arial', 12))
        self.network_combo = QComboBox()
        self.network_combo.addItems(['mainnet', 'testnet', 'regtest'])
        network_layout.addWidget(network_label)
        network_layout.addWidget(self.network_combo)
        network_layout.addStretch()
        main_layout.addLayout(network_layout)
        
        # Area di visualizzazione dei risultati
        self.address_display = QTextEdit()
        self.address_display.setReadOnly(True)
        self.address_display.setMinimumHeight(300)
        self.address_display.setFont(QFont('Courier', 12))
        self.address_display.setPlainText('Clicca "Genera Indirizzo" per iniziare')
        main_layout.addWidget(self.address_display)
        
        # Pulsanti di controllo
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('Genera Indirizzo')
        self.generate_button.setFont(QFont('Arial', 12))
        self.generate_button.setMinimumHeight(40)
        
        self.download_button = QPushButton('Scarica Chiave')
        self.download_button.setFont(QFont('Arial', 12))
        self.download_button.setMinimumHeight(40)
        self.download_button.setEnabled(False)  # Disabilitato fino alla generazione
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.download_button)
        main_layout.addLayout(button_layout)
        
        # Footer informativo
        footer_label = QLabel('Creato da davide3011 | Versione 1.0 | Bitcoin P2PKH Address Generator')
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setFont(QFont('Arial', 10))
        main_layout.addWidget(footer_label)
        main_layout.addStretch()
    
    # Metodi di utilità per l'interfaccia
    def update_address_display(self, text):
        self.address_display.setPlainText(text)
    
    def set_generate_button_enabled(self, enabled):
        self.generate_button.setEnabled(enabled)
    
    def set_download_button_enabled(self, enabled):
        self.download_button.setEnabled(enabled)
    
    def get_selected_network(self):
        return self.network_combo.currentText()