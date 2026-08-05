# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from .danmaku_widget import DanmakuWidget


class AITeleprompterWidget(QFrame):
    """专业极简级副屏 AI 直播智囊提词卡片 (Pro Sleek AI Teleprompter Card)"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("teleprompter_card")
        self.setMinimumHeight(70)
        self.font_scale: float = 1.0

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QFrame#teleprompter_card {
                background: rgba(18, 20, 28, 240);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 10px;
            }
            QPushButton#copy_btn {
                background: rgba(255, 255, 255, 15);
                color: #cdd6f4;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 5px;
                padding: 3px 8px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton#copy_btn:hover {
                background: rgba(255, 255, 255, 35);
                color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_lbl = QLabel("LIVE COPILOT | AI 提词建议")
        self.title_lbl.setObjectName("title_lbl")

        self.copy_btn = QPushButton("📋 复制")
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_suggestion)

        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.copy_btn)

        layout.addLayout(header_layout)

        self.question_lbl = QLabel("观众: 尚未收到提问")
        self.question_lbl.setObjectName("question_lbl")
        layout.addWidget(self.question_lbl)

        self.suggestion_lbl = QLabel("手感好那都是演给你看的")
        self.suggestion_lbl.setObjectName("suggestion_lbl")
        self.suggestion_lbl.setWordWrap(True)
        layout.addWidget(self.suggestion_lbl)

        self.update_font_size()

    def update_font_size(self):
        """高级极简Pro排版字号调节"""
        title_sz = int(11 * self.font_scale)
        q_sz = int(12 * self.font_scale)
        sug_sz = int(21 * self.font_scale)

        self.title_lbl.setStyleSheet(f"color: #89b4fa; font-size: {title_sz}px; font-weight: 800; letter-spacing: 0.5px;")
        self.question_lbl.setStyleSheet(f"color: #a6adc8; font-size: {q_sz}px; font-weight: 500;")
        self.suggestion_lbl.setStyleSheet(
            f"color: #ffffff; font-size: {sug_sz}px; font-weight: 900; "
            f"font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; line-height: 135%; padding: 2px 0px;"
        )

    def set_font_scale(self, scale: float):
        self.font_scale = scale
        self.update_font_size()

    def set_suggestion(self, uname: str, question: str, suggestion: str):
        """更新展示最新的提词建议"""
        self.title_lbl.setText(f"LIVE COPILOT | 观众: {uname}")
        self.question_lbl.setText(f"提问: {question}")
        self.suggestion_lbl.setText(suggestion)

    def copy_suggestion(self):
        """一键复制台词到剪贴板"""
        raw_text = self.suggestion_lbl.text().strip()
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(raw_text)
            self.copy_btn.setText("✓ 已复制")
            QTimer.singleShot(1500, lambda: self.copy_btn.setText("📋 复制"))
