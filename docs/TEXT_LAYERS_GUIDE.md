# Guide des Couches de Texte / Text Layers Guide

## Vue d'ensemble / Overview

🎉 **Nouvelle fonctionnalité !** / **New Feature!**

Whiteboard-It supporte maintenant les **couches de texte dynamiques** avec animation de handwriting ! Plus besoin de créer des images de texte - le texte est généré à la volée et animé comme s'il était écrit à la main.

Whiteboard-It now supports **dynamic text layers** with handwriting animation! No need to create text images - text is generated on-the-fly and animated as if written by hand.

## Fonctionnalités / Features

✅ **Texte dynamique** / **Dynamic text** - Généré automatiquement, pas besoin d'images  
✅ **Multi-ligne** / **Multi-line** - Support complet avec `\n` pour les sauts de ligne  
✅ **Écriture ligne par ligne** / **Line-by-line typing** - Écrit chaque ligne complètement avant la suivante  
✅ **Polices personnalisées** / **Custom fonts** - N'importe quelle police système  
✅ **Styles** / **Styles** - Normal, bold, italic, bold_italic  
✅ **Couleurs** / **Colors** - RGB, hex, noms de couleurs  
✅ **Animation handwriting** - Écrit comme avec un stylo / Written like with a pen  
✅ **Tous les modes** / **All modes** - draw, eraser, static  
✅ **Animations d'entrée/sortie** - fade_in, slide_in, zoom_in, etc.  
✅ **Positionnement précis** / **Precise positioning** - x, y, alignment  

## Configuration de base / Basic Configuration

### Exemple simple / Simple Example

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 6,
      "layers": [
        {
          "type": "text",
          "z_index": 1,
          "skip_rate": 12,
          "text_config": {
            "text": "Bonjour!\nCeci est un texte",
            "font": "DejaVuSans",
            "size": 48,
            "color": [0, 0, 255],
            "style": "bold",
            "align": "center"
          }
        }
      ]
    }
  ]
}
```

### Options de configuration / Configuration Options

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `text` | string | **Requis** | Le texte à afficher (utilisez `\n` pour sauts de ligne) |
| `font` | string | "Arial" | Nom de la police (système) |
| `size` | int | 32 | Taille en pixels |
| `color` | RGB/hex | `[0, 0, 0]` | Couleur du texte |
| `style` | string | "normal" | "normal", "bold", "italic", "bold_italic" |
| `line_height` | float | 1.2 | Espacement des lignes (multiplicateur) |
| `align` | string | "left" | "left", "center", "right" |
| `position` | dict | null | Position absolue `{x, y}` (optionnel) |

### ⚠️ Important: Positionnement Absolu / Absolute Positioning

**Depuis la correction du positionnement absolu:**

Lorsque `position` est spécifié avec `{x, y}`, ces coordonnées représentent **toujours le coin supérieur gauche** de la zone de texte, **indépendamment de la valeur de `align`**.

L'attribut `align` contrôle uniquement comment le texte est aligné *à l'intérieur* de sa zone de rendu, mais n'affecte pas le point d'ancrage de la position.

When `position` is specified with `{x, y}`, these coordinates always represent the **top-left corner** of the text bounding box, regardless of the `align` value.

The `align` attribute only controls how the text is aligned *within* its rendering area, but does not affect the position anchor point.

**Exemple:**
```json
{
  "text": "Mon texte",
  "align": "center",
  "position": {"x": 100, "y": 200}
}
```

- Le texte démarrera à la position x=100 (pas centré sur x=100).
- The text will start at position x=100 (not centered on x=100).

## Exemples / Examples

### 1. Texte centré avec style / Centered Styled Text

```json
{
  "type": "text",
  "z_index": 1,
  "skip_rate": 10,
  "text_config": {
    "text": "Titre Principal",
    "font": "DejaVuSans",
    "size": 64,
    "color": "#0066CC",
    "style": "bold",
    "align": "center"
  }
}
```

### 2. Texte multi-ligne aligné à gauche / Multi-line Left-aligned Text

```json
{
  "type": "text",
  "z_index": 2,
  "skip_rate": 15,
  "text_config": {
    "text": "• Point 1\n• Point 2\n• Point 3",
    "font": "DejaVuSans",
    "size": 36,
    "color": [51, 51, 51],
    "line_height": 1.6,
    "align": "left",
    "position": {"x": 100, "y": 200}
  }
}
```

### 3. Texte statique (sans animation) / Static Text (No Animation)

```json
{
  "type": "text",
  "z_index": 3,
  "skip_rate": 20,
  "mode": "static",
  "text_config": {
    "text": "Footer Text",
    "font": "DejaVuSans",
    "size": 24,
    "color": "#666666",
    "style": "italic",
    "align": "center",
    "position": {"x": 0, "y": 520}
  },
  "entrance_animation": {
    "type": "fade_in",
    "duration": 0.8
  }
}
```

### 4. Mélanger texte et images / Mix Text and Images

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1,
          "skip_rate": 8
        },
        {
          "type": "text",
          "z_index": 2,
          "skip_rate": 15,
          "text_config": {
            "text": "Texte sur image",
            "size": 56,
            "color": "#FFFFFF",
            "style": "bold",
            "align": "center"
          }
        }
      ]
    }
  ]
}
```

