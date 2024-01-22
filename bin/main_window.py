# main_window.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QListWidget, QAbstractItemView, QListWidgetItem, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
from bin.settings_window import SettingsWindow
from bin.naming_window import NamingWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art Namer")
        self.setWindowIcon(QIcon('bin/images/icon.png'))
        self.setGeometry(100, 100, 550, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.setup_ui()

    def setup_ui(self):

        # Image display area
        self.image_list = QListWidget()
        self.image_list.setStyleSheet("background-color: black;") 
        self.image_list.setViewMode(QListWidget.IconMode)  # Display only icons
        self.image_list.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Enable multiple item selection
        self.image_list.setResizeMode(QListWidget.Adjust)  # Adjust layout on window resize
        self.image_list.setFlow(QListWidget.LeftToRight)  # Set flow of items left to right
        self.image_list.setIconSize(QSize(150, 150))  # Set the icon size for thumbnails
        self.layout.addWidget(self.image_list)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Select/Deselect All checkbox
        self.select_all_checkbox = QCheckBox()
        self.select_all_checkbox.stateChanged.connect(self.select_deselect_all)
        button_layout.addWidget(self.select_all_checkbox)

        # Spacer to push the checkbox to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addSpacerItem(spacer)

        # Add button with an icon
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon('bin/images/add.png'))
        self.add_button.setIconSize(QSize(24, 24))
        self.add_button.clicked.connect(self.add_images)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
            }
        """)
        button_layout.addWidget(self.add_button)

        # Remove button with an icon
        self.remove_button = QPushButton()
        self.remove_button.setIcon(QIcon('bin/images/delete.png'))
        self.remove_button.setIconSize(QSize(24, 24))
        self.remove_button.clicked.connect(self.remove_images)
        self.remove_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
            }
        """)
        button_layout.addWidget(self.remove_button)

        # Spacer to push the checkbox to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addSpacerItem(spacer)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(button_layout)

        # Settings button
        #self.settings_button = QPushButton("Settings")
        #self.settings_button.clicked.connect(self.open_settings)
        #self.layout.addWidget(self.settings_button)

        # Horizontal layout for centering the next button
        next_button_layout = QHBoxLayout()

        # Add spacer to push the button to the center
        next_button_layout.addStretch()

        # Continue button
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon('bin/images/continue.png'))  # Set icon for the button
        self.next_button.setIconSize(QSize(150, 45))  # You can adjust this size as needed
        self.next_button.clicked.connect(self.proceed_to_naming)
        self.next_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
            }
        """)
        next_button_layout.addWidget(self.next_button)

        # Add another spacer to ensure the button stays in the center
        next_button_layout.addStretch()

        # Add the next button layout to the main layout
        self.layout.addLayout(next_button_layout)

    def set_next_button_size(self, width, height):
        self.next_button.setFixedSize(QSize(width, height))

    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg)")
        for file in files:
            pixmap = QPixmap(file)
            thumbnail = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            icon = QIcon(thumbnail)
            item = QListWidgetItem(icon, "")  # Set text to empty string
            item.setData(Qt.UserRole, file)  # Store the file path
            self.image_list.addItem(item)

    def remove_images(self):
        selected_items = self.image_list.selectedItems()
        if not selected_items:
            return  # No item selected, nothing to remove
        for item in selected_items:
            self.image_list.takeItem(self.image_list.row(item))

    def select_deselect_all(self):
        all_selected = all(self.image_list.item(i).isSelected() for i in range(self.image_list.count()))
        for i in range(self.image_list.count()):
            self.image_list.item(i).setSelected(not all_selected)

    def open_settings(self):
        # Assuming SettingsWindow is a class you will define in settings_window.py
        # This will create and display the settings window
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def proceed_to_naming(self):
        all_files = [self.image_list.item(i).data(Qt.UserRole) for i in range(self.image_list.count())]
        if not all_files:
            print("No images added.")
            return
        self.naming_window = NamingWindow(all_files)
        self.naming_window.restart_signal.connect(self.restart_main_window)  # Connect the signal
        self.naming_window.show()
        self.hide()  # Optionally hide the main window

    def clear_image_list(self):
        self.image_list.clear()

    def restart_main_window(self):
        self.clear_image_list()  # Clear the list before showing the main window again
        self.show()  # Show the main window again