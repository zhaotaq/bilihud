# -*- coding: utf-8 -*-
from __future__ import annotations

import collections
import re
from typing import Any

import blivedm.models.web as web_models


class LiveStatsTracker:
    """直播间实时数据统计与送礼金榜追踪器 (Live Streaming Stats & Leaderboard)"""

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        """重置本场直播统计数据"""
        self.total_danmaku_count: int = 0
        self.total_gift_count: int = 0
        self.total_battery: int = 0  # 电池总数 (10电池 = 1元人民币)
        
        # 观众送礼榜单: uname -> {"uname": str, "total_price": int, "gift_count": int, "last_gift": str}
        self.leaderboard: dict[str, dict[str, Any]] = collections.defaultdict(
            lambda: {"uname": "", "total_price": 0, "gift_count": 0, "last_gift": ""}
        )
        
        # 互动观众集合: uname
        self.active_users: set[str] = set()

        # 高频词汇统计
        self.word_counts: collections.Counter[str] = collections.Counter()

    def process_message(self, message: Any) -> None:
        """处理新收到的弹幕/礼物/互动消息并更新统计数据"""
        if isinstance(message, web_models.DanmakuMessage) or (
            hasattr(message, "uname") and hasattr(message, "msg") and not getattr(message, "is_system_info", False)
        ):
            self.total_danmaku_count += 1
            uname = str(getattr(message, "uname", ""))
            if uname:
                self.active_users.add(uname)

            msg_text = str(getattr(message, "msg", ""))
            self._analyze_words(msg_text)

        elif isinstance(message, web_models.GiftMessage) or (
            hasattr(message, "gift_name") and hasattr(message, "uname")
        ):
            self.total_gift_count += 1
            uname = str(getattr(message, "uname", ""))
            gift_name = str(getattr(message, "gift_name", "礼物"))
            num = int(getattr(message, "num", 1))
            price = int(getattr(message, "price", 0))  # 单位: 瓜子/电池

            total_gift_price = price * num
            self.total_battery += total_gift_price

            if uname:
                self.active_users.add(uname)
                user_stat = self.leaderboard[uname]
                user_stat["uname"] = uname
                user_stat["total_price"] += total_gift_price
                user_stat["gift_count"] += num
                user_stat["last_gift"] = gift_name

        elif isinstance(message, web_models.InteractWordV2Message):
            uname = str(getattr(message, "username", ""))
            if uname:
                self.active_users.add(uname)

    def _analyze_words(self, text: str) -> None:
        """提取短句和高频表情/关键词"""
        if not text:
            return
        
        # 清理常见无意义字符，按空格或符号切割
        words = re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]{2,}", text)
        for w in words:
            # 过滤过长的无意义重复句子
            if len(w) <= 10:
                self.word_counts[w] += 1

    def get_top_supporters(self, limit: int = 10) -> list[dict[str, Any]]:
        """获取前 N 名金榜打赏观众"""
        sorted_users = sorted(
            self.leaderboard.values(),
            key=lambda x: x["total_price"],
            reverse=True
        )
        return sorted_users[:limit]

    def get_top_words(self, limit: int = 8) -> list[tuple[str, int]]:
        """获取前 N 个高频词汇"""
        return self.word_counts.most_common(limit)

    def get_summary(self) -> dict[str, Any]:
        """获取全场数据概览"""
        total_yuan = round(self.total_battery / 1000.0, 2)  # B站 1000电池 = 1元
        return {
            "total_danmaku": self.total_danmaku_count,
            "total_gifts": self.total_gift_count,
            "active_users_count": len(self.active_users),
            "total_rmb": total_yuan,
            "top_supporters": self.get_top_supporters(10),
            "top_words": self.get_top_words(8),
        }
