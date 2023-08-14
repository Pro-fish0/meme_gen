import sys
import requests
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QScrollArea, QGridLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

# GIPHY API key
GIPHY_API_KEY = 'API_KEY'
GIPHY_ENDPOINT = 'https://api.giphy.com/v1/gifs/search'

class ImageSearchApp(QWidget):
    imageFetchedSignal = pyqtSignal(str, QPixmap)

    def __init__(self):
        super().__init__()

        self.initUI()
        self.imageFetchedSignal.connect(self.onImageFetched)
        self.image_count = 0  # Add this line to initialize the counter

    def initUI(self):
        layout = QVBoxLayout()

        self.tag_input = QLineEdit(self)
        self.tag_input.setPlaceholderText("Enter meme template tag")
        layout.addWidget(self.tag_input)

        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.show_meme_templates)
        layout.addWidget(search_button)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.image_grid = QGridLayout()
        self.image_frame = QFrame()
        self.image_frame.setLayout(self.image_grid)
        self.scroll_area.setWidget(self.image_frame)

        self.setLayout(layout)

    def search_giphy(self, tag, limit=10):
        params = {
            'api_key': GIPHY_API_KEY,
            'q': tag,
            'limit': limit
        }
        response = requests.get(GIPHY_ENDPOINT, params=params)
        if response.status_code == 200:
            data = response.json()
            return [img['images']['original']['url'] for img in data['data']]
        else:
            print(f"Error fetching from Giphy: {response.text}")
            return []

    def fetch_image(self, url):
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.imageFetchedSignal.emit(url, pixmap)

    def show_meme_templates(self):
        tag = self.tag_input.text()
        urls = self.search_giphy(tag)

        # Clear previous items
        for i in reversed(range(self.image_grid.count())): 
            widget = self.image_grid.itemAt(i).widget()
            widget.deleteLater()

        # Fetch images in separate threads
        for url in urls:
            threading.Thread(target=self.fetch_image, args=(url,)).start()

    def onImageFetched(self, url, pixmap):
        label = QLabel(self)
        label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        
        row = self.image_count // 3
        col = self.image_count % 3

        self.image_grid.addWidget(label, row, col)
        self.image_count += 1  # Increment the counter

app = QApplication(sys.argv)
window = ImageSearchApp()
window.setWindowTitle('Meme Template Search')
window.resize(650, 300)
window.show()
sys.exit(app.exec_())

