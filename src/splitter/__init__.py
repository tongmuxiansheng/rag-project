"""
文本切片器模块
支持按字符 / 按语义 / 递归切片
"""
from .character_splitter import CharacterSplitter
from .recursive_splitter import RecursiveSplitter

__all__ = [
    "CharacterSplitter",
    "RecursiveSplitter",
]
