import sys
from PyQt6.QtWidgets import QApplication
from main_window import GUIApplication


def run_visualizer() -> None:
    """Запуск визуализатора данных"""
    qt_app = QApplication(sys.argv)
    main_gui = GUIApplication()
    main_gui.show()  
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    run_visualizer()