# -*- coding: utf-8 -*-
import tempfile
from pathlib import Path
from bilihud.obsidian_indexer import ObsidianVaultIndexer


def test_obsidian_vault_indexer():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_path = Path(tmp_dir)

        note1 = dir_path / "黑神话攻略.md"
        note1.write_text("# 虎先锋打法\n\n先等它拍地闪避，然后再用定身术输出。", encoding="utf-8")

        note2 = dir_path / "硬件配置.md"
        note2.write_text("# 电脑配置\n\nFedora Linux + RTX 4090，4K高帧率绝无卡顿。", encoding="utf-8")

        indexer = ObsidianVaultIndexer(str(dir_path))
        assert len(indexer.documents) == 2

        res1 = indexer.search_relevant_context("虎先锋怎么打？")
        assert "虎先锋打法" in res1
        assert "定身术" in res1

        res2 = indexer.search_relevant_context("主播显卡配置是多少")
        assert "RTX 4090" in res2
