# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QApplication, QWidget
from bilihud.mock_simulator_dialog import MockSimulatorDialog


class DummyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.received_messages = []

    def add_message(self, msg):
        self.received_messages.append(msg)


def test_mock_simulator_dialog_actions():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    dummy_widget = DummyWidget()
    dialog = MockSimulatorDialog(parent=dummy_widget)

    # 1. 测试发送普通弹幕
    dialog.send_mock_danmaku()
    assert len(dummy_widget.received_messages) == 1

    # 2. 测试发送舰长弹幕
    dialog.send_mock_guard()
    assert len(dummy_widget.received_messages) == 2

    # 3. 测试发送礼物通知
    dialog.send_mock_gift()
    assert len(dummy_widget.received_messages) == 3

    # 4. 测试发送进房互动
    dialog.send_mock_interact()
    assert len(dummy_widget.received_messages) == 4

    # 5. 测试自定义弹幕文本
    dialog.custom_input.setText("自定义 4K 测试弹幕")
    dialog.send_custom_danmaku()
    assert len(dummy_widget.received_messages) == 5
    assert dummy_widget.received_messages[-1].msg == "自定义 4K 测试弹幕"

    # 6. 测试自动刷屏定时器开关
    dialog.toggle_auto_play(True)
    assert dialog._auto_timer.isActive()
    dialog.toggle_auto_play(False)
    assert not dialog._auto_timer.isActive()
