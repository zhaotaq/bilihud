# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QApplication
from bilihud.danmaku_widget import DanmakuWidget
from bilihud.gift_banner_widget import GiftBannerWidget
from bilihud.system_info_widget import SystemInfoWidget
from bilihud.mock_generator import MockMessageGenerator


def test_zone_layout_routing():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    widget = DanmakuWidget()
    widget.show()

    danmaku_msg = MockMessageGenerator.create_mock_danmaku(user="路人甲", msg="主播好棒！")
    widget.add_message(danmaku_msg)
    assert widget.danmaku_list.count() == 1

    gift_msg = MockMessageGenerator.create_mock_gift(user="大榜哥", gift_name="小电视", num=1)
    widget.add_message(gift_msg)
    assert "大榜哥" in widget.gift_banner.text_lbl.text()
    assert "小电视" in widget.gift_banner.text_lbl.text()

    interact_msg = MockMessageGenerator.create_mock_interact(user="粉丝A", msg_type=1)
    widget.add_message(interact_msg)
    assert "粉丝A" in widget.system_info_bar.info_lbl.text()


def test_dynamic_font_scaling():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    widget = DanmakuWidget()
    initial_scale = widget.font_scale

    widget.change_font_scale(0.15)
    assert widget.font_scale == initial_scale + 0.15

    widget.change_font_scale(-0.30)
    assert round(widget.font_scale, 2) == round(initial_scale - 0.15, 2)
