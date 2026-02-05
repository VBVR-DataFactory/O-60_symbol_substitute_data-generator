"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   SYMBOL SUBSTITUTE TASK CONFIGURATION                        ║
║                                                                               ║
║  Configuration for Symbol Worlds_SymbolEditing_3:                            ║
║  Substitute a symbol at a specific position with a new symbol.               ║
║                                                                               ║
║  Task: Replace symbol S at position P with new symbol T                      ║
║  Result: [A, B, S, C, ...] → [A, B, T, C, ...]                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


# ══════════════════════════════════════════════════════════════════════════════
#  COLOR DEFINITIONS (Scaling Feature)
# ══════════════════════════════════════════════════════════════════════════════

# Rainbow 7 colors - used for symbols that will be substituted (easy to reference in prompts)
RAINBOW_COLORS = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'indigo': (75, 0, 130),
    'violet': (238, 130, 238),
}

# Extended 20 colors - used for all symbols in sequence
ALL_COLORS = {
    # Rainbow 7 (must be first for easy substitution targeting)
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'indigo': (75, 0, 130),
    'violet': (238, 130, 238),
    # Extended 13 colors
    'pink': (255, 192, 203),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'brown': (165, 42, 42),
    'gray': (128, 128, 128),
    'olive': (128, 128, 0),
    'teal': (0, 128, 128),
    'navy': (0, 0, 128),
    'maroon': (128, 0, 0),
    'lime': (50, 205, 50),
    'aqua': (127, 255, 212),
    'silver': (192, 192, 192),
    'coral': (255, 127, 80),
}

# Symbol English names for prompts
SYMBOL_NAMES = {
    '●': 'circle',
    '▲': 'triangle',
    '■': 'square',
    '★': 'star',
    '◆': 'diamond',
    '♥': 'heart',
    '◯': 'hollow circle',
    '△': 'hollow triangle',
    '□': 'hollow square',
    '☆': 'hollow star',
    '◇': 'hollow diamond',
    '♦': 'filled diamond',
    '▼': 'down triangle',
    '▶': 'right triangle',
    '◀': 'left triangle',
}


class TaskConfig(GenerationConfig):
    """
    Symbol Substitute Task configuration.

    Task: Replace a symbol at a specific position with a new symbol.

    Inherited from GenerationConfig:
        - num_samples: int          # Number of samples to generate
        - domain: str               # Task domain name
        - difficulty: Optional[str] # Difficulty level
        - random_seed: Optional[int] # For reproducibility
        - output_dir: Path          # Where to save outputs
        - image_size: tuple[int, int] # Image dimensions
    """

    # ══════════════════════════════════════════════════════════════════════════
    #  OVERRIDE DEFAULTS
    # ══════════════════════════════════════════════════════════════════════════

    domain: str = Field(default="symbol_substitute")
    image_size: tuple[int, int] = Field(default=(1024, 1024))  # 1:1 aspect ratio

    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════

    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )

    video_fps: int = Field(
        default=16,
        description="Video frame rate"
    )

    # ══════════════════════════════════════════════════════════════════════════
    #  SYMBOL SUBSTITUTE TASK SETTINGS
    # ══════════════════════════════════════════════════════════════════════════

    min_sequence_length: int = Field(
        default=5,
        ge=4,
        le=9,
        description="Minimum number of symbols in sequence"
    )

    max_sequence_length: int = Field(
        default=9,
        ge=5,
        le=12,
        description="Maximum number of symbols in sequence"
    )

    symbol_set: str = Field(
        default="shapes",
        description="Symbol set to use: 'shapes', 'letters', 'numbers', 'mixed'"
    )

    symbol_size: int = Field(
        default=85,
        ge=40,
        le=120,
        description="Size of each symbol in pixels (adjusted for 1024x1024 resolution)"
    )
