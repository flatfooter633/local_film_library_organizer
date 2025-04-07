import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QCheckBox, \
    QTextEdit, QLabel, QMainWindow
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QSize
from logging import config, getLogger
from utils.logger import user_config
import aiohttp
import asyncio
from os import path
from config import SEARCH_BY_NAME_QUERY
from app.app import rename_files

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Movie Renamer')
        self.setGeometry(100, 100, 1200, 675)
        self.setStyleSheet("background-image: url('background.png'); background-repeat: no-repeat;")


        self.background_image = QtGui.QPixmap('background.png')
        # self.background_label = QLabel(self)
        # self.background_label.setPixmap(self.background_image)
        # self.background_label.setStyleSheet("background-color: transparent;")

        self.title_label = QLabel(self)
        self.title_label.setText('Movie Renamer')
        self.title_label.setFont(QtGui.QFont('Unispace', 32))
        self.title_label.setStyleSheet("background-color: yellow; border: none; color: black;")

        self.folder_entry = QLineEdit(self)
        self.folder_entry.setFont(QtGui.QFont('Unispace', 14))
        self.folder_entry.setPlaceholderText('Enter folder path')
        self.folder_entry.setMaxLength(40)
        self.folder_entry.setStyleSheet("color: black;")

        self.select_folder_button = QPushButton(self)
        self.select_folder_button.setText('Select Folder')
        self.select_folder_button.setFont(QtGui.QFont('Unispace', 14))
        self.select_folder_button.setStyleSheet("background-color: yellow; color: black;")
        self.select_folder_button.clicked.connect(self.select_folder)
        self.select_folder_button.setFixedWidth(200)

        self.create_folder_check = QCheckBox(self)
        self.create_folder_check.setText('Sort by Genres')
        self.create_folder_check.setFont(QtGui.QFont('Unispace', 14))
        self.create_folder_check.setStyleSheet("background-color: yellow; color: black;")

        self.start_button = QPushButton(self)
        self.start_button.setText('Start')
        self.start_button.setFont(QtGui.QFont('Unispace', 24))
        self.start_button.setStyleSheet("background-color: green; color: black;")
        self.start_button.clicked.connect(lambda: asyncio.run(self.start_app()))
        self.start_button.setFixedWidth(200)

        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(QtGui.QFont('Unispace', 10))
        self.log_text_edit.setStyleSheet("background-color: white; color: black;")

        layout = QVBoxLayout()

        layout.addWidget(self.title_label)
        layout.addWidget(self.folder_entry)
        layout.addWidget(self.select_folder_button)
        layout.addWidget(self.create_folder_check)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log_text_edit)
        # layout.addWidget(self.background_label)

        # Set vertical stretch factor to 0 for the layout
        self.setCentralWidget(self.start_button)
        self.setFixedSize(QSize(1200, 675))

        # Center-align the main layout
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', '/')
        self.folder_entry.setText(folder_path)

    async def start_app(self):
        # Ваш код здесь
        logger.info("Событие 'main' обработано")
        # Ввод пути к папке с фильмами
        main_path = path.normpath(self.folder_entry.text())
        create_folder = "1" if self.create_folder_check.isChecked() else "0"
        # Создание aiohttp-сессии
        async with aiohttp.ClientSession() as session:
            await rename_files(session, main_path, SEARCH_BY_NAME_QUERY, create_folder=create_folder)

if __name__ == '__main__':
    # Naстроjka logging
    config.dictConfig(user_config)
    # Получение root логгера
    logger = getLogger()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    asyncio.run(window.start_app())
    sys.exit(app.exec())