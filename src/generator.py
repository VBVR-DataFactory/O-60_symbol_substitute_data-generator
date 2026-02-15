"""Symbol Substitute Task generator - Replace symbol at position."""

import random
from pathlib import Path
import tempfile
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig, ALL_COLORS, RAINBOW_COLORS
from .prompts import get_prompt


# Symbol sets
SYMBOL_SETS = {
    "shapes": ["●", "▲", "■", "★", "◆", "♥", "◯", "△", "□", "☆", "◇", "♦", "▼", "▶", "◀"],
    "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "numbers": list("0123456789"),
    "mixed": ["●", "▲", "■", "★", "A", "B", "C", "1", "2", "3", "X", "Y", "Z"]
}


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
        
        # Color names list for random selection
        self.all_color_names = list(ALL_COLORS.keys())
        self.rainbow_color_names = list(RAINBOW_COLORS.keys())

    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one symbol substitution task with colored symbols."""
        # Generate initial sequence (now with colors, allowing duplicate symbol types)
        seq_length = random.randint(self.config.min_sequence_length, self.config.max_sequence_length)
        
        # Pick which position to substitute FIRST (ensures equal probability for all positions)
        substitute_position = random.randint(0, seq_length - 1)
        
        # Generate sequence: each position is (symbol_type, color_name)
        # The position to be substituted MUST use a rainbow color (for prompt clarity)
        sequence = []
        for i in range(seq_length):
            symbol_type = random.choice(self.symbols)
            if i == substitute_position:
                # This is the position to be substituted - use rainbow color
                color_name = random.choice(self.rainbow_color_names)
            else:
                # Other positions can use any of the 20 colors
                color_name = random.choice(self.all_color_names)
            sequence.append((symbol_type, color_name))
        
        old_symbol, old_color = sequence[substitute_position]
        
        # Pick a new symbol (can be any type, but color must be rainbow for prompt clarity)
        new_symbol = random.choice(self.symbols)
        new_color = random.choice(self.rainbow_color_names)  # Only rainbow colors for new symbol
        
        # Create final sequence (with substituted symbol)
        final_sequence = sequence.copy()
        final_sequence[substitute_position] = (new_symbol, new_color)
        
        # Generate animation frames first to ensure alignment
        frames = self._create_animation_frames(sequence, final_sequence, old_symbol, old_color, new_symbol, new_color, substitute_position)
        
        # Extract first and final images from frames
        first_image = frames[0]
        final_image = frames[-1]
        
        # Generate video if enabled
        video_path = None
        if self.config.generate_videos and self.video_generator:
            temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
            temp_dir.mkdir(parents=True, exist_ok=True)
            video_path = temp_dir / f"{task_id}_ground_truth.mp4"
            result = self.video_generator.create_video_from_frames(frames, video_path)
            video_path = str(result) if result else None
        
        # Get prompt (1-indexed position, old symbol identified by position, new symbol with color)
        prompt = get_prompt(old_symbol, new_symbol, new_color, substitute_position + 1)

        # Build object-centric metadata
        optimized_task_data = self._build_objects_metadata(
            initial_sequence=sequence,
            final_sequence=final_sequence,
            substitute_position=substitute_position,
            old_symbol=old_symbol,
            old_color=old_color,
            new_symbol=new_symbol,
            new_color=new_color
        )
        
        # Build metadata
        metadata = self._build_metadata(task_id, optimized_task_data)
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path,
            metadata=metadata
        )

    def _render_sequence(self, sequence: List[Tuple[str, str]]) -> Image.Image:
        """Render a sequence of colored symbols (centered dynamically)."""
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
        for i, (symbol_type, color_name) in enumerate(sequence):
            x = start_x + i * spacing
            rgb_color = ALL_COLORS[color_name]
            self._draw_symbol(draw, symbol_type, x, center_y, symbol_size, rgb_color, font)

        return img

    def _render_sequence_fixed(self, sequence: List[Tuple[str, str]], fixed_start_x: int) -> Image.Image:
        """Render a sequence of colored symbols using a fixed starting position (prevents jumping)."""
        width, height = self.config.image_size
        img = Image.new("RGB", (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        if not sequence:
            return img

        # Calculate symbol spacing
        symbol_size = self.config.symbol_size
        spacing = symbol_size + 20
        center_y = height // 2

        # Load font - try fonts with good Unicode symbol support
        font_size = symbol_size
        font = self._get_unicode_font(font_size)

        # Draw each symbol using fixed start position
        for i, (symbol_type, color_name) in enumerate(sequence):
            x = fixed_start_x + i * spacing
            rgb_color = ALL_COLORS[color_name]
            self._draw_symbol(draw, symbol_type, x, center_y, symbol_size, rgb_color, font)

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

    def _generate_video(self, initial_seq: List[Tuple[str, str]], final_seq: List[Tuple[str, str]],
                       old_symbol: str, old_color: str, new_symbol: str, new_color: str,
                       substitute_pos: int, task_id: str) -> Optional[str]:
        """Generate video showing the substitution animation."""
        import tempfile
        from pathlib import Path

        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"

        frames = self._create_animation_frames(
            initial_seq, final_seq, old_symbol, old_color, new_symbol, new_color, substitute_pos
        )
        result = self.video_generator.create_video_from_frames(frames, video_path)
        return str(result) if result else None

    def _create_animation_frames(self, initial_seq: List[Tuple[str, str]], final_seq: List[Tuple[str, str]],
                                 old_symbol: str, old_color: str, new_symbol: str, new_color: str,
                                 substitute_pos: int,
                                 hold_frames: int = 5,
                                 fadeout_frames: int = 6,
                                 fadein_frames: int = 6) -> List[Image.Image]:
        """Create animation frames for symbol substitution: fade-out then fade-in (clean process)."""
        frames = []
        
        # Calculate fixed center position (prevents any jumping)
        width, height = self.config.image_size
        symbol_size = self.config.symbol_size
        spacing = symbol_size + 20
        total_width = len(initial_seq) * spacing - 20
        fixed_start_x = (width - total_width) // 2  # Fixed for entire animation

        # Show initial sequence (using fixed position)
        frames.extend([self._render_sequence_fixed(initial_seq, fixed_start_x)] * hold_frames)

        # Phase 1: Fade out old symbol (only the target symbol disappears)
        for i in range(fadeout_frames):
            progress = (i + 1) / fadeout_frames
            frame = self._render_fadeout_frame(initial_seq, substitute_pos, progress, fixed_start_x)
            frames.append(frame)

        # Phase 2: Fade in new symbol (new symbol gradually appears)
        for i in range(fadein_frames):
            progress = (i + 1) / fadein_frames
            frame = self._render_fadein_frame(initial_seq, new_symbol, new_color, substitute_pos, 
                                             progress, fixed_start_x)
            frames.append(frame)

        # Show final sequence (using fixed position)
        frames.extend([self._render_sequence_fixed(final_seq, fixed_start_x)] * hold_frames)

        return frames

    def _render_fadeout_frame(self, sequence: List[Tuple[str, str]], substitute_pos: int,
                              progress: float, fixed_start_x: int) -> Image.Image:
        """Render frame with old symbol fading out (only target symbol changes)."""
        width, height = self.config.image_size
        symbol_size = self.config.symbol_size
        spacing = symbol_size + 20
        center_y = height // 2

        # Create base image
        img = Image.new('RGB', (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # Load font
        font_size = symbol_size
        font = self._get_unicode_font(font_size)

        # STEP 1: Draw all normal symbols FIRST (not the fading one)
        for i, (symbol_type, color_name) in enumerate(sequence):
            if i != substitute_pos:
                x = fixed_start_x + i * spacing
                rgb_color = ALL_COLORS[color_name]
                self._draw_symbol(draw, symbol_type, x, center_y, symbol_size, rgb_color, font)

        # STEP 2: Now handle the fading symbol with alpha composite
        if substitute_pos < len(sequence):
            symbol_type, color_name = sequence[substitute_pos]
            x = fixed_start_x + substitute_pos * spacing
            alpha = int(255 * (1 - progress))  # 255 -> 0
            
            # Create overlay for alpha blending
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # Get text bounding box for centering
            bbox = overlay_draw.textbbox((0, 0), symbol_type, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x - text_width // 2
            text_y = center_y - text_height // 2

            # Draw old symbol with fading alpha
            rgb_color = ALL_COLORS[color_name]
            rgba_color = (*rgb_color, alpha)
            overlay_draw.text((text_x, text_y), symbol_type, fill=rgba_color, font=font)

            # Composite
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            img = img.convert('RGB')

        return img

    def _render_fadein_frame(self, sequence: List[Tuple[str, str]], new_symbol: str, new_color: str,
                            substitute_pos: int, progress: float, fixed_start_x: int) -> Image.Image:
        """Render frame with new symbol fading in (only target symbol changes)."""
        width, height = self.config.image_size
        symbol_size = self.config.symbol_size
        spacing = symbol_size + 20
        center_y = height // 2

        # Create base image
        img = Image.new('RGB', (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # Load font
        font_size = symbol_size
        font = self._get_unicode_font(font_size)

        # STEP 1: Draw all normal symbols FIRST (not the position being substituted)
        for i, (symbol_type, color_name) in enumerate(sequence):
            if i != substitute_pos:
                x = fixed_start_x + i * spacing
                rgb_color = ALL_COLORS[color_name]
                self._draw_symbol(draw, symbol_type, x, center_y, symbol_size, rgb_color, font)

        # STEP 2: Now handle the fading-in new symbol with alpha composite
        x = fixed_start_x + substitute_pos * spacing
        alpha = int(255 * progress)  # 0 -> 255
        
        # Create overlay for alpha blending
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        # Get text bounding box for centering
        bbox = overlay_draw.textbbox((0, 0), new_symbol, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x - text_width // 2
        text_y = center_y - text_height // 2

        # Draw new symbol with fading in alpha
        rgb_color = ALL_COLORS[new_color]
        rgba_color = (*rgb_color, alpha)
        overlay_draw.text((text_x, text_y), new_symbol, fill=rgba_color, font=font)

        # Composite
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')

        return img

    # ══════════════════════════════════════════════════════════════════════════
    #  METADATA BUILDING
    # ══════════════════════════════════════════════════════════════════════════
    
    def _build_objects_metadata(
        self,
        initial_sequence: List[Tuple[str, str]],
        final_sequence: List[Tuple[str, str]],
        substitute_position: int,
        old_symbol: str,
        old_color: str,
        new_symbol: str,
        new_color: str
    ) -> dict:
        """
        Build object-centric metadata for symbol substitute task.
        
        Args:
            initial_sequence: Initial sequence of (symbol, color_name) tuples
            final_sequence: Final sequence after substitution
            substitute_position: 0-indexed position of substituted symbol
            old_symbol: Original symbol that was replaced
            old_color: Original color name
            new_symbol: New symbol that replaced the old one
            new_color: New color name
            
        Returns:
            Dictionary with object-centric metadata
        """
        from typing import Dict, Any
        from .config import ALL_COLORS
        
        # Create objects for each symbol in the sequence
        objects = []
        for i, (symbol, color_name) in enumerate(initial_sequence):
            color_rgb = ALL_COLORS.get(color_name, (0, 0, 0))
            is_substituted = (i == substitute_position)
            
            obj = {
                "symbol": f"symbol_{i}",
                "index": i,
                "initial_symbol": symbol,
                "initial_color_name": color_name,
                "initial_color_rgb": list(color_rgb),
                "is_substituted": is_substituted
            }
            
            # Add final symbol/color information
            if is_substituted:
                obj["final_symbol"] = new_symbol
                obj["final_color_name"] = new_color
                obj["final_color_rgb"] = list(ALL_COLORS.get(new_color, (0, 0, 0)))
            else:
                obj["final_symbol"] = symbol
                obj["final_color_name"] = color_name
                obj["final_color_rgb"] = list(color_rgb)
            
            objects.append(obj)
        
        # Build task-specific metadata
        optimized_task_data = {
            "sequence_length": len(initial_sequence),
            "substitute_position": substitute_position,
            "old_symbol": old_symbol,
            "old_color_name": old_color,
            "old_color_rgb": list(ALL_COLORS.get(old_color, (0, 0, 0))),
            "new_symbol": new_symbol,
            "new_color_name": new_color,
            "new_color_rgb": list(ALL_COLORS.get(new_color, (0, 0, 0))),
            "objects": objects
        }
        
        return optimized_task_data
