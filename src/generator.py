"""Symbol Substitute Task generator - Replace symbol at position."""

import random
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


# Symbol sets
SYMBOL_SETS = {
    "shapes": ["●", "▲", "■", "★", "◆", "♥", "◯", "△", "□", "☆", "◇", "♦", "▼", "▶", "◀"],
    "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "numbers": list("0123456789"),
    "mixed": ["●", "▲", "■", "★", "A", "B", "C", "1", "2", "3", "X", "Y", "Z"]
}

# Colors for symbols (diverse palette)
SYMBOL_COLORS = [
    (220, 60, 60),    # Red
    (60, 60, 220),    # Blue
    (60, 180, 60),    # Green
    (220, 160, 60),   # Orange
    (160, 60, 220),   # Purple
    (60, 180, 180),   # Cyan
    (220, 60, 160),   # Pink
    (100, 150, 60),   # Olive
    (220, 120, 60),   # Coral
    (80, 80, 200),    # Indigo
]


class SymbolSubstituteGenerator(BaseGenerator):
    """Generates symbol substitution tasks."""

    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.renderer = ImageRenderer(image_size=config.image_size)
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(fps=config.video_fps, output_format="mp4")

        # Select symbol set
        self.symbols = SYMBOL_SETS.get(config.symbol_set, SYMBOL_SETS["shapes"])

        # Colors
        self.bg_color = (255, 255, 255)  # Pure white background
        self.border_color = (60, 60, 60)
        self.text_color = (40, 40, 40)

    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one symbol substitution task."""
        # Generate initial sequence
        seq_length = random.randint(self.config.min_sequence_length, self.config.max_sequence_length)

        # Pick symbols without replacement for the sequence
        sequence = random.sample(self.symbols, seq_length)

        # Pick which symbol to substitute (random position)
        substitute_position = random.randint(0, len(sequence) - 1)
        old_symbol = sequence[substitute_position]

        # Pick a new symbol (not in current sequence)
        available_symbols = [s for s in self.symbols if s not in sequence]
        new_symbol = random.choice(available_symbols)

        # Create final sequence (with substituted symbol)
        final_sequence = sequence[:substitute_position] + [new_symbol] + sequence[substitute_position + 1:]

        # Assign colors to symbols (including both old and new)
        all_symbols = set(sequence + [new_symbol])
        color_map = self._create_color_map(list(all_symbols))

        # Render images
        first_image = self._render_sequence(sequence, color_map)
        final_image = self._render_sequence(final_sequence, color_map)

        # Generate video if enabled
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(
                sequence, final_sequence, old_symbol, new_symbol, substitute_position, color_map, task_id
            )

        # Get prompt (1-indexed position for human readability)
        prompt = get_prompt(old_symbol, new_symbol, substitute_position + 1)

        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path
        )

    def _create_color_map(self, all_symbols: List[str]) -> dict:
        """Assign consistent colors to symbols."""
        color_map = {}
        for i, symbol in enumerate(set(all_symbols)):
            color_map[symbol] = SYMBOL_COLORS[i % len(SYMBOL_COLORS)]
        return color_map

    def _render_sequence(self, sequence: List[str], color_map: dict) -> Image.Image:
        """Render a sequence of symbols."""
        width, height = self.config.image_size
        img = Image.new("RGB", (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        if not sequence:
            return img

        # Calculate symbol spacing
        symbol_size = self.config.symbol_size
        spacing = symbol_size + 20
        total_width = len(sequence) * spacing - 20
        start_x = (width - total_width) // 2
        center_y = height // 2

        # Load font - try fonts with good Unicode symbol support
        font_size = symbol_size
        font = self._get_unicode_font(font_size)

        # Draw each symbol
        for i, symbol in enumerate(sequence):
            x = start_x + i * spacing
            self._draw_symbol(draw, symbol, x, center_y, symbol_size, color_map[symbol], font)

        return img

    def _draw_symbol(self, draw: ImageDraw.Draw, symbol: str, x: int, y: int,
                    size: int, color: tuple, font: ImageFont.FreeTypeFont):
        """Draw a single symbol at position (x, y)."""
        # Get text bounding box
        bbox = draw.textbbox((0, 0), symbol, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center the text
        text_x = x - text_width // 2
        text_y = y - text_height // 2

        # Draw the symbol
        draw.text((text_x, text_y), symbol, fill=color, font=font)

    def _get_unicode_font(self, font_size: int) -> ImageFont.FreeTypeFont:
        """Get a font that supports Unicode symbols well."""
        # Try fonts in order of preference (best Unicode symbol support first)
        font_paths = [
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",  # macOS - excellent Unicode support
            "/Library/Fonts/Arial Unicode.ttf",  # macOS alternative location
            "/System/Library/Fonts/Apple Symbols.ttf",  # macOS - good for symbols
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux
            "Arial Unicode MS",  # Cross-platform name
            "DejaVu Sans",  # Cross-platform name
            "Segoe UI Symbol",  # Windows
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, font_size)
            except (OSError, IOError):
                continue

        # Final fallback
        return ImageFont.load_default()

    def _generate_video(self, initial_seq: List[str], final_seq: List[str],
                       old_symbol: str, new_symbol: str, substitute_pos: int, color_map: dict,
                       task_id: str) -> Optional[str]:
        """Generate video showing the substitution animation."""
        import tempfile
        from pathlib import Path

        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"

        frames = self._create_animation_frames(
            initial_seq, final_seq, old_symbol, new_symbol, substitute_pos, color_map
        )
        result = self.video_generator.create_video_from_frames(frames, video_path)
        return str(result) if result else None

    def _create_animation_frames(self, initial_seq: List[str], final_seq: List[str],
                                 old_symbol: str, new_symbol: str, substitute_pos: int, color_map: dict,
                                 hold_frames: int = 5,
                                 crossfade_frames: int = 10) -> List[Image.Image]:
        """Create animation frames for symbol substitution using cross-fade."""
        frames = []

        # Show initial sequence
        frames.extend([self._render_sequence(initial_seq, color_map)] * hold_frames)

        # Phase: Cross-fade from old symbol to new symbol
        for i in range(crossfade_frames):
            progress = (i + 1) / crossfade_frames
            frame = self._render_crossfade_frame(initial_seq, new_symbol, substitute_pos,
                                                 color_map, progress)
            frames.append(frame)

        # Show final sequence
        frames.extend([self._render_sequence(final_seq, color_map)] * hold_frames)

        return frames

    def _render_crossfade_frame(self, sequence: List[str], new_symbol: str,
                                substitute_pos: int, color_map: dict,
                                progress: float) -> Image.Image:
        """Render frame with cross-fade between old and new symbol."""
        width, height = self.config.image_size
        symbol_size = self.config.symbol_size
        spacing = symbol_size + 20

        # Create base image
        img = Image.new('RGB', (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # Calculate layout
        total_width = len(sequence) * spacing - 20
        start_x = (width - total_width) // 2
        center_y = height // 2

        # Load font - try fonts with good Unicode symbol support
        font_size = symbol_size
        font = self._get_unicode_font(font_size)

        # Draw all symbols
        for i, symbol in enumerate(sequence):
            x = start_x + i * spacing
            if i == substitute_pos:
                # Draw cross-fading symbols
                old_alpha = int(255 * (1 - progress))
                new_alpha = int(255 * progress)

                # Create overlay for alpha blending
                overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)

                # Get text bounding box for both symbols (for centering)
                old_bbox = overlay_draw.textbbox((0, 0), symbol, font=font)
                old_text_width = old_bbox[2] - old_bbox[0]
                old_text_height = old_bbox[3] - old_bbox[1]
                old_text_x = x - old_text_width // 2
                old_text_y = center_y - old_text_height // 2

                new_bbox = overlay_draw.textbbox((0, 0), new_symbol, font=font)
                new_text_width = new_bbox[2] - new_bbox[0]
                new_text_height = new_bbox[3] - new_bbox[1]
                new_text_x = x - new_text_width // 2
                new_text_y = center_y - new_text_height // 2

                # Draw old symbol with fading out alpha
                old_color = color_map[symbol]
                old_rgba_color = (*old_color, old_alpha)
                overlay_draw.text((old_text_x, old_text_y), symbol, fill=old_rgba_color, font=font)

                # Draw new symbol with fading in alpha
                new_color = color_map[new_symbol]
                new_rgba_color = (*new_color, new_alpha)
                overlay_draw.text((new_text_x, new_text_y), new_symbol, fill=new_rgba_color, font=font)

                # Composite
                img = img.convert('RGBA')
                img = Image.alpha_composite(img, overlay)
                img = img.convert('RGB')
            else:
                # Draw normal symbol
                self._draw_symbol(draw, symbol, x, center_y, symbol_size, color_map[symbol], font)

        return img
