# naming_window.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QFileDialog, QCheckBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QGuiApplication, QIcon, QCursor, QTextCursor, QTextCharFormat, QFontMetrics, QTextOption
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer
from bin.api_threads import ImageAnalysisThread, TitleRegenerationThread
import os
import re
import enchant

class NamingWindow(QMainWindow):


########## Constructor and Initialization Methods ##########


    restart_signal = pyqtSignal()
    def __init__(self, image_files):
        super().__init__()
        self.setWindowTitle("Art Namer")
        self.setWindowIcon(QIcon('bin/images/icon.png'))
        self.setGeometry(100, 100, 800, 600)
        self.image_files = image_files
        self.current_index = 0
        #print("Image Files:", image_files)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        self.apply_custom_style()
        self.setup_ui()
        self.display_current_image()

    def setup_ui(self):
        # Left side layout Begin
        self.left_layout = QVBoxLayout()

        # Analyze button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_image)
        self.analyze_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.left_layout.addWidget(self.analyze_button)

        # User Context input field
        self.user_context_input = SpellCheckTextEdit("Enter context here...")
        self.user_context_input.setStyleSheet("background-color: black; color: white; border:none;")

        # Set the fixed height based on font metrics plus an additional margin
        fm = QFontMetrics(self.user_context_input.font())
        margin = 30  # You can adjust this margin as needed
        self.user_context_input.setFixedHeight(fm.height() + margin)

        # Set the vertical size policy to Fixed
        self.user_context_input.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.left_layout.addWidget(self.user_context_input)


        # Display Analysis
        self.analysis_display = QTextEdit()
        self.analysis_display.setStyleSheet("background-color: black; color: white; border:none;")
        self.analysis_display.setReadOnly(True)
        self.left_layout.addWidget(self.analysis_display)

        # Regenerate, Save, and Copy buttons with images HLayout
        self.button_layout = QHBoxLayout()

        #Regenerate Button
        self.regenerate_button = QPushButton()
        self.regenerate_button.setIcon(QIcon('bin/images/refresh.png'))
        self.regenerate_button.setIconSize(QSize(24, 24))
        self.regenerate_button.clicked.connect(self.regenerate_titles)
        self.regenerate_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.regenerate_button.setEnabled(False)
        self.regenerate_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
            }
        """)
        self.button_layout.addWidget(self.regenerate_button)

        # Save Button
        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon('bin/images/save.png'))
        self.save_button.setIconSize(QSize(24, 24))
        self.save_button.clicked.connect(self.save_analysis_to_file)
        self.save_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.save_button.setEnabled(False)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
            }
        """)
        self.button_layout.addWidget(self.save_button)

        # Copy Button
        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon('bin/images/copy.png'))
        self.copy_button.setIconSize(QSize(24, 24))
        self.copy_button.clicked.connect(self.copy_analysis_to_clipboard)
        self.copy_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.copy_button.setEnabled(False)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                border: none;
            }
            QPushButton:hover {
                border: 2px solid white;
            }
        """)
        self.button_layout.addWidget(self.copy_button)

        # Title Layout Begin
        self.left_layout.addLayout(self.button_layout)

        # Title recommendation checkboxes and buttons
        self.title_layouts = []
        self.title_checkboxes = []
        self.title_buttons = []

        # Checkboxes Disabled
        for checkbox in self.title_checkboxes:
            checkbox.setEnabled(False)

        for i in range(5):
            title_layout = QHBoxLayout()
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.checkbox_changed)
            title_button = QPushButton(f"Title {i+1}")
            title_button.clicked.connect(self.select_title)
            title_button.setCursor(QCursor(Qt.PointingHandCursor))
            title_button.setEnabled(False)

            title_layout.addWidget(checkbox)
            title_layout.addWidget(title_button, 1)  # Set stretch factor to 1 for the title button

            self.title_checkboxes.append(checkbox)
            self.title_buttons.append(title_button)
            self.title_layouts.append(title_layout)

            # Title Layout End
            self.left_layout.addLayout(title_layout)

        # Back and Next buttons with images
        navigation_layout = QHBoxLayout()

        # Back Button
        #self.back_button = QPushButton()
        #self.back_button.setIcon(QIcon('bin/images/back.png'))
        #self.back_button.setIconSize(QSize(24, 24))
        #self.back_button.clicked.connect(self.previous_image)
        #self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        #self.back_button.setStyleSheet("""
        #    QPushButton {
        #        background-color: transparent; 
        #        border: none;
        #    }
        #    QPushButton:hover {
        #        border: 2px solid white;
        #    }
        #""")
        #navigation_layout.addWidget(self.back_button)

        # Continue Button
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon('bin/images/next.png'))
        self.next_button.setIconSize(QSize(24, 24))
        self.next_button.clicked.connect(self.next_image)
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
        navigation_layout.addWidget(self.next_button)

        self.left_layout.addLayout(navigation_layout)

        # Right side layout for image display
        self.right_layout = QVBoxLayout()
        self.image_label = QLabel("Image will appear here")
        self.image_label.setAlignment(Qt.AlignCenter)  # Ensure image is centered
        self.right_layout.addWidget(self.image_label)

        # Add layouts to main layout
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

    def apply_custom_style(self):
        # Apply custom style for disabled buttons
        disabled_style = "QPushButton:disabled { color: #ffffff; background-color: #626262; }"
        self.setStyleSheet(disabled_style)



