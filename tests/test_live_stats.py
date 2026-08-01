# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QApplication, QWidget
from bilihud.live_stats_dialog import LiveStatsDialog
from bilihud.live_stats_tracker import LiveStatsTracker
from bilihud.mock_generator import MockMessageGenerator


class DummyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stats_tracker = LiveStatsTracker()


def test_live_stats_tracker_logic():
    tracker = LiveStatsTracker()

    # 1. 模拟处理弹幕
    msg1 = MockMessageGenerator.create_mock_danmaku(user="神级观众", msg="太强了 6666")
    msg2 = MockMessageGenerator.create_mock_danmaku(user="普通路人", msg="学习了")
    tracker.process_message(msg1)
    tracker.process_message(msg2)

    assert tracker.total_danmaku_count == 2
    assert len(tracker.active_users) == 2

    # 2. 模拟处理礼物
    gift1 = MockMessageGenerator.create_mock_gift(user="大佬A", gift_name="辣条", num=10)
    gift1.price = 100  # 100 电池
    tracker.process_message(gift1)

    assert tracker.total_gift_count == 1
    assert tracker.total_battery == 1000  # 10 * 100

    # 3. 获取 Top 排行榜与摘要
    summary = tracker.get_summary()
    assert summary["total_danmaku"] == 2
    assert summary["total_gifts"] == 1
    assert summary["total_rmb"] == 1.0  # 1000 电池 = 1.0 元

    top_supporters = tracker.get_top_supporters()
    assert len(top_supporters) == 1
    assert top_supporters[0]["uname"] == "大佬A"

    # 4. 测试重置数据
    tracker.reset()
    assert tracker.total_danmaku_count == 0
    assert tracker.total_battery == 0


def test_live_stats_dialog_ui():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    dummy_widget = DummyWidget()

    # 先填充测试数据
    gift = MockMessageGenerator.create_mock_gift(user="土豪一号", gift_name="舰长", num=1)
    gift.price = 198000
    dummy_widget.stats_tracker.process_message(gift)

    dialog = LiveStatsDialog(parent=dummy_widget)

    # 验证面板成功获取数据并渲染 Table
    assert dialog.table.rowCount() == 1
    assert dialog.table.item(0, 1).text() == "土豪一号"

    # 测试重置按钮交互
    dialog.reset_stats()
    assert dialog.table.rowCount() == 0