## Utilisation / Usage

### Ligne de commande / Command Line

```bash
# Avec un placeholder blanc pour texte seul
python whiteboard_animator.py placeholder.png --config text_config.json --split-len 30

# Avec des images et du texte
python whiteboard_animator.py background.png --config mixed_config.json --split-len 30
```

### Placeholder blanc / White Placeholder

Pour créer une vidéo avec uniquement du texte, créez d'abord une image blanche :

To create a video with only text, first create a white image:

```python
import cv2
import numpy as np

white_img = np.ones((1080, 1920, 3), dtype=np.uint8) * 255
cv2.imwrite('white_placeholder.png', white_img)
```

Puis utilisez-la / Then use it:

```bash
python whiteboard_animator.py white_placeholder.png --config text_only.json
```

## Couleurs / Colors

Les couleurs peuvent être spécifiées de plusieurs façons :

Colors can be specified in multiple ways:

### RGB Tuple/List
```json
"color": [255, 0, 0]      // Rouge / Red
"color": [0, 255, 0]      // Vert / Green
"color": [0, 0, 255]      // Bleu / Blue
```

### Code Hex
```json
"color": "#FF0000"        // Rouge / Red
"color": "#00FF00"        // Vert / Green
"color": "#0066CC"        // Bleu / Blue
```

### Noms de couleurs / Color Names
```json
"color": "black"
"color": "white"
"color": "red"
"color": "green"
"color": "blue"
```

## Polices / Fonts

### Polices système courantes / Common System Fonts

**Linux:**
- DejaVuSans (recommandé / recommended)
- Liberation Sans
- Ubuntu

**Windows:**
- Arial
- Calibri
- Times New Roman

**macOS:**
- Helvetica
- Arial
- Times

### Fallback automatique / Automatic Fallback

Si la police spécifiée n'est pas trouvée, le système utilise automatiquement DejaVuSans ou Arial.

If the specified font is not found, the system automatically uses DejaVuSans or Arial.

## Animations

Les couches de texte supportent toutes les animations :

Text layers support all animations:

### Animations d'entrée / Entrance Animations
- `fade_in` - Apparition en fondu
- `slide_in_left` - Glissement depuis la gauche
- `slide_in_right` - Glissement depuis la droite
- `slide_in_top` - Glissement depuis le haut
- `slide_in_bottom` - Glissement depuis le bas
- `zoom_in` - Zoom avant

