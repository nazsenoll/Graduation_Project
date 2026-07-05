import subprocess
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QListWidget
)
from PyQt6.QtGui import QIcon
from pathlib import Path

import generate_composite_output
import gui_manuel
import predict
import mapInterface

import webbrowser


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon = QIcon('./ui/logo.png')
        self.setWindowIcon(icon)

        self.setWindowTitle('Crop Type Detector v_1.0')
        self.setGeometry(400, 200, 500, 300)

        layout = QGridLayout()
        self.setLayout(layout)

        # file selection
        file_browser_btn = QPushButton('Import File')
        file_browser_btn.clicked.connect(self.open_file_dialog)

        predict_btn = QPushButton('Run Classification')
        predict_btn.clicked.connect(self.run_program)


        self.file_list = QListWidget(self)

        layout.addWidget(QLabel('Input File:'), 0, 0)
        layout.addWidget(self.file_list, 1, 0)
        layout.addWidget(file_browser_btn, 2, 0)
        layout.addWidget(predict_btn, 3, 0)

        self.show()

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\images')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Prediction Files (*.txt)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.file_list.addItems([str(Path(filename)) for filename in filenames])
                self.path = filenames[0]

    def run_program(self):
        predict.run_predict(self.path)
        composite_image_ls = generate_composite_output.run_gco()
        gui_manuel.update_final_map(composite_image_ls)
        import try4
        mapInterface.run_map_interface()

        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        html_file_path = 'C:/Users/oguzh/PycharmProjects/graduationProject/output.html'
        command = [chrome_path, html_file_path]
        subprocess.Popen(command)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
