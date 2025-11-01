# Guide des Nouveaux Modes d'Animation

## Vue d'ensemble

Whiteboard-it propose maintenant **quatre styles d'animation de main** pour créer vos vidéos :

1. **Draw** - Animation de dessin classique par carreaux (tile-based)
2. **Erase** - Animation d'effacement par carreaux
3. **Flood Fill** - Remplissage par régions connectées (NOUVEAU!)
4. **Coloriage** - Coloriage progressif pixel par pixel (NOUVEAU!)

Les modes **Flood Fill** et **Coloriage** offrent de nouvelles façons d'animer vos contenus, chacun avec ses avantages spécifiques.

## Fonctionnalités

### Mode Flood Fill
- 🎨 **Remplissage par région** : Identifie automatiquement les zones connectées
- 🖌️ **Animation progressive** : Remplit chaque région de manière fluide avec la main
- 🎯 **Optimisé** : Plus rapide que le mode tile pour des images avec peu de régions distinctes
- 🔄 **Compatible** : Fonctionne avec tous les paramètres existants (layers, transitions, etc.)

### Mode Coloriage
- 🖍️ **Coloriage naturel** : Colorie l'image de gauche à droite, de haut en bas
- 🎨 **Effet de coloriage** : Simule le coloriage avec des crayons ou marqueurs
- 📊 **Bandes horizontales** : Organise le coloriage en bandes pour un effet fluide
- ✨ **Idéal pour les formes colorées** : Parfait pour des images avec zones de couleurs distinctes

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

Vous pouvez maintenant choisir parmi **cinq modes d'animation** :

1. **`draw`** (par défaut) : Animation de dessin tile par tile avec la main
2. **`erase`** : Animation d'effacement tile par tile avec une gomme
3. **`flood_fill`** (nouveau) : Remplissage progressif par régions connectées
4. **`coloriage`** (nouveau) : Coloriage progressif ligne par ligne
5. **`static`** : Affichage immédiat sans animation

### Exemple Coloriage

Utiliser le mode coloriage pour un effet de coloriage naturel :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 4,
      "skip_rate": 5,
      "layers": [
        {
          "image_path": "drawing.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 3,
          "mode": "coloriage"
        }
      ]
    }
  ]
}
```

### Exemple multi-couches

Combinez différents modes dans une même slide :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 6,
      "layers": [
        {
          "image_path": "outline.png",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "colors.png",
          "z_index": 2,
          "mode": "coloriage"
        },
        {
          "image_path": "highlights.png",
          "z_index": 3,
          "mode": "flood_fill"
        },
        {
          "image_path": "logo.png",
          "z_index": 4,
          "mode": "static"
        }
      ]
    }
  ]
}
```

## Comparaison des modes

| Mode | Animation | Vitesse relative | Frames (exemple) | Usage recommandé |
|------|-----------|------------------|------------------|------------------|
| `draw` | Tile par tile | Moyenne | ~88 frames | Images complexes, textures, dessins détaillés |
| `erase` | Tile par tile inverse | Moyenne | ~88 frames | Effets de révélation, animations inverses |
| `flood_fill` | Par régions | Rapide | ~21 frames | Formes simples, logos, diagrammes, icônes |
| `coloriage` | Ligne par ligne | Lente | ~201 frames | Images colorées, dessins à colorier, art |
| `static` | Instantanée | Instantanée | 0 frames | Éléments statiques, logos, watermarks |

## Cas d'usage

### Idéal pour flood_fill
- 🎨 Logos et icônes
- 📊 Diagrammes et graphiques
- 🔷 Formes géométriques simples
- 🗺️ Cartes avec zones distinctes
- 🎯 Images avec peu de régions (<20)

### Idéal pour coloriage
- 🖍️ Dessins à colorier
- 🎨 Images avec zones colorées distinctes
- 🌈 Art coloré et illustrations
- 📚 Livres de coloriage
- 🎭 Effet de peinture/coloriage artistique

### Meilleur avec draw mode
- 🖼️ Images photographiques
- 📝 Illustrations détaillées
- 🎭 Textures complexes
- ✍️ Dessins à main levée
- 📐 Schémas techniques

## Paramètres

Le mode flood fill utilise les mêmes paramètres que les autres modes :

- **`skip_rate`** : Contrôle la vitesse d'animation (plus petit = plus lent)
- **`duration`** : Durée totale de la slide
- **`position`** : Position de la couche
- **`scale`** : Échelle de la couche
- **`opacity`** : Opacité de la couche

## Algorithmes

### Algorithme Flood Fill

Le mode flood fill fonctionne en :

1. **Détection** : Analyse l'image pour identifier les pixels de contenu
2. **Segmentation** : Utilise `cv2.connectedComponents()` avec **8-connectivité** pour trouver les régions connectées
   - La 8-connectivité inclut les voisins diagonaux, permettant de remplir correctement les coins et zones étroites
   - Améliore la couverture par rapport à la 4-connectivité (seulement horizontal/vertical)
3. **Tri** : Ordonne les régions de haut en bas, gauche à droite
4. **Remplissage** : Remplit progressivement chaque région avec la main qui suit le mouvement
5. **Finalisation** : Applique les couleurs finales de l'image

### Algorithme Coloriage

Le mode coloriage fonctionne en :

1. **Détection** : Identifie tous les pixels de contenu de l'image
2. **Organisation** : Trie les pixels de haut en bas, gauche à droite
3. **Bandes** : Groupe les pixels en bandes horizontales (5 pixels de hauteur)
4. **Coloriage** : Colorie chaque bande progressivement, segment par segment
5. **Animation** : La main suit le mouvement de coloriage de gauche à droite

## Exemples de configuration

### Configuration complète - Tous les modes

Exemple démontrant les 4 modes d'animation :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 3,
      "layers": [
        {
          "image_path": "image1.png",
          "z_index": 1,
          "mode": "draw",
          "skip_rate": 5
        }
      ]
    },
    {
      "index": 1,
      "duration": 3,
      "layers": [
        {
          "image_path": "image2.png",
          "z_index": 1,
          "mode": "flood_fill",
          "skip_rate": 3
        }
      ]
    },
    {
      "index": 2,
      "duration": 4,
      "layers": [
        {
          "image_path": "image3.png",
          "z_index": 1,
          "mode": "coloriage",
          "skip_rate": 3
        }
      ]
    },
    {
      "index": 3,
      "duration": 3,
      "layers": [
        {
          "image_path": "image4.png",
          "z_index": 1,
          "mode": "eraser",
          "skip_rate": 5
        }
      ]
    }
  ],
  "transitions": [
    {"after_slide": 0, "type": "fade", "duration": 0.5},
    {"after_slide": 1, "type": "wipe", "duration": 0.5},
    {"after_slide": 2, "type": "fade", "duration": 0.5}
  ]
}
```

Voir aussi le fichier `examples/flood_fill_demo.json` pour un exemple complet avec :
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

Les modes flood fill et coloriage sont actuellement supportés pour :
- ✅ Couches d'images
- ✅ Multi-couches
- ✅ Animations d'entrée/sortie
- ✅ Transitions
- ✅ Watermarks
- ✅ Tous les paramètres de layer (position, scale, opacity, etc.)
- ⚠️ Couches de texte (utilisent handwriting par défaut si flood_fill ou coloriage est spécifié)

## Voir aussi

- [GUIDE_COMPLET.md](GUIDE_COMPLET.md) - Documentation complète
- [CONFIG_FORMAT.md](CONFIG_FORMAT.md) - Format de configuration JSON
- [LAYERS_GUIDE.md](LAYERS_GUIDE.md) - Guide des couches multiples
