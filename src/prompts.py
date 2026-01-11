"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SYMBOL SUBSTITUTE TASK PROMPTS                             ║
║                                                                               ║
║  Prompt templates for Symbol Worlds_SymbolEditing_3:                         ║
║  Substitute a symbol at a specific position with a new symbol.               ║
║                                                                               ║
║  Each prompt clearly specifies:                                               ║
║  - Which symbol to replace (old symbol)                                       ║
║  - What to replace it with (new symbol)                                       ║
║  - At which position (1-indexed)                                              ║
║  - The animation sequence (cross-fade effect)                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  DEFINE YOUR PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPT_TEMPLATES = [
    "Substitute symbol {old_symbol} at position {position} with symbol {new_symbol}. The video shows the old symbol fading out while the new symbol simultaneously fades in at the same position.",

    "Replace symbol {old_symbol} at position {position} with symbol {new_symbol}. Animate the substitution with a cross-fade effect, where the old symbol gradually disappears as the new symbol appears.",

    "Substitute the symbol {old_symbol} at position {position} with {new_symbol}. The substitution is shown by cross-fading: the original symbol fades out while the replacement symbol fades in at the same location.",

    "Replace the symbol {old_symbol} at position {position} with symbol {new_symbol}. Show a smooth transition where both symbols are visible briefly during the cross-fade, with the old one fading out and the new one fading in.",
]


def get_prompt(old_symbol: str, new_symbol: str, position: int) -> str:
    """
    Generate a prompt for symbol substitution task.

    Args:
        old_symbol: The symbol to be replaced
        new_symbol: The symbol to replace with
        position: The 1-indexed position of the symbol to substitute

    Returns:
        Formatted prompt string
    """
    template = random.choice(PROMPT_TEMPLATES)
    return template.format(old_symbol=old_symbol, new_symbol=new_symbol, position=position)


def get_all_prompts() -> list[str]:
    """Get all prompt templates."""
    return PROMPT_TEMPLATES
