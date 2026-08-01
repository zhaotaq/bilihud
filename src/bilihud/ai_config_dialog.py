# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from .utils import load_config, save_config

if TYPE_CHECKING:
    from .danmaku_widget import DanmakuWidget


class AIConfigDialog(QDialog):
    """DeepSeek / AI 智囊 API 配置窗口"""

    def __init__(self, parent: DanmakuWidget | None = None):
        super().__init__(parent)
        self.danmaku_widget = parent
        self.setWindowTitle("DeepSeek / AI 直播智囊配置")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setFixedSize(380, 260)

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            QLabel {
                color: #a6adc8;
                font-size: 11px;
            }
            QLineEdit {
                background-color: #181825;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 6px;
                color: #cdd6f4;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #cba6f7;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #45475a;
                color: #ffffff;
            }
            QPushButton#save_btn {
                background: #cba6f7;
                color: #11111b;
                border: none;
            }
            QPushButton#save_btn:hover {
                background: #dce0e8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        layout.addWidget(QLabel("🔑 DeepSeek API Key (或 OpenAI Key):"))
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.key_input)

        layout.addWidget(QLabel("🌐 API Base URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://api.deepseek.com")
        layout.addWidget(self.url_input)

        layout.addWidget(QLabel("🤖 AI 模型名字:"))
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("deepseek-chat")
        layout.addWidget(self.model_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.save_btn = QPushButton("保存配置")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_settings)

        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def load_settings(self):
        config = load_config()
        key = config.get("ai_api_key", "")
        url = config.get("ai_base_url", "https://api.deepseek.com")
        model = config.get("ai_model", "deepseek-chat")

        self.key_input.setText(key)
        self.url_input.setText(url)
        self.model_input.setText(model)

    def save_settings(self):
        key = self.key_input.text().strip()
        url = self.url_input.text().strip() or "https://api.deepseek.com"
        model = self.model_input.text().strip() or "deepseek-chat"

        config = load_config()
        config["ai_api_key"] = key
        config["ai_base_url"] = url
        config["ai_model"] = model
        save_config(config)

        if self.danmaku_widget is not None and hasattr(self.danmaku_widget, "ai_copilot_service"):
            srv = self.danmaku_widget.ai_copilot_service
            srv.api_key = key
            srv.base_url = url
            srv.model = model

        self.accept()
