# 📚 Guide Complet - Whiteboard-CLI

**Documentation complète pour exploiter au maximum whiteboard-cli**

> Ce guide couvre TOUTES les fonctionnalités, TOUTES les commandes CLI, et TOUS les paramètres de configuration JSON disponibles.

---

## Table des matières

1. [Introduction et Installation](#1-introduction-et-installation)
2. [Commandes CLI - Référence Complète](#2-commandes-cli---référence-complète)
3. [Format de Configuration JSON Complet](#3-format-de-configuration-json-complet)
4. [Fonctionnalités Avancées](#4-fonctionnalités-avancées)
5. [Exemples Pratiques par Cas d'Usage](#5-exemples-pratiques-par-cas-dusage)
6. [Workflows et Meilleures Pratiques](#6-workflows-et-meilleures-pratiques)
7. [Guide de Référence Rapide](#7-guide-de-référence-rapide)

---

## 1. Introduction et Installation

### Qu'est-ce que Whiteboard-CLI ?

Whiteboard-CLI est un outil puissant pour créer des vidéos d'animation style "tableau blanc" (whiteboard animation) à partir d'images. Il offre des fonctionnalités professionnelles incluant :

- ✅ Animation de dessin automatique avec main réaliste
- ✅ Support multi-couches (layers) pour compositions complexes
- ✅ Système de caméra cinématique avec zoom et pan
- ✅ Effets de particules (confettis, étincelles, explosions, fumée)
- ✅ Support audio complet (musique, effets sonores, voix off)
- ✅ Animations de texte dynamiques
- ✅ Formes géométriques vectorielles
- ✅ Transitions entre slides
- ✅ Export multi-formats (MP4, GIF, WebM, PNG)
- ✅ Presets pour réseaux sociaux (TikTok, YouTube, Instagram)
- ✅ Timeline et synchronisation avancée

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/armelwanes/whiteboard-cli.git
cd whiteboard-cli

# Dépendances requises
pip install opencv-python numpy pillow

# Dépendances fortement recommandées
pip install av              # Pour conversion H.264 et combinaison de vidéos
pip install fontTools       # Pour support de polices avancé

# Dépendances optionnelles
pip install pydub           # Pour support audio
pip install arabic-reshaper python-bidi  # Pour texte RTL (arabe, hébreu)
```

**Prérequis système:**
- Python 3.7+
- FFmpeg (pour l'export vidéo)
- 4GB+ RAM recommandé pour vidéos HD

---

## 2. Commandes CLI - Référence Complète

### Syntaxe de base

```bash
python whiteboard_animator.py [image_paths...] [options]
```

### Arguments positionnels

#### `image_paths` (optionnel)

Chemin(s) vers les image(s) à animer. Supporte plusieurs formats :

```bash
# Une seule image
python whiteboard_animator.py image.png

# Plusieurs images (génère une vidéo combinée)
python whiteboard_animator.py slide1.png slide2.png slide3.png

# Peut être omis si configuration JSON fournie
python whiteboard_animator.py --config my_config.json
```

**Formats supportés:** PNG, JPG, JPEG, BMP, GIF (première frame), TIFF

---

### 2.1 Paramètres de Base

#### `--split-len SPLIT_LEN`

Taille de la grille pour le dessin. Affecte la précision et la vitesse de l'animation.

- **Par défaut:** 15
- **Valeurs recommandées:** Diviseurs de la résolution cible (10, 15, 20, 30)
- **Impact:** Plus petit = plus précis mais plus lent

```bash
# Dessin fin et précis
python whiteboard_animator.py image.png --split-len 10

# Dessin rapide et stylisé
python whiteboard_animator.py image.png --split-len 30

# Trouver les valeurs recommandées pour votre image
python whiteboard_animator.py image.png --get-split-lens
```

#### `--frame-rate FRAME_RATE`

Images par seconde (FPS) de la vidéo.

- **Par défaut:** 30
- **Valeurs communes:** 24 (cinéma), 30 (standard), 60 (haute fluidité)

```bash
python whiteboard_animator.py image.png --frame-rate 60
```

#### `--skip-rate SKIP_RATE`

Vitesse de dessin. Contrôle combien de tuiles sont dessinées par frame.

- **Par défaut:** 8
- **Plage:** 1-50+
- **Impact:** Plus grand = animation plus rapide

```bash
# Dessin très lent (détaillé)
python whiteboard_animator.py image.png --skip-rate 3

# Dessin rapide
python whiteboard_animator.py image.png --skip-rate 20
```

#### `--duration DURATION`

**Durée TOTALE de la slide en secondes** (animation + affichage final).

- **Par défaut:** 3
- **Important:** Inclut le temps d'animation ET le temps d'affichage final
- Si l'animation dépasse cette durée, elle sera utilisée comme durée totale

```bash
# Slide de 10 secondes au total
python whiteboard_animator.py image.png --duration 10

# Si l'animation prend 4s, l'image finale sera affichée 6s
# Si l'animation prend 12s, la durée totale sera 12s
```

**Voir [DURATION_GUIDE.md](DURATION_GUIDE.md) pour plus de détails**

---

### 2.2 Qualité et Formats

#### `--quality 0-51`

Qualité vidéo (paramètre CRF de H.264).

- **Par défaut:** 18 (visually lossless)
- **Plage:** 0-51 (plus bas = meilleure qualité)
- **Recommandations:**
  - `15` : Ultra qualité (fichiers très volumineux)
  - `18` : Qualité visuelle maximale (recommandé)
  - `23` : Haute qualité (bon compromis)
  - `28` : Qualité moyenne (fichiers légers)

```bash
# Qualité maximale pour archivage
python whiteboard_animator.py image.png --quality 15

# Qualité standard pour web
python whiteboard_animator.py image.png --quality 23
```

#### `--aspect-ratio {original,1:1,16:9,9:16}`

Ratio d'aspect de la vidéo finale.

- **Par défaut:** original
- **Options:**
  - `original` : Conserve le ratio de l'image source
  - `1:1` : Carré (Instagram, profils)
  - `16:9` : Paysage HD (YouTube, télévision)
  - `9:16` : Vertical (Stories, Reels, TikTok)

```bash
# Format YouTube
python whiteboard_animator.py image.png --aspect-ratio 16:9

# Format TikTok/Reels
python whiteboard_animator.py image.png --aspect-ratio 9:16

# Format Instagram feed
python whiteboard_animator.py image.png --aspect-ratio 1:1
```

#### `--export-formats FORMAT [FORMAT ...]`

Formats d'export supplémentaires en plus du MP4.

- **Options:** `gif`, `webm`, `png`, `png-sequence`, `webm-alpha`, `transparent`, `lossless`
- **Peut spécifier plusieurs formats**

```bash
# Export GIF animé
python whiteboard_animator.py image.png --export-formats gif

# Export multiple
python whiteboard_animator.py image.png --export-formats gif webm png

# Export avec transparence (overlay)
python whiteboard_animator.py image.png --export-formats webm-alpha

# Export sans perte (archivage)
python whiteboard_animator.py image.png --export-formats lossless
```

**Voir [EXPORT_FORMATS_GUIDE.md](EXPORT_FORMATS_GUIDE.md) pour détails complets**

#### `--social-preset {youtube,youtube-shorts,tiktok,instagram-feed,instagram-story,instagram-reel,facebook,twitter,linkedin}`

Presets optimisés pour plateformes de médias sociaux.

```bash
# TikTok (1080x1920, 9:16)
python whiteboard_animator.py image.png --social-preset tiktok

# YouTube standard (1920x1080, 16:9)
python whiteboard_animator.py image.png --social-preset youtube

# YouTube Shorts (1080x1920, 9:16)
python whiteboard_animator.py image.png --social-preset youtube-shorts

# Instagram Reels (1080x1920, 9:16)
python whiteboard_animator.py image.png --social-preset instagram-reel

# Instagram Feed (1080x1080, 1:1)
python whiteboard_animator.py image.png --social-preset instagram-feed

# Lister tous les presets
python whiteboard_animator.py --list-presets
```

---

### 2.3 Watermark (Filigrane)

#### `--watermark WATERMARK`

Chemin vers l'image de filigrane à appliquer.

```bash
python whiteboard_animator.py image.png --watermark logo.png
```

#### `--watermark-position {top-left,top-right,bottom-left,bottom-right,center}`

Position du filigrane sur la vidéo.

- **Par défaut:** bottom-right

```bash
python whiteboard_animator.py image.png --watermark logo.png --watermark-position top-right
```

#### `--watermark-opacity WATERMARK_OPACITY`

Opacité du filigrane (0.0 = invisible, 1.0 = opaque).

- **Par défaut:** 0.5

```bash
python whiteboard_animator.py image.png --watermark logo.png --watermark-opacity 0.3
```

#### `--watermark-scale WATERMARK_SCALE`

Échelle du filigrane par rapport à la largeur de la vidéo.

- **Par défaut:** 0.1 (10% de la largeur)

```bash
python whiteboard_animator.py image.png --watermark logo.png --watermark-scale 0.15
```

**Exemple complet:**
```bash
python whiteboard_animator.py presentation.png \
  --watermark company_logo.png \
  --watermark-position bottom-right \
  --watermark-opacity 0.6 \
  --watermark-scale 0.12
```

---

### 2.4 Transitions

#### `--transition {none,fade,wipe,push_left,push_right,iris}`

Type de transition entre slides.

- **Par défaut:** none
- **Options:**
  - `none` : Pas de transition (changement instantané)
  - `fade` : Fondu enchaîné
  - `wipe` : Balayage de gauche à droite
  - `push_left` : Pousse la slide vers la gauche
  - `push_right` : Pousse la slide vers la droite
  - `iris` : Cercle qui s'agrandit depuis le centre

```bash
python whiteboard_animator.py slide1.png slide2.png --transition fade
```

#### `--transition-duration TRANSITION_DURATION`

Durée de la transition en secondes.

- **Par défaut:** 0.5

```bash
python whiteboard_animator.py slide1.png slide2.png \
  --transition fade \
  --transition-duration 1.0
```

**Voir [TRANSITIONS.md](TRANSITIONS.md) pour détails complets**

---

### 2.5 Configuration JSON

#### `--config CONFIG`

Chemin vers fichier JSON de configuration personnalisée.

Permet de définir des paramètres individuels pour chaque slide :
- Durée personnalisée
- Vitesse de dessin
- Couches multiples (layers)
- Animations de caméra
- Effets de particules
- Et bien plus...

```bash
python whiteboard_animator.py slide1.png slide2.png --config my_config.json
```

**Voir Section 3 pour format JSON complet**

---

### 2.6 Export de Données

#### `--export-json`

Exporte les données d'animation au format JSON.

Génère un fichier JSON contenant :
- Séquence de dessin frame par frame
- Positions de la main
- Coordonnées des tuiles
- Métadonnées de l'animation

```bash
# Export avec vidéo
python whiteboard_animator.py image.png --export-json

# Multiple images (un JSON par image)
python whiteboard_animator.py img1.png img2.png img3.png --export-json
```

**Voir [EXPORT_FORMAT.md](EXPORT_FORMAT.md) pour format complet**

#### `--get-split-lens`

Affiche les valeurs `split_len` recommandées pour une image.

```bash
python whiteboard_animator.py image.png --get-split-lens
```

---

### 2.7 Performance et Optimisation

#### `--preview`

Mode preview rapide pour tests (50% résolution, qualité réduite).

```bash
python whiteboard_animator.py --config video.json --preview
```

#### `--quality-preset {preview,draft,standard,high,ultra}`

Préréglages de qualité globaux.

- `preview` : Test rapide (CRF 28, 50% résolution)
- `draft` : Brouillon (CRF 28, 75% résolution)
- `standard` : Standard (CRF 23, 100% résolution)
- `high` : Haute qualité (CRF 18, 100% résolution)
- `ultra` : Ultra qualité (CRF 15, 100% résolution)

```bash
python whiteboard_animator.py image.png --quality-preset ultra
```

#### `--enable-checkpoints`

Active les points de contrôle pour reprendre les rendus interrompus.

```bash
python whiteboard_animator.py --config long_video.json --enable-checkpoints
```

#### `--resume CHECKPOINT_ID`

Reprend un rendu depuis un checkpoint.

```bash
# Lister les checkpoints disponibles
python whiteboard_animator.py --list-checkpoints

# Reprendre depuis un checkpoint
python whiteboard_animator.py --resume a1b2c3d4e5f6g7h8
```

#### `--list-checkpoints`

Affiche tous les checkpoints disponibles.

```bash
python whiteboard_animator.py --list-checkpoints
```

#### `--background`

Exécute le rendu en arrière-plan avec fichier de statut.

Génère un fichier `render_status.json` pour suivre la progression.

```bash
python whiteboard_animator.py --config video.json --background
```

#### `--batch CONFIG_FILE [CONFIG_FILE ...]`

Mode batch : traite plusieurs fichiers de configuration en série.

```bash
python whiteboard_animator.py --batch video1.json video2.json video3.json
```

#### `--batch-parallel`

Active le traitement parallèle en mode batch.

```bash
python whiteboard_animator.py --batch video1.json video2.json video3.json --batch-parallel
```

#### `--threads N`

Nombre de threads pour traitement parallèle.

```bash
python whiteboard_animator.py --batch *.json --batch-parallel --threads 4
```

#### `--memory-efficient`

Active le mode optimisation mémoire pour grandes vidéos.

```bash
python whiteboard_animator.py --config large_video.json --memory-efficient
```

**Voir [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) pour guide complet**

---

### 2.8 Audio

#### `--audio-config AUDIO_CONFIG`

Chemin vers fichier JSON de configuration audio complète.

```bash
python whiteboard_animator.py --config video.json --audio-config audio.json
```

#### `--background-music BACKGROUND_MUSIC`

Chemin vers fichier audio pour musique de fond.

Formats supportés : MP3, WAV, OGG, M4A, FLAC

```bash
python whiteboard_animator.py image.png --background-music music.mp3
```

#### `--music-volume MUSIC_VOLUME`

Volume de la musique de fond (0.0 à 1.0).

- **Par défaut:** 0.5

```bash
python whiteboard_animator.py image.png \
  --background-music music.mp3 \
  --music-volume 0.3
```

#### `--music-fade-in MUSIC_FADE_IN`

Durée du fade-in de la musique en secondes.

```bash
python whiteboard_animator.py image.png \
  --background-music music.mp3 \
  --music-fade-in 2.0
```

#### `--music-fade-out MUSIC_FADE_OUT`

Durée du fade-out de la musique en secondes.

```bash
python whiteboard_animator.py image.png \
  --background-music music.mp3 \
  --music-fade-out 3.0
```

#### `--enable-typewriter-sound`

Active les sons de machine à écrire pour animations de texte.

```bash
python whiteboard_animator.py --config text_video.json --enable-typewriter-sound
```

#### `--enable-drawing-sound`

Active les sons de dessin pour animations de tracé.

```bash
python whiteboard_animator.py image.png --enable-drawing-sound
```

#### `--audio-output AUDIO_OUTPUT`

Chemin pour exporter l'audio mixé séparément.

```bash
python whiteboard_animator.py --config video.json \
  --audio-config audio.json \
  --audio-output final_audio.wav
```

**Voir [AUDIO_GUIDE.md](AUDIO_GUIDE.md) pour guide complet**

---

## 3. Format de Configuration JSON Complet

### Structure de base

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "skip_rate": 8,
      "layers": [...],
      "cameras": [...]
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 0.5,
      "pause_before": 1.0
    }
  ]
}
```

---

### 3.1 Section `slides`

Configuration individuelle de chaque slide.

#### Propriétés principales d'une slide

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `index` | int | Index de la slide (commence à 0) | **Requis** |
| `duration` | float | Durée TOTALE en secondes (animation + affichage) | CLI `--duration` ou 3 |
| `skip_rate` | int | Vitesse de dessin (plus grand = plus rapide) | CLI `--skip-rate` ou 8 |
| `bg_skip_rate` | int | Vitesse de dessin de l'arrière-plan | CLI `--bg-skip-rate` ou 20 |
| `layers` | array | Liste des couches d'images/texte/formes | `null` |
| `cameras` | array | Séquence de caméras avec transitions | `null` |

**Exemple minimal:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "skip_rate": 12
    }
  ]
}
```

---

### 3.2 Couches (Layers)

Les couches permettent de superposer plusieurs éléments (images, texte, formes) sur une même slide.

#### Types de couches

1. **Couche d'image** (`type` non spécifié ou omis)
2. **Couche de texte** (`type: "text"`)
3. **Couche de forme** (`type: "shape"`)

#### Propriétés communes à toutes les couches

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `type` | string | Type de couche : `"text"`, `"shape"`, ou omis pour image | image |
| `z_index` | int | Ordre de superposition (plus grand = au-dessus) | 0 |
| `position` | object | Position `{"x": 0, "y": 0}` sur le canvas | `{"x": 0, "y": 0}` |
| `scale` | float | Échelle (1.0 = taille originale) | 1.0 |
| `opacity` | float | Opacité (0.0 = invisible, 1.0 = opaque) | 1.0 |
| `skip_rate` | int | Vitesse de dessin de cette couche | Hérite de la slide |
| `mode` | string | Mode d'animation : `"draw"`, `"eraser"`, `"static"` | `"draw"` |
| `camera` | object | Contrôles de caméra pour cette couche | `null` |
| `animation` | object | Animation post-dessin (zoom, rotation, etc.) | `null` |
| `entrance` | object | Animation d'entrée | `null` |
| `exit` | object | Animation de sortie | `null` |
| `morph` | object | Effet de morphing | `null` |
| `particle_effect` | object | Effet de particules | `null` |
| `push_animation` | object | Animation "hand push" | `null` |

---

### 3.3 Couches d'Image

Pour utiliser des images dans les couches.

#### Propriétés spécifiques

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `image_path` | string | Chemin vers l'image | **Requis** |

**Exemple complet:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 5,
          "scale": 1.0,
          "opacity": 1.0,
          "mode": "draw"
        },
        {
          "image_path": "logo.png",
          "position": {"x": 100, "y": 50},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.5,
          "opacity": 0.9,
          "mode": "draw",
          "entrance": {
            "type": "fade_in",
            "duration": 1.0
          }
        }
      ]
    }
  ]
}
```

---

### 3.4 Couches de Texte

Pour générer du texte dynamiquement.

#### Propriétés spécifiques

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `type` | string | Doit être `"text"` | **Requis** |
| `text_config` | object | Configuration du texte | **Requis** |

#### Configuration `text_config`

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `text` | string | Texte à afficher (utilisez `\n` pour sauts de ligne) | **Requis** |
| `font` | string | Nom de la police système | `"DejaVuSans"` |
| `size` | int | Taille de la police en pixels | `48` |
| `color` | array/string | Couleur RGB `[R, G, B]` ou hex `"#FF0000"` | `[0, 0, 0]` |
| `style` | string | Style : `"normal"`, `"bold"`, `"italic"`, `"bold_italic"` | `"normal"` |
| `line_height` | float | Espacement des lignes | `1.5` |
| `align` | string | Alignement : `"left"`, `"center"`, `"right"` | `"center"` |
| `use_svg_paths` | bool | Utiliser animation SVG path-based | `false` |
| `position` | object | Position absolue `{"x": 640, "y": 360}` | Centre |

**Exemple:**
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
            "text": "Bonjour!\nCeci est un texte\navec animation",
            "font": "Arial",
            "size": 64,
            "color": [0, 100, 255],
            "style": "bold",
            "line_height": 1.8,
            "align": "center"
          },
          "entrance": {
            "type": "slide_in",
            "duration": 1.0,
            "direction": "bottom"
          }
        }
      ]
    }
  ]
}
```

**Voir [TEXT_LAYERS_GUIDE.md](TEXT_LAYERS_GUIDE.md) pour guide complet**

---

### 3.5 Couches de Formes

Pour créer des formes géométriques vectorielles.

#### Propriétés spécifiques

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `type` | string | Doit être `"shape"` | **Requis** |
| `shape_config` | object | Configuration de la forme | **Requis** |

#### Configuration `shape_config`

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `shape` | string | Type : `"circle"`, `"rectangle"`, `"triangle"`, `"polygon"`, `"line"`, `"arrow"` | **Requis** |
| `color` | string | Couleur de contour (hex) | `"#000000"` |
| `fill_color` | string | Couleur de remplissage (hex, `null` = pas de remplissage) | `null` |
| `stroke_width` | int | Épaisseur du trait | `2` |
| `position` | object | Position `{"x": 640, "y": 360}` | Centre |
| `size` | int/array | Taille (cercle) ou `[largeur, hauteur]` (rectangle) | Requis |
| `radius` | int | Rayon (cercle) | Requis pour cercle |
| `sides` | int | Nombre de côtés (polygone) | Requis pour polygone |
| `start` | array | Point de départ `[x, y]` (ligne/flèche) | Requis pour ligne/flèche |
| `end` | array | Point d'arrivée `[x, y]` (ligne/flèche) | Requis pour ligne/flèche |
| `arrow_size` | int | Taille de la tête de flèche | `20` |

**Exemples:**

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "type": "shape",
          "z_index": 1,
          "skip_rate": 10,
          "shape_config": {
            "shape": "circle",
            "color": "#0066CC",
            "fill_color": "#99CCFF",
            "stroke_width": 3,
            "position": {"x": 640, "y": 360},
            "size": 100
          }
        },
        {
          "type": "shape",
          "z_index": 2,
          "skip_rate": 8,
          "shape_config": {
            "shape": "rectangle",
            "color": "#FF6600",
            "fill_color": "#FFCC99",
            "stroke_width": 4,
            "position": {"x": 400, "y": 300},
            "size": [200, 150]
          }
        },
        {
          "type": "shape",
          "z_index": 3,
          "skip_rate": 12,
          "shape_config": {
            "shape": "arrow",
            "color": "#00AA00",
            "stroke_width": 5,
            "start": [200, 500],
            "end": [1000, 500],
            "arrow_size": 30
          }
        }
      ]
    }
  ]
}
```