########## UI Update Methods ########## (These methods directly modify the UI elements)



    def display_current_image(self):
        if self.current_index < len(self.image_files):
            image_path = self.image_files[self.current_index]
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), 
                                                     self.image_label.height(), 
                                                     Qt.KeepAspectRatio))

            # Disable regenerate, save, and copy buttons for new image
            self.regenerate_button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.copy_button.setEnabled(False)

            # Also disable the title buttons for new image
            for btn in self.title_buttons:
                btn.setEnabled(False)
        else:
            self.image_label.setText("No more images.")

        # Disable checkboxes during analysis
        for checkbox in self.title_checkboxes:
            checkbox.setEnabled(False)

    def clear_analysis_context_titles(self):
        # Clear analysis and context
        self.analysis_display.clear()
        self.user_context_input.setText(self.user_context_input.placeholder_text)

        # Reset and disable title buttons
        for i, btn in enumerate(self.title_buttons):
            btn.setText(f"Title {i+1}")
            btn.setEnabled(False)

        # Disable buttons that should not be active without an analysis
        self.regenerate_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.copy_button.setEnabled(False)



########## Event Handlers ########## (Methods connected to UI signals like button clicks)



    def analyze_image(self):
        # Disable UI elements
        self.disable_ui()

        current_image_path = self.image_files[self.current_index]
        user_context = self.user_context_input.toPlainText()

        self.analysisThread = ImageAnalysisThread(current_image_path, user_context)
        self.analysisThread.resultSignal.connect(self.handle_analysis_result)
        self.analysisThread.start()

    def handle_analysis_result(self, result):
        self.enable_ui()

        # Split the result into analysis and titles
        analysis, titles = self.split_analysis_and_titles(result)

        # Update the analysis display with just the analysis part
        self.analysis_display.setText(analysis)

        # Update and enable title buttons with the titles
        for i, btn in enumerate(self.title_buttons):
            if i < len(titles):
                btn.setText(titles[i])
                btn.setVisible(True)
                btn.setEnabled(True)  # Enable the button
            else:
                btn.setVisible(False)
                btn.setEnabled(False)  # Disable the button if no title is available

        # Enable regenerate, save, and copy buttons if titles are available
        if titles:
            self.regenerate_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.copy_button.setEnabled(True)

        # Enable checkboxes if titles are available
        for checkbox in self.title_checkboxes:
            checkbox.setEnabled(len(titles) > 0)

    def regenerate_titles(self):

        self.disable_ui()

        # Disable checkboxes
        for checkbox in self.title_checkboxes:
            checkbox.setEnabled(False)

        analysis_text = self.analysis_display.toPlainText()
        user_context = self.user_context_input.toPlainText()
        self.titleRegenerationThread = TitleRegenerationThread(analysis_text, user_context)
        self.titleRegenerationThread.resultSignal.connect(self.handle_title_regeneration_result)
        self.titleRegenerationThread.start()

    def handle_title_regeneration_result(self, result):

        self.enable_ui()

        if "Error" in result:
            # Handle the error case
            QMessageBox.warning(self, "Error", result)
        else:
            titles = result.split('\n')  # Assuming titles are line-separated
            for i, btn in enumerate(self.title_buttons):
                if i < len(titles):
                    btn.setText(titles[i].strip())
                    btn.setVisible(True)
                else:
                    btn.setVisible(False)

        # Enable checkboxes if titles are available
        for checkbox in self.title_checkboxes:
            checkbox.setEnabled(len(titles) > 0)

        # Enable checkboxes if titles are available
        for checkbox in self.title_checkboxes:
            checkbox.setEnabled(len(titles) > 0)

    def select_title(self):
        sender = self.sender()
        selected_title = sender.text()
        current_image_path = self.image_files[self.current_index]
        new_file_path = self.create_new_file_path(current_image_path, selected_title)

        if self.confirm_rename(current_image_path, new_file_path):
            self.rename_file(current_image_path, new_file_path)
            self.next_image()  # Move to next image after renaming

    def checkbox_changed(self, state):
        # Only one checkbox can be checked at a time
        for checkbox in self.title_checkboxes:
            if checkbox is not self.sender():
                checkbox.setChecked(False)

    def copy_analysis_to_clipboard(self):
        analysis_text = self.analysis_display.toPlainText()
        QGuiApplication.clipboard().setText(analysis_text)
        #QMessageBox.information(self, "Copied", "Analysis copied to clipboard.")

    def save_analysis_to_file(self):
        analysis_text = self.analysis_display.toPlainText()
        options = QFileDialog.Options()

        # Default filename based on the selected title
        default_filename = self.get_sanitized_default_filename()

        # Get the directory of the current image
        current_image_path = self.image_files[self.current_index]
        current_directory = os.path.dirname(current_image_path)

        # Append the default filename to the current directory
        default_filepath = os.path.join(current_directory, default_filename)

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Analysis", default_filepath, "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(analysis_text)
                # Optional: Inform the user that the file has been saved
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error saving file: {e}', QMessageBox.Ok)


    def get_sanitized_default_filename(self):
        default_filename = ""
        for checkbox, title_button in zip(self.title_checkboxes, self.title_buttons):
            if checkbox.isChecked():
                sanitized_title = self.sanitize_title(title_button.text())
                default_filename = sanitized_title + ".txt"
                break
        return default_filename
    
    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current_image()
        else:
            # Optional: Add a message or disable the Back button when on the first image
            pass

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.clear_analysis_context_titles()  # Reset the analysis, context, and titles
            self.reset_checkboxes()  # Reset the checkboxes
            self.display_current_image()
        else:
            # Create a custom QMessageBox
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Queue Finished')
            msgBox.setText("You've reached the end of the queue.")
            msgBox.setInformativeText("Do you want to close or restart?")

            # Add custom buttons
            close_button = msgBox.addButton("Close", QMessageBox.RejectRole)
            restart_button = msgBox.addButton("Restart", QMessageBox.AcceptRole)

            # Display the message box and wait for user input
            msgBox.exec_()

            # Check which button was clicked
            if msgBox.clickedButton() == restart_button:
                self.restart_signal.emit()  # Emit the signal to restart
                self.close()
            else:
                self.close()



