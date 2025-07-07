import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui_components import BitcoinGeneratorUI
from controller import BitcoinController
from themes import ThemeManager

# Funzione di utilità per ottenere il percorso dell'icona
def get_icon_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'icon.ico')  # PyInstaller
    return os.path.join(os.path.dirname(__file__), 'icon.ico')  # Sviluppo

# Classe principale dell'applicazione
class BitcoinAddressGenerator(BitcoinGeneratorUI):
    def __init__(self):
        super().__init__()
        self.controller = BitcoinController(self)
        
        # Connette il cambio di rete al tema
        self.network_combo.currentTextChanged.connect(self.on_network_changed)
        
        # Imposta l'icona se disponibile
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.apply_theme('mainnet')
    
    def apply_theme(self, network):
        # Applica il tema basato sulla rete selezionata
        self.setStyleSheet(ThemeManager.get_stylesheet(network))
        self.header_label.setStyleSheet(ThemeManager.get_header_style(network))
    
    def on_network_changed(self, network):
        # Gestisce il cambio di rete
        self.apply_theme(network)
        self.controller.on_network_changed(network)

def main():
    app = QApplication(sys.argv)
    
    # Imposta l'icona globale dell'applicazione
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Crea e mostra la finestra principale
    window = BitcoinAddressGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