**Voir [SHAPES_GUIDE.md](SHAPES_GUIDE.md) pour guide complet**

---

### 3.6 Modes de Couche

Le paramètre `mode` contrôle comment une couche est animée.

| Mode | Description | Usage |
|------|-------------|-------|
| `draw` | Dessin progressif standard | Animation normale |
| `eraser` | Gomme qui efface progressivement | Effets de révélation |
| `static` | Apparaît instantanément (pas d'animation) | Éléments de fond |

**Exemple:**
```json
{
  "layers": [
    {
      "image_path": "background.png",
      "z_index": 1,
      "mode": "static"
    },
    {
      "image_path": "element.png",
      "z_index": 2,
      "mode": "draw",
      "skip_rate": 10
    },
    {
      "image_path": "overlay.png",
      "z_index": 3,
      "mode": "eraser",
      "skip_rate": 15
    }
  ]
}
```

**Voir [INTELLIGENT_ERASER.md](INTELLIGENT_ERASER.md) pour détails sur le mode eraser**

---

### 3.7 Animations d'Entrée et de Sortie

#### Propriété `entrance`

Animation d'apparition de la couche.

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `type` | string | Type d'animation (voir ci-dessous) | **Requis** |
| `duration` | float | Durée en secondes | `1.0` |
| `direction` | string | Direction (pour `slide_in`) : `"top"`, `"bottom"`, `"left"`, `"right"` | `"bottom"` |
| `delay` | float | Délai avant démarrage | `0.0` |

**Types disponibles:**
- `fade_in` : Fondu progressif
- `slide_in` : Glissement depuis une direction
- `zoom_in` : Zoom depuis petit vers normal
- `pop_in` : Apparition avec rebond
- `spiral_in` : Spirale entrante

#### Propriété `exit`

Animation de disparition de la couche.

Mêmes propriétés que `entrance`, types disponibles :
- `fade_out`
- `slide_out`
- `zoom_out`
- `pop_out`
- `spiral_out`

**Exemple:**
```json
{
  "layers": [
    {
      "image_path": "logo.png",
      "z_index": 1,
      "entrance": {
        "type": "slide_in",
        "duration": 1.5,
        "direction": "top",
        "delay": 0.5
      },
      "exit": {
        "type": "fade_out",
        "duration": 1.0
      }
    }
  ]
}
```

---

### 3.8 Morphing

Transformation progressive d'une couche vers une autre.

#### Propriété `morph`

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `target_layer_index` | int | Index de la couche cible dans le même slide | **Requis** |
| `duration` | float | Durée de la transformation | `2.0` |
| `delay` | float | Délai avant démarrage | `0.0` |
| `easing` | string | Fonction d'interpolation | `"ease_in_out"` |

**Fonctions d'easing disponibles:**
- `linear`
- `ease_in`
- `ease_out`
- `ease_in_out`
- `ease_in_cubic`
- `ease_out_cubic`

**Exemple:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "form1.png",
          "z_index": 1,
          "morph": {
            "target_layer_index": 1,
            "duration": 2.5,
            "delay": 1.0,
            "easing": "ease_in_out"
          }
        },
        {
          "image_path": "form2.png",
          "z_index": 1,
          "mode": "static",
          "opacity": 0
        }
      ]
    }
  ]
}
```

---

### 3.9 Contrôles de Caméra

#### Caméra par Couche

Applique un zoom/position de caméra pendant le dessin d'une couche.

**Propriété `camera`:**

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `zoom` | float | Niveau de zoom (1.0 = normal) | `1.0` |
| `position` | object | Position focus `{"x": 0.5, "y": 0.5}` (0-1, relatif) | `{"x": 0.5, "y": 0.5}` |

**Exemple:**
```json
{
  "layers": [
    {
      "image_path": "diagram.png",
      "z_index": 1,
      "camera": {
        "zoom": 1.8,
        "position": {"x": 0.3, "y": 0.25}
      }
    }
  ]
}
```

---

### 3.10 Système de Caméra Avancé

Séquences de caméras multiples avec transitions fluides.

#### Propriété `cameras` (au niveau slide)

Array de séquences de caméra.

**Propriétés d'une caméra:**

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `zoom` | float | Niveau de zoom | `1.0` |
| `position` | object | Position `{"x": 0.5, "y": 0.5}` | Centre |
| `duration` | float | Durée de maintien de cette caméra | **Requis** |
| `transition_duration` | float | Durée de transition vers cette caméra | `0.0` |
| `easing` | string | Fonction d'interpolation | `"linear"` |
| `camera_size` | array | Taille personnalisée `[largeur, hauteur]` | Résolution cible |

**Exemple complet:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {
          "image_path": "diagram.png",
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
          "duration": 3.0,
          "transition_duration": 1.0,
          "easing": "ease_out"
        },
        {
          "zoom": 2.2,
          "position": {"x": 0.7, "y": 0.6},
          "duration": 2.5,
          "transition_duration": 1.5,
          "easing": "ease_in_out"
        },
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0,
          "transition_duration": 1.0,
          "easing": "ease_in"
        }
      ]
    }
  ]
}
```

