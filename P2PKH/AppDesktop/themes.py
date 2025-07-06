# Gestisce i temi dell'applicazione per le diverse reti Bitcoin
class ThemeManager:
    # Colori per ogni tipo di rete
    THEMES = {
        'mainnet': {
            'base': '#ffe4b5', 'primary': '#ffefd5', 'secondary': '#fff8dc',
            'accent': '#daa520', 'text': '#2f4f4f'
        },
        'testnet': {
            'base': '#f0fff0', 'primary': '#f5fffa', 'secondary': '#e6ffe6',
            'accent': '#228b22', 'text': '#2f4f4f'
        },
        'regtest': {
            'base': '#e6f3ff', 'primary': '#f0f8ff', 'secondary': '#e0f6ff',
            'accent': '#4682b4', 'text': '#2f4f4f'
        }
    }
    
    @classmethod
    def get_stylesheet(cls, network):
        # Ottiene i colori per la rete specificata (default: mainnet)
        colors = cls.THEMES.get(network, cls.THEMES['mainnet'])
        
        return f"""
            QMainWindow {{
                background-color: {colors['base']};
                color: {colors['text']};
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel {{
                color: {colors['text']};
                font-size: 14px;
                padding: 5px;
            }}
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {colors['primary']}, stop:1 {colors['secondary']});
                color: {colors['text']};
                border: 2px solid {colors['accent']};
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {colors['secondary']}, stop:1 {colors['primary']});
            }}
            QPushButton:pressed {{
                background: {colors['accent']};
            }}
            QPushButton:disabled {{
                background: #333;
                color: #666;
                border: 2px solid #555;
            }}
            QComboBox {{
                background: {colors['primary']};
                color: {colors['text']};
                border: 2px solid {colors['accent']};
                border-radius: 6px;
                padding: 8px 16px;
                selection-background-color: {colors['secondary']};
                min-width: 150px;
            }}
            QTextEdit {{
                background: {colors['primary']};
                color: {colors['text']};
                border: 2px solid {colors['accent']};
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }}
            QScrollBar:vertical {{
                background: {colors['primary']};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['secondary']};
                min-height: 20px;
                border-radius: 6px;
            }}
        """
    
    @classmethod
    def get_header_style(cls, network):
        # Stile specifico per l'header con colore accent
        colors = cls.THEMES.get(network, cls.THEMES['mainnet'])
        return f"QLabel {{ color: {colors['accent']}; }}"