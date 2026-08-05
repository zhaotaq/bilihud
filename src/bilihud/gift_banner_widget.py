# -*- coding: utf-8 -*-
from __future__ import annotations

import blivedm.models.web as web_models
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class GiftBannerWidget(QFrame):
    """区域 2：打赏与送礼独立高亮卡片横幅 (Gift Highlight Banner Zone)"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("gift_banner")
        self.setVisible(False)
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

        self.font_scale: float = 1.0
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QFrame#gift_banner {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 105, 180, 220), stop:1 rgba(255, 215, 0, 220));
                border: 2px solid #ffd700;
                border-radius: 10px;
            }
            QLabel#gift_text_lbl {
                color: #11111b;
                font-weight: 900;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        self.icon_lbl = QLabel("🎁")
        self.icon_lbl.setStyleSheet("font-size: 20px;")

        self.text_lbl = QLabel("感谢老王送出 辣条 x100 ！")
        self.text_lbl.setObjectName("gift_text_lbl")

        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.text_lbl)
        layout.addStretch()

        self.update_font_size()

    def update_font_size(self):
        base_size = int(17 * self.font_scale)
        icon_size = int(22 * self.font_scale)
        self.text_lbl.setStyleSheet(f"font-size: {base_size}px; color: #11111b; font-weight: 900;")
        self.icon_lbl.setStyleSheet(f"font-size: {icon_size}px;")

    def set_font_scale(self, scale: float):
        self.font_scale = scale
        self.update_font_size()

    def add_gift(self, gift_msg: web_models.GiftMessage | Any):
        """收到送礼消息时，触发独立送礼高亮展示"""
        uname = getattr(gift_msg, "uname", "观众")
        action = getattr(gift_msg, "action", "赠送")
        gift_name = getattr(gift_msg, "gift_name", "礼物")
        num = getattr(gift_msg, "num", 1)

        display_str = f"🎉 感谢 {uname} {action} {gift_name} x{num} !"
        self.text_lbl.setText(display_str)

        self.show()
        self._hide_timer.start(10000)