**Voir [ADVANCED_CAMERA_GUIDE.md](ADVANCED_CAMERA_GUIDE.md) pour guide complet**

---

### 3.11 Animations Post-Dessin

Animations appliquées après le dessin complet d'une couche.

#### Propriété `animation`

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `type` | string | Type : `"zoom_in"`, `"zoom_out"` | **Requis** |
| `duration` | float | Durée de l'animation | `2.0` |
| `start_zoom` | float | Zoom initial | `1.0` |
| `end_zoom` | float | Zoom final | `2.0` |
| `focus_position` | object | Point de focus `{"x": 0.5, "y": 0.5}` | Centre |
| `delay` | float | Délai après dessin | `0.0` |

**Exemple:**
```json
{
  "layers": [
    {
      "image_path": "product.png",
      "z_index": 1,
      "animation": {
        "type": "zoom_in",
        "duration": 2.0,
        "start_zoom": 1.0,
        "end_zoom": 2.5,
        "focus_position": {"x": 0.7, "y": 0.4},
        "delay": 0.5
      }
    }
  ]
}
```

**Voir [CAMERA_ANIMATION_GUIDE.md](CAMERA_ANIMATION_GUIDE.md) pour détails**

---

### 3.12 Effets de Particules

Enrichissez vos animations avec des effets de particules dynamiques.

