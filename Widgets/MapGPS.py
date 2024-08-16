import folium
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import QWebEngineView

class MapGPS(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        map = folium.Map(location=[39.81890428624599, 32.56358312070704], zoom_start=18)
        folium.Marker([39.81890428624599, 32.56358312070704], popup=f"MTT - BeeRocketry").add_to(map)
        map.save(f"./Assets/map_{name}.html")

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.web = QWebEngineView()
        self.web.setHtml(open(f"./Assets/map_{name}.html").read())

        self.layout.addWidget(self.web)


    def update(self, location):
        map = folium.Map(location=location, zoom_start=12)
        folium.Marker(location, popup=self.name).add_to(map)
        map.save(f"./Assets/map_{self.name}.html")
        self.web.setHtml(open(f"./Assets/map_{self.name}.html").read())