# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from .danmaku_widget import DanmakuWidget


class LiveStatsDialog(QDialog):
    """直播间实时数据看板与打赏金榜弹窗 (Live Stats & Leaderboard Window)"""

    def __init__(self, parent: DanmakuWidget | None = None):
        super().__init__(parent)
        self.danmaku_widget = parent
        self.setWindowTitle("直播间实时数据看板与打赏金榜")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setFixedSize(480, 420)

        # 自动刷新定时器 (2 秒刷新一次数据)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(2000)
        self._refresh_timer.timeout.connect(self.refresh_stats)

        self.init_ui()
        self.refresh_stats()

    def init_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #11111b;
                color: #cdd6f4;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            QFrame#summary_card {
                background-color: #1e1e2e;
                border: 1px solid rgba(255, 255, 255, 12);
                border-radius: 8px;
                padding: 6px;
            }
            QLabel#num_label {
                font-size: 16px;
                font-weight: 800;
                color: #f5e0dc;
            }
            QLabel#title_label {
                font-size: 11px;
                color: #a6adc8;
            }
            QTableWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                gridline-color: #313244;
                border: 1px solid rgba(255, 255, 255, 12);
                border-radius: 8px;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #313244;
                color: #b4befe;
                font-weight: bold;
                font-size: 11px;
                border: none;
                padding: 4px;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 6px;
                padding: 5px 12px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #45475a;
                color: #ffffff;
            }
            QPushButton#reset_btn {
                background-color: rgba(243, 139, 168, 30);
                color: #f38ba8;
                border-color: rgba(243, 139, 168, 60);
            }
            QPushButton#reset_btn:hover {
                background-color: rgba(243, 139, 168, 60);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # 头部数据看板行
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(8)

        self.card_battery = self._create_card("打赏收益", "￥0.00", "#fab387")
        self.card_danmaku = self._create_card("弹幕总量", "0 条", "#89b4fa")
        self.card_gifts = self._create_card("礼物次数", "0 次", "#f5c2e7")
        self.card_users = self._create_card("互动人数", "0 人", "#a6e3a1")

        summary_layout.addWidget(self.card_battery[0])
        summary_layout.addWidget(self.card_danmaku[0])
        summary_layout.addWidget(self.card_gifts[0])
        summary_layout.addWidget(self.card_users[0])

        layout.addLayout(summary_layout)

        # 排行榜表格标题
        table_title = QLabel("🏆 本场直播观众打赏榜 Top 10")
        t_font = QFont()
        t_font.setBold(True)
        t_font.setPixelSize(13)
        table_title.setFont(t_font)
        table_title.setStyleSheet("color: #f9e2af; margin-top: 4px;")
        layout.addWidget(table_title)

        # 打赏榜单表格
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["排名", "观众昵称", "打赏估值", "最近送出"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setColumnWidth(0, 50)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.table)

        # 底部控制栏
        bottom_layout = QHBoxLayout()

        self.btn_reset = QPushButton("🗑 重置本场统计")
        self.btn_reset.setObjectName("reset_btn")
        self.btn_reset.clicked.connect(self.reset_stats)

        self.btn_refresh = QPushButton("🔄 刷新")
        self.btn_refresh.clicked.connect(self.refresh_stats)

        bottom_layout.addWidget(self.btn_reset)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_refresh)

        layout.addLayout(bottom_layout)

    def _create_card(self, title: str, init_val: str, color_hex: str) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("summary_card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(6, 6, 6, 6)
        card_layout.setSpacing(2)

        t_lbl = QLabel(title)
        t_lbl.setObjectName("title_label")

        num_lbl = QLabel(init_val)
        num_lbl.setObjectName("num_label")
        num_lbl.setStyleSheet(f"color: {color_hex}; font-size: 14px; font-weight: 800;")

        card_layout.addWidget(t_lbl)
        card_layout.addWidget(num_lbl)
        return card, num_lbl

    def refresh_stats(self):
        """刷新看板与表格数据"""
        if self.danmaku_widget is None or not hasattr(self.danmaku_widget, "stats_tracker"):
            return

        tracker = self.danmaku_widget.stats_tracker
        summary = tracker.get_summary()

        # 更新顶部卡片
        self.card_battery[1].setText(f"￥{summary['total_rmb']:.2f}")
        self.card_danmaku[1].setText(f"{summary['total_danmaku']} 条")
        self.card_gifts[1].setText(f"{summary['total_gifts']} 次")
        self.card_users[1].setText(f"{summary['active_users_count']} 人")

        # 更新排行榜表格
        supporters = summary["top_supporters"]
        self.table.setRowCount(len(supporters))

        medals = ["🥇 1", "🥈 2", "🥉 3"]

        for row, user_data in enumerate(supporters):
            rank_str = medals[row] if row < 3 else f"  {row + 1}"
            rank_item = QTableWidgetItem(rank_str)
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            name_item = QTableWidgetItem(user_data["uname"])
            
            val_yuan = user_data["total_price"] / 1000.0
            val_str = f"￥{val_yuan:.2f}" if val_yuan >= 0.01 else f"{user_data['total_price']} 电池"
            val_item = QTableWidgetItem(val_str)
            val_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            gift_item = QTableWidgetItem(user_data["last_gift"] or "礼物")

            self.table.setItem(row, 0, rank_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, val_item)
            self.table.setItem(row, 3, gift_item)

    def reset_stats(self):
        """清空重置"""
        if self.danmaku_widget is not None and hasattr(self.danmaku_widget, "stats_tracker"):
            self.danmaku_widget.stats_tracker.reset()
            self.refresh_stats()

    def showEvent(self, event):
        self.refresh_stats()
        self._refresh_timer.start()
        super().showEvent(event)

    def closeEvent(self, event):
        self._refresh_timer.stop()
        super().closeEvent(event)
