# Absolute Layer Positioning Fix

## Issue
Les layers (couches) n'utilisaient pas un positionnement absolu cohérent. Le positionnement variait selon le type de couche et l'alignement du texte.

## Problème Identifié

### Avant le correctif:
1. **Couches Image**: Position = coin supérieur gauche ✓ (correct)
2. **Couches Texte**: Position = point d'ancrage variable selon l'alignement ✗ (incohérent)
   - `align: "left"`: position = bord gauche du texte
   - `align: "center"`: position = centre du texte
   - `align: "right"`: position = bord droit du texte
3. **Couches Forme**: Position = centre de la forme ✗ (incohérent)

### Après le correctif:
1. **Couches Image**: Position = coin supérieur gauche ✓
2. **Couches Texte**: Position = coin supérieur gauche de la boîte englobante du texte ✓
   - L'attribut `align` n'affecte plus le point d'ancrage de la position
   - Tous les textes avec la même position.x démarrent au même point, peu importe l'alignement
3. **Couches Forme**: Inchangé (utilise toujours le centre)

## Changements de Code

### 1. render_text_to_image() - Ligne ~353-371
**Avant:**
```python
if position and 'x' in position:
    # Position is specified - interpret based on alignment
    # This matches frontend behavior where position is the anchor point
    if align == 'center':
        # For center align, x is the center of the text
        x = position['x'] - line_width // 2
    elif align == 'right':
        # For right align, x is the right edge of the text
        x = position['x'] - line_width
    else:  # left
        # For left align, x is the left edge of the text
        x = position['x']
```

**Après:**
```python
if position and 'x' in position:
    # ABSOLUTE POSITIONING: position.x is always the left edge of the text bounding box
    # Alignment does not affect the position anchor point
    x = position['x']
    # Note: alignment could be used to affect multi-line text alignment within the bounding box
    # but for now we treat position as absolute top-left corner
```

### 2. draw_svg_path_handwriting() - Ligne ~786-803
Changement similaire pour l'animation de dessin de texte.

## Impact sur les Configurations Existantes

⚠️ **BREAKING CHANGE** pour les couches de texte avec alignement "center" ou "right":

- Les textes avec `align: "center"` ou `align: "right"` qui avaient une position spécifiée verront leur position changée
- La position est maintenant toujours le coin supérieur gauche, indépendamment de l'alignement
- Les configurations devront être mises à jour pour ajuster les valeurs x des positions

### Exemple de Migration:
**Avant (position = point d'ancrage variable):**
```json
{
  "text": "Mon texte",
  "align": "right",
  "position": {"x": 1000, "y": 100}
}
```
Le texte se terminait à x=1000.

**Après (position = coin supérieur gauche):**
```json
{
  "text": "Mon texte",
  "align": "right",
  "position": {"x": 800, "y": 100}
}
```
Le texte démarre à x=800 (ajusté selon la largeur du texte).

## Test

Un fichier de test a été créé: `examples/test-absolute-positioning.json`

Ce fichier contient trois textes avec différents alignements (left, center, right) mais tous avec la même position x=100. Après le correctif, tous les trois devraient démarrer au même point x=100.

## Bénéfices

1. **Cohérence**: Tous les types de couches utilisent maintenant un système de positionnement cohérent
2. **Prévisibilité**: La position spécifie toujours le coin supérieur gauche
3. **Compatibilité CSS**: Le comportement correspond au positionnement absolu standard (CSS)
4. **Simplicité**: Plus besoin de calculer différents points d'ancrage selon l'alignement
