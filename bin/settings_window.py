#settings_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # File Mode Setting
        self.file_mode_label = QLabel("File Mode:")
        self.file_mode_combo = QComboBox()
        self.file_mode_combo.addItems(["Overwrite Files", "New Files"])
        
        file_mode_layout = QHBoxLayout()
        file_mode_layout.addWidget(self.file_mode_label)
        file_mode_layout.addWidget(self.file_mode_combo)
        self.layout.addLayout(file_mode_layout)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def load_settings(self):
        # TODO: Load settings from a config file or similar
        pass

    def save_settings(self):
        # TODO: Save the selected settings to a config file or similar
        # Example: save the file mode setting
        selected_file_mode = self.file_mode_combo.currentText()
        # Implement saving mechanism here
        pass

# TODO: Implement additional settings and functionalities as needed
