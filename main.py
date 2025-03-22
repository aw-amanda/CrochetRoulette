import sys
import random
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class CrochetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Crochet Roulette')
        self.setGeometry(200, 400, 500, 500)
        self.setWindowIcon(QIcon('CrochetRouletteIcon.ico'))
        self.setStyleSheet('background-color: #262625')

        main_layout = QVBoxLayout()

        # Project Type, Selector, and Submit Button
        group1_layout = QVBoxLayout()
        self.project_label = QLabel("PROJECT TYPE:")
        self.project_label.setFont(QFont('Arial', 16))
        self.project_label.setStyleSheet("color: #9369e0")
        self.project_label.setAlignment(Qt.AlignCenter)
        self.project_selector = QComboBox()
        self.project_selector.setFont(QFont('Arial', 14))
        self.project_selector.setStyleSheet("background-color:#cab6f0; color: #0e0124; padding: 10px; border-radius: 5px;")
        self.project_selector.addItems(sorted([
            "Dishcloth", "Washcloth", "Coaster", "Potholder", "Blanket", "Throw", "Tapestry",
            "Mug Cozy", "Bookmark", "Cat Toy", "Accessories", "Top", "Pants", "Skirt", "Hat",
            "Scarf", "Shawl", "Wrap", "Socks", "Appliqués", "Purse", "Bag", "Market Bag",
            "Home Decor", "Wall Hanging", "Table Runner", "Amigurumi", "Granny Square",
            "Tablecloth", "Flower", "Heart", "Succulent", "Toys", "Gift", "Ornament",
            "Holiday Decor", "Tissue Box Cover", "Car seat cover", "Beginner", "Gloves",
            "Basket", "Bavarian Crochet", "Tunisian Crochet", "Bosnian Crochet", "Lace Crochet",
            "Clones Lace Crochet", "Aran Crochet", "Bullion Crochet", "Broomstick Crochet",
            "Bruges Crochet", "Clothesline Crochet", "Cro-hook Crochet", "Filet Crochet",
            "Finger Crochet", "Freeform Crochet", "Hairpin Crochet", "Micro Crochet",
            "Overlay Crochet", "Stained Glass Crochet", "Chart Crochet", "Symbol Crochet"
        ]))
        self.submit_button = QPushButton("submit")
        self.submit_button.setFont(QFont('Arial', 14))
        self.submit_button.setStyleSheet("background-color: #9369e0; color: #0e0124; padding: 10px; border-radius: 5px;")
        self.submit_button.clicked.connect(self.on_submit)
        
        group1_layout.addWidget(self.project_label)
        group1_layout.addWidget(self.project_selector)
        group1_layout.addWidget(self.submit_button)
        main_layout.addLayout(group1_layout)

        # Vertical spacer between Group 1 and Group 2
        spacer1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(spacer1)
        
        # OR Label and Random Button
        group2_layout = QVBoxLayout()
        self.or_label = QLabel("- OR -")
        self.or_label.setAlignment(Qt.AlignCenter)
        self.or_label.setFont(QFont('Arial', 16))
        self.or_label.setStyleSheet("color: #82dae0")
        self.random_button = QPushButton("random")
        self.random_button.setFont(QFont('Arial', 14))
        self.random_button.setStyleSheet("background-color: #04bfcc; color: #011d1f; padding: 10px; border-radius: 5px;")
        self.random_button.clicked.connect(self.on_random)

        group2_layout.addWidget(self.or_label)
        group2_layout.addWidget(self.random_button)
        main_layout.addLayout(group2_layout)

        # Vertical spacer between Group 2 and Group 3
        spacer2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(spacer2)
       
        # Result Label and Result Link
        group3_layout = QVBoxLayout()
        self.result_label = QLabel("RESULT:")
        self.result_label.setFont(QFont('Arial', 16))
        self.result_label.setStyleSheet("color: #a9f5c9")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_link = QLabel("")
        self.result_link.setFont(QFont('Arial', 12))
        self.result_link.setAlignment(Qt.AlignCenter)
        self.result_link.setOpenExternalLinks(True)
        self.result_link.setTextFormat(Qt.RichText) 
        self.result_link.setStyleSheet("color: #cab6f0;")

        group3_layout.addWidget(self.result_label)
        group3_layout.addWidget(self.result_link)
        main_layout.addLayout(group3_layout)

        # Vertical spacer between Group 3 and Group 4
        spacer3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(spacer3)

        # Try Again Button
        group4_layout = QVBoxLayout()
        self.try_again_button = QPushButton("try again")
        self.try_again_button.setFont(QFont('Arial', 14))
        self.try_again_button.setStyleSheet("background-color: #90e8b5; color: #011c12; padding: 10px; border-radius: 5px;")
        self.try_again_button.clicked.connect(self.on_try_again)

        group4_layout.addWidget(self.try_again_button)
        main_layout.addLayout(group4_layout)

        self.setLayout(main_layout)

    def on_submit(self):
        project = self.project_selector.currentText()
        self.fetch_pattern(project)

    def on_random(self):
        project = random.choice([self.project_selector.itemText(i) for i in range(self.project_selector.count())])
        self.project_selector.setCurrentText(project)  # Update the selector to show the random choice
        self.fetch_pattern(project)

    def fetch_pattern(self, project):
        try:
            response = requests.get(f"http://127.0.0.1:5000/search?project={project}")
            response.raise_for_status()  # Raise an error for bad status codes
            if response.status_code == 200:
                result = response.json().get("url", "No result found.")
                self.result_link.setText(f'<a href="{result}" style="color: #cab6f0; text-decoration: none;">{result}</a>')
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to connect to the server: {e}")

    def on_try_again(self):
        self.project_selector.setCurrentIndex(0)
        self.result_link.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrochetApp()
    window.show()
    sys.exit(app.exec_())