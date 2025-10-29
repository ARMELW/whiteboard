# Configuration personnalisée par slide

Ce document décrit le format du fichier de configuration JSON pour personnaliser les paramètres de chaque slide individuellement.

## ⏱️ Comportement de la durée (IMPORTANT)

**Changement important:** Le paramètre `duration` représente maintenant la **durée TOTALE** de la slide, et non plus uniquement le temps d'affichage après l'animation.

### Comment ça fonctionne

1. **Animation calculée automatiquement:** Le système calcule le temps nécessaire pour animer le dessin en fonction de:
   - La taille et le contenu de l'image
   - Le `skip_rate` (vitesse de dessin)
   - Le nombre de couches (layers)

2. **Durée totale respectée:** Si vous spécifiez `duration: 5`:
   - Si l'animation prend 2 secondes → l'image finale sera affichée pendant 3 secondes
   - Si l'animation prend 5 secondes → aucun temps d'attente supplémentaire
   - Si l'animation prend 7 secondes → un avertissement sera affiché et la durée totale sera de 7 secondes

3. **Affichage des informations:** Le système affiche:
   ```
   ⏱️ Animation: 1.33s (40 frames)
   ⏱️ Final hold: 2.67s (80 frames)
   ⏱️ Total duration: 4.00s
   ```

### Exemple pratique

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "skip_rate": 5
        }
      ]
    }
  ]
}
```

Avec cette configuration:
- La slide aura une durée totale de **10 secondes**
- Si l'animation prend 3 secondes, l'image finale sera affichée pendant 7 secondes
- Le total sera toujours 10 secondes (sauf si l'animation dépasse 10s)

## Format du fichier JSON

Le fichier de configuration contient plusieurs sections :
- `canvas_width` et `canvas_height` : Dimensions du canvas source (optionnel)
- `slides` : Configuration spécifique à chaque slide
- `transitions` : Configuration des transitions entre les slides

### Exemple complet

```json
{
  "canvas_width": 1920,
  "canvas_height": 1080,
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
    },
    {
      "index": 2,
      "duration": 4,
      "skip_rate": 8
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 0.8,
      "pause_before": 1.0
    },
    {
      "after_slide": 1,
      "type": "wipe",
      "duration": 1.0,
      "pause_before": 0.5
    }
  ]
}
```

## Canvas Dimensions (Optionnel)

### canvas_width et canvas_height

Ces paramètres définissent les dimensions du canvas source utilisé dans l'éditeur. Si les dimensions du canvas source diffèrent des dimensions de la vidéo de sortie (définies par `--aspect-ratio`), toutes les positions des couches seront automatiquement mises à l'échelle proportionnellement.

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `canvas_width` | int | Largeur du canvas source en pixels | 1920 |
| `canvas_height` | int | Hauteur du canvas source en pixels | 1080 |

**Exemple d'utilisation:**
Si votre éditeur utilise un canvas de 1200x800 mais vous voulez générer une vidéo en 1920x1080:
```json
{
  "canvas_width": 1200,
  "canvas_height": 800,
  "slides": [ ... ]
}
```

Les positions de toutes les couches seront automatiquement converties:
- Position X sera multipliée par 1920/1200 = 1.6
- Position Y sera multipliée par 1080/800 = 1.35

## Section `slides`

Permet de définir des paramètres spécifiques pour chaque slide.

### Propriétés disponibles

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `index` | int | Index de la slide (commence à 0) | Requis |
| `duration` | int/float | **Durée TOTALE de la slide en secondes** (inclut l'animation + temps d'affichage final). Si l'animation dépasse cette durée, seule l'animation sera utilisée. | Valeur globale `--duration` |
| `skip_rate` | int | Vitesse de dessin (plus grand = plus rapide) | Valeur globale `--skip-rate` |
| `layers` | array | Liste des couches d'images superposées (optionnel) | null |
| `cameras` | array | Séquence de caméras avec transitions (système de caméra avancé) | null |

### Exemple

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "skip_rate": 10
    }
  ]
}
```

Dans cet exemple :
- La première slide (index 0) aura une durée totale de 2 secondes
- Le système calcule automatiquement le temps d'animation basé sur l'image et le skip_rate
- Si l'animation prend 0.5 secondes, l'image finale sera affichée pendant 1.5 secondes
- Si l'animation prend plus de 2 secondes, seule l'animation sera montrée (avec un avertissement)
- Le dessin sera effectué avec une vitesse de 10 (plus rapide que la valeur par défaut de 8)