########## Utility Methods ########## (Independent of the main flow, often reusable)



    def split_analysis_and_titles(self, result):
        # Assuming the analysis and titles are separated by a specific pattern
        # Adjust the split logic based on the actual format of the API response
        parts = result.split('\n\n', 1)  # Splitting at the first occurrence of double newline
        if len(parts) == 2:
            analysis = parts[0].strip()
            titles = [title.strip() for title in parts[1].split('\n') if title.strip()]
        else:
            analysis = result
            titles = []

        return analysis, titles

    def extract_titles(self, result):
        # Assuming the titles are at the end of the result, separated by new lines
        # You might need to adjust this based on the actual format of the response
        titles = result.split('\n')[-5:]
        return [title.strip() for title in titles if title.strip()]


    def confirm_rename(self, old_path, new_path):
        # Check if file with new name exists or if overwrite is enabled
        overwrite = True  # Placeholder for the overwrite setting

        if not overwrite and os.path.exists(new_path):
            msg = f"A file named '{os.path.basename(new_path)}' already exists. Do you want to replace it?"
            return self.show_confirmation_dialog(msg)

        return True  # If overwrite is enabled or no conflict exists

    def show_confirmation_dialog(self, message):
        reply = QMessageBox.question(self, 'Confirm Rename', message, 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def rename_file(self, old_path, new_path):
        try:
            os.rename(old_path, new_path)
            print(f"File renamed to {new_path}")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error renaming file: {e}', QMessageBox.Ok)

    def create_new_file_path(self, old_path, title):
        # Sanitize the title to remove illegal characters and replace ':' with '-'
        sanitized_title = self.sanitize_title(title)

        # Create a new file path based on the sanitized title
        directory = os.path.dirname(old_path)
        extension = os.path.splitext(old_path)[1]
        new_filename = sanitized_title + extension
        return os.path.join(directory, new_filename)

    def sanitize_title(self, title):
        # Remove leading number or bullet, along with a period and a space if present
        title = re.sub(r'^(\d+\.?|\•|\-|\*)\s?', '', title)

        # Replace ':' with '-'
        title = title.replace(':', '-')
        
        # Remove illegal characters (e.g., *, /, ?, etc.)
        return re.sub(r'[<>:"/\\|?*]', '', title)

    def reset_checkboxes(self):
        for checkbox in self.title_checkboxes:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

    def disable_ui(self):
        # List of widgets to disable
        widgets_to_disable = [self.analyze_button, self.user_context_input, 
                              self.regenerate_button, self.save_button, 
                              self.copy_button, self.next_button] + self.title_buttons
        for widget in widgets_to_disable:
            widget.setEnabled(False)

    def enable_ui(self):
        # List of widgets to enable
        widgets_to_enable = [self.analyze_button, self.user_context_input, 
                             self.regenerate_button, self.save_button, 
                             self.copy_button, self.next_button] + self.title_buttons
        for widget in widgets_to_enable:
            widget.setEnabled(True)

class SpellCheckTextEdit(QTextEdit):
    def __init__(self, placeholder_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder_text = placeholder_text
        self.setPlaceholderText(self.placeholder_text)
        self.spell_checker = enchant.Dict("en_US")
        self.spell_check_timer = QTimer()
        self.spell_check_timer.setSingleShot(True)
        self.spell_check_timer.timeout.connect(self.check_spelling)
        self.textChanged.connect(self.schedule_spell_check)
        self.setWordWrapMode(QTextOption.NoWrap)

    def schedule_spell_check(self):
        # Schedule the spell check to occur after a short delay
        self.spell_check_timer.start(500)  # 500 ms delay

    def check_spelling(self):
        self.blockSignals(True)  # Block signals while updating the text format

        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)  # Select the entire document
        cursor.setCharFormat(QTextCharFormat())  # Reset the format

        cursor.setPosition(0)
        while cursor.position() < len(self.toPlainText()):
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
            word = cursor.selectedText()
            if word and not self.spell_checker.check(word):
                cursor.mergeCharFormat(self.highlight_format())
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.NextWord)

        self.blockSignals(False)  # Unblock signals

    def highlight_format(self):
        fmt = QTextCharFormat()
        fmt.setUnderlineColor(Qt.red)
        fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        return fmt

    def contextMenuEvent(self, event):
        menu = super().createStandardContextMenu()
        cursor = self.cursorForPosition(event.pos())
        cursor.select(QTextCursor.WordUnderCursor)
        word_under_cursor = cursor.selectedText()

        if word_under_cursor and not self.spell_checker.check(word_under_cursor):
            # Add a separator in the context menu
            menu.addSeparator()

            # Get suggestions for the misspelled word
            suggestions = self.spell_checker.suggest(word_under_cursor)

            # No suggestions found
            if not suggestions:
                action = menu.addAction("(no suggestions)")
                action.setEnabled(False)

            # Add suggestions to the menu
            for suggestion in suggestions:
                action = menu.addAction(suggestion)
                action.triggered.connect(lambda _, s=suggestion, c=cursor: self.replace_word(c, s))

        # Show the context menu at the current position
        menu.exec_(event.globalPos())

    def replace_word(self, cursor, suggestion):
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(suggestion)
        cursor.endEditBlock()

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        h = fm.height()
        return QSize(super().sizeHint().width(), h)
        
#class CustomLineEdit(QLineEdit):
#    def __init__(self, placeholder_text, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.placeholder_text = placeholder_text
#        self.setText(self.placeholder_text)
#
#    def focusInEvent(self, event):
#        if self.text() == self.placeholder_text:
#            self.setText('')
#        super().focusInEvent(event)
#
#    def focusOutEvent(self, event):
#        if self.text().strip() == '':
#            self.setText(self.placeholder_text)
#        super().focusOutEvent(event)