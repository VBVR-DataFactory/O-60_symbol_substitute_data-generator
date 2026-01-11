# Symbol Substitute Task Generator 🔄

A data generator for creating synthetic visual reasoning tasks where a symbol must be substituted with another symbol at a specific position in a sequence. This task tests a model's ability to understand positional reasoning and symbol replacement through visual animation.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/weihangxiao/symbol-substitute-data-genertor.git
cd symbol-substitute-data-genertor

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate tasks
python examples/generate.py --num-samples 50
```

---

## 📋 Task Description

The **Symbol Substitute Task** (Symbol Worlds_SymbolEditing_3) is a visual reasoning task where:

- **Initial State**: A sequence of symbols displayed horizontally
- **Goal**: Replace a specific symbol at a given position with a new symbol
- **Animation**: The old symbol fades out while the new symbol simultaneously fades in (cross-fade effect)
- **Solution**: Exactly **one unique solution** - substitute symbol S at position P with symbol T

### Key Features

- ✅ **Unique Solution**: Only one way to substitute at a specific position with a given symbol
- ✅ **Clear Visual Reasoning**: Animation shows smooth cross-fade transition
- ✅ **Scalable**: 10K+ unique samples with 99% uniqueness
- ✅ **Fast Generation**: No complex solving algorithms required
- ✅ **Short Videos**: ~2.0 seconds per video (well under 10s limit)

---

## 📁 Project Structure

```
symbol-substitute-data-genertor/
├── core/                    # Core utilities (framework code)
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image rendering helpers
│   ├── video_utils.py      # Video generation utilities
│   └── output_writer.py    # File output management
├── src/                     # Task-specific implementation
│   ├── generator.py        # Symbol substitute task generator
│   ├── prompts.py          # Task instruction prompts
│   └── config.py           # Task configuration
├── examples/
│   └── generate.py         # Entry point script
└── data/                    # Generated output
    └── questions/
        └── symbol_substitute_task/
            └── symbol_substitute_0000/
                ├── first_frame.png
                ├── final_frame.png
                ├── prompt.txt
                └── ground_truth.mp4
```

---

## 📦 Output Format

Each generated task produces:

```
data/questions/symbol_substitute_task/{task_id}/
├── first_frame.png          # Initial state: sequence before substitution
├── final_frame.png          # Final state: sequence after substitution
├── prompt.txt               # Task instructions
└── ground_truth.mp4         # Solution animation video (~2.0 seconds)
```

### Output Details

- **first_frame.png**: Shows the initial sequence of symbols (e.g., [●, ▲, ■, ★, ◆])
- **final_frame.png**: Shows the final sequence with symbol substituted (e.g., [●, ♥, ■, ★, ◆])
- **prompt.txt**: Contains instructions specifying which symbol to replace, with what, and at which position (e.g., "Substitute symbol ▲ at position 2 with symbol ♥")
- **ground_truth.mp4**: Animated video showing:
  - Initial sequence held for 0.5s
  - Old and new symbols cross-fading (1.0s)
  - Final sequence held for 0.5s
  - **Total duration: ~2.0 seconds**

---

## ⚙️ Configuration

All task parameters are configured in `src/config.py`:

```python
class TaskConfig(GenerationConfig):
    domain: str = "symbol_substitute"
    image_size: tuple[int, int] = (800, 200)

    # Symbol set selection
    symbol_set: str = "shapes"  # Options: shapes, letters, numbers, mixed

    # Sequence configuration
    min_sequence_length: int = 5   # Minimum symbols in sequence
    max_sequence_length: int = 9   # Maximum symbols in sequence

    # Visual configuration
    symbol_size: int = 60          # Symbol size in pixels

    # Video settings
    generate_videos: bool = True
    video_fps: int = 10
