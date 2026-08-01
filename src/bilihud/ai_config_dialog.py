# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from .utils import load_config, save_config

if TYPE_CHECKING:
    from .danmaku_widget import DanmakuWidget


class AIConfigDialog(QDialog):
    """DeepSeek / AI 智囊 API 与 Obsidian 游戏知识库配置窗口"""

    def __init__(self, parent: DanmakuWidget | None = None):
        super().__init__(parent)
        self.danmaku_widget = parent
        self.setWindowTitle("DeepSeek AI 智囊与 Obsidian 知识库配置")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setFixedSize(450, 480)

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
            QLineEdit, QTextEdit {
                background-color: #181825;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 6px;
                color: #cdd6f4;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus {
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
        layout.setSpacing(8)

        layout.addWidget(QLabel("🔑 DeepSeek API Key (或 OpenAI Key):"))
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.key_input)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(6)

        url_box = QVBoxLayout()
        url_box.addWidget(QLabel("🌐 API Base URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://api.deepseek.com")
        url_box.addWidget(self.url_input)

        model_box = QVBoxLayout()
        model_box.addWidget(QLabel("🤖 AI 模型名字:"))
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("deepseek-chat")
        model_box.addWidget(self.model_input)

        row_layout.addLayout(url_box)
        row_layout.addLayout(model_box)
        layout.addLayout(row_layout)

        layout.addWidget(QLabel("📂 Obsidian 游戏攻略笔记文件夹 (含多篇 .md 档案):"))
        vault_layout = QHBoxLayout()
        vault_layout.setSpacing(6)

        self.vault_input = QLineEdit()
        self.vault_input.setPlaceholderText("例如: /home/user/Documents/Obsidian Vault/游戏攻略")

        self.browse_btn = QPushButton("📁 浏览")
        self.browse_btn.clicked.connect(self.browse_vault_folder)

        vault_layout.addWidget(self.vault_input)
        vault_layout.addWidget(self.browse_btn)
        layout.addLayout(vault_layout)

        layout.addWidget(QLabel("📝 常用随手记 / 核心规则 (每行一条):"))
        self.knowledge_input = QTextEdit()
        self.knowledge_input.setPlaceholderText(
            "例如:\n"
            "- 黑神话悟空虎先锋打法：先等它拍地，闪避后再用定身术。\n"
            "- 显卡配置：i9-14900K + RTX 4090，4K高帧率绝无卡顿。"
        )
        layout.addWidget(self.knowledge_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.save_btn = QPushButton("保存配置与知识库")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_settings)

        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def browse_vault_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择 Obsidian 游戏攻略笔记文件夹", self.vault_input.text().strip())
        if folder:
            self.vault_input.setText(folder)

    def load_settings(self):
        config = load_config()
        key = config.get("ai_api_key", "")
        url = config.get("ai_base_url", "https://api.deepseek.com")
        model = config.get("ai_model", "deepseek-chat")
        kb = config.get("ai_knowledge_base", "")
        vault = config.get("ai_vault_path", "")

        self.key_input.setText(key)
        self.url_input.setText(url)
        self.model_input.setText(model)
        self.knowledge_input.setPlainText(kb)
        self.vault_input.setText(vault)

    def save_settings(self):
        key = self.key_input.text().strip()
        url = self.url_input.text().strip() or "https://api.deepseek.com"
        model = self.model_input.text().strip() or "deepseek-chat"
        kb = self.knowledge_input.toPlainText().strip()
        vault = self.vault_input.text().strip()

        config = load_config()
        config["ai_api_key"] = key
        config["ai_base_url"] = url
        config["ai_model"] = model
        config["ai_knowledge_base"] = kb
        config["ai_vault_path"] = vault
        save_config(config)

        if self.danmaku_widget is not None and hasattr(self.danmaku_widget, "ai_copilot_service"):
            srv = self.danmaku_widget.ai_copilot_service
            srv.api_key = key
            srv.base_url = url
            srv.model = model
            srv.knowledge_base = kb
            srv.vault_indexer.set_vault_path(vault)

        self.accept()
