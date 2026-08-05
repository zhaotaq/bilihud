# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

import blivedm.models.web as web_models
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class GiftItemCard(QFrame):
    """单条高亮送礼卡片"""

    def __init__(self, uname: str, action: str, gift_name: str, num: int, font_scale: float = 1.0, parent: QWidget | None = None):
        super().__init__(parent)
        self.font_scale = font_scale
        self.setObjectName("gift_item_card")
        self.init_ui(uname, action, gift_name, num)

    def init_ui(self, uname: str, action: str, gift_name: str, num: int):
        self.setStyleSheet("""
            QFrame#gift_item_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 180, 0, 230), stop:1 rgba(255, 100, 150, 230));
                border: 1px solid rgba(255, 235, 150, 180);
                border-radius: 8px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(6)

        icon_lbl = QLabel("🎁")
        text_lbl = QLabel(f"感谢 {uname} {action} {gift_name} x{num} !")
        text_lbl.setObjectName("text_lbl")

        sz = int(15 * self.font_scale)
        icon_sz = int(18 * self.font_scale)
        text_lbl.setStyleSheet(f"color: #11111b; font-size: {sz}px; font-weight: 900;")
        icon_lbl.setStyleSheet(f"font-size: {icon_sz}px;")

        layout.addWidget(icon_lbl)
        layout.addWidget(text_lbl)
        layout.addStretch()


class GiftBannerWidget(QWidget):
    """区域 2：支持最多 4 行并存的打赏/送礼独立高亮卡片区 (Multi-Row Gift Highlight Zone)"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("gift_banner_zone")
        self.font_scale: float = 1.0
        self.cards: list[GiftItemCard] = []

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)
        self.hide()

    def set_font_scale(self, scale: float):
        self.font_scale = scale
        for card in self.cards:
            card.font_scale = scale
            card.init_ui(card.uname, card.action, card.gift_name, card.num)

    def add_gift(self, gift_msg: web_models.GiftMessage | Any):
        """收到送礼消息时，新增一行送礼卡片（最多保留 4 行）"""
        uname = getattr(gift_msg, "uname", "观众")
        action = getattr(gift_msg, "action", "赠送")
        gift_name = getattr(gift_msg, "gift_name", "礼物")
        num = getattr(gift_msg, "num", 1)

        card = GiftItemCard(uname, action, gift_name, num, font_scale=self.font_scale, parent=self)
        card.uname = uname
        card.action = action
        card.gift_name = gift_name
        card.num = num

        self.cards.append(card)
        self.layout.addWidget(card)
        self.show()

        if len(self.cards) > 4:
            oldest = self.cards.pop(0)
            self.layout.removeWidget(oldest)
            oldest.deleteLater()

        QTimer.singleShot(10000, lambda c=card: self._remove_card(c))

    def _remove_card(self, card: GiftItemCard):
        if card in self.cards:
            self.cards.remove(card)
            self.layout.removeWidget(card)
            card.deleteLater()
        if not self.cards:
            self.hide()
