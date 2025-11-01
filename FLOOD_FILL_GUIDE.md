# Guide du Mode Flood Fill

## Vue d'ensemble

Le mode **Flood Fill** (remplissage par zone) est un nouveau style d'animation de main disponible dans whiteboard-it. Contrairement aux modes `draw` et `erase` qui fonctionnent par carreaux (tiles), le mode flood fill identifie et remplit les régions connectées de l'image de manière progressive, créant un effet de coloration/remplissage naturel.

## Fonctionnalités

- 🎨 **Remplissage par région** : Identifie automatiquement les zones connectées
- 🖌️ **Animation progressive** : Remplit chaque région de manière fluide avec la main
- 🎯 **Optimisé** : Plus rapide que le mode tile pour des images avec peu de régions distinctes
- 🔄 **Compatible** : Fonctionne avec tous les paramètres existants (layers, transitions, etc.)

## Utilisation

### Configuration de base

Dans votre fichier de configuration JSON, définissez simplement `"mode": "flood_fill"` pour une couche :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 3,
      "skip_rate": 5,
      "layers": [
        {
          "image_path": "path/to/image.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 3,
          "mode": "flood_fill"
        }
      ]
    }
  ]
}
```

### Modes disponibles

Vous pouvez maintenant choisir parmi quatre modes d'animation :

1. **`draw`** (par défaut) : Animation de dessin tile par tile avec la main
2. **`erase`** : Animation d'effacement tile par tile avec une gomme
3. **`flood_fill`** (nouveau) : Remplissage progressif par régions connectées
4. **`static`** : Affichage immédiat sans animation

### Exemple multi-couches

Combinez différents modes dans une même slide :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "shapes.png",
          "z_index": 2,
          "mode": "flood_fill"
        },
        {
          "image_path": "logo.png",
          "z_index": 3,
          "mode": "static"
        }
      ]
    }
  ]
}
```

## Comparaison des modes

| Mode | Animation | Vitesse | Usage recommandé |
|------|-----------|---------|------------------|
| `draw` | Tile par tile | Moyenne | Images complexes, textures |
| `erase` | Tile par tile inverse | Moyenne | Effets de révélation |
| `flood_fill` | Par régions | Rapide | Formes simples, logos, diagrammes |
| `static` | Instantanée | Instantanée | Éléments statiques, logos |

## Cas d'usage

### Idéal pour flood fill
- 🎨 Logos et icônes
- 📊 Diagrammes et graphiques
- 🔷 Formes géométriques simples
- 🗺️ Cartes avec zones distinctes

### Meilleur avec draw mode
- 🖼️ Images photographiques
- 📝 Illustrations détaillées
- 🎭 Textures complexes
- ✍️ Dessins à main levée

## Paramètres

Le mode flood fill utilise les mêmes paramètres que les autres modes :

- **`skip_rate`** : Contrôle la vitesse d'animation (plus petit = plus lent)
- **`duration`** : Durée totale de la slide
- **`position`** : Position de la couche
- **`scale`** : Échelle de la couche
- **`opacity`** : Opacité de la couche

## Algorithme

Le mode flood fill fonctionne en :

1. **Détection** : Analyse l'image pour identifier les pixels de contenu
2. **Segmentation** : Utilise `cv2.connectedComponents()` pour trouver les régions connectées
3. **Tri** : Ordonne les régions de haut en bas, gauche à droite
4. **Remplissage** : Remplit progressivement chaque région avec la main qui suit le mouvement
5. **Finalisation** : Applique les couleurs finales de l'image

## Exemples de configuration

### Configuration complète

Voir le fichier `examples/flood_fill_demo.json` pour un exemple complet avec :
- Différents modes sur différentes slides
- Transitions entre les slides
- Configuration multi-couches

### Ligne de commande

```bash
# Utiliser flood fill avec la configuration
python whiteboard_animator.py --config examples/flood_fill_demo.json

# Les paramètres CLI habituels fonctionnent également
python whiteboard_animator.py image.png --fps 30 --skip 5
```

## Notes techniques

- 🔍 Le mode flood fill détecte automatiquement les régions distinctes
- 🎯 Fonctionne mieux avec des images ayant des zones clairement séparées
- ⚡ Plus rapide que le mode draw pour des images avec peu de régions (< 20)
- 📐 Compatible avec les masques d'objets et les animations d'entrée/sortie

## Support

Le mode flood fill est actuellement supporté pour :
- ✅ Couches d'images
- ✅ Multi-couches
- ✅ Animations d'entrée/sortie
- ✅ Transitions
- ✅ Watermarks
- ⚠️ Couches de texte (utilise handwriting par défaut)

## Voir aussi

- [GUIDE_COMPLET.md](GUIDE_COMPLET.md) - Documentation complète
- [CONFIG_FORMAT.md](CONFIG_FORMAT.md) - Format de configuration JSON
- [LAYERS_GUIDE.md](LAYERS_GUIDE.md) - Guide des couches multiples
