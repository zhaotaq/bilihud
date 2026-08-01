# -*- coding: utf-8 -*-
import pytest
from PyQt6.QtWidgets import QApplication
from bilihud.ai_copilot_service import AICopilotService
from bilihud.ai_teleprompter_widget import AITeleprompterWidget


@pytest.mark.asyncio
async def test_ai_copilot_fallback_generation():
    service = AICopilotService(api_key="", enabled=True)

    sug1 = await service.generate_suggestion("观众A", "主播你用的是什么显卡和系统啊")
    assert "Linux" in sug1 or "配置" in sug1

    sug2 = await service.generate_suggestion("观众B", "这关怎么过啊？如何操作？")
    assert "细节" in sug2 or "操作" in sug2


def test_ai_copilot_knowledge_base():
    kb_text = "黑神话虎先锋打法：先等它拍地再用定身术。"
    service = AICopilotService(api_key="sk-test", knowledge_base=kb_text)
    assert service.knowledge_base == kb_text


def test_ai_teleprompter_widget_ui():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    card = AITeleprompterWidget()
    card.set_suggestion("极客小明", "主播今天玩什么游戏？", "今晚带大家通关神作！")

    assert "极客小明" in card.title_lbl.text()
    assert "主播今天玩什么游戏" in card.question_lbl.text()
    assert "今晚带大家通关神作" in card.suggestion_lbl.text()

    card.copy_suggestion()
    clipboard = QApplication.clipboard()
    assert clipboard.text() == "今晚带大家通关神作！"
