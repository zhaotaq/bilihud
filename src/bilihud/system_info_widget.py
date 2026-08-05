# -*- coding: utf-8 -*-
from __future__ import annotations

import collections
from typing import Any

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class SystemInfoWidget(QFrame):
    """区域 4：最底部进房与关注次要低干扰消息栏 (Bottom Low-Interference System Info Zone)"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("system_info_bar")
        self.history = collections.deque(maxlen=10)
        self.font_scale: float = 1.0

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QFrame#system_info_bar {
                background: rgba(0, 0, 0, 80);
                border-top: 1px solid rgba(255, 255, 255, 20);
                border-radius: 4px;
            }
            QLabel#info_lbl {
                color: rgba(205, 214, 244, 150);
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(6)

        self.icon_lbl = QLabel("🚪")
        self.icon_lbl.setStyleSheet("font-size: 11px;")

        self.info_lbl = QLabel("欢迎来到直播间~")
        self.info_lbl.setObjectName("info_lbl")

        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.info_lbl)
        layout.addStretch()

        self.update_font_size()

    def update_font_size(self):
        base_size = int(12 * self.font_scale)
        self.info_lbl.setStyleSheet(f"font-size: {base_size}px; color: rgba(205, 214, 244, 160);")

    def set_font_scale(self, scale: float):
        self.font_scale = scale
        self.update_font_size()

    def add_info(self, uname: str, action: str):
        """展示极简进房/关注流提示"""
        text = f"{uname} {action}"
        self.info_lbl.setText(text)
        self.show()
