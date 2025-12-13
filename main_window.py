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
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #222;
                color: #666;
            }
        """)

        central_panel = QWidget()
        central_panel.setStyleSheet("background-color: #2b2b2b;")
        self.setCentralWidget(central_panel)

        main_panel_layout = QVBoxLayout(central_panel)
        main_panel_layout.setSpacing(10)
        main_panel_layout.setContentsMargins(10, 10, 10, 10)

        source_selection_panel = QHBoxLayout()
        source_selection_panel.setSpacing(10)

        self.btn_choose_directory = QPushButton("📁 Открыть папку")
        self.btn_choose_directory.clicked.connect(self.choose_directory)
        self.btn_choose_directory.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0099ff;
            }
        """)
        source_selection_panel.addWidget(self.btn_choose_directory)

        self.btn_choose_csv = QPushButton("📄 Открыть CSV")
        self.btn_choose_csv.clicked.connect(self.choose_csv_file)
        self.btn_choose_csv.setStyleSheet("""
            QPushButton {
                background-color: #555;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        source_selection_panel.addWidget(self.btn_choose_csv)
        
        source_selection_panel.addStretch()

        main_panel_layout.addLayout(source_selection_panel)

        self.info_panel = QLabel("Выберите папку с картинками или CSV-файл")
        self.info_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_panel.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #aaa;
                padding: 5px;
                background-color: #333;
                border-radius: 3px;
            }
        """)
        main_panel_layout.addWidget(self.info_panel)

        self.image_display = PictureCanvas()
        main_panel_layout.addWidget(self.image_display, stretch=1)

        navigation_panel = QHBoxLayout()
        navigation_panel.setSpacing(10)

        self.btn_go_back = QPushButton("◀ Назад")
        self.btn_go_back.clicked.connect(self.show_prev_image)
        self.btn_go_back.setEnabled(False)
        navigation_panel.addWidget(self.btn_go_back)

        navigation_panel.addStretch()

        self.file_info_label = QLabel("Нет выбранного файла")
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setStyleSheet("""
            QLabel {
                color: #fff;
                font-weight: bold;
                font-size: 13px;
                padding: 8px;
                background-color: #333;
                border-radius: 4px;
                min-width: 300px;
            }
        """)
        navigation_panel.addWidget(self.file_info_label)

        navigation_panel.addStretch()

        self.btn_go_forward = QPushButton("Вперёд ▶")
        self.btn_go_forward.clicked.connect(self.show_next_image)
        self.btn_go_forward.setEnabled(False)
        self.btn_go_forward.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34ce57;
            }
        """)
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

    def show_next_image(self) -> None:
        """Отображение следующего изображения в наборе"""
        if not self.image_navigator:
            return

        try:
            self.active_filepath = next(self.image_navigator)
            self.render_picture(self.active_filepath)
            self.btn_go_back.setEnabled(True)

            if self.image_navigator.index >= len(self.image_navigator):
                self.btn_go_forward.setEnabled(False)

        except StopIteration:
            self.btn_go_forward.setEnabled(False)
            QMessageBox.information(
                self, 
                "Конец", 
                "Все изображения просмотрены"
            )

    def show_prev_image(self) -> None:
        """Отображение предыдущего изображения"""
        if not self.image_navigator or self.image_navigator.index <= 1:
            return

        self.image_navigator.index = max(0, self.image_navigator.index - 2)
        self.show_next_image()

        if self.image_navigator.index == 1:
            self.btn_go_back.setEnabled(False)

        self.btn_go_forward.setEnabled(True)

    def render_picture(self, picture_path: str) -> None:
        """Визуализация выбранного изображения"""
        try:
            self.image_display.set_picture(picture_path)
            filename = Path(picture_path).name
            
            if self.image_navigator:
                current_num = self.image_navigator.index
                total_count = len(self.image_navigator)
                file_info = f"{current_num}/{total_count} - {filename}"
            else:
                file_info = f"Файл: {filename}"
                
            self.file_info_label.setText(file_info)

        except Exception as err:
            QMessageBox.warning(
                self, 
                "Ошибка", 
                f"Не удалось открыть файл:\n{str(err)}"
            )