# Guide des Effets de Particules 🎆

Ce guide décrit le système d'effets de particules pour enrichir vos animations whiteboard avec des effets visuels dynamiques.

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Effets Prédéfinis](#effets-prédéfinis)
3. [Configuration](#configuration)
4. [Exemples d'Utilisation](#exemples-dutilisation)
5. [Système Personnalisé](#système-personnalisé)
6. [Paramètres Avancés](#paramètres-avancés)

---

## Introduction

Le système de particules permet d'ajouter des effets visuels dynamiques à vos animations :
- **Confettis** pour les célébrations
- **Étincelles** scintillantes
- **Traînées de fumée/poussière**
- **Explosions** spectaculaires
- **Étincelles magiques** pour texte/objets
- **Systèmes personnalisés** complètement configurables

### Installation

Le système de particules utilise les bibliothèques déjà présentes :
- `numpy` - Opérations mathématiques
- `opencv-python` - Rendu graphique

Aucune installation supplémentaire n'est nécessaire !

---

## Effets Prédéfinis

### 1. 🎊 Confettis (Confetti)

Effet de confettis colorés pour célébrations.

**Caractéristiques :**
- Particules multicolores (rouge, vert, bleu, jaune, magenta, cyan, orange, violet)
- Formes variées (carrés, cercles, triangles)
- Mouvement avec gravité (tombent vers le bas)
- Parfait pour les moments de célébration

**Configuration de base :**
```json
"particle_effect": {
  "type": "confetti",
  "position": [360, 100],
  "duration": 3.0,
  "burst_count": 100
}
```

**Paramètres :**
- `position`: Position `[x, y]` d'émission des confettis
- `duration`: Durée de vie des particules en secondes (défaut: 3.0)
- `burst_count`: Nombre de confettis à émettre (défaut: 100)

---

### 2. ✨ Étincelles (Sparkle)

Effet d'étoiles scintillantes.

**Caractéristiques :**
- Particules brillantes (blanc, jaune pâle, rose pâle)
- Formes étoile et cercle
- Émission continue
- Aucune gravité (flottent)

**Configuration de base :**
```json
"particle_effect": {
  "type": "sparkle",
  "position": [360, 320],
  "duration": 2.0,
  "emission_rate": 30.0
}
```

**Paramètres :**
- `position`: Position `[x, y]` d'émission
- `duration`: Durée totale de l'effet en secondes (défaut: 2.0)
- `emission_rate`: Particules émises par seconde (défaut: 30.0)

---

### 3. 💨 Fumée/Poussière (Smoke)

Traînées de fumée ou de poussière.

**Caractéristiques :**
- Particules grises/blanches
- Mouvement ascendant (gravité négative)
- Effet de traînée
- Idéal pour effets de mouvement

**Configuration de base :**
```json
"particle_effect": {
  "type": "smoke",
  "position": [360, 500],
  "duration": 2.0,
  "emission_rate": 20.0
}
```

**Paramètres :**
- `position`: Position `[x, y]` d'émission
- `duration`: Durée de l'effet (défaut: 2.0)
- `emission_rate`: Particules par seconde (défaut: 20.0)

---

### 4. 💥 Explosion

Effet d'explosion radiale.

**Caractéristiques :**
- Particules aux couleurs de feu (orange-rouge, orange, doré, jaune)
- Explosion instantanée (burst)
- Propagation radiale (360°)
- Particules qui tombent avec gravité

**Configuration de base :**
```json
"particle_effect": {
  "type": "explosion",
  "position": [360, 320],
  "duration": 1.5,
  "particle_count": 50
}
```

**Paramètres :**
- `position`: Position `[x, y]` du centre de l'explosion
- `duration`: Durée de vie des particules (défaut: 1.5)
- `particle_count`: Nombre de particules (défaut: 50)

---

### 5. 🪄 Magie (Magic)

Étincelles magiques pour texte ou objets.

**Caractéristiques :**
- Couleurs magiques (bleu clair, rose clair, jaune clair, vert clair)
- Forme d'étoiles uniquement
- Flottent vers le haut (gravité négative)
- Effet continu

**Configuration de base :**
```json
"particle_effect": {
  "type": "magic",
  "position": [360, 320],
  "duration": 3.0,
  "emission_rate": 15.0
}
```

**Paramètres :**
- `position`: Position `[x, y]` d'émission
- `duration`: Durée de l'effet (défaut: 3.0)
- `emission_rate`: Particules par seconde (défaut: 15.0)

---

## Configuration

Les effets de particules se configurent au niveau de la couche (layer) dans votre fichier JSON :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "z_index": 1,
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

### Positionnement

La position `[x, y]` est spécifiée en pixels à partir du coin supérieur gauche :
- `x`: Position horizontale (0 = gauche, largeur de l'image = droite)
- `y`: Position verticale (0 = haut, hauteur de l'image = bas)

Pour centrer un effet sur un canvas 720x640 :
```json
"position": [360, 320]
```

---

## Exemples d'Utilisation

### Exemple 1 : Confettis de célébration

Ajoutez des confettis après avoir dessiné une image :

```bash
python whiteboard_animator.py demo/1.jpg --config examples/particle_confetti.json --split-len 30
```

Configuration (`particle_confetti.json`) :
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "z_index": 1,
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

---

### Exemple 2 : Texte avec étincelles magiques

Créez du texte avec des étincelles magiques :

```bash
python whiteboard_animator.py demo/placeholder.png --config examples/particle_magic.json --split-len 30
```

Configuration (`particle_magic.json`) :
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
            "text": "✨ Magic Text ✨",
            "font": "Arial",
            "size": 72,
            "color": [0, 0, 200],
            "style": "bold",
            "align": "center",
            "position": {"x": 360, "y": 280}
          },
          "z_index": 1,
          "skip_rate": 5,
          "mode": "draw",
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

---

### Exemple 3 : Explosion sur une image

Ajoutez une explosion spectaculaire :

```bash
python whiteboard_animator.py demo/3.png --config examples/particle_explosion.json --split-len 30
```

---

### Exemple 4 : Étincelles scintillantes

Effet d'étincelles continues :

```bash
python whiteboard_animator.py demo/2.jpg --config examples/particle_sparkles.json --split-len 30
```

---

### Exemple 5 : Traînée de fumée

Ajoutez une traînée de fumée :

```bash
python whiteboard_animator.py demo/1.jpg --config examples/particle_smoke.json --split-len 30
```

---

## Système Personnalisé

Pour un contrôle total, utilisez le type `custom` avec des émetteurs personnalisés.

### Structure de base

```json
"particle_effect": {
  "type": "custom",
  "duration": 4.0,
  "frame_rate": 30,
  "emitters": [
    {
      "position": [200, 320],
      "emission_rate": 20.0,
      "particle_lifetime": 2.5,
      "direction": 45,
      "spread": 30,
      "speed": [80, 150],
      "colors": [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
      "sizes": [5, 12],
      "shapes": ["circle", "star"],
      "gravity": 50,
      "burst_mode": false
    }
  ]
}
```

### Paramètres des émetteurs

| Paramètre | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `position` | `[x, y]` | Position de l'émetteur | Requis |
| `emission_rate` | float | Particules par seconde (0 pour burst) | 10.0 |
| `particle_lifetime` | float | Durée de vie des particules (secondes) | 2.0 |
| `direction` | float | Direction principale (degrés, 0=droite, 90=haut) | 90.0 |
| `spread` | float | Angle de dispersion (degrés) | 45.0 |
| `speed` | `[min, max]` | Vitesse min et max (pixels/seconde) | [50, 100] |
| `colors` | array | Liste de couleurs BGR, ex: `[[255, 0, 0]]` | [[255, 255, 255]] |
| `sizes` | `[min, max]` | Taille min et max des particules | [3, 8] |
| `shapes` | array | Formes : "circle", "square", "star", "triangle" | ["circle"] |
| `gravity` | float | Gravité (pixels/s²), négatif = monte | 0.0 |
| `burst_mode` | boolean | Mode burst (émission instantanée) | false |
| `burst_count` | int | Nombre de particules en mode burst | 50 |

### Exemple avancé : Multiple émetteurs

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "demo/2.jpg",
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw",
          "particle_effect": {
            "type": "custom",
            "duration": 4.0,
            "emitters": [
              {
                "position": [200, 320],
                "emission_rate": 20.0,
                "direction": 45,
                "colors": [[255, 0, 0], [0, 255, 0]],
                "shapes": ["star"]
              },
              {
                "position": [520, 320],
                "burst_mode": true,
                "burst_count": 60,
                "direction": 90,
                "spread": 360,
                "colors": [[255, 255, 0]]
              }
            ]
          }
        }
      ]
    }
  ]
}
```

---

## Paramètres Avancés

### Couleurs

Les couleurs sont spécifiées en format BGR (Blue, Green, Red) :

```json
"colors": [
  [255, 0, 0],     // Bleu
  [0, 255, 0],     // Vert
  [0, 0, 255],     // Rouge
  [255, 255, 0],   // Cyan
  [255, 0, 255],   // Magenta
  [0, 255, 255],   // Jaune
  [255, 255, 255]  // Blanc
]
```

### Formes

Quatre formes sont disponibles :
- `circle` : Cercle
- `square` : Carré (rotation automatique)
- `star` : Étoile à 5 branches (rotation automatique)
- `triangle` : Triangle (rotation automatique)

### Direction et Spread

- **Direction** : Angle en degrés
  - 0° = droite →
  - 90° = haut ↑
  - 180° = gauche ←
  - 270° = bas ↓

- **Spread** : Angle de dispersion
  - 0° = toutes les particules dans la même direction
  - 360° = dispersion complète dans toutes les directions

### Gravité

- **Positive** : Les particules tombent (ex: 200)
- **Zéro** : Les particules flottent (0)
- **Négative** : Les particules montent (ex: -50)

---

## Conseils et Astuces

### Performance

- Limitez le nombre de particules pour des animations fluides
- Pour des effets longs, préférez `emission_rate` faible plutôt que `burst_count` élevé
- Les formes simples (circle) sont plus rapides à rendre que les formes complexes (star)

### Timing

- Les particules commencent **après** le dessin de la couche
- Ajustez `duration` pour contrôler combien de temps l'effet dure
- Utilisez `particle_lifetime` pour contrôler combien de temps chaque particule vit

### Positionnement

- Testez différentes positions pour trouver le meilleur effet
- Pour un effet centré : utilisez la moitié de la largeur et hauteur de votre canvas
- Pour un effet en coin : utilisez des valeurs proches de 0 ou max

### Combinaisons

Vous pouvez combiner des effets de particules avec :
- Animations d'entrée/sortie
- Animations de caméra
- Animations de chemin
- Texte dynamique

---

## Dépannage

### Les particules n'apparaissent pas

1. Vérifiez que le module `particle_system.py` est présent
2. Vérifiez la console pour des messages d'erreur
3. Vérifiez que `position` est dans les limites du canvas

### Les particules sont trop rapides/lentes

- Ajustez le paramètre `speed` : `[min, max]`
- Valeurs typiques : `[50, 100]` pour lent, `[150, 300]` pour rapide

### L'effet ne dure pas assez longtemps

- Augmentez `duration` pour l'effet global
- Augmentez `particle_lifetime` pour chaque particule

### Trop de particules à l'écran

- Réduisez `emission_rate`
- Réduisez `burst_count` en mode burst
- Réduisez `particle_lifetime`

---

## Support et Documentation

Pour plus d'informations :
- Voir les exemples dans `/examples/particle_*.json`
- Consulter `PARTICLE_QUICKSTART.md` pour un démarrage rapide
- Consulter `CONFIG_FORMAT.md` pour la structure complète des configurations

---

**Bon amusement avec les effets de particules ! 🎆✨💥**
