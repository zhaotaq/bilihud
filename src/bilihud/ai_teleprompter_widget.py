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
    """副屏 AI 直播智囊悬浮提词卡片 (AI Live Teleprompter Floating Card)"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("teleprompter_card")
        self.setMinimumHeight(75)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QFrame#teleprompter_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(30, 24, 54, 230), stop:1 rgba(20, 30, 48, 230));
                border: 1px solid rgba(137, 180, 250, 80);
                border-radius: 10px;
            }
            QLabel#title_lbl {
                color: #cba6f7;
                font-size: 11px;
                font-weight: 700;
            }
            QLabel#question_lbl {
                color: #a6adc8;
                font-size: 11px;
                font-style: italic;
            }
            QLabel#suggestion_lbl {
                color: #f9e2af;
                font-size: 14px;
                font-weight: 800;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            QPushButton#copy_btn {
                background: rgba(137, 180, 250, 30);
                color: #89b4fa;
                border: 1px solid rgba(137, 180, 250, 60);
                border-radius: 5px;
                padding: 2px 6px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton#copy_btn:hover {
                background: rgba(137, 180, 250, 80);
                color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_lbl = QLabel("🤖 AI 智囊实时提词器")
        self.title_lbl.setObjectName("title_lbl")

        self.copy_btn = QPushButton("📋 复制台词")
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_suggestion)

        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.copy_btn)

        layout.addLayout(header_layout)

        self.question_lbl = QLabel("观众弹幕: 尚未收到提问")
        self.question_lbl.setObjectName("question_lbl")
        layout.addWidget(self.question_lbl)

        self.suggestion_lbl = QLabel("💡 提词建议: 开播大吉，随时准备接梗！")
        self.suggestion_lbl.setObjectName("suggestion_lbl")
        self.suggestion_lbl.setWordWrap(True)
        layout.addWidget(self.suggestion_lbl)

    def set_suggestion(self, uname: str, question: str, suggestion: str):
        """更新展示最新的提词卡片"""
        self.title_lbl.setText(f"🤖 AI 智囊提词器 [观众: {uname}]")
        self.question_lbl.setText(f"观众问: \"{question}\"")
        self.suggestion_lbl.setText(f"💡 提词: \"{suggestion}\"")

    def copy_suggestion(self):
        """一键复制台词到剪贴板"""
        raw_text = self.suggestion_lbl.text().replace("💡 提词: ", "").strip('"')
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(raw_text)
            self.copy_btn.setText("✓ 已复制")
            QTimer.singleShot(1500, lambda: self.copy_btn.setText("📋 复制台词"))