### Support des couches multiples (layers)

Une slide peut contenir plusieurs images superposées (layers), chacune positionnée à un endroit spécifique du canvas.

#### Propriétés d'une couche

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `image_path` | string | Chemin vers l'image de la couche | Requis |
| `position` | object | Position de la couche sur le canvas avec `x` et `y` | `{"x": 0, "y": 0}` |
| `z_index` | int | Ordre de superposition (plus grand = au-dessus) | 0 |
| `skip_rate` | int | Vitesse de dessin spécifique à cette couche | Hérite de la slide |
| `scale` | float | Échelle de l'image (1.0 = taille originale) | 1.0 |
| `opacity` | float | Opacité de la couche (0.0 à 1.0) | 1.0 |
| `mode` | string | Mode de dessin: `draw` (main), `eraser` (gomme), `static` (sans animation) | `draw` |
| `intelligent_eraser` | boolean | Efface le contenu superposé avant de dessiner (effet gomme naturel) | `false` |
| `entrance_animation` | object | Animation d'entrée (voir détails ci-dessous) | null |
| `exit_animation` | object | Animation de sortie (voir détails ci-dessous) | null |
| `morph` | object | Morphing depuis la couche précédente (voir détails ci-dessous) | null |
| `particle_effect` | object | Effet de particules (voir détails ci-dessous) | null |

##### Mode de dessin (`mode`)