### Animations de sortie / Exit Animations
- `fade_out` - Disparition en fondu
- `slide_out_*` - Glissement vers l'extérieur
- `zoom_out` - Zoom arrière

### Exemple avec animations / Example with Animations

```json
{
  "type": "text",
  "z_index": 2,
  "text_config": {
    "text": "Apparition progressive",
    "size": 48
  },
  "entrance_animation": {
    "type": "fade_in",
    "duration": 1.0
  },
  "exit_animation": {
    "type": "slide_out_top",
    "duration": 0.8
  }
}
```

## Modes de couche / Layer Modes

### Mode `draw` (défaut / default)
Animation de handwriting complète avec la main qui "écrit" le texte.

Full handwriting animation with hand "writing" the text.

```json
{
  "type": "text",
  "mode": "draw",
  "skip_rate": 12
}
```

### Mode `static`
Le texte apparaît directement sans animation de dessin (mais les animations d'entrée/sortie fonctionnent).

Text appears directly without drawing animation (but entrance/exit animations work).

```json
{
  "type": "text",
  "mode": "static"
}
```

### Mode `eraser`
Utilise une gomme au lieu de la main pour "révéler" le texte.

Uses an eraser instead of hand to "reveal" the text.

```json
{
  "type": "text",
  "mode": "eraser",
  "skip_rate": 15
}
```

## Performance

### Optimisation / Optimization

- **skip_rate plus élevé** = animation plus rapide / higher skip_rate = faster animation
- **Mode static** = pas de dessin, instantané / no drawing, instant
- **Taille de police plus petite** = rendu plus rapide / smaller font = faster rendering

### Exemples de vitesse / Speed Examples

```json
// Très lent / Very slow
"skip_rate": 5

// Normal
"skip_rate": 12

// Rapide / Fast
"skip_rate": 20

// Très rapide / Very fast
"skip_rate": 30
```

## Exemples complets / Complete Examples

Voir / See:
- `examples/text_layer_example.json` - Exemple complet avec 3 couches de texte
- `test_text_layer.json` - Exemple simple de test

## Dépannage / Troubleshooting

### Le texte n'apparaît pas / Text doesn't appear

✅ Vérifiez que `type: "text"` est spécifié  
✅ Vérifiez que `text_config.text` contient du texte  
✅ Vérifiez que la couleur n'est pas blanche sur fond blanc  

### Police non trouvée / Font not found

✅ Le système utilise automatiquement une police de fallback  
✅ Utilisez "DejaVuSans" pour garantir la compatibilité  
✅ Listez les polices disponibles : `fc-list` (Linux)  

### Texte tronqué / Text truncated

✅ Vérifiez la position si `position` est spécifié  
✅ Réduisez la taille de police (`size`)  
✅ Utilisez plusieurs couches pour texte long  

### Animation trop lente/rapide / Animation too slow/fast

✅ Ajustez `skip_rate` (plus grand = plus rapide)  
✅ Utilisez `mode: "static"` pour pas d'animation  
✅ Ajustez `duration` de la slide  

## Limitations

1. **Polices** - Dépend des polices installées sur le système
2. **Effets de texte** - Pas d'ombres, contours ou dégradés (pour l'instant)
3. **Text complexe** - Pas de RTL (arabe, hébreu) ou texte vertical
4. **Taille maximale** - Limité par la résolution de la vidéo

## Ressources / Resources

- [IMPLEMENTATION_TEXT_HANDWRITING.md](IMPLEMENTATION_TEXT_HANDWRITING.md) - Détails techniques
- [LAYERS_GUIDE.md](LAYERS_GUIDE.md) - Guide complet des couches
- [examples/text_layer_example.json](examples/text_layer_example.json) - Exemple pratique

## Support

Pour questions ou problèmes, ouvrez une issue sur GitHub :
https://github.com/armelgeek/whiteboard-it/issues

For questions or issues, open an issue on GitHub:
https://github.com/armelgeek/whiteboard-it/issues
