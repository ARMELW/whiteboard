# Format d'export JSON de l'animation

## Vue d'ensemble

L'option `--export-json` permet d'exporter les données d'animation au format JSON. Ce format contient toutes les informations nécessaires pour recréer ou manipuler l'animation dans d'autres logiciels.

## Utilisation

```bash
python whiteboard_animator.py image.png --export-json
```

Cela génère deux fichiers :
- Un fichier vidéo MP4 (comme d'habitude)
- Un fichier JSON contenant les données d'animation

## Structure du fichier JSON

```json
{
  "metadata": {
    "frame_rate": 30,
    "width": 480,
    "height": 360,
    "split_len": 20,
    "object_skip_rate": 20,
    "total_frames": 100,
    "hand_dimensions": {
      "width": 284,
      "height": 467
    }
  },
  "animation": {
    "drawing_sequence": [],
    "frames_written": [
      {
        "frame_number": 0,
        "tile_drawn": {
          "grid_position": [8, 8],
          "pixel_coords": {
            "x_start": 160,
            "x_end": 180,
            "y_start": 160,
            "y_end": 180
          }
        },
        "hand_position": {
          "x": 170,
          "y": 170
        },
        "tiles_remaining": 13
      }
    ]
  }
}
```

## Description des champs

### metadata
- **frame_rate** : Images par seconde (FPS)
- **width** : Largeur de la vidéo en pixels
- **height** : Hauteur de la vidéo en pixels
- **split_len** : Taille de la grille utilisée pour le dessin
- **object_skip_rate** : Taux de saut pour la vitesse de dessin
- **total_frames** : Nombre total de frames enregistrées
- **hand_dimensions** : Dimensions de l'image de la main
  - **width** : Largeur de la main en pixels
  - **height** : Hauteur de la main en pixels

### animation.frames_written
Liste des frames enregistrées, chaque frame contient :

- **frame_number** : Numéro de la frame (0-indexé)
- **tile_drawn** : Information sur la tuile dessinée
  - **grid_position** : Position dans la grille [ligne, colonne]
  - **pixel_coords** : Coordonnées en pixels
    - **x_start** : Position X de début
    - **x_end** : Position X de fin
    - **y_start** : Position Y de début
    - **y_end** : Position Y de fin
- **hand_position** : Position de la main sur cette frame
  - **x** : Position X de la main
  - **y** : Position Y de la main
- **tiles_remaining** : Nombre de tuiles restantes à dessiner

## Cas d'utilisation

Ce format JSON permet de :

1. **Recréer l'animation** dans d'autres logiciels
2. **Analyser la séquence de dessin** pour optimiser les paramètres
3. **Créer des animations personnalisées** en utilisant les données de séquence
4. **Intégrer dans des applications** comme VideoScribe ou similaires
5. **Modifier la séquence** de dessin sans régénérer la vidéo

## Exemple d'utilisation en Python

```python
import json

# Charger les données d'animation
with open('animation_20231007_123456.json', 'r') as f:
    data = json.load(f)

# Accéder aux métadonnées
width = data['metadata']['width']
height = data['metadata']['height']
fps = data['metadata']['frame_rate']

# Parcourir les frames
for frame in data['animation']['frames_written']:
    print(f"Frame {frame['frame_number']}: Main à ({frame['hand_position']['x']}, {frame['hand_position']['y']})")
    print(f"  Tuile dessinée: {frame['tile_drawn']['grid_position']}")
```

## Notes

- Les coordonnées sont en pixels, avec l'origine (0,0) en haut à gauche
- Les positions de grille sont indexées à partir de 0
- Le format est compatible avec tous les parseurs JSON standards