- **`draw`** (par défaut): Dessine avec l'animation de la main
- **`eraser`**: Dessine avec l'animation d'une gomme (pour effet d'effacement)
- **`static`**: Affiche l'image sans animation de dessin (apparaît directement)

##### Gomme intelligente (`intelligent_eraser`)

Lorsque `intelligent_eraser: true`, la couche efface automatiquement le contenu superposé avant d'être dessinée, créant un effet naturel où le nouveau contenu remplace l'ancien.

**Fonctionnement:**
1. Détecte les pixels non-blancs (contenu réel) de la nouvelle couche
2. Efface ces zones sur le canvas existant
3. Dessine ensuite la nouvelle couche normalement

**Cas d'usage:**
- Créer des animations où de nouveaux éléments remplacent les anciens
- Gérer proprement les superpositions de couches
- Simuler un effet naturel de gomme lors de l'ajout de contenu

**Exemple:**
```json
{
  "image_path": "layer2.png",
  "position": {"x": 100, "y": 100},
  "z_index": 2,
  "intelligent_eraser": true
}
```

**Note:** Cette fonctionnalité est différente du `mode: "eraser"`. L'intelligent_eraser efface avant de dessiner, tandis que le mode eraser anime une gomme qui efface progressivement.

Voir [INTELLIGENT_ERASER.md](INTELLIGENT_ERASER.md) pour plus de détails.

##### Animations d'entrée et de sortie

Les animations peuvent être appliquées à l'apparition (`entrance_animation`) ou à la disparition (`exit_animation`) d'une couche.

**Propriétés:**
- `type`: Type d'animation (`fade_in`, `fade_out`, `slide_in_left`, `slide_in_right`, `slide_in_top`, `slide_in_bottom`, `slide_out_left`, `slide_out_right`, `slide_out_top`, `slide_out_bottom`, `zoom_in`, `zoom_out`, `none`)
- `duration`: Durée de l'animation en secondes (défaut: 0.5)

**Exemple:**
```json
"entrance_animation": {
  "type": "fade_in",
  "duration": 1.0
}
```

##### Morphing (`morph`)

Permet une transition fluide en morphing depuis la couche précédente.

**Propriétés:**
- `enabled`: Active le morphing (true/false)
- `duration`: Durée du morphing en secondes

**Exemple:**
```json
"morph": {
  "enabled": true,
  "duration": 0.5
| `type` | string | Type de couche: `image`, `text` | `image` |
| `camera` | object | Configuration de la caméra (zoom, position) | null |
| `animation` | object | Effets d'animation post-dessin (zoom_in, zoom_out) | null |

##### Configuration de la caméra (camera)

La caméra permet de zoomer et de se concentrer sur des zones spécifiques:

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `zoom` | float | Niveau de zoom (1.0 = normal, 2.0 = zoom x2) | 1.0 |
| `position` | object | Point focal avec `x` et `y` (0.0-1.0, 0.5 = centre) | `{"x": 0.5, "y": 0.5}` |

**Exemple:**
```json
"camera": {
  "zoom": 1.5,
  "position": {"x": 0.5, "y": 0.3}
}
```

##### Effets d'animation (animation)

Effets appliqués après le dessin de la couche:

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `type` | string | Type d'effet: `none`, `zoom_in`, `zoom_out` | `none` |
| `duration` | float | Durée de l'effet en secondes | 1.0 |
| `start_zoom` | float | Zoom de départ | 1.0 |
| `end_zoom` | float | Zoom final | 1.5 |
| `focus_position` | object | Point focal pendant le zoom avec `x` et `y` | `{"x": 0.5, "y": 0.5}` |

**Exemple zoom-in:**
```json
"animation": {
  "type": "zoom_in",
  "duration": 1.5,
  "start_zoom": 1.0,
  "end_zoom": 2.0,
  "focus_position": {"x": 0.5, "y": 0.5}
}
```

##### Effets de particules (particle_effect)

Les effets de particules enrichissent vos animations avec des effets visuels dynamiques.

**Propriétés communes:**

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `type` | string | Type d'effet: `confetti`, `sparkle`, `smoke`, `explosion`, `magic`, `custom` | Requis |
| `position` | array | Position `[x, y]` de l'effet | Centre du canvas |
| `duration` | float | Durée de l'effet en secondes | Dépend du type |

**Types d'effets disponibles:**

1. **Confetti** - Confettis de célébration
   - `burst_count`: Nombre de confettis (défaut: 100)
   
2. **Sparkle** - Étoiles scintillantes
   - `emission_rate`: Particules par seconde (défaut: 30)
   
3. **Smoke** - Traînée de fumée/poussière
   - `emission_rate`: Particules par seconde (défaut: 20)
   
4. **Explosion** - Effet d'explosion
   - `particle_count`: Nombre de particules (défaut: 50)
   
5. **Magic** - Étincelles magiques
   - `emission_rate`: Particules par seconde (défaut: 15)
   
6. **Custom** - Système personnalisé (voir PARTICLE_GUIDE.md)

**Exemples:**

Confettis:
```json
"particle_effect": {
  "type": "confetti",
  "position": [360, 100],
  "duration": 3.0,
  "burst_count": 150
}
```

Étincelles magiques:
```json
"particle_effect": {
  "type": "magic",
  "position": [360, 320],
  "duration": 4.0,
  "emission_rate": 25.0
}
```

Explosion:
```json
"particle_effect": {
  "type": "explosion",
  "position": [360, 320],
  "particle_count": 80
}
```

**Documentation complète:** Voir [PARTICLE_GUIDE.md](PARTICLE_GUIDE.md) pour tous les détails et [PARTICLE_QUICKSTART.md](PARTICLE_QUICKSTART.md) pour un démarrage rapide.

#### Exemple avec couches

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 3,
      "layers": [
        {
          "image_path": "background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8
        },
        {
          "image_path": "element1.png",
          "position": {"x": 100, "y": 150},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.5
        },
        {
          "image_path": "element2.png",
          "position": {"x": 500, "y": 200},
          "z_index": 3,
          "skip_rate": 20,
          "opacity": 0.8
        }
      ]
    }
  ]
}
```

Dans cet exemple :
- La slide 0 contient 3 images superposées
- L'image de fond est dessinée en premier (z_index: 1)
- element1.png est dessiné ensuite à la position (100, 150) avec une échelle de 50%
- element2.png est dessiné en dernier à la position (500, 200) avec 80% d'opacité
- Chaque couche a sa propre vitesse de dessin

#### Exemple avec les nouvelles fonctionnalités

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8,
          "mode": "draw"
        },
        {
          "image_path": "element_to_erase.png",
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

Dans cet exemple avancé :
- Le fond est dessiné normalement avec la main
- Un élément est "effacé" avec l'animation d'une gomme et apparaît avec un fondu
- Un logo apparaît statiquement (sans main) avec un zoom-in et disparaît avec un fondu
- Un texte apparaît avec un morphing depuis la couche précédente

**Note:** Lorsque `layers` est spécifié, l'image de la ligne de commande pour cette slide n'est pas utilisée. Toutes les images doivent être définies dans les couches.

## Section `transitions`

Permet de définir des transitions personnalisées entre les slides.

### Propriétés disponibles

| Propriété | Type | Description | Par défaut |
|-----------|------|-------------|------------|
| `after_slide` | int | Index de la slide après laquelle appliquer la transition (commence à 0) | Requis |
| `type` | string | Type de transition : `none`, `fade`, `wipe`, `push_left`, `push_right`, `iris` | Valeur globale `--transition` |
| `duration` | float | Durée de la transition en secondes | Valeur globale `--transition-duration` |
| `pause_before` | float | Durée de pause avant la transition (en secondes) | 0 |

### Exemple

```json
{
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 0.8,
      "pause_before": 1.0
    }
  ]
}
```

Dans cet exemple :
- Après la première slide (index 0), il y aura une pause de 1 seconde
- Puis une transition de type "fade" d'une durée de 0.8 secondes vers la slide suivante

## Types de transitions disponibles

- **`none`** : Pas de transition (changement instantané)
- **`fade`** : Fondu enchaîné entre les slides
- **`wipe`** : Balayage de gauche à droite
- **`push_left`** : Pousse la slide actuelle vers la gauche
- **`push_right`** : Pousse la slide actuelle vers la droite
- **`iris`** : Transition en cercle qui s'agrandit depuis le centre

## Utilisation

### Créer un fichier de configuration

1. Créez un fichier JSON (par exemple `my_config.json`)
2. Définissez vos paramètres personnalisés
3. Utilisez le paramètre `--config` pour l'appliquer

```bash
python whiteboard_animator.py slide1.png slide2.png slide3.png --config my_config.json
```

### Exemple d'utilisation avancée

```bash
# Configuration complète avec paramètres globaux et personnalisés
python whiteboard_animator.py slide1.png slide2.png slide3.png \
  --config my_config.json \
  --frame-rate 30 \
  --split-len 15 \
  --export-json
```

Dans cet exemple :
- Le fichier `my_config.json` définit les paramètres personnalisés par slide
- Les paramètres globaux (`--frame-rate`, `--split-len`) s'appliquent à toutes les slides sauf si surchargés dans le fichier de configuration
- Les données d'animation sont exportées au format JSON

## Comportement par défaut

Si une propriété n'est pas spécifiée dans le fichier de configuration :
- Les valeurs des paramètres CLI globaux seront utilisées
- Si aucun paramètre CLI n'est spécifié, les valeurs par défaut du programme seront utilisées

## Exemples de cas d'usage

### Cas 1 : Vitesses de dessin différentes

```json
{
  "slides": [
    {
      "index": 0,
      "skip_rate": 5
    },
    {
      "index": 1,
      "skip_rate": 20
    },
    {
      "index": 2,
      "skip_rate": 10
    }
  ]
}
```

La première slide sera dessinée lentement (5), la deuxième rapidement (20), et la troisième à vitesse moyenne (10).

### Cas 2 : Durées d'affichage personnalisées

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 1
    },
    {
      "index": 1,
      "duration": 5
    },
    {
      "index": 2,
      "duration": 2
    }
  ]
}
```

La première slide s'affiche 1 seconde, la deuxième 5 secondes, et la troisième 2 secondes après leur dessin.

### Cas 3 : Transitions variées avec pauses

```json
{
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 0.5,
      "pause_before": 2.0
    },
    {
      "after_slide": 1,
      "type": "iris",
      "duration": 1.5,
      "pause_before": 1.0
    }
  ]
}
```

- Après la slide 1 : pause de 2 secondes, puis transition fade de 0.5 seconde
- Après la slide 2 : pause de 1 seconde, puis transition iris de 1.5 secondes

### Cas 4 : Configuration complète

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "skip_rate": 8
    },
    {
      "index": 1,
      "duration": 3,
      "skip_rate": 15
    },
    {
      "index": 2,
      "duration": 4,
      "skip_rate": 10
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 0.8,
      "pause_before": 1.5
    },
    {
      "after_slide": 1,
      "type": "wipe",
      "duration": 1.0,
      "pause_before": 2.0
    }
  ]
}
```

