"""
Your custom task implementation.

Files to customize:
    - config.py   : Task-specific configuration (TaskConfig)
    - generator.py: Task generation logic (SymbolSubstituteGenerator)
    - prompts.py  : Task prompts/instructions (get_prompt)
"""

from .config import TaskConfig
from .generator import SymbolSubstituteGenerator as TaskGenerator
from .prompts import get_prompt

__all__ = ["TaskConfig", "TaskGenerator", "get_prompt"]
