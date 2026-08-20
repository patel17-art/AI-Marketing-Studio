import sys

from utils.paths import BASE_DIR

# When running as the packaged .exe, send all print() output and
# any crash tracebacks to a log file instead of a console window,
# since the console will be hidden. When running normally as a
# script (e.g. from VS Code), this is skipped entirely and output
# still goes to the visible terminal as usual.
if getattr(sys, "frozen", False):

    log_path = BASE_DIR / "app_log.txt"

    log_file = open(log_path, "w", encoding="utf-8")

    sys.stdout = log_file
    sys.stderr = log_file


from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()