Cet exemple combine tous les paramètres :
- Chaque slide a sa propre durée d'affichage et vitesse de dessin
- Chaque transition a son propre type, durée et temps de pause

### Cas 5 : Utilisation de couches multiples (layers)

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 4,
      "layers": [
        {
          "image_path": "examples/background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 5
        },
        {
          "image_path": "examples/logo.png",
          "position": {"x": 50, "y": 50},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.3
        },
        {
          "image_path": "examples/text.png",
          "position": {"x": 200, "y": 400},
          "z_index": 3,
          "skip_rate": 20,
          "opacity": 0.9
        }
      ]
    },
    {
      "index": 1,
      "duration": 3,
      "skip_rate": 10
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 0.5
    }
  ]
}
```

Dans cet exemple :
- La première slide est composée de 3 couches superposées :
  - Un fond dessiné lentement (skip_rate: 5)
  - Un logo à 30% de sa taille positionné en haut à gauche
  - Du texte semi-transparent positionné plus bas
- Les couches sont dessinées selon leur ordre z_index (1, 2, 3)
- La deuxième slide utilise une seule image (celle fournie en ligne de commande)
- Une transition fade relie les deux slides

**Important:** Quand vous utilisez des couches (layers), vous devez quand même fournir au moins une image en ligne de commande pour définir le nombre de slides, mais cette image sera ignorée pour les slides avec configuration de couches.

### Cas 6 : Contrôles de caméra et animations

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "examples/diagram.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10,
          "camera": {
            "zoom": 1.5,
            "position": {"x": 0.5, "y": 0.5}
          },
          "animation": {
            "type": "zoom_in",
            "duration": 1.5,
            "start_zoom": 1.5,
            "end_zoom": 2.0,
            "focus_position": {"x": 0.7, "y": 0.4}
          }
        }
      ]
    }
  ]
}
```

