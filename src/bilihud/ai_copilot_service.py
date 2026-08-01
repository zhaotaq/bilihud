# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)

FALLBACK_SUGGESTIONS = [
    (r"显卡|配置|电脑|系统", "Fedora Linux 加上神仙配置，丝滑无卡顿！"),
    (r"怎么|咋办|如何|求助|教教", "这波操作看仔细了，细节决定成败！"),
    (r"价格|多少钱|贵不贵|优惠", "现在下单最划算，主播亲测真香！"),
    (r"主播|叫什么|几点|明天", "关注主播不迷路，每天精彩不停歇！"),
    (r"666|牛|厉害|强", "感谢老铁点赞，低调低调，常规操作！"),
]


class AICopilotService(QObject):
    """DeepSeek / OpenAI AI 直播智囊副屏提词生成服务"""

    suggestion_generated = pyqtSignal(str, str, str)

    def __init__(
        self,
        api_key: str = "",
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-chat",
        enabled: bool = True,
    ):
        super().__init__()
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.enabled = enabled

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def process_message(self, message: Any) -> None:
        """异步评估并处理弹幕消息，符合条件的触发 AI 提词"""
        if not self.enabled:
            return

        uname = str(getattr(message, "uname", ""))
        text = str(getattr(message, "msg", "")).strip()

        if not text or getattr(message, "is_system_info", False):
            return

        if len(text) < 2 or re.match(r"^[0-9a-zA-Z\s]+$", text) and len(text) <= 4:
            return

        asyncio.create_task(self.generate_suggestion(uname, text))

    async def generate_suggestion(self, uname: str, text: str) -> str:
        """调用 DeepSeek API 或降级引擎生成 15 字口语化副屏提词"""
        if not self.is_configured():
            suggestion = self._get_fallback_suggestion(text)
            self.suggestion_generated.emit(uname, text, suggestion)
            return suggestion

        try:
            import aiohttp

            system_prompt = (
                "你是一名顶级AI直播副屏提词助手。根据观众弹幕，为主播生成一条15字以内的口语化、诙谐搞笑、可直接念出的接话台词。"
                "要求：绝对不超过15个字！不要标点符号堆砌！接地气！"
            )
            user_prompt = f"观众 [{uname}] 说：\"{text}\""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 50,
                "temperature": 0.7,
            }

            url = f"{self.base_url}/chat/completions"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        suggestion = data["choices"][0]["message"]["content"].strip()
                        suggestion = suggestion.replace('"', "").replace("\n", " ")
                        if len(suggestion) > 20:
                            suggestion = suggestion[:18] + "..."
                        self.suggestion_generated.emit(uname, text, suggestion)
                        return suggestion
                    else:
                        logger.warning("AI API HTTP Error %s, using fallback", resp.status)
        except Exception as exc:
            logger.error("Failed to generate AI suggestion: %s", exc)

        suggestion = self._get_fallback_suggestion(text)
        self.suggestion_generated.emit(uname, text, suggestion)
        return suggestion

    def _get_fallback_suggestion(self, text: str) -> str:
        for pattern, sug in FALLBACK_SUGGESTIONS:
            if re.search(pattern, text, re.IGNORECASE):
                return sug
        return "这个问题问得好！咱们边看边聊~"