#### Propriété `particle_effect`

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `type` | string | Type (voir ci-dessous) | **Requis** |
| `position` | array | Position `[x, y]` | Centre |
| `duration` | float | Durée de l'effet | Variable |

#### Types de particules disponibles

**1. Confetti (célébration)**

```json
{
  "particle_effect": {
    "type": "confetti",
    "position": [640, 100],
    "duration": 3.0,
    "burst_count": 150
  }
}
```

**2. Sparkle (étincelles scintillantes)**

```json
{
  "particle_effect": {
    "type": "sparkle",
    "position": [640, 360],
    "duration": 2.5,
    "particle_count": 50
  }
}
```

**3. Explosion**

```json
{
  "particle_effect": {
    "type": "explosion",
    "position": [640, 360],
    "particle_count": 80
  }
}
```

**4. Smoke (fumée)**

```json
{
  "particle_effect": {
    "type": "smoke",
    "position": [640, 500],
    "duration": 4.0,
    "emission_rate": 15.0
  }
}
```

**5. Magic (étincelles magiques)**

```json
{
  "particle_effect": {
    "type": "magic",
    "position": [640, 360],
    "duration": 3.0,
    "emission_rate": 25.0
  }
}
```

**6. Custom (personnalisé)**

```json
{
  "particle_effect": {
    "type": "custom",
    "position": [640, 360],
    "duration": 3.0,
    "particle_count": 100,
    "colors": ["#FF0000", "#00FF00", "#0000FF"],
    "velocity": [5, 10],
    "gravity": 0.5,
    "lifetime": 2.0
  }
}
```

**Voir [PARTICLE_GUIDE.md](PARTICLE_GUIDE.md) et [PARTICLE_QUICKSTART.md](PARTICLE_QUICKSTART.md)**

---

### 3.13 Animation "Hand Push"

Animation d'une main poussant des éléments vers leur position.

#### Propriété `push_animation`

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `enabled` | bool | Activer l'animation push | `false` |
| `direction` | string | Direction : `"left"`, `"right"`, `"top"`, `"bottom"` | `"left"` |
| `distance` | int | Distance de poussée en pixels | `300` |
| `hand_size` | float | Taille relative de la main | `1.0` |
| `push_duration` | float | Durée de la poussée | `1.5` |
| `settle_duration` | float | Durée de stabilisation | `0.5` |

**Exemple:**
```json
{
  "layers": [
    {
      "image_path": "element.png",
      "z_index": 1,
      "push_animation": {
        "enabled": true,
        "direction": "left",
        "distance": 400,
        "hand_size": 1.2,
        "push_duration": 2.0,
        "settle_duration": 0.7
      }
    }
  ]
}
```

**Voir [PUSH_ANIMATION_GUIDE.md](PUSH_ANIMATION_GUIDE.md) et [PUSH_ANIMATION_QUICKSTART.md](PUSH_ANIMATION_QUICKSTART.md)**

---

### 3.14 Timeline et Synchronisation Avancée

Système complet de timeline avec keyframes, markers, et sync points.

#### Configuration Timeline

**Format:**
```json
{
  "slides": [
    {
      "index": 0,
      "timeline": {
        "keyframes": [...],
        "markers": [...],
        "sync_points": [...],
        "loop_segments": [...]
      }
    }
  ]
}
```

#### Keyframes

Animation par keyframes avec interpolation automatique.

```json
{
  "timeline": {
    "keyframes": [
      {
        "time": 0.0,
        "layer_index": 0,
        "properties": {
          "opacity": 0.0,
          "scale": 0.5,
          "position": {"x": 100, "y": 100}
        }
      },
      {
        "time": 2.0,
        "layer_index": 0,
        "properties": {
          "opacity": 1.0,
          "scale": 1.0,
          "position": {"x": 640, "y": 360}
        },
        "easing": "ease_in_out"
      }
    ]
  }
}
```

#### Time Markers

Marqueurs visuels pour organiser la timeline.

```json
{
  "timeline": {
    "markers": [
      {
        "time": 2.5,
        "label": "Intro terminée",
        "color": "#00FF00"
      },
      {
        "time": 5.0,
        "label": "Début du contenu principal",
        "color": "#FF0000"
      }
    ]
  }
}
```

#### Sync Points

Synchronisation parfaite entre plusieurs éléments.

```json
{
  "timeline": {
    "sync_points": [
      {
        "name": "reveal_all",
        "time": 3.0,
        "elements": [
          {"layer_index": 0, "action": "show"},
          {"layer_index": 1, "action": "show"},
          {"layer_index": 2, "action": "show"}
        ]
      }
    ]
  }
}
```

#### Loop Segments

Répétition de segments d'animation.

```json
{
  "timeline": {
    "loop_segments": [
      {
        "start_time": 2.0,
        "end_time": 5.0,
        "loop_count": 3,
        "layer_indices": [0, 1]
      }
    ]
  }
}
```

**Voir [TIMELINE_GUIDE.md](TIMELINE_GUIDE.md) et [TIMELINE_QUICKSTART.md](TIMELINE_QUICKSTART.md)**

---

### 3.15 Configuration Audio

Configuration audio complète via fichier JSON séparé.

#### Format audio_config.json

