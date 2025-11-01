# Quick Start : Effets de Particules 🚀

Guide de démarrage rapide pour ajouter des effets de particules à vos animations whiteboard.

## Installation

Aucune installation supplémentaire nécessaire ! Les effets de particules utilisent les bibliothèques déjà installées (`numpy` et `opencv-python`).

## Utilisation Basique

### 1. Confettis 🎊

Ajoutez des confettis après avoir dessiné une image :

```bash
python whiteboard_animator.py demo/1.jpg --config examples/particle_confetti.json --split-len 30
```

### 2. Étincelles ✨

Ajoutez des étincelles scintillantes :

```bash
python whiteboard_animator.py demo/2.jpg --config examples/particle_sparkles.json --split-len 30
```

### 3. Explosion 💥

Créez une explosion spectaculaire :

```bash
python whiteboard_animator.py demo/3.png --config examples/particle_explosion.json --split-len 30
```

### 4. Magie 🪄

Ajoutez des étincelles magiques à du texte :

```bash
python whiteboard_animator.py demo/placeholder.png --config examples/particle_magic.json --split-len 30
```

### 5. Fumée 💨

Créez une traînée de fumée :

```bash
python whiteboard_animator.py demo/1.jpg --config examples/particle_smoke.json --split-len 30
```

## Configuration Simple

Ajoutez un effet de particules à n'importe quelle couche :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "votre_image.jpg",
          "skip_rate": 10,
          "particle_effect": {
            "type": "confetti",
            "position": [360, 100],
            "duration": 3.0
          }
        }
      ]
    }
  ]
}
```

## Types d'Effets Disponibles

| Type | Description | Usage |
|------|-------------|-------|
| `confetti` | Confettis colorés | Célébrations |
| `sparkle` | Étoiles scintillantes | Brillance |
| `smoke` | Traînée de fumée | Mouvement |
| `explosion` | Explosion radiale | Impact |
| `magic` | Étincelles magiques | Texte/Objets |
| `custom` | Système personnalisé | Contrôle total |

## Paramètres Rapides

### Confetti
```json
{
  "type": "confetti",
  "position": [x, y],
  "duration": 3.0,
  "burst_count": 100
}
```

### Sparkle
```json
{
  "type": "sparkle",
  "position": [x, y],
  "duration": 2.0,
  "emission_rate": 30.0
}
```

### Explosion
```json
{
  "type": "explosion",
  "position": [x, y],
  "particle_count": 50
}
```

### Magic
```json
{
  "type": "magic",
  "position": [x, y],
  "duration": 3.0,
  "emission_rate": 15.0
}
```

### Smoke
```json
{
  "type": "smoke",
  "position": [x, y],
  "duration": 2.0,
  "emission_rate": 20.0
}
```

## Positionnement

Pour un canvas 720x640 :
- Centre : `[360, 320]`
- Haut centre : `[360, 100]`
- Bas centre : `[360, 540]`
- Coin supérieur gauche : `[100, 100]`
- Coin supérieur droit : `[620, 100]`

## Exemples Complets

### Confettis de Célébration

Fichier `my_confetti.json` :
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "skip_rate": 10,
          "mode": "draw",
          "particle_effect": {
            "type": "confetti",
            "position": [360, 100],
            "duration": 3.0,
            "burst_count": 150
          }
        }
      ]
    }
  ]
}
```

Commande :
```bash
python whiteboard_animator.py demo/1.jpg --config my_confetti.json --split-len 30
```

### Texte Magique

Fichier `my_magic_text.json` :
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "type": "text",
          "text_config": {
            "text": "Success!",
            "font": "Arial",
            "size": 64,
            "color": [0, 0, 200],
            "style": "bold",
            "align": "center",
            "position": {"x": 360, "y": 280}
          },
          "skip_rate": 5,
          "particle_effect": {
            "type": "magic",
            "position": [360, 320],
            "duration": 4.0,
            "emission_rate": 25.0
          }
        }
      ]
    }
  ]
}
```

Commande :
```bash
python whiteboard_animator.py demo/placeholder.png --config my_magic_text.json --split-len 30
```

## Astuces

1. **Position** : Ajustez `position` pour placer l'effet où vous le voulez
2. **Durée** : Augmentez `duration` pour des effets plus longs
3. **Intensité** : Augmentez `burst_count` ou `emission_rate` pour plus de particules
4. **Combinaisons** : Combinez avec des animations d'entrée/sortie pour des effets plus complexes

## Prochaines Étapes

- Consultez `PARTICLE_GUIDE.md` pour la documentation complète
- Explorez les exemples dans `/examples/particle_*.json`
- Essayez le type `custom` pour un contrôle total

---

**Amusez-vous avec les particules ! 🎆**
