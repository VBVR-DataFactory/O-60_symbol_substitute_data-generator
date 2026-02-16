# O-60: Symbol Substitute Data Generator

Generates synthetic symbol sequence substitution tasks. The goal is to substitute a symbol at a specific position with a new symbol, with the animation showing the old symbol fading out completely and the new symbol gradually fading in at the same position.

Each sample pairs a **task** (first frame + prompt describing what needs to happen) with its **ground truth solution** (final frame showing the result + video demonstrating how to achieve it). This structure enables both model evaluation and training.

---

## 📌 Basic Information

| Property | Value |
|----------|-------|
| **Task ID** | O-60 |
| **Task** | Symbol Substitute |
| **Category** | Transformation |
| **Resolution** | 1024×1024 px |
| **FPS** | 16 fps |
| **Duration** | ~2-3 seconds |
| **Output** | PNG images + MP4 video |

---

## 🚀 Usage

### Installation

```bash
# Clone the repository
git clone https://github.com/Jiaqi-Gong/Gong_VBVR_Data.git
cd Gong_VBVR_Data/O-60_symbol_substitute_data-generator

# Install dependencies
pip install -r requirements.txt
```

### Generate Data

```bash
# Generate 100 samples
python examples/generate.py --num-samples 100

# Generate with specific seed
python examples/generate.py --num-samples 100 --seed 42

# Generate without videos
python examples/generate.py --num-samples 100 --no-videos

# Custom output directory
python examples/generate.py --num-samples 100 --output data/my_output
```

### Command-Line Options

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--num-samples` | int | Number of samples to generate | Required |
| `--seed` | int | Random seed for reproducibility | Random |
| `--output` | str | Output directory | data/questions |
| `--no-videos` | flag | Skip video generation | False |

---

## 📖 Task Example

### Prompt

```
Substitute □ at position 7 with a orange ●. The animation shows the old symbol fading out completely, then the new symbol gradually fading in at the same position.
```
### Visual

<table>
<tr>
  <td align="center"><img src="samples/O-60_first_0.png" width="250"/></td>
  <td align="center"><img src="samples/O-60_video_0.gif" width="320"/></td>
  <td align="center"><img src="samples/O-60_final_0.png" width="250"/></td>
</tr>
<tr>
  <td align="center"><b>Initial Frame</b><br/>Symbol sequence with symbol to replace</td>
  <td align="center"><b>Animation</b><br/>Old symbol fading out, new symbol fading in</td>
  <td align="center"><b>Final Frame</b><br/>Sequence after substitution</td>
</tr>
</table>

---

## 📖 Task Description

### Objective

Substitute a symbol at a specific position with a new symbol, with the animation showing the old symbol fading out completely and the new symbol gradually fading in at the same position.

### Task Setup

- **Sequence Length**: 5-9 symbols
- **Symbol Set**: Shapes (circles, triangles, squares, stars, diamonds, hearts, etc.)
- **Symbol Colors**: 20 distinct colors (rainbow 7 + extended 13)
- **Old Symbol**: Symbol at target position to be replaced
- **New Symbol**: Rainbow-colored symbol (red, orange, yellow, green, blue, indigo, violet)
- **Position**: 1-indexed position of symbol to substitute
- **Symbol Size**: 85 pixels (adjustable 40-120)
- **Animation**: Fade out old symbol, fade in new symbol at same position

### Key Features

- **Sequence manipulation**: Tests ability to understand sequence substitution operations
- **Position awareness**: Requires identifying specific position in sequence
- **Visual animation**: Clear fade-out and fade-in animation
- **Color coding**: New symbols use rainbow colors for easy identification
- **Symbol variety**: Multiple symbol types and colors for diversity
- **Smooth transitions**: Smooth fading animations

---

## 📦 Data Format

```
data/questions/symbol_substitute_task/symbol_substitute_00000000/
├── first_frame.png      # Initial state (sequence with symbol to replace)
├── final_frame.png      # Goal state (sequence after substitution)
├── prompt.txt           # Task instructions
├── ground_truth.mp4     # Solution video (16 fps)
└── question_metadata.json # Task metadata
```


**File specifications**: Images are 1024×1024 PNG. Videos are MP4 at 16 fps, approximately 2-3 seconds long.

---

## 🏷️ Tags

`symbol-substitute` `sequence-manipulation` `symbol-editing` `abstraction` `position-reasoning` `visual-animation`

---
