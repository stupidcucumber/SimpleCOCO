from PyQt6.QtWidgets import (
    QLayout,
    QWidget
)


def setup_box(parent: QWidget, layout: QLayout, widgets: QWidget) -> QWidget:
    widget = QWidget(parent)
    [layout.addWidget(_widget) for _widget in widgets]
    widget.setLayout(layout)
    return widget