```json
{
  "background_music": {
    "path": "music.mp3",
    "volume": 0.5,
    "loop": true,
    "fade_in": 2.0,
    "fade_out": 3.0,
    "start_time": 0.0
  },
  "sound_effects": [
    {
      "path": "whoosh.wav",
      "time": 2.5,
      "volume": 0.8,
      "layer_index": 0
    },
    {
      "path": "ding.wav",
      "time": 5.0,
      "volume": 0.6
    }
  ],
  "voiceover": {
    "path": "narration.mp3",
    "volume": 1.0,
    "segments": [
      {
        "start": 0.0,
        "end": 5.0,
        "slide_index": 0
      },
      {
        "start": 5.0,
        "end": 10.0,
        "slide_index": 1
      }
    ]
  },
  "auto_sounds": {
    "typewriter_enabled": true,
    "typewriter_volume": 0.4,
    "drawing_enabled": true,
    "drawing_volume": 0.3
  }
}
```

**Voir [AUDIO_GUIDE.md](AUDIO_GUIDE.md) et [AUDIO_QUICKSTART.md](AUDIO_QUICKSTART.md)**

---

### 3.16 Section `transitions`

Configuration des transitions entre slides.

#### Propriétés d'une transition

| Propriété | Type | Description | Défaut |
|-----------|------|-------------|--------|
| `after_slide` | int | Index de la slide après laquelle appliquer | **Requis** |
| `type` | string | Type de transition (voir section 2.4) | `"none"` |
| `duration` | float | Durée en secondes | `0.5` |
| `pause_before` | float | Pause avant la transition | `0.0` |

**Exemple complet:**
```json
{
  "slides": [
    {"index": 0, "duration": 5},
    {"index": 1, "duration": 4},
    {"index": 2, "duration": 6}
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 1.0,
      "pause_before": 2.0
    },
    {
      "after_slide": 1,
      "type": "iris",
      "duration": 1.5,
      "pause_before": 1.5
    }
  ]
}
```

---

### 3.17 Exemple de Configuration Complète

Voici un exemple utilisant la plupart des fonctionnalités :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "skip_rate": 10,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1,
          "mode": "static",
          "opacity": 0.3
        },
        {
          "type": "text",
          "z_index": 2,
          "skip_rate": 15,
          "text_config": {
            "text": "Bienvenue à notre présentation!",
            "font": "Arial",
            "size": 72,
            "color": "#0066CC",
            "style": "bold"
          },
          "entrance": {
            "type": "slide_in",
            "duration": 1.5,
            "direction": "top"
          },
          "particle_effect": {
            "type": "sparkle",
            "position": [640, 200],
            "duration": 2.0
          }
        },
        {
          "type": "shape",
          "z_index": 3,
          "skip_rate": 12,
          "shape_config": {
            "shape": "circle",
            "color": "#FF6600",
            "fill_color": "#FFCC99",
            "stroke_width": 4,
            "position": {"x": 640, "y": 500},
            "size": 150
          },
          "entrance": {
            "type": "zoom_in",
            "duration": 1.0,
            "delay": 1.0
          }
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 3.0
        },
        {
          "zoom": 1.5,
          "position": {"x": 0.5, "y": 0.3},
          "duration": 4.0,
          "transition_duration": 1.5,
          "easing": "ease_in_out"
        },
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0,
          "transition_duration": 1.0,
          "easing": "ease_out"
        }
      ]
    },
    {
      "index": 1,
      "duration": 10,
      "layers": [
        {
          "image_path": "diagram.png",
          "z_index": 1,
          "skip_rate": 8,
          "animation": {
            "type": "zoom_in",
            "duration": 2.0,
            "start_zoom": 1.0,
            "end_zoom": 2.0,
            "focus_position": {"x": 0.7, "y": 0.4}
          }
        }
      ]
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 1.0,
      "pause_before": 2.0
    }
  ]
}
```

---

## 4. Fonctionnalités Avancées

### 4.1 Dessin Progressif par Couche

Par défaut, les couches sont dessinées séquentiellement tout en préservant les couches précédentes, créant un effet additif naturel.

**Caractéristiques:**
- Animation additive (comme VideoScribe/Doodly)
- Préservation des couches précédentes
- Ordre basé sur z_index
- Performance optimisée

**Configuration:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "layer1.png",
          "z_index": 1,
          "skip_rate": 8
        },
        {
          "image_path": "layer2.png",
          "z_index": 2,
          "skip_rate": 10
        },
        {
          "image_path": "layer3.png",
          "z_index": 3,
          "skip_rate": 12
        }
      ]
    }
  ]
}
```

**Voir [PROGRESSIVE_LAYER_DRAWING.md](PROGRESSIVE_LAYER_DRAWING.md) et [LAYERS_GUIDE.md](LAYERS_GUIDE.md)**

---

### 4.2 Gomme Intelligente

Effet d'effacement naturel pour les couches superposées.

**Utilisation:**
```json
{
  "layers": [
    {
      "image_path": "background.png",
      "z_index": 1,
      "mode": "draw"
    },
    {
      "image_path": "overlay.png",
      "z_index": 2,
      "mode": "eraser",
      "skip_rate": 12
    }
  ]
}
```

**Cas d'usage:**
- Effet de révélation progressive
- Animations de dévoilement
- Transitions créatives

**Voir [INTELLIGENT_ERASER.md](INTELLIGENT_ERASER.md)**

---

### 4.3 Animation de Chemins SVG

Animations basées sur des chemins pour texte et formes.

**Activation:**
```json
{
  "type": "text",
  "text_config": {
    "text": "Hello World",
    "use_svg_paths": true,
    "font": "Arial",
    "size": 64
  }
}
```

**Avantages:**
- Animation plus fluide
- Suit les contours exacts
- Meilleur pour calligraphie

**Voir [SVG_TEXT_HANDWRITING.md](SVG_TEXT_HANDWRITING.md)**

---

### 4.4 Export Multi-Formats

Exportez vers différents formats simultanément.

**Formats disponibles:**

| Format | Description | Usage |
|--------|-------------|-------|
| `mp4` | Vidéo standard H.264 | **Défaut**, usage général |
| `gif` | GIF animé | Web, réseaux sociaux |
| `webm` | WebM VP9 | Web moderne, bonne compression |
| `webm-alpha` | WebM avec transparence | Overlays, post-production |
| `png` / `png-sequence` | Frames PNG individuels | Édition vidéo, compositing |
| `lossless` | Codec FFV1 sans perte | Archivage, qualité parfaite |

**Utilisation:**
```bash
python whiteboard_animator.py image.png \
  --export-formats gif webm png lossless \
  --quality 18
```

**Voir [EXPORT_FORMATS_GUIDE.md](EXPORT_FORMATS_GUIDE.md)**

---

### 4.5 Presets Médias Sociaux

Configurations optimisées pour chaque plateforme.

| Preset | Résolution | Ratio | Description |
|--------|-----------|-------|-------------|
| `youtube` | 1920x1080 | 16:9 | YouTube standard |
| `youtube-shorts` | 1080x1920 | 9:16 | YouTube Shorts |
| `tiktok` | 1080x1920 | 9:16 | TikTok |
| `instagram-feed` | 1080x1080 | 1:1 | Instagram Feed |
| `instagram-story` | 1080x1920 | 9:16 | Instagram Stories |
| `instagram-reel` | 1080x1920 | 9:16 | Instagram Reels |
| `facebook` | 1280x720 | 16:9 | Facebook |
| `twitter` | 1280x720 | 16:9 | Twitter/X |
| `linkedin` | 1280x720 | 16:9 | LinkedIn |

**Utilisation:**
```bash
python whiteboard_animator.py content.png --social-preset tiktok
```

---

### 4.6 Points de Contrôle (Checkpoints)

Reprise de rendus interrompus.

**Activation:**
```bash
python whiteboard_animator.py --config long_video.json --enable-checkpoints
```

**Reprise:**
```bash
# Lister les checkpoints
python whiteboard_animator.py --list-checkpoints

# Reprendre
python whiteboard_animator.py --resume a1b2c3d4e5f6g7h8
```

**Fonctionnement:**
- Sauvegarde automatique tous les N frames
- Reprend exactement où interrompu
- Conserve toute la configuration

---

### 4.7 Mode Batch

Traitement de plusieurs vidéos en série ou parallèle.

**Série (séquentiel):**
```bash
python whiteboard_animator.py --batch video1.json video2.json video3.json
```

**Parallèle (multi-threading):**
```bash
python whiteboard_animator.py \
  --batch video1.json video2.json video3.json \
  --batch-parallel \
  --threads 4
```

