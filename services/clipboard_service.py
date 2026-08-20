from PySide6.QtGui import QGuiApplication


class ClipboardService:

    @staticmethod
    def copy(text: str):

        clipboard = QGuiApplication.clipboard()

        clipboard.setText(text)