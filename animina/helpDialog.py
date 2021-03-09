from Qt.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
)

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent=parent)

        self.setWindowTitle("Animina Help")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        blank = QLabel("    ")

        message = QLabel("Welcome to Animina, a tool for any Maya user to quickly store"
                         " and recover complex selections ")

        messageS = QLabel("How to get started:")

        message2 = QLabel("Create: Select objects from the viewport"
                          " or outliner and use the text field to name your selection. Press Create ")

        message3 = QLabel("Save: Enter a folder name in the text field and press Save to "
                          "save all current selection groups in Animina to your ../scenes/animina/<folder name> .")

        message4 = QLabel("          With no name specified saves all objects in Animina to  ../scenes/animina/default")

        message5 = QLabel("Load: Works like save but recovers from either the user saved folder or the default Animina folder.")
        message6 = QLabel("          Enter a save folder name and press Load, or enter no name to restore from default.")

        self.layout.addWidget(message)
        self.layout.addWidget(blank)
        self.layout.addWidget(messageS)
        self.layout.addWidget(blank)
        self.layout.addWidget(message2)
        self.layout.addWidget(blank)
        self.layout.addWidget(message3)
        self.layout.addWidget(message4)
        self.layout.addWidget(blank)
        self.layout.addWidget(message5)
        self.layout.addWidget(message6)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
