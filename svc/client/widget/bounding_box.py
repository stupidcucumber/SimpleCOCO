from __future__ import annotations
from typing import Callable
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ...backend.src.structs import (
    Annotation
)
from ..request.annotation import (
    update_annotation,
    delete_annotation
)
from ..utils import Connection


class AnnotationBox(QGraphicsRectItem):
    def __init__(self, annotation: Annotation, color: QColor, 
                 geometry: QRect, slot: Callable[[AnnotationBox], None], 
                 parent: QObject | None = None) -> None:
        super(AnnotationBox, self).__init__(parent)
        self.annotation = annotation
        self.color = color
        self.slot = slot
        self.__resizeEnabled = False
        self.__resize_square_f = False
        self.__line_width = 3
        self.__default_width = 200.0
        self.__default_height = 200.0
        self.__min_width = 30
        self.__min_height = 30
        self.__cursor = QCursor()
        self.__initPosition()
        self.__initUi()
        self.setGeometry(geometry)
        
    def geometry(self) -> QRectF:
        x = int(self.x())
        y = int(self.y())
        width = int(self.rect().width())
        height = int(self.rect().height())
        return QRect(x, y, width, height)
        
    def setGeometry(self, rect: QRect) -> None:
        self.setX(rect.x())
        self.setY(rect.y())
        self.setWidth(rect.width())
        self.setHeight(rect.height())

    def __initUi(self):
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.__setStyleOfBoundingBox()

    def __initPosition(self):
        self.__top = False
        self.__bottom = False
        self.__left = False
        self.__right = False
        
    def __isAbleToSetTop(self, rect, y):
        return rect.bottom() - y > self.__min_height
    def __isAbleToSetBottom(self, y):
        return y > self.__min_height
    def __isAbleToSetLeft(self, rect, x):
        return rect.right() - x > self.__min_width
    def __isAbleToSetRight(self, x):
        return x > self.__min_width

    def __setStyleOfBoundingBox(self):
        pen = QPen(self.color)
        pen.setWidth(self.__line_width)
        self.setRect(QRectF(0.0, 0.0, self.__default_width, self.__default_height))
        self.setPen(pen)

    def __setCursorShapeForCurrentPoint(self, p):
        # allow mouse cursor to change shape for scale more easily
        rect = self.rect()
        rect.setX(self.rect().x() + self.__line_width)
        rect.setY(self.rect().y() + self.__line_width)
        rect.setWidth(self.rect().width() - self.__line_width * 2)
        rect.setHeight(self.rect().height() - self.__line_width * 2)

        if rect.contains(p):
            # move
            self.setFlags(self.flags() | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.__cursor.setShape(Qt.CursorShape.SizeAllCursor)
            self.setCursor(self.__cursor)
            self.__cursor = self.cursor()
            self.__resizeEnabled = False
            self.__initPosition()
        else:
            # scale
            x = p.x()
            y = p.y()

            def setResizeEnabled():
                self.setFlags(self.flags() & ~QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
                self.setCursor(self.__cursor)
                self.__resizeEnabled = True

            x1 = self.rect().x()
            y1 = self.rect().y()
            x2 = self.rect().width()
            y2 = self.rect().height()

            self.__left = abs(x - x1) <= self.__line_width  # if mouse cursor is at the almost far left
            self.__top = abs(y - y1) <= self.__line_width  # far top
            self.__right = abs(x - (x2 + x1)) <= self.__line_width  # far right
            self.__bottom = abs(y - (y2 + y1)) <= self.__line_width  # far bottom

            # set the cursor shape based on flag above
            if self.__top or self.__left or self.__bottom or self.__right:
                if self.__top and self.__left:
                    self.__cursor.setShape(Qt.CursorShape.SizeFDiagCursor)
                elif self.__top and self.__right:
                    self.__cursor.setShape(Qt.CursorShape.SizeBDiagCursor)
                elif self.__bottom and self.__left:
                    self.__cursor.setShape(Qt.CursorShape.SizeBDiagCursor)
                elif self.__bottom and self.__right:
                    self.__cursor.setShape(Qt.CursorShape.SizeFDiagCursor)
                elif self.__left:
                    self.__cursor.setShape(Qt.CursorShape.SizeHorCursor)
                elif self.__top:
                    self.__cursor.setShape(Qt.CursorShape.SizeVerCursor)
                elif self.__right:
                    self.__cursor.setShape(Qt.CursorShape.SizeHorCursor)
                elif self.__bottom:
                    self.__cursor.setShape(Qt.CursorShape.SizeVerCursor)
                setResizeEnabled()

    def mouseMoveEvent(self, e):
        if self.__resizeEnabled:
            rect = self.rect()
            p = e.pos()
            x = p.x()
            y = p.y()

            if self.__resize_square_f:
                # TODO i'm still working on this, refactoring is necessary
                # get the average of width and height
                size = p.manhattanLength() // 2
                p = QPoint(int(size), int(size))
                if x < 0 or y < 0:
                    p = QPoint(int(size)*-1, int(size)*-1)
                if self.__cursor.shape() == Qt.CursorShape.SizeFDiagCursor:
                    if self.__top and self.__left and self.__isAbleToSetTop(rect, y) and self.__isAbleToSetLeft(rect, x):
                        rect.setTopLeft(p)
                    elif self.__bottom and self.__right and self.__isAbleToSetBottom(y) and self.__isAbleToSetRight(x):
                        rect.setBottomRight(p)
            else:
                if self.__cursor.shape() == Qt.CursorShape.SizeHorCursor:
                    if self.__left and self.__isAbleToSetLeft(rect, x):
                        rect.setLeft(x)
                    elif self.__right and self.__isAbleToSetRight(x):
                        rect.setRight(x)
                elif self.__cursor.shape() == Qt.CursorShape.SizeVerCursor:
                    if self.__top and self.__isAbleToSetTop(rect, y):
                        rect.setTop(y)
                    elif self.__bottom and self.__isAbleToSetBottom(y):
                        rect.setBottom(y)
                elif self.__cursor.shape() == Qt.CursorShape.SizeBDiagCursor:
                    if self.__top and self.__right and self.__isAbleToSetTop(rect, y) and self.__isAbleToSetRight(x):
                        rect.setTopRight(p)
                    elif self.__bottom and self.__left and self.__isAbleToSetBottom(y) and self.__isAbleToSetLeft(rect, x):
                        rect.setBottomLeft(p)
                elif self.__cursor.shape() == Qt.CursorShape.SizeFDiagCursor:
                    if self.__top and self.__left and self.__isAbleToSetTop(rect, y) and self.__isAbleToSetLeft(rect, x):
                        rect.setTopLeft(p)
                    elif self.__bottom and self.__right and self.__isAbleToSetBottom(y) and self.__isAbleToSetRight(x):
                        rect.setBottomRight(p)

            self.setRect(rect)

        return super().mouseMoveEvent(e)

    def hoverMoveEvent(self, e):
        p = e.pos()

        if self.boundingRect().contains(p) or self.rect().contains(p):
            self.__setCursorShapeForCurrentPoint(p)

        return super().hoverMoveEvent(e)

    # moving with arrow keys
    def keyPressEvent(self, e) -> None:
        tr = self.transform()
        if e.key() == 16777219:
            self.slot(self)
            return
        else:
            if e.key() == Qt.Key.Key_Up:
                tr.translate(0, -1)
            if e.key() == Qt.Key.Key_Down:
                tr.translate(0, 1)
            if e.key() == Qt.Key.Key_Left:
                tr.translate(-1, 0)
            if e.key() == Qt.Key.Key_Right:
                tr.translate(1, 0)
        self.setTransform(tr)
        return super().keyPressEvent(e)

    def setLineWidth(self, n: int):
        self.__line_width = n
        self.__setStyleOfBoundingBox()

    def setColor(self, color: QColor):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)

    # https: // doc.qt.io / qt - 6 / qt.html  # PenStyle-enum
    def setStyle(self, style: Qt.PenStyle):
        pen = self.pen()
        pen.setStyle(style)
        self.setPen(pen)

    def setWidth(self, width: int):
        rect = self.rect()
        rect.setWidth(width)
        self.setRect(rect)

    def setHeight(self, height: int):
        rect = self.rect()
        rect.setHeight(height)
        self.setRect(rect)

    def setSize(self, width: int, height: int):
        rect = self.rect()
        rect.setSize(QSizeF(width, height))
        self.setRect(rect)

    def setResizeAsSquare(self, f: bool):
        self.__resize_square_f = f

    def setMinimumSize(self, width, height):
        self.__min_width = width
        self.__min_height = height
        # TODO set width or height of the current rect larger than minimum size after at least one of them is set by