# Файл: image_viewer.py
from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QResizeEvent
from PyQt6.QtCore import Qt


class PictureCanvas(QLabel):
    """Виджет для отрисовки картинок с сохранением соотношения сторон"""

    def __init__(self) -> None:
        super().__init__()
        self.source_image: Optional[QPixmap] = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            "QLabel { background-color: #e8e8e8; border: 2px dashed #aaa; border-radius: 5px; }"
        )
        self.setMinimumSize(450, 450)
        self.setText("Картинка не выбрана")
        self.setScaledContents(False)

    def set_picture(self, filepath: str) -> None:
        """Установка и отображение графического файла"""
        
        self.source_image = QPixmap(filepath)
        if self.source_image.isNull():
            raise RuntimeError(f"Ошибка загрузки файла: {filepath}")
        self.refresh_canvas()

    def refresh_canvas(self) -> None:
        """Перерисовка изображения с учётом текущего размера"""

        if self.source_image and not self.source_image.isNull():
            resized_image = self.source_image.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(resized_image)

    def resizeEvent(self, resize_evt: QResizeEvent) -> None:
        """Обработчик изменения размеров окна"""

        super().resizeEvent(resize_evt)
        self.refresh_canvas()

    def clear_canvas(self) -> None:
        """Очистка виджета от изображения"""

        self.source_image = None
        self.setPixmap(QPixmap())
        self.setText("Картинка не выбрана")