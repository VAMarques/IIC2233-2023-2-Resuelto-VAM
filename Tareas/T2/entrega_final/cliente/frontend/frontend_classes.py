from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint

class DraggableLabel(QLabel):
    """
    Una Clase de label arrastrable que activa una señal drop cuando es botada, una vez es botada
    vuelve a su posicion original
    """
    drop = pyqtSignal(str, int, int)

    def __init__(self, nombre, x, y, width, height, parent=None):
        super().__init__(parent)
        # No se si es necesario
#        self.setAcceptDrops(False)
        self.press = False
        self.move_pos = None
        self.nombre = nombre
        self.setGeometry(x, y, width, height)
        self.old_geometry = self.geometry()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            new_rect = QRect(0, 0, 32, 32)
            new_x = int(self.old_geometry.x() + event.pos().x())
            new_y = int(self.old_geometry.y() + event.pos().y())
            new_rect.moveCenter(QPoint(new_x, new_y))
            self.setGeometry(new_rect)
            self.press = True
            self.move_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        # Esta notacion la habia encontrado en un post de stackoverflow similar.
        # Me refiero al uso de &.
        # Potencialmente mejor explicado en Readme, si no, es que me olvide.
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.press:
                delta_x = event.globalPosition().x() - self.move_pos.x()
                delta_y = event.globalPosition().y() - self.move_pos.y()
                self.move(int(self.x() + delta_x), int(self.y() + delta_y))
                self.move_pos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            centro_x = self.x() + (self.size().width() // 2)
            centro_y = self.y() + (self.size().height() // 2)
            self.drop.emit(self.nombre, centro_x, centro_y)
            self.press = False
            self.setGeometry(self.old_geometry)
