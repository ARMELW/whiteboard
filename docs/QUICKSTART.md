# Quick Start: Per-Slide Configuration

This guide gets you started with per-slide customization in 2 minutes.

## Step 1: Create a Configuration File

Create a file named `my_slides.json`:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "skip_rate": 10
    },
    {
      "index": 1,
      "duration": 3,
      "skip_rate": 15
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 1.0,
      "pause_before": 2.0
    }
  ]
}
```

## Step 2: Run the Command

```bash
python whiteboard_animator.py slide1.png slide2.png --config my_slides.json
```

## That's It!

Your video will have:
- Slide 1: Drawn at speed 10, displayed for 2 seconds
- **2 second pause**
- Fade transition (1 second)
- Slide 2: Drawn at speed 15, displayed for 3 seconds

## What You Can Customize

### Per-Slide Settings
- `duration` - How long the slide displays (seconds)
- `skip_rate` - Drawing speed (higher = faster)

### Per-Transition Settings
- `type` - Transition effect: `none`, `fade`, `wipe`, `push_left`, `push_right`, `iris`
- `duration` - Length of transition (seconds)
- `pause_before` - Wait time before transition (seconds) ⭐

## Need More Help?

- See [CONFIG_FORMAT.md](CONFIG_FORMAT.md) for complete reference
- See [example_config.json](example_config.json) for ready-to-use template
- See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for feature overview

## Examples

### Fast Introduction, Slow Explanation
```json
{
  "slides": [
    {"index": 0, "duration": 1, "skip_rate": 20},
    {"index": 1, "duration": 5, "skip_rate": 5}
  ]
}
```

### Dramatic Pauses Between Slides
```json
{
  "transitions": [
    {"after_slide": 0, "pause_before": 3.0},
    {"after_slide": 1, "pause_before": 2.5}
  ]
}
```

### Different Transitions
```json
{
  "transitions": [
    {"after_slide": 0, "type": "fade", "duration": 0.5},
    {"after_slide": 1, "type": "iris", "duration": 1.2},
    {"after_slide": 2, "type": "wipe", "duration": 0.8}
  ]
}
```

## Common Use Cases

**Educational Video:**
- Slow drawing for diagrams
- Long display time for complex slides
- Pauses to let information sink in

**Marketing Presentation:**
- Fast drawing for impact
- Short display time to maintain pace
- Dynamic transitions

**Tutorial:**
- Medium drawing speed
- Varied display times based on complexity
- Clear transitions between topics