**Avantages:**
- Traitement automatisé
- Logs séparés par vidéo
- Gestion d'erreurs robuste

---

### 4.8 Rendu en Arrière-Plan

Exécutez le rendu sans bloquer le terminal.

```bash
python whiteboard_animator.py --config video.json --background
```

**Suivi de progression:**
Le fichier `render_status.json` contient :
- Progression actuelle (%)
- Temps écoulé
- Temps estimé restant
- Statut (running, completed, error)

**Lecture du statut:**
```bash
cat render_status.json
```

---

### 4.9 Optimisation Mémoire

Pour les vidéos de grande taille.

```bash
python whiteboard_animator.py --config large_video.json --memory-efficient
```

**Techniques appliquées:**
- Traitement par chunks
- Libération de mémoire aggressive
- Cache optimisé
- Gestion d'images en streaming

---

## 5. Exemples Pratiques par Cas d'Usage

### 5.1 Présentation d'Entreprise

**Objectif:** Vidéo professionnelle avec logo et transitions

```bash
python whiteboard_animator.py \
  intro.png content1.png content2.png outro.png \
  --aspect-ratio 16:9 \
  --quality 18 \
  --transition fade \
  --transition-duration 0.8 \
  --watermark company_logo.png \
  --watermark-position bottom-right \
  --watermark-opacity 0.5 \
  --background-music corporate.mp3 \
  --music-volume 0.3
```

---

### 5.2 Tutoriel TikTok/Reels

**Objectif:** Format vertical avec sous-titres et effets

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "diagram.png",
          "z_index": 1,
          "skip_rate": 12
        },
        {
          "type": "text",
          "z_index": 2,
          "text_config": {
            "text": "Astuce du jour!",
            "font": "Arial",
            "size": 56,
            "color": "#FFFFFF",
            "style": "bold"
          },
          "entrance": {
            "type": "pop_in",
            "duration": 0.8
          },
          "particle_effect": {
            "type": "sparkle",
            "duration": 2.0
          }
        }
      ]
    }
  ]
}
```

```bash
python whiteboard_animator.py \
  --config tutorial.json \
  --social-preset tiktok \
  --enable-drawing-sound \
  --export-formats gif
```

---

### 5.3 Post Instagram Carré

**Objectif:** Format carré avec animations dynamiques

```bash
python whiteboard_animator.py content.png \
  --aspect-ratio 1:1 \
  --quality 18 \
  --config animations.json \
  --watermark logo.png \
  --social-preset instagram-feed
```

---

### 5.4 Vidéo YouTube Éducative

**Objectif:** Longue vidéo avec chapitres et narration

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 30,
      "layers": [
        {
          "image_path": "chapter1.png",
          "z_index": 1,
          "skip_rate": 8
        },
        {
          "type": "text",
          "z_index": 2,
          "text_config": {
            "text": "Chapitre 1: Introduction",
            "size": 64,
            "color": "#0066CC"
          }
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 5.0
        },
        {
          "zoom": 1.5,
          "position": {"x": 0.3, "y": 0.3},
          "duration": 10.0,
          "transition_duration": 2.0,
          "easing": "ease_in_out"
        }
      ]
    }
  ]
}
```

```bash
python whiteboard_animator.py \
  --config educational.json \
  --audio-config narration.json \
  --aspect-ratio 16:9 \
  --quality 18 \
  --enable-checkpoints
```

---

### 5.5 Diagramme Technique avec Formes

**Objectif:** Schéma animé avec formes et flèches

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {
          "type": "shape",
          "z_index": 1,
          "shape_config": {
            "shape": "rectangle",
            "color": "#0066CC",
            "fill_color": "#CCE5FF",
            "stroke_width": 3,
            "position": {"x": 300, "y": 360},
            "size": [200, 150]
          }
        },
        {
          "type": "shape",
          "z_index": 2,
          "shape_config": {
            "shape": "arrow",
            "color": "#FF6600",
            "stroke_width": 4,
            "start": [500, 360],
            "end": [780, 360],
            "arrow_size": 25
          }
        },
        {
          "type": "shape",
          "z_index": 3,
          "shape_config": {
            "shape": "circle",
            "color": "#00AA00",
            "fill_color": "#CCFFCC",
            "stroke_width": 3,
            "position": {"x": 980, "y": 360},
            "size": 100
          }
        }
      ]
    }
  ]
}
```

```bash
python whiteboard_animator.py \
  --config flowchart.json \
  --aspect-ratio 16:9 \
  --quality 18
```

---

### 5.6 Célébration avec Particules

**Objectif:** Animation festive avec confettis

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "type": "text",
          "z_index": 1,
          "text_config": {
            "text": "Félicitations!",
            "font": "Arial",
            "size": 96,
            "color": "#FFD700",
            "style": "bold"
          },
          "entrance": {
            "type": "zoom_in",
            "duration": 1.5
          },
          "particle_effect": {
            "type": "confetti",
            "position": [640, 100],
            "duration": 4.0,
            "burst_count": 200
          }
        }
      ]
    }
  ]
}
```

```bash
python whiteboard_animator.py \
  --config celebration.json \
  --aspect-ratio 1:1 \
  --quality 18
```

---

## 6. Workflows et Meilleures Pratiques

### 6.1 Workflow de Production Standard

**Étape 1: Préparation**
```bash
# Préparer vos assets
mkdir -p project/images project/audio project/configs

# Copier vos images, musiques, logos
cp *.png project/images/
cp *.mp3 project/audio/
```

**Étape 2: Test rapide**
```bash
# Preview rapide pour validation
python whiteboard_animator.py \
  project/images/slide1.png \
  --preview \
  --config project/configs/draft.json
```

**Étape 3: Configuration**
```bash
# Créer configuration complète
nano project/configs/production.json
```

**Étape 4: Rendu final**
```bash
# Rendu haute qualité avec checkpoints
python whiteboard_animator.py \
  --config project/configs/production.json \
  --audio-config project/configs/audio.json \
  --quality-preset high \
  --enable-checkpoints \
  --aspect-ratio 16:9 \
  --watermark project/images/logo.png
```

---

### 6.2 Optimisation des Performances

**Pour vidéos courtes (<30s):**
```bash
# Qualité maximale sans optimisations
python whiteboard_animator.py --config short.json --quality 15
```

**Pour vidéos moyennes (30s-2min):**
```bash
# Bon équilibre performance/qualité
python whiteboard_animator.py --config medium.json --quality 18 --enable-checkpoints
```

**Pour longues vidéos (>2min):**
```bash
# Optimisations complètes
python whiteboard_animator.py \
  --config long.json \
  --quality 18 \
  --memory-efficient \
  --enable-checkpoints \
  --background
```

**Pour production batch:**
```bash
# Traitement parallèle
python whiteboard_animator.py \
  --batch *.json \
  --batch-parallel \
  --threads 4 \
  --memory-efficient
```

---

### 6.3 Gestion de la Qualité

**Recommandations CRF par usage:**

| Usage | CRF | Description |
|-------|-----|-------------|
| Archivage | 12-15 | Qualité maximale |
| YouTube/Production | 18 | Visually lossless (recommandé) |
| Réseaux sociaux | 20-23 | Bon compromis |
| Preview/Brouillon | 28-30 | Tests rapides |

**Exemples:**
```bash
# Archivage professionnel
python whiteboard_animator.py video.png --quality 15 --export-formats lossless

# Production YouTube
python whiteboard_animator.py video.png --quality 18 --social-preset youtube

# Tests rapides
python whiteboard_animator.py video.png --preview
```

---

### 6.4 Organisation des Projets

**Structure recommandée:**
```
mon_projet/
├── assets/
│   ├── images/           # Images sources
│   ├── logos/            # Logos et watermarks
│   ├── audio/            # Musiques et effets sonores
│   └── fonts/            # Polices personnalisées (optionnel)
├── configs/
│   ├── slides.json       # Configuration principale
│   ├── audio.json        # Configuration audio
│   └── presets/          # Configurations réutilisables
├── output/               # Vidéos générées
├── checkpoints/          # Points de contrôle
└── README.md             # Documentation du projet
```

---

### 6.5 Bonnes Pratiques

#### Images

**Résolution recommandée:**
- HD (1920x1080) pour YouTube, production professionnelle
- FHD+ (2560x1440) si zoom important prévu
- Formats verticaux : 1080x1920

