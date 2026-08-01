# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ObsidianVaultIndexer:
    """Obsidian / 本地 Markdown 游戏攻略库极速索引与搜索器"""

    def __init__(self, vault_path: str = ""):
        self.vault_path = str(vault_path).strip()
        self.documents: list[dict[str, str]] = []
        if self.vault_path and os.path.exists(self.vault_path):
            self.reload_vault()

    def set_vault_path(self, path: str) -> None:
        self.vault_path = str(path).strip()
        self.reload_vault()

    def reload_vault(self) -> None:
        """扫描指定文件夹下所有 .md / .txt 笔记并构建索引"""
        self.documents.clear()
        if not self.vault_path or not os.path.isdir(self.vault_path):
            return

        try:
            vault_dir = Path(self.vault_path)
            for file_path in vault_dir.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in (".md", ".txt", ".markdown"):
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
                        if content:
                            title = file_path.stem
                            self.documents.append({
                                "title": title,
                                "path": str(file_path),
                                "content": content
                            })
                    except Exception as err:
                        logger.warning("Failed to read note file %s: %s", file_path, err)
        except Exception as exc:
            logger.error("Error reading vault directory %s: %s", self.vault_path, exc)

    def search_relevant_context(self, query: str, top_k: int = 2, max_chars: int = 400) -> str:
        """在 0.005 秒内匹配与观众提问最相关的 1-2 篇短笔记片段，极省 Token"""
        if not self.documents or not query.strip():
            return ""

        raw_words = re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]+", query)
        keywords = set()
        for w in raw_words:
            if len(w) >= 2:
                keywords.add(w)
                for i in range(len(w) - 1):
                    keywords.add(w[i:i+2])
            else:
                keywords.add(w)

        if not keywords:
            keywords = {query.strip()}

        scored_docs: list[tuple[float, str, str]] = []

        for doc in self.documents:
            title = doc["title"]
            content = doc["content"]

            title_score = sum(3.0 for kw in keywords if kw.lower() in title.lower())
            body_score = sum(1.0 for kw in keywords if kw.lower() in content.lower())

            total_score = title_score + body_score
            if total_score > 0:
                snippet = content[:250] if len(content) > 250 else content
                scored_docs.append((total_score, title, snippet))

        if not scored_docs:
            return ""

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        selected_texts = []
        total_len = 0

        for score, title, snippet in scored_docs[:top_k]:
            formatted_item = f"【Obsidian 笔记: {title}】\n{snippet}"
            if len(formatted_item) + total_len > max_chars:
                break
            selected_texts.append(formatted_item)
            total_len += len(formatted_item)

        return "\n\n".join(selected_texts)