Dans cet exemple :
- La couche est dessinée avec un zoom de caméra de 1.5x centré
- Après le dessin, un effet de zoom progressif est appliqué
- Le zoom passe de 1.5x à 2.0x sur 1.5 secondes
- Le focus se déplace vers la position (0.7, 0.4) pendant le zoom

### Cas 7 : Système de caméra avancé avec séquences multiples

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {
          "image_path": "examples/complex_diagram.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.5
        },
        {
          "zoom": 1.8,
          "position": {"x": 0.3, "y": 0.25},
          "duration": 2.5,
          "transition_duration": 1.0,
          "easing": "ease_out"
        },
        {
          "zoom": 1.8,
          "position": {"x": 0.7, "y": 0.75},
          "duration": 2.5,
          "transition_duration": 1.2,
          "easing": "ease_out"
        },
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 1.5,
          "transition_duration": 1.0,
          "easing": "ease_out"
        }
      ]
    }
  ]
}
```

Dans cet exemple :
- La slide utilise le **système de caméra avancé** avec 4 caméras
- Chaque caméra a sa propre durée d'affichage (duration)
- Les transitions entre caméras sont fluides avec fonction d'easing
- Camera 1: Vue d'ensemble pendant 2.5s
- Camera 2: Zoom sur le coin supérieur gauche avec transition de 1s
- Camera 3: Pan vers le coin inférieur droit avec transition de 1.2s
- Camera 4: Retour à la vue d'ensemble avec transition de 1s
- Les fonctions d'easing ("ease_out") rendent les mouvements plus naturels

**Propriétés des caméras:**
- `zoom`: Niveau de zoom (1.0 = normal, 2.0 = zoom x2)
- `position`: Position focale avec x, y (0.0-1.0, 0.5 = centre)
- `size`: Taille optionnelle de la caméra (ex: `{"width": 2275, "height": 1280}`)
- `duration`: Durée d'affichage de cette caméra en secondes
- `transition_duration`: Durée de transition depuis la caméra précédente (défaut: 0)
- `easing`: Type de transition: "linear", "ease_in", "ease_out", "ease_in_out", "ease_in_cubic", "ease_out_cubic" (défaut: "ease_out")

📖 **Pour plus de détails**, voir [ADVANCED_CAMERA_GUIDE.md](ADVANCED_CAMERA_GUIDE.md)

## Notes importantes

1. **Index des slides** : Les index commencent à 0 (première slide = index 0)
2. **Index des transitions** : `after_slide` indique l'index de la slide AVANT la transition
3. **Compatibilité** : Si vous spécifiez des paramètres globaux via CLI ET un fichier de configuration, les valeurs du fichier de configuration ont la priorité pour les slides spécifiées
4. **Slides non configurées** : Les slides non mentionnées dans le fichier de configuration utiliseront les paramètres globaux
5. **Validation** : Le programme ne valide pas strictement la structure JSON, assurez-vous que votre fichier est bien formaté

## Dépannage

### Erreur "Fichier de configuration introuvable"
Vérifiez que le chemin vers votre fichier JSON est correct et que le fichier existe.

### Les paramètres ne sont pas appliqués
Assurez-vous que :
- Le format JSON est valide (utilisez un validateur JSON en ligne)
- Les index correspondent bien à vos slides (commence à 0)
- Les types de transition sont bien orthographiés

### Transitions incorrectes
Vérifiez que `after_slide` pointe vers le bon index (0 pour après la première slide, 1 pour après la deuxième, etc.)