**Formats:**
- PNG : meilleure qualité, transparence supportée
- JPG : fichiers plus légers, pas de transparence
- Éviter : BMP (trop volumineux), GIF (qualité limitée)

**Optimisation:**
```bash
# Redimensionner en batch avec ImageMagick
mogrify -resize 1920x1080 -quality 95 *.jpg
```

#### Animations

**Vitesse de dessin (skip_rate):**
- 3-5 : Très lent, détails complexes
- 8-12 : Standard, bon équilibre
- 15-20 : Rapide, aperçu stylisé
- 25+ : Très rapide, effet sketch

**Durée des slides:**
- Titre : 3-5 secondes
- Contenu simple : 5-8 secondes
- Contenu complexe : 10-15 secondes
- Fin/outro : 3-5 secondes

#### Audio

**Niveaux de volume recommandés:**
- Musique de fond : 0.3-0.5
- Effets sonores : 0.5-0.8
- Voix off : 0.8-1.0
- Sons auto-générés : 0.3-0.5

**Formats audio:**
- MP3 : Standard, bon compromis
- WAV : Qualité maximale, fichiers volumineux
- OGG : Bonne compression, moins compatible
- M4A : Qualité/taille excellentes

---

### 6.6 Résolution de Problèmes Courants

#### Vidéo trop longue/lente

**Solution 1: Augmenter skip_rate**
```json
{
  "slides": [
    {
      "index": 0,
      "skip_rate": 20  // Plus rapide
    }
  ]
}
```

**Solution 2: Réduire durée**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5  // Plus court
    }
  ]
}
```

#### Qualité insuffisante

**Solution: Ajuster CRF et résolution**
```bash
python whiteboard_animator.py image.png \
  --quality 15 \
  --aspect-ratio 16:9
```

#### Fichiers trop volumineux

**Solution 1: CRF plus élevé**
```bash
python whiteboard_animator.py image.png --quality 23
```

**Solution 2: Résolution réduite**
```bash
python whiteboard_animator.py image.png --aspect-ratio 16:9 --quality 23
```

#### Rendu interrompu

**Solution: Utiliser checkpoints**
```bash
# Activer checkpoints
python whiteboard_animator.py --config video.json --enable-checkpoints

# Si interrompu, lister et reprendre
python whiteboard_animator.py --list-checkpoints
python whiteboard_animator.py --resume <checkpoint_id>
```

#### Mémoire insuffisante

**Solution: Mode memory-efficient**
```bash
python whiteboard_animator.py \
  --config video.json \
  --memory-efficient \
  --quality 23
```

---

## 7. Guide de Référence Rapide

### 7.1 Commandes Essentielles

```bash
# Vidéo simple
python whiteboard_animator.py image.png

# Qualité HD pour YouTube
python whiteboard_animator.py image.png --aspect-ratio 16:9 --quality 18

# Format vertical TikTok
python whiteboard_animator.py image.png --social-preset tiktok

# Plusieurs slides avec transitions
python whiteboard_animator.py slide1.png slide2.png slide3.png --transition fade

# Configuration avancée
python whiteboard_animator.py --config video.json --audio-config audio.json

# Preview rapide
python whiteboard_animator.py --config video.json --preview

# Export multi-formats
python whiteboard_animator.py image.png --export-formats gif webm png

# Avec watermark
python whiteboard_animator.py image.png --watermark logo.png

# Batch processing
python whiteboard_animator.py --batch video1.json video2.json --batch-parallel
```

---

### 7.2 Configuration JSON Minimale

**Une slide simple:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5
    }
  ]
}
```

**Plusieurs slides avec transition:**
```json
{
  "slides": [
    {"index": 0, "duration": 5},
    {"index": 1, "duration": 5}
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

**Avec couches:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1
        },
        {
          "image_path": "foreground.png",
          "z_index": 2,
          "position": {"x": 100, "y": 100}
        }
      ]
    }
  ]
}
```

**Avec texte:**
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
          "text_config": {
            "text": "Hello World!",
            "size": 64,
            "color": "#0066CC"
          }
        }
      ]
    }
  ]
}
```

---

### 7.3 Valeurs par Défaut

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `split_len` | 15 | Taille de grille |
| `frame_rate` | 30 | FPS |
| `skip_rate` | 8 | Vitesse de dessin |
| `duration` | 3 | Durée slide (secondes) |
| `quality` | 18 | CRF (qualité vidéo) |
| `aspect_ratio` | original | Ratio d'aspect |
| `transition` | none | Type de transition |
| `transition_duration` | 0.5 | Durée transition |
| `watermark_opacity` | 0.5 | Opacité watermark |
| `watermark_scale` | 0.1 | Échelle watermark |
| `music_volume` | 0.5 | Volume musique |

---

### 7.4 Raccourcis et Astuces

**Lister les presets disponibles:**
```bash
python whiteboard_animator.py --list-presets
```

**Trouver les bonnes valeurs split_len:**
```bash
python whiteboard_animator.py image.png --get-split-lens
```

**Lister les checkpoints:**
```bash
python whiteboard_animator.py --list-checkpoints
```

**Export JSON seulement (pas de vidéo):**
```bash
python whiteboard_animator.py image.png --export-json
```

**Utiliser config sans spécifier d'images:**
```bash
# Si le JSON contient les chemins d'images dans layers
python whiteboard_animator.py --config complete.json
```

---

### 7.5 Liens vers Documentation Détaillée

#### Guides Principaux
- **[README.md](README.md)** - Vue d'ensemble générale
- **[CONFIG_FORMAT.md](CONFIG_FORMAT.md)** - Format JSON complet
- **[LAYERS_GUIDE.md](LAYERS_GUIDE.md)** - Guide des couches

#### Fonctionnalités Avancées
- **[ADVANCED_CAMERA_GUIDE.md](ADVANCED_CAMERA_GUIDE.md)** - Système de caméra avancé
- **[CAMERA_ANIMATION_GUIDE.md](CAMERA_ANIMATION_GUIDE.md)** - Animations de caméra
- **[TEXT_LAYERS_GUIDE.md](TEXT_LAYERS_GUIDE.md)** - Couches de texte
- **[SHAPES_GUIDE.md](SHAPES_GUIDE.md)** - Formes géométriques
- **[PARTICLE_GUIDE.md](PARTICLE_GUIDE.md)** - Effets de particules
- **[AUDIO_GUIDE.md](AUDIO_GUIDE.md)** - Support audio complet
- **[TIMELINE_GUIDE.md](TIMELINE_GUIDE.md)** - Timeline et synchronisation
- **[PUSH_ANIMATION_GUIDE.md](PUSH_ANIMATION_GUIDE.md)** - Animation hand push
- **[PATH_ANIMATION_GUIDE.md](PATH_ANIMATION_GUIDE.md)** - Animations de chemin

#### Guides Rapides
- **[QUICKSTART.md](QUICKSTART.md)** - Démarrage rapide général
- **[PARTICLE_QUICKSTART.md](PARTICLE_QUICKSTART.md)** - Particules en 5 min
- **[AUDIO_QUICKSTART.md](AUDIO_QUICKSTART.md)** - Audio en 5 min
- **[TIMELINE_QUICKSTART.md](TIMELINE_QUICKSTART.md)** - Timeline en 5 min
- **[QUICKSTART_SHAPES.md](QUICKSTART_SHAPES.md)** - Formes en 5 min
- **[QUICKSTART_TEXT_ANIMATIONS.md](QUICKSTART_TEXT_ANIMATIONS.md)** - Texte en 5 min
- **[PUSH_ANIMATION_QUICKSTART.md](PUSH_ANIMATION_QUICKSTART.md)** - Push en 5 min
- **[QUICKSTART_ADVANCED_CAMERA.md](QUICKSTART_ADVANCED_CAMERA.md)** - Caméra en 5 min
- **[SVG_QUICKSTART.md](SVG_QUICKSTART.md)** - SVG paths en 5 min

#### Guides Techniques
- **[EXPORT_FORMATS_GUIDE.md](EXPORT_FORMATS_GUIDE.md)** - Formats d'export
- **[EXPORT_FORMAT.md](EXPORT_FORMAT.md)** - Format JSON exporté
- **[PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md)** - Optimisation performance
- **[VIDEO_QUALITY.md](VIDEO_QUALITY.md)** - Qualité vidéo
- **[DURATION_GUIDE.md](DURATION_GUIDE.md)** - Gestion des durées
- **[PROGRESSIVE_LAYER_DRAWING.md](PROGRESSIVE_LAYER_DRAWING.md)** - Dessin progressif
- **[INTELLIGENT_ERASER.md](INTELLIGENT_ERASER.md)** - Gomme intelligente
- **[TRANSITIONS.md](TRANSITIONS.md)** - Transitions entre slides

#### Exemples
- **[examples/README.md](examples/README.md)** - Documentation des exemples
- **[examples/QUICK_REFERENCE.md](examples/QUICK_REFERENCE.md)** - Référence rapide exemples
- **[EXAMPLES_SUMMARY.md](EXAMPLES_SUMMARY.md)** - Résumé des exemples

---

## 8. Ressources et Support

### 8.1 Fichiers d'Exemple

Le dossier `examples/` contient **40+ fichiers de configuration JSON** couvrant tous les cas d'usage :

**Basiques:**
- `basic_drawing.json` - Animation simple
- `per_slide_config.json` - Configuration par slide
- `multi_slide_transitions.json` - Transitions

**Couches:**
- `layers_composition.json` - Superposition d'images
- `advanced_layer_modes.json` - Modes draw/eraser/static
- `entrance_exit_animations.json` - Animations entrée/sortie
- `morphing_layers.json` - Effets de morphing

**Caméra:**
- `camera_zoom_basic.json` - Zoom simple
- `animation_zoom_in.json` - Zoom post-dessin
- `camera_and_animation.json` - Caméra + animation
- `multi_layer_camera.json` - Caméra multi-couches
- `cinematic_reveal.json` - Révélation cinématique
- `example_advanced_cameras.json` - Caméra avancée

**Particules:**
- `particle_confetti.json` - Confettis
- `particle_sparkles.json` - Étincelles
- `particle_explosion.json` - Explosion
- `particle_smoke.json` - Fumée
- `particle_magic.json` - Magie
- `particle_custom.json` - Personnalisé

**Texte:**
- `text_layer_example.json` - Texte basique
- `multiline_text_example.json` - Texte multiligne
- `multilingual_text.json` - Texte multilingue
- `advanced_text_animations.json` - Animations avancées
- `svg_text_showcase.json` - SVG paths
- `text_effects.json` - Effets de texte

**Formes:**
- `example_shapes_config.json` - Formes variées
- `example_flowchart.json` - Organigramme

**Push Animation:**
- `push_animation_example.json` - Push basique
- `push_all_directions.json` - Toutes directions
- `push_product_demo.json` - Démo produit

**Timeline:**
- `example_timeline_sequence.json` - Séquence
- `example_timeline_advanced.json` - Avancé
- `example_timeline_crossfade.json` - Crossfade

**Chemins:**
- `path_animation_basic.json` - Chemin basique
- `path_animation_bezier.json` - Courbes Bézier
- `path_animation_spline.json` - Splines
- `path_animation_complete.json` - Complet

**Audio:**
- `example_audio_config.json` - Configuration audio

**Complet:**
- `complete_showcase.json` - Showcase de toutes les fonctionnalités
- `intelligent_eraser_example.json` - Gomme intelligente

### 8.2 Scripts d'Exemple

**`examples/use_animation_data.py`**
Script Python pour analyser et utiliser les données JSON exportées.

```bash
# Analyser une animation
python examples/use_animation_data.py animation.json

