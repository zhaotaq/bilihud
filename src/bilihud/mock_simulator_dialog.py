# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QPoint, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .mock_generator import MockMessageGenerator

if TYPE_CHECKING:
    from .danmaku_widget import DanmakuWidget


class MockSimulatorDialog(QDialog):
    """开播前视觉效果与弹幕样式测试面板 (Mock Simulator Control Panel)"""

    def __init__(self, parent: DanmakuWidget | None = None):
        super().__init__(parent)
        self.danmaku_widget = parent
        self.setWindowTitle("开播前弹幕与视觉效果模拟器")
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool
        )
        self.setFixedSize(360, 320)

        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(1200)
        self._auto_timer.timeout.connect(self._on_auto_tick)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            QFrame#card {
                background-color: #2a2b3d;
                border: 1px solid rgba(255, 255, 255, 15);
                border-radius: 10px;
            }
            QLabel {
                color: #a6adc8;
                font-size: 12px;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #45475a;
                border-color: #89b4fa;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
            QPushButton#primary_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #89b4fa, stop:1 #b4befe);
                color: #11111b;
                border: none;
            }
            QPushButton#primary_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #99c1ff, stop:1 #c5ccff);
            }
            QPushButton#toggle_btn:checked {
                background: #a6e3a1;
                color: #11111b;
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
                border-color: #89b4fa;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        title_label = QLabel("🧪 弹幕与视觉效果测试面板")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPixelSize(14)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #89b4fa;")
        main_layout.addWidget(title_label)

        grid_card = QFrame()
        grid_card.setObjectName("card")
        grid_layout = QGridLayout(grid_card)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(8)

        self.btn_danmaku = QPushButton("💬 普通弹幕")
        self.btn_danmaku.clicked.connect(self.send_mock_danmaku)

        self.btn_guard = QPushButton("👑 舰长/大航海")
        self.btn_guard.clicked.connect(self.send_mock_guard)

        self.btn_gift = QPushButton("🎁 礼物通知")
        self.btn_gift.clicked.connect(self.send_mock_gift)

        self.btn_interact = QPushButton("✨ 观众进房")
        self.btn_interact.clicked.connect(self.send_mock_interact)

        grid_layout.addWidget(self.btn_danmaku, 0, 0)
        grid_layout.addWidget(self.btn_guard, 0, 1)
        grid_layout.addWidget(self.btn_gift, 1, 0)
        grid_layout.addWidget(self.btn_interact, 1, 1)

        main_layout.addWidget(grid_card)

        custom_card = QFrame()
        custom_card.setObjectName("card")
        custom_layout = QHBoxLayout(custom_card)
        custom_layout.setContentsMargins(8, 8, 8, 8)
        custom_layout.setSpacing(6)

        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText("输入自定义测试文字...")
        self.custom_input.returnPressed.connect(self.send_custom_danmaku)

        self.btn_send_custom = QPushButton("测试")
        self.btn_send_custom.setObjectName("primary_btn")
        self.btn_send_custom.clicked.connect(self.send_custom_danmaku)

        custom_layout.addWidget(self.custom_input)
        custom_layout.addWidget(self.btn_send_custom)

        main_layout.addWidget(custom_card)

        auto_card = QFrame()
        auto_card.setObjectName("card")
        auto_layout = QHBoxLayout(auto_card)
        auto_layout.setContentsMargins(8, 8, 8, 8)

        auto_label = QLabel("模拟持续刷屏:")
        self.btn_auto_toggle = QPushButton("▶ 开启自动刷屏")
        self.btn_auto_toggle.setObjectName("toggle_btn")
        self.btn_auto_toggle.setCheckable(True)
        self.btn_auto_toggle.toggled.connect(self.toggle_auto_play)

        auto_layout.addWidget(auto_label)
        auto_layout.addStretch()
        auto_layout.addWidget(self.btn_auto_toggle)

        main_layout.addWidget(auto_card)

    def _emit_to_widget(self, message):
        if self.danmaku_widget is not None and hasattr(self.danmaku_widget, "add_message"):
            self.danmaku_widget.add_message(message)

    def send_mock_danmaku(self):
        msg = MockMessageGenerator.create_mock_danmaku()
        self._emit_to_widget(msg)

    def send_mock_guard(self):
        msg = MockMessageGenerator.create_mock_danmaku(is_guard=True)
        self._emit_to_widget(msg)

    def send_mock_gift(self):
        msg = MockMessageGenerator.create_mock_gift()
        self._emit_to_widget(msg)

    def send_mock_interact(self):
        msg = MockMessageGenerator.create_mock_interact()
        self._emit_to_widget(msg)

    def send_custom_danmaku(self):
        text = self.custom_input.text().strip()
        if not text:
            text = "副屏测试：这就是预设的测试弹幕样式"
        msg = MockMessageGenerator.create_mock_danmaku(user="主播测试", msg=text)
        self._emit_to_widget(msg)
        self.custom_input.clear()

    def toggle_auto_play(self, checked: bool):
        if checked:
            self.btn_auto_toggle.setText("⏸ 停止自动刷屏")
            self._auto_timer.start()
        else:
            self.btn_auto_toggle.setText("▶ 开启自动刷屏")
            self._auto_timer.stop()

    def _on_auto_tick(self):
        handlers = [
            self.send_mock_danmaku,
            self.send_mock_guard,
            self.send_mock_gift,
            self.send_mock_interact,
        ]
        import random
        random.choice(handlers)()

    def closeEvent(self, event):
        self._auto_timer.stop()
        self.btn_auto_toggle.setChecked(False)
        super().closeEvent(event)
