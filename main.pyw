# main.pyw

import sys
from PyQt5.QtWidgets import QApplication
from bin.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Extended dark theme style sheet
    dark_stylesheet = """
    QMainWindow, QDialog {
        background-color: #292929;
    }
    QPushButton, QComboBox {
        background-color: #353535;
        color: white;
        border: 1px solid #1a1a1a;
        font-size: 18px;
        padding: 5px;
    }
    QPushButton:hover, QComboBox:hover {
        background-color: #3d3d3d;
        border: 2px solid white;
    }
    QLabel, QComboBox {
        color: white;
        font-size: 18px;
    }
    QComboBox::drop-down {
        border: 0px;
    }
    QComboBox::down-arrow {
        image: url(/path/to/your/icon.png);  /* Path to a suitable arrow icon */
    }
    QComboBox QAbstractItemView {
        background: #353535;
        color: white;
        selection-background-color: #3d3d3d;
    }
    """

    # Apply the dark theme style sheet
    app.setStyleSheet(dark_stylesheet)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