```

### Available Symbol Sets

- **shapes**: ●, ▲, ■, ★, ◆, ♥, ◯, △, □, ☆, ◇, ♦, ▼, ▶, ◀ (15 symbols)
- **letters**: A-Z (26 symbols)
- **numbers**: 0-9 (10 symbols)
- **mixed**: Combination of shapes, letters, and numbers (13 symbols)

---

## 🎬 Generation Algorithm

The generator uses a simple but effective approach:

1. **Sequence Generation**: Randomly select N symbols (5-9) from chosen symbol set without replacement
2. **Substitute Position Selection**: Randomly select substitution position (1 to N)
3. **New Symbol Selection**: Choose a new symbol not in the current sequence
4. **Final Sequence Creation**: Replace old symbol with new symbol at target position
5. **Color Assignment**: Assign distinct colors to each unique symbol for visual clarity
6. **Animation Creation**: Generate smooth animation frames:
   - Cross-fade (10 frames) - Old symbol fades out while new symbol fades in simultaneously
   - Hold frames at start and end (5 frames each)

### Key Features

- ✅ **Guaranteed Uniqueness**: Each task has exactly one solution path
- ✅ **Pure White Background**: RGB(255, 255, 255) for clean visual presentation
- ✅ **Colorful Symbols**: 10 distinct colors assigned consistently
- ✅ **Smooth Animation**: Cross-fade effect with alpha blending
- ✅ **Fast Generation**: ~1 sample/second, no complex algorithms

---

## 📝 Usage Examples

### Generate 100 tasks with shapes (default)

```bash
python examples/generate.py --num-samples 100
```

### Generate 1000 tasks with letters

```bash
python examples/generate.py --num-samples 1000 --symbol-set letters
```

### Generate 500 tasks with custom sequence length

```bash
python examples/generate.py --num-samples 500 --min-length 6 --max-length 9
```

### Generate without videos (faster)

```bash
python examples/generate.py --num-samples 10000 --no-videos
```

### Generate with specific random seed

```bash
python examples/generate.py --num-samples 200 --seed 42
```

### Generate with custom output directory

```bash
python examples/generate.py --num-samples 50 --output data/my_custom_output
```

---

## 🔧 Command Line Options

```bash
python examples/generate.py --help
```

Options:
- `--num-samples`: Number of task samples to generate (required)
- `--symbol-set`: Symbol set to use: shapes, letters, numbers, mixed (default: shapes)
- `--min-length`: Minimum sequence length (default: 5)
- `--max-length`: Maximum sequence length (default: 9)
- `--output`: Output directory (default: `data/questions`)
- `--seed`: Random seed for reproducibility (optional)
- `--no-videos`: Disable video generation (faster)

---

## 📚 Dependencies

See `requirements.txt` for the complete list. Main dependencies:

- `numpy`: Numerical operations
- `Pillow`: Image processing and rendering
- `pydantic`: Configuration management
- `opencv-python`: Video generation

No specialized dependencies required (unlike chess, maze solvers, etc.)

---

## 🎯 Task Characteristics

### Scalability Analysis

- **3x3 Combinations**: ~15 symbols × 5 lengths × avg 7 positions × avg 8 replacement choices = **4000+ base variations**
- **With randomization**: Each sequence is randomly generated, creating **10K+ unique samples**
- **Measured uniqueness**: 99% unique in 100-sample test

### Video Specifications

- **Frame breakdown**:
  - Hold initial: 5 frames (0.5s)
  - Cross-fade: 10 frames (1.0s)
  - Hold final: 5 frames (0.5s)
- **Total**: 20 frames at 10 FPS = **2.0 seconds**
- **Status**: ✅ Well under 10-second limit

### Prompt Specifications

- **Average length**: ~35 words
- **Format**: "Substitute symbol {old} at position {P} with symbol {new}. [Animation description]"
- **Status**: ✅ Well under 200-word limit

---

## 🎨 Visual Design

- **Background**: Pure white (255, 255, 255)
- **Symbol Colors**: 10 distinct colors from a diverse palette
- **Symbol Size**: 60 pixels (configurable)
- **Spacing**: 20 pixels between symbols
- **Centering**: Sequences are centered horizontally and vertically

---

## 📊 Quality Metrics

Based on 100-sample test:

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Uniqueness | 99% | >95% | ✅ Pass |
| Video Length | 2.0s | <10s | ✅ Pass |
| Prompt Length | 35 words | <200 words | ✅ Pass |
| Generation Speed | ~1 sample/sec | N/A | ✅ Fast |
| Solution Uniqueness | 100% | 100% | ✅ Pass |

---

## 🏷️ Task Type

**Symbol Worlds → SymbolEditing → Symbol Worlds_SymbolEditing_3**

- **Task Name**: Substitute Symbol
- **Description**: Replace a symbol at a specific position with a new symbol
- **Reasoning Type**: Visual reasoning through symbol replacement

---

## 📄 License

See `LICENSE` file for details.

---
