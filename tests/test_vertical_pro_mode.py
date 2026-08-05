# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QApplication
from bilihud.danmaku_widget import DanmakuDelegate, DanmakuWidget
from bilihud.ai_teleprompter_widget import AITeleprompterWidget
from bilihud.mock_generator import MockMessageGenerator


def test_vertical_pro_large_font_html():
    delegate = DanmakuDelegate()
    msg = MockMessageGenerator.create_mock_danmaku(user="副屏主播", msg="测试大字号副屏呈现")
    html_output = delegate.get_html_for_message(msg)

    assert "font-size: 17px" in html_output
    assert "font-size: 15px" in html_output
    assert "line-height: 140%" in html_output


def test_ai_teleprompter_large_font_style():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    card = AITeleprompterWidget()
    card.set_suggestion("热心观众", "如何通关此关卡", "这波操作看好了，细节拉满！")

    style = card.suggestion_lbl.styleSheet()
    assert "font-size: 21px" in style
    assert "font-weight: 900" in style


def test_fullscreen_fill_toggle():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    widget = DanmakuWidget()
    assert hasattr(widget, "fullscreen_btn")
    assert widget.fullscreen_btn.text() == "🖥️ 铺满"

    widget.toggle_fullscreen_fill(True)
    assert widget.fullscreen_btn.text() == "🖥️ 还原"

    widget.toggle_fullscreen_fill(False)
    assert widget.fullscreen_btn.text() == "🖥️ 铺满"