# Exporter séquence simplifiée
python examples/use_animation_data.py animation.json --export-sequence output.json
```

---

### 8.3 Tests et Validation

Pour tester le système, plusieurs scripts de test sont disponibles :

```bash
# Tests de base
python test_text_animations.py
python test_shapes.py
python test_particle_system.py
python test_audio.py
python test_timeline.py
python test_path_animation.py

# Tests d'intégration
python test_integration_text.py
python test_integration_export.py
```

---

### 8.4 Dépannage Avancé

#### FFmpeg non trouvé

**Erreur:** `Couldn't find ffmpeg or avconv`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Télécharger depuis https://ffmpeg.org/download.html
# Ajouter au PATH système
```

#### Module Python manquant

**Erreur:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
pip install opencv-python numpy pillow av fontTools pydub
```

#### Polices non trouvées (texte)

**Erreur:** Texte ne s'affiche pas correctement

**Solution:**
```bash
# Lister les polices disponibles
fc-list

# Installer polices supplémentaires (Ubuntu/Debian)
sudo apt-get install fonts-dejavu fonts-liberation

# macOS
# Copier .ttf dans ~/Library/Fonts/
```

#### Support RTL (arabe, hébreu)

**Installation:**
```bash
pip install arabic-reshaper python-bidi
```

---

### 8.5 Contribuer

Le projet est open-source et accueille les contributions !

**Issues GitHub:**
- Signaler des bugs
- Proposer des fonctionnalités
- Demander de l'aide

**Pull Requests:**
- Corrections de bugs
- Nouvelles fonctionnalités
- Améliorations de documentation
- Nouveaux exemples

**Repository:** https://github.com/armelwanes/whiteboard-cli

---

## 9. Changelog et Évolution

### Fonctionnalités Récentes

#### ✨ Système de Timeline Avancé
- Keyframes avec interpolation
- Time markers pour organisation
- Sync points pour synchronisation parfaite
- Loop segments pour répétitions
- Courbes Bézier personnalisées

#### 🎆 Effets de Particules
- 6 types de particules (confetti, sparkle, explosion, smoke, magic, custom)
- Configuration complète des propriétés
- Performance optimisée
- Intégration avec layers

#### 🔊 Support Audio Complet
- Musique de fond avec loop et fade
- Effets sonores synchronisés
- Voix off segmentée
- Sons auto-générés (typewriter, drawing)
- Mixage multi-pistes automatique

#### 🎥 Système de Caméra Avancé
- Séquences multiples avec transitions
- Fonctions d'easing variées
- Taille de caméra personnalisable
- Support de mouvements complexes

#### 🔷 Formes Géométriques
- 6 types de formes vectorielles
- Remplissage et contour personnalisables
- Animation progressive
- Intégration parfaite avec layers

#### 📊 Performance et Optimisation
- Mode preview pour tests rapides
- Quality presets (5 niveaux)
- Checkpoints pour reprise
- Background rendering
- Batch processing parallèle
- Memory optimization

#### 📤 Export Multi-Formats
- GIF animé
- WebM (standard et alpha)
- PNG sequence
- Lossless (FFV1)
- 9 presets médias sociaux

---

## 10. Glossaire

| Terme | Définition |
|-------|------------|
| **CRF** | Constant Rate Factor - Contrôle qualité vidéo (0-51, plus bas = meilleur) |
| **Skip Rate** | Vitesse de dessin - Nombre de tuiles dessinées par frame |
| **Split Len** | Taille de la grille de dessin en pixels |
| **z_index** | Ordre de superposition des couches (plus grand = au-dessus) |
| **Layer** | Couche - Élément individuel (image, texte, forme) sur une slide |
| **Slide** | Diapositive - Scène complète de l'animation |
| **Easing** | Fonction d'interpolation pour transitions fluides |
| **Keyframe** | Image-clé définissant un état à un moment précis |
| **Morph** | Transformation progressive d'une forme vers une autre |
| **Canvas** | Canevas - Zone de dessin complète de la vidéo |
| **Watermark** | Filigrane - Logo ou texte superposé sur la vidéo |
| **Checkpoint** | Point de contrôle pour reprendre un rendu |
| **Batch** | Lot - Traitement de plusieurs vidéos |
| **Timeline** | Ligne de temps - Séquence chronologique d'événements |

---

## Conclusion

Ce guide couvre **toutes les fonctionnalités** de whiteboard-cli. Pour aller plus loin :

1. **Commencez simple** : Utilisez les exemples de base dans `examples/`
2. **Expérimentez** : Testez différentes configurations avec `--preview`
3. **Explorez** : Lisez les guides spécialisés pour chaque fonctionnalité
4. **Créez** : Construisez vos propres vidéos professionnelles !

**Ressources principales:**
- 📖 Ce guide complet
- 📁 40+ exemples de configuration JSON
- 📚 20+ guides spécialisés
- 🎓 10+ guides quickstart (5 minutes)
- 🔧 Scripts de test et validation

**Support:**
- GitHub Issues: https://github.com/armelwanes/whiteboard-cli/issues
- Documentation: Voir section 7.5
- Exemples: Dossier `examples/`

---

**Whiteboard-CLI** - Créez des vidéos d'animation professionnelles en quelques commandes ! 🎬✨

---

*Dernière mise à jour: 2025-10-15*
*Version: 2.0*
*Auteur: armelwanes*

