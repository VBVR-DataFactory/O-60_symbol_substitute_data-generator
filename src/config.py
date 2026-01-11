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
    image_size: tuple[int, int] = Field(default=(800, 200))

    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════

    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )

    video_fps: int = Field(
        default=10,
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
        default=60,
        ge=40,
        le=100,
        description="Size of each symbol in pixels"
    )
