from __future__ import annotations

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel
)
from PyQt6.QtCore import Qt

from image_viewer import PictureCanvas


class GUIApplication(QMainWindow):
    """Простой просмотрщик изображений"""

    def __init__(self) -> None:
        super().__init__()
        self.setup_interface()

    def setup_interface(self) -> None:
        """Создание и настройка элементов интерфейса"""
        self.setWindowTitle("Просмотр изображений")
        self.setGeometry(150, 150, 900, 650)

        central_panel = QWidget()
        self.setCentralWidget(central_panel)

        main_panel_layout = QVBoxLayout(central_panel)
        main_panel_layout.setSpacing(10)
        main_panel_layout.setContentsMargins(10, 10, 10, 10)

        source_selection_panel = QHBoxLayout()
        source_selection_panel.setSpacing(10)

        self.btn_choose_directory = QPushButton("📁 Открыть папку")
        source_selection_panel.addWidget(self.btn_choose_directory)

        self.btn_choose_csv = QPushButton("📄 Открыть CSV")
        source_selection_panel.addWidget(self.btn_choose_csv)
        
        source_selection_panel.addStretch()

        main_panel_layout.addLayout(source_selection_panel)

        self.info_panel = QLabel("Выберите папку с картинками или CSV-файл")
        self.info_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_panel_layout.addWidget(self.info_panel)

        self.image_display = PictureCanvas()
        main_panel_layout.addWidget(self.image_display, stretch=1)

        navigation_panel = QHBoxLayout()
        navigation_panel.setSpacing(10)

        self.btn_go_back = QPushButton("◀ Назад")
        self.btn_go_back.setEnabled(False)
        navigation_panel.addWidget(self.btn_go_back)

        navigation_panel.addStretch()

        self.file_info_label = QLabel("Нет выбранного файла")
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        navigation_panel.addWidget(self.file_info_label)

        navigation_panel.addStretch()

        self.btn_go_forward = QPushButton("Вперёд ▶")
        self.btn_go_forward.setEnabled(False)
        navigation_panel.addWidget(self.btn_go_forward)

        main_panel_layout.addLayout(navigation_panel)