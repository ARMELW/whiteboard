# Nouvelles fonctionnalités - Animations avancées

## Vue d'ensemble

Cette mise à jour ajoute plusieurs fonctionnalités avancées pour les couches (layers), permettant des animations plus variées et professionnelles :

1. **Mode Eraser** : Animation avec une gomme pour effet d'effacement
2. **Mode Static** : Affichage sans animation de dessin
3. **Animations d'entrée/sortie** : Effets d'apparition et disparition
4. **Morphing entre couches** : Transitions fluides entre couches

## 1. Modes de dessin

### Mode `draw` (par défaut)
Animation classique avec la main qui dessine le contenu.

```json
{
  "mode": "draw"
}
```

### Mode `eraser`
Utilise une gomme au lieu de la main pour créer un effet d'effacement ou de révélation.

```json
{
  "mode": "eraser"
}
```

**Utilisation recommandée :**
- Effacer des erreurs ou des éléments
- Révéler du contenu masqué
- Créer des effets de nettoyage

### Mode `static`
Affiche l'image directement sans animation de dessin. Idéal pour les logos, watermarks, ou éléments décoratifs.

```json
{
  "mode": "static"
}
```

**Utilisation recommandée :**
- Logos et branding
- Éléments décoratifs
- Watermarks
- Éléments qui doivent apparaître instantanément

## 2. Animations d'entrée

Les animations d'entrée contrôlent comment une couche apparaît à l'écran.

### Types disponibles

- `fade_in` : Fondu depuis blanc
- `slide_in_left` : Glissement depuis la gauche
- `slide_in_right` : Glissement depuis la droite
- `slide_in_top` : Glissement depuis le haut
- `slide_in_bottom` : Glissement depuis le bas
- `zoom_in` : Zoom depuis 50% de la taille

### Configuration

```json
{
  "entrance_animation": {
    "type": "fade_in",
    "duration": 1.0
  }
}
```

### Exemple complet

```json
{
  "image_path": "logo.png",
  "position": {"x": 50, "y": 50},
  "z_index": 3,
  "scale": 0.3,
  "mode": "static",
  "entrance_animation": {
    "type": "zoom_in",
    "duration": 1.5
  }
}
```

## 3. Animations de sortie

Les animations de sortie contrôlent comment une couche disparaît de l'écran.

### Types disponibles

- `fade_out` : Fondu vers blanc
- `slide_out_left` : Glissement vers la gauche
- `slide_out_right` : Glissement vers la droite
- `slide_out_top` : Glissement vers le haut
- `slide_out_bottom` : Glissement vers le bas
- `zoom_out` : Zoom vers 150% de la taille

### Configuration

```json
{
  "exit_animation": {
    "type": "fade_out",
    "duration": 0.8
  }
}
```

### Exemple complet

```json
{
  "image_path": "message.png",
  "position": {"x": 100, "y": 200},
  "z_index": 2,
  "mode": "static",
  "entrance_animation": {
    "type": "slide_in_bottom",
    "duration": 0.5
  },
  "exit_animation": {
    "type": "slide_out_top",
    "duration": 0.5
  }
}
```

## 4. Morphing entre couches

Le morphing crée une transition fluide et progressive entre deux couches consécutives.

### Configuration

```json
{
  "morph": {
    "enabled": true,
    "duration": 0.5
  }
}
```

### Fonctionnement

Le morphing s'applique automatiquement entre la couche N-1 et la couche N lorsqu'il est activé. Il crée une interpolation progressive entre les deux images.

**Note :** Le morphing fonctionne mieux entre images de contenu ou style similaire.

### Exemple

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "scene1.png",
          "z_index": 1,
          "skip_rate": 10
        },
        {
          "image_path": "scene2.png",
          "z_index": 2,
          "skip_rate": 10,
          "morph": {
            "enabled": true,
            "duration": 0.5
          }
        }
      ]
    }
  ]
}
```

## Exemple complet

Voici un exemple combinant toutes les fonctionnalités :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "image_path": "error_element.png",
          "position": {"x": 200, "y": 150},
          "z_index": 2,
          "skip_rate": 15,
          "mode": "eraser",
          "entrance_animation": {
            "type": "fade_in",
            "duration": 1.0
          }
        },
        {
          "image_path": "logo.png",
          "position": {"x": 50, "y": 50},
          "z_index": 3,
          "scale": 0.3,
          "mode": "static",
          "entrance_animation": {
            "type": "zoom_in",
            "duration": 1.5
          },
          "exit_animation": {
            "type": "fade_out",
            "duration": 1.0
          }
        },
        {
          "image_path": "text.png",
          "position": {"x": 300, "y": 400},
          "z_index": 4,
          "skip_rate": 12,
          "mode": "draw",
          "morph": {
            "enabled": true,
            "duration": 0.5
          }
        }
      ]
    }
  ]
}
```

**Résultat :**
1. Le fond est dessiné normalement avec la main (2-3 secondes)
2. Un élément d'erreur est "effacé" avec l'animation d'une gomme, apparaissant en fondu (2-3 secondes)
3. Un logo apparaît statiquement avec un zoom-in, reste visible, puis disparaît en fondu (3-4 secondes)
4. Du texte apparaît avec un morphing fluide depuis la couche précédente, puis est dessiné normalement (2-3 secondes)

## Conseils d'utilisation

### Durées recommandées

- **Entrance/Exit animations** : 0.5-1.5 secondes
- **Morphing** : 0.3-0.8 secondes

### Combinaisons efficaces

1. **Mode static + entrance/exit** : Idéal pour logos et éléments décoratifs
2. **Mode eraser + fade_in** : Excellent pour corriger ou révéler
3. **Mode draw + morph** : Parfait pour transitions entre contenus similaires

### Performance

- Chaque animation ajoute des frames à la vidéo finale
- Ajustez la durée de la slide en conséquence
- Les morphings courts (< 0.5s) sont plus naturels

## Fichiers requis

- `data/images/eraser.png` : Image de la gomme (créée automatiquement)
- `data/images/eraser-mask.png` : Masque de la gomme (créé automatiquement)

## Compatibilité

Ces fonctionnalités sont compatibles avec :
- ✅ Toutes les propriétés de couches existantes (position, scale, opacity, z_index)
- ✅ Toutes les transitions entre slides
- ✅ Export JSON
- ✅ Watermarks
- ✅ Tous les ratios d'aspect

## Exemples de configuration

Des exemples de configuration sont disponibles dans :
- `test_new_features_config.json` : Configuration de test simple
- `example_config.json` : Configuration d'exemple mise à jour

## Référence complète

Pour plus de détails, consultez :
- `CONFIG_FORMAT.md` : Format complet de configuration
- `LAYERS_GUIDE.md` : Guide détaillé des couches
