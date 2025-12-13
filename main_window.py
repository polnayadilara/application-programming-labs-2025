from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import sys

CURRENT_FOLDER = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_FOLDER.parent.parent  
ITERATOR_MODULE_PATH = PROJECT_ROOT / "lab_2" / "image_crawler"

if str(ITERATOR_MODULE_PATH) not in sys.path:
    sys.path.insert(0, str(ITERATOR_MODULE_PATH))

from paths_iterator import ImageList as ImagePathIterator

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from image_viewer import PictureCanvas


class GUIApplication(QMainWindow):
    """Простой просмотрщик изображений"""

    def __init__(self) -> None:
        super().__init__()
        self.image_navigator: Optional[ImagePathIterator] = None
        self.active_filepath: Optional[str] = None
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
        self.btn_choose_directory.clicked.connect(self.choose_directory)
        source_selection_panel.addWidget(self.btn_choose_directory)

        self.btn_choose_csv = QPushButton("📄 Открыть CSV")
        self.btn_choose_csv.clicked.connect(self.choose_csv_file)
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

    def choose_directory(self) -> None:
        """Выбор директории с графическими файлами"""
        selected_dir = QFileDialog.getExistingDirectory(
            self, "Выберите папку с изображениями"
        )
        if selected_dir:
            self.load_data_source(selected_dir)

    def choose_csv_file(self) -> None:
        """Выбор CSV-файла с метаданными"""
        csv_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл", "", "CSV файлы (*.csv)"
        )
        if csv_path:
            self.load_data_source(csv_path)

    def load_data_source(self, data_source: str) -> None:
        """Инициализация источника данных"""
        try:
            self.image_navigator = ImagePathIterator(data_source)
            file_count = len(self.image_navigator)

            source_desc = "папки" if Path(data_source).is_dir() else "CSV-файла"
            status_text = f"Загружено {file_count} файлов из {source_desc}"
            self.info_panel.setText(status_text)

            self.btn_go_forward.setEnabled(True)
            self.btn_go_back.setEnabled(False)
            self.image_display.clear_canvas()
            self.file_info_label.setText("Файл не выбран")
            self.active_filepath = None

        except Exception as err:
            QMessageBox.critical(
                self, 
                "Ошибка загрузки", 
                f"Не удалось загрузить данные:\n{str(err)}"
            )