"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SYMBOL SUBSTITUTE TASK PROMPTS                             ║
║                                                                               ║
║  Unified prompt template for Symbol Worlds_SymbolEditing_3:                  ║
║  Substitute a symbol at a specific position with a new symbol.               ║
║                                                                               ║
║  Each prompt clearly specifies:                                               ║
║  - Which symbol to replace (emoji at position)                               ║
║  - What to replace it with (color description + emoji)                       ║
║  - The animation sequence (fade-out then fade-in)                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


# ══════════════════════════════════════════════════════════════════════════════
#  DEFINE YOUR PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

# Unified prompt template (position identifies old symbol, color describes new symbol)
PROMPT_TEMPLATE = (
    "Substitute {old_symbol} at position {position} with a {new_color} {new_symbol}. "
    "The animation shows the old symbol fading out completely, "
    "then the new symbol gradually fading in at the same position."
)


def get_prompt(old_symbol: str, new_symbol: str, new_color: str, position: int) -> str:
    """
    Generate a prompt for symbol substitution task.

    Args:
        old_symbol: The symbol emoji to be replaced (e.g., '●')
        new_symbol: The symbol emoji to replace with (e.g., '■')
        new_color: The color name of the new symbol (e.g., 'red', 'blue')
        position: The 1-indexed position of the symbol to substitute

    Returns:
        Formatted prompt string (e.g., "Substitute ● at position 3 with red的■. The animation shows...")
    """
    return PROMPT_TEMPLATE.format(
        old_symbol=old_symbol,
        new_symbol=new_symbol,
        new_color=new_color,
        position=position
    )
