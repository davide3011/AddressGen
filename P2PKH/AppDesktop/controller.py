import json
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox, QFileDialog
from utils import generate_address

# Thread separato per evitare il blocco dell'interfaccia durante la generazione
class AddressGeneratorThread(QThread):
    address_generated = Signal(dict)
    
    def __init__(self, network):
        super().__init__()
        self.network = network
    
    def run(self):
        # Genera l'indirizzo e emette il segnale con il risultato
        self.address_generated.emit(generate_address(self.network))

# Controller principale - gestisce la logica di business
class BitcoinController:
    def __init__(self, ui):
        self.ui = ui
        self.current_data = None  # Dati dell'ultimo indirizzo generato
        self.generator_thread = None
        # Connette i pulsanti alle rispettive funzioni
        self.ui.generate_button.clicked.connect(self.generate_new_address)
        self.ui.download_button.clicked.connect(self.download_key)
    
    def on_network_changed(self, network):
        # Reset dei dati quando cambia la rete
        self.current_data = None
        self.ui.update_address_display('Clicca "Genera Indirizzo" per la nuova rete')
        self.ui.set_download_button_enabled(False)
    
    def generate_new_address(self):
        # Avvia la generazione in un thread separato
        self.ui.update_address_display('Generazione in corso...')
        self.ui.set_generate_button_enabled(False)
        
        self.generator_thread = AddressGeneratorThread(self.ui.get_selected_network())
        self.generator_thread.address_generated.connect(self.on_address_generated)
        self.generator_thread.start()
    
    def on_address_generated(self, data):
        # Gestisce il risultato della generazione
        if 'error' in data:
            self.ui.update_address_display(f'Errore: {data["error"]}')
        else:
            self.current_data = data
            # Formatta e mostra i dati generati
            display_text = (f"Indirizzo: {data['address']}\n\n"
                          f"Chiave Privata (HEX): {data['private_key_hex']}\n\n"
                          f"Chiave Privata (WIF): {data['private_key_wif']}\n\n"
                          f"Chiave Pubblica: {data['public_key']}\n\n"
                          f"Network: {data['network']}\nTipo: {data['type']}")
            self.ui.update_address_display(display_text)
            self.ui.set_download_button_enabled(True)
        
        self.ui.set_generate_button_enabled(True)
    

    
    def download_key(self):
        # Salva i dati della chiave in un file JSON
        if not self.current_data:
            QMessageBox.warning(self.ui, 'Attenzione', 'Nessuna chiave generata ancora!')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.ui, 'Salva Chiave', 'key.json', 'JSON Files (*.json)')
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_data, f, indent=2)
                QMessageBox.information(self.ui, 'Successo', f'Chiave salvata in: {file_path}')
            except Exception as e:
                QMessageBox.critical(self.ui, 'Errore', f'Errore nel salvare il file: {str(e)}')