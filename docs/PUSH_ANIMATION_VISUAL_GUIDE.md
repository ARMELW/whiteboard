# Push Animation - Visual Comparison

## Feature Overview

The push animation feature adds interactive hand-based entrance animations where a visible hand appears to push elements onto the scene.

**Recent Improvements (v2):**
- ✅ Added smooth easing (ease_out) for natural deceleration
- ✅ Increased hand overlap (70%) for better visibility and pushing effect
- ✅ Improved hand positioning to move dynamically with elements
- ✅ More realistic physics-based motion

## Animation Types

### 1. Push From Left (`push_from_left`)

**Behavior:**
- Element slides in from left side of screen
- Hand positioned at left edge of element
- Hand moves with element as it slides in

**Use Cases:**
- Introducing side panels
- Adding elements from left menu area
- Sequential left-to-right reveals

**Configuration:**
```json
{
  "entrance_animation": {
    "type": "push_from_left",
    "duration": 1.5
  }
}
```

---

### 2. Push From Right (`push_from_right`)

**Behavior:**
- Element slides in from right side of screen
- Hand positioned at right edge of element
- Hand moves with element as it slides in

**Use Cases:**
- Adding contextual information panels
- Right-to-left content flow
- Sidebar reveals

**Configuration:**
```json
{
  "entrance_animation": {
    "type": "push_from_right",
    "duration": 1.5
  }
}
```

---

### 3. Push From Top (`push_from_top`)

**Behavior:**
- Element slides in from top of screen
- Hand positioned at top edge of element
- Hand moves with element as it slides down

**Use Cases:**
- Adding headers or titles
- Top navigation elements
- Dropdown content reveals

**Configuration:**
```json
{
  "entrance_animation": {
    "type": "push_from_top",
    "duration": 1.5
  }
}
```

---

### 4. Push From Bottom (`push_from_bottom`)

**Behavior:**
- Element slides in from bottom of screen
- Hand positioned at bottom edge of element
- Hand moves with element as it slides up

**Use Cases:**
- Footer elements
- Call-to-action buttons
- Bottom navigation reveals

**Configuration:**
```json
{
  "entrance_animation": {
    "type": "push_from_bottom",
    "duration": 1.5
  }
}
```

---

## Comparison with Other Animations

### Push vs Slide Animations

| Feature | Push Animation | Standard Slide Animation |
|---------|---------------|--------------------------|
| Hand Visible | ✅ Yes | ❌ No |
| Interactive Feel | ✅ High | ⚠️ Medium |
| Use Case | Product demos, tutorials | General transitions |
| Configuration Complexity | Same | Same |
| Performance | Same | Same |

### Push vs Fade Animations

| Feature | Push Animation | Fade Animation |
|---------|---------------|----------------|
| Movement | ✅ Yes | ❌ No |
| Hand Visible | ✅ Yes | ❌ No |
| Subtlety | ⚠️ Medium | ✅ High |
| Attention-grabbing | ✅ High | ⚠️ Low |

## Animation Timeline

```
Frame 0    Frame 15   Frame 30   (30 FPS, 1.0s duration)
│          │          │
├──────────┼──────────┤
│          │          │
│    ✋🖼️  │   ✋🖼️   │    🖼️     (push_from_left with ease_out)
│          │          │
└──────────┴──────────┘

Element and hand start off-screen → 
Move together with smooth deceleration → 
Element reaches final position (hand fades)

Note: Animation uses ease_out easing for natural deceleration -
starts fast and gradually slows down for realistic pushing motion.
```

## Example Scenarios

### Scenario 1: Product Showcase

```json
{
  "slides": [{
    "layers": [
      {"image_path": "background.jpg", "mode": "draw"},
      {
        "image_path": "laptop.png",
        "position": {"x": 200, "y": 150},
        "entrance_animation": {
          "type": "push_from_left",
          "duration": 1.5
        }
      }
    ]
  }]
}
```

**Result:** Background is drawn, then laptop is pushed in from left with visible hand

---

### Scenario 2: Multi-Direction Demo

```json
{
  "slides": [{
    "layers": [
      {"image_path": "background.jpg", "mode": "draw"},
      {
        "image_path": "top.png",
        "entrance_animation": {"type": "push_from_top"}
      },
      {
        "image_path": "bottom.png",
        "entrance_animation": {"type": "push_from_bottom"}
      },
      {
        "image_path": "left.png",
        "entrance_animation": {"type": "push_from_left"}
      },
      {
        "image_path": "right.png",
        "entrance_animation": {"type": "push_from_right"}
      }
    ]
  }]
}
```

**Result:** Background drawn, then 4 elements pushed in from all directions sequentially

---

## Visual Design Considerations

### Hand Position

The hand is positioned with increased overlap (70% for left/top, 20% offset for right/bottom) to create a more visible and natural pushing effect:

```
push_from_left (70% overlap):
┌──────────┐
│   Hand   │────────┐
└──────────┘        │
      └─────────────┼─────┐
                    │ Obj │
                    └─────┘

push_from_right (20% offset):
        ┌──────────┐
    ┌───┤   Hand   │
    │   └──────────┘
┌───┼─────┘
│Obj│
└───┘
```

The increased overlap creates a stronger "pushing" appearance where the hand is clearly behind and pushing the element.

### Animation Easing

All push animations use **ease_out** easing, which means:
- Fast initial movement (like a real push)
- Gradual deceleration as element reaches position
- Natural, realistic motion that mimics physics

### Duration Guidelines

- **Short (0.5-0.8s)**: Quick, snappy animations
- **Medium (1.0-1.5s)**: Recommended, natural feel
- **Long (1.5-2.5s)**: Dramatic, attention-grabbing

### Layering

Ensure proper z-index ordering:

```
z_index: 1 → Background (drawn first)
z_index: 2 → First pushed element
z_index: 3 → Second pushed element
z_index: 4 → Third pushed element
```

## Testing Your Animations

1. **Start Simple**: Test with one push animation first
2. **Adjust Duration**: Try different durations (1.0-2.0s)
3. **Check Position**: Ensure element position makes sense for push direction
4. **Verify Scale**: Adjust object scale for visual balance
5. **Test Multiple**: Try combining multiple push animations

## Troubleshooting

### Hand Not Visible
- Check that layer mode is set to `"static"`
- Verify hand image exists in `data/images/drawing-hand.png`
- Ensure z-index allows hand to be visible

### Animation Too Fast/Slow
- Adjust `duration` parameter (1.0-2.0s recommended)
- Check frame rate setting (default: 30 FPS)

### Element Position Wrong
- Verify `position` coordinates are correct
- Check that element scale is appropriate
- Ensure element size fits within frame

## Reference

See the reference image from the original issue showing a hand pushing a laptop onto a table - this is exactly what the feature accomplishes.

## Next Steps

1. Try the basic example: `examples/push_animation_example.json`
2. View all directions: `examples/push_all_directions.json`
3. Check product demo: `examples/push_product_demo.json`
4. Read full guide: `PUSH_ANIMATION_GUIDE.md`
5. Quick reference: `PUSH_ANIMATION_QUICKSTART.md`
