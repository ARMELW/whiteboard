# Whiteboard-It

Application de création d'animations de type "dessin sur tableau blanc" (whiteboard animation) à partir d'images.

## 📚 Documentation Complète

**→ [GUIDE_COMPLET.md](GUIDE_COMPLET.md) - Documentation exhaustive de toutes les fonctionnalités**

Ce guide de 2800+ lignes couvre :
- ✅ Toutes les commandes CLI avec exemples
- ✅ Format de configuration JSON complet avec tous les paramètres
- ✅ Toutes les fonctionnalités avancées (layers, caméra, particules, audio, formes, texte, timeline)
- ✅ Exemples pratiques par cas d'usage
- ✅ Workflows et meilleures pratiques
- ✅ Guide de référence rapide

**C'est LA ressource ultime pour exploiter whiteboard-cli au maximum ! 🚀**

## Fonctionnalités

- ✅ Génération de vidéos d'animation de dessin à partir d'images
- ✅ **🆕 Modes d'Animation Multiples** - Draw, Erase, Flood Fill, Coloriage (NOUVEAU!)
- ✅ **🆕 Mode Flood Fill** - Remplissage progressif par régions connectées (NOUVEAU!)
- ✅ **🆕 Mode Coloriage** - Coloriage progressif ligne par ligne pour un effet artistique (NOUVEAU!)
- ✅ **🆕 Configuration de Polices Simplifiée** - Système de configuration centralisé pour les polices (NOUVEAU!)
- ✅ **🆕 Effets de Particules** - Confettis, étincelles, explosions, fumée, magie (NOUVEAU!)
- ✅ **🆕 Support Audio Complet** - Musique de fond, effets sonores, voix off, sons auto-générés (NOUVEAU!)
- ✅ **🆕 Performance & Optimisation** - Preview mode, checkpoints, batch processing, memory optimization
- ✅ **🆕 Timeline et Synchronisation Avancée** - Système complet de timeline avec keyframes, markers, sync points (NOUVEAU!)
- ✅ **🆕 Formes géométriques** - Cercles, rectangles, triangles, polygones, lignes, flèches
- ✅ **🆕 Animation "Hand Push"** - Main poussant des éléments vers leur position
- ✅ **🆕 Couches de texte dynamiques** - Texte généré à la volée avec animation handwriting
- ✅ **🆕 Système de caméra avancé** - Séquences de caméras multiples avec transitions fluides
- ✅ **Contrôles de caméra** - Zoom et focus sur des zones spécifiques
- ✅ **Animations avancées** - Effets de zoom-in/zoom-out post-dessin
- ✅ **Gomme intelligente** - Effet d'effacement naturel pour les couches superposées
- ✅ **Couches multiples (layers)** - Superposition d'images sur une même slide avec hiérarchie
- ✅ **🆕 Dessin progressif par couche** - Animation additive préservant les couches précédentes (style VideoScribe/Doodly)
- ✅ **Qualité vidéo améliorée** - CRF ajustable pour une qualité optimale
- ✅ **Export multi-formats** - Support 1:1, 16:9, 9:16 en HD
- ✅ **Filigrane (watermark)** - Ajout de logo/texte avec position et opacité personnalisables
- ✅ **Support de plusieurs images avec combinaison automatique**
- ✅ **Transitions entre slides** (fade, wipe, push, iris)
- ✅ Personnalisation des paramètres (FPS, vitesse, grille)
- ✅ Export JSON des données d'animation
- ✅ Support de plusieurs formats d'image
- ✅ Animation avec main réaliste

### 🎨 Modes d'Animation Multiples (NOUVEAU!)

Choisissez parmi **six styles d'animation** pour créer vos vidéos :

| Mode | Description | Vitesse | Idéal pour |
|------|-------------|---------|------------|
| **`draw`** | Dessin tile par tile classique | Moyenne | Dessins détaillés, illustrations |
| **`erase`** | Effacement tile par tile | Moyenne | Effets de révélation inverse |
| **`flood_fill`** | Remplissage par régions connectées | Rapide | Logos, icônes, formes simples |
| **`coloriage`** | Coloriage progressif ligne par ligne | Lente | Dessins à colorier, art coloré |
| **`path_follow`** | Animation point par point avec main naturelle | Variable | Signatures, calligraphie, dessins réalistes |
| **`static`** | Affichage instantané | Instantanée | Watermarks, logos statiques |

**Exemple de configuration :**
```json
{
  "layers": [
    {
      "image_path": "drawing.png",
      "mode": "draw",
      "skip_rate": 5
    },
    {
      "image_path": "colors.png",
      "mode": "coloriage",
      "skip_rate": 3
    },
    {
      "image_path": "highlights.png",
      "mode": "flood_fill",
      "skip_rate": 3
    },
    {
      "image_path": "signature.png",
      "mode": "path_follow",
      "skip_rate": 2
    }
  ]
}
```

**Documentation complète:** Voir [FLOOD_FILL_GUIDE.md](FLOOD_FILL_GUIDE.md)

### 🔤 Configuration de Polices Simplifiée (NOUVEAU!)

Gérez vos polices personnalisées facilement avec le nouveau système de configuration centralisé :

- **Configuration centralisée** - Toutes les polices définies dans `fonts.json`
- **Pas besoin de `font_path`** - Spécifiez uniquement le nom de la police
- **Support multi-styles** - Normal, bold, italic, bold italic
- **Ajout facile** - Ajoutez de nouvelles polices sans modifier le code
- **Fallback automatique** - Utilise les polices système si non configuré

```json
// Avant : vous deviez spécifier font_path à chaque fois
{
  "text_config": {
    "text": "Your text",
    "font": "Pacifico",
    "font_path": "../fonts/Pacifico/Pacifico-Regular.ttf"
  }
}

// Maintenant : juste le nom de la police !
{
  "text_config": {
    "text": "Your text",
    "font": "Pacifico"
  }
}
```

**Configuration dans fonts.json :**
```json
{
  "fonts": {
    "Pacifico": {
      "normal": "fonts/Pacifico/Pacifico-Regular.ttf"
    },
    "Roboto": {
      "normal": "fonts/Roboto/Roboto-Regular.ttf",
      "bold": "fonts/Roboto/Roboto-Bold.ttf"
    }
  }
}
```

**Documentation complète:** Voir [FONT_CONFIG_GUIDE.md](FONT_CONFIG_GUIDE.md)

### 🎆 Effets de Particules (NOUVEAU!)

Enrichissez vos animations avec des effets de particules dynamiques:

- **Confettis 🎊** - Célébrations avec particules colorées qui tombent
- **Étincelles ✨** - Étoiles scintillantes pour effets de brillance
- **Explosions 💥** - Effets d'explosion radiale avec particules de feu
- **Fumée 💨** - Traînées de fumée ou poussière en mouvement
- **Magie 🪄** - Étincelles magiques pour texte et objets
- **Systèmes personnalisés ⚙️** - Configuration complète pour effets uniques

```bash
# Confettis de célébration
python whiteboard_animator.py image.jpg --config examples/particle_confetti.json --split-len 30

# Étincelles magiques sur texte
python whiteboard_animator.py --config examples/particle_magic.json --split-len 30

# Explosion spectaculaire
python whiteboard_animator.py image.jpg --config examples/particle_explosion.json --split-len 30
```

**Documentation complète:** Voir [PARTICLE_GUIDE.md](PARTICLE_GUIDE.md) et [PARTICLE_QUICKSTART.md](PARTICLE_QUICKSTART.md)

### 🆕 Support Audio (NOUVEAU!)

Créez des vidéos professionnelles avec audio complet:

- **Musique de fond** - Avec boucle, fade-in/fade-out, contrôle de volume
- **Effets sonores** - Synchronisés précisément avec les animations
- **Voix off** - Narration professionnelle avec timing exact
- **Sons de machine à écrire** - Auto-générés pour animations de texte
- **Sons de dessin** - Auto-générés pour animations de tracé
- **Mixage multi-pistes** - Combinaison automatique de toutes les sources audio
- **Contrôle de volume** - Volume individuel par élément audio

```bash
# Exemple rapide avec musique de fond
python whiteboard_animator.py image.jpg --background-music music.mp3

# Activer les sons auto-générés
python whiteboard_animator.py image.jpg --enable-drawing-sound --enable-typewriter-sound

# Configuration complète
python whiteboard_animator.py --config slides.json --audio-config audio.json
```

**Voir**: [AUDIO_GUIDE.md](AUDIO_GUIDE.md) pour la documentation complète!

### 🆕 Export Formats Avancés (NOUVEAU!)

Exportez vos animations vers multiples formats pour différents usages:

- **GIF animé** - Format universel pour le web et réseaux sociaux
- **WebM** - Codec VP9 moderne, meilleure compression
- **PNG Sequence** - Frames individuels pour post-production
- **Transparence** - WebM avec canal alpha pour overlays
- **Lossless** - Qualité parfaite sans perte (FFV1)
- **9 Presets Médias Sociaux** - YouTube, TikTok, Instagram, Facebook, Twitter, LinkedIn

Voir [EXPORT_FORMATS_GUIDE.md](EXPORT_FORMATS_GUIDE.md) pour la documentation complète.

### 🆕 Performance & Optimisation (NOUVEAU!)

Optimisez vos rendus avec ces fonctionnalités avancées:

- **Preview Mode** - Rendu rapide 50% résolution pour tests
- **Quality Presets** - 5 niveaux (preview, draft, standard, high, ultra)
- **Checkpoints** - Reprise de rendus interrompus
- **Background Rendering** - Rendu en arrière-plan avec suivi de progrès
- **Batch Processing** - Traitement de plusieurs vidéos en série ou parallèle
- **Memory Optimization** - Gestion mémoire efficace pour grandes vidéos
- **Multi-threading** - Infrastructure prête pour traitement parallèle

**Voir**: [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) pour le guide complet!

### 🆕 Timeline et Synchronisation (NOUVEAU!)

Le système de timeline offre un contrôle précis sur le timing et la synchronisation:

- **Keyframes** - Animation par keyframes avec interpolation automatique
- **Courbes d'animation** - 8 types d'easing (linear, ease_in, ease_out, ease_in_out, etc.)
- **Time markers** - Marqueurs visuels pour organiser votre timeline
- **Sync points** - Synchronisation parfaite entre plusieurs éléments
- **Loop segments** - Répétition de segments d'animation
- **Time remapping** - Contrôle de la vitesse (slow-motion, accéléré)
- **Courbes Bézier** - Courbes d'animation personnalisées

**Voir**: [TIMELINE_QUICKSTART.md](TIMELINE_QUICKSTART.md) pour démarrer en 5 minutes!

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/armelgeek/whiteboard-it.git
cd whiteboard-it

# Installer les dépendances de base
pip install opencv-python numpy pillow

# Requis pour la conversion H.264 et la concaténation de vidéos multiples
pip install av

# Optionnel: Support audio (musique, effets sonores, voix off)
pip install pydub
```

**Note:** 
- Le module `av` (PyAV) est fortement recommandé pour la conversion H.264 et la combinaison de vidéos
- Le module `pillow` est requis pour les couches de texte dynamiques
- Le module `pydub` est optionnel mais recommandé pour le support audio complet
- FFmpeg doit être installé sur votre système (généralement déjà présent)

## Utilisation

### Génération de vidéo

```bash
# Génération simple (une image)
python whiteboard_animator.py image.png

# Avec paramètres personnalisés
python whiteboard_animator.py image.png --split-len 15 --frame-rate 30 --skip-rate 8

# Plusieurs images (génère une vidéo combinée)
python whiteboard_animator.py image1.png image2.png image3.png

# Plusieurs images avec paramètres personnalisés
python whiteboard_animator.py image1.png image2.png image3.png --split-len 15 --frame-rate 30 --skip-rate 8
```

**Note:** Lorsque plusieurs images sont fournies, le script génère une vidéo pour chaque image puis les combine automatiquement en une seule vidéo finale. Chaque image est dessinée dans l'ordre.

### Qualité vidéo et formats d'export (NOUVEAU)

```bash
# Haute qualité pour YouTube (16:9 HD)
python whiteboard_animator.py image.png --aspect-ratio 16:9 --quality 18

# Format vertical pour TikTok/Reels (9:16 HD)
python whiteboard_animator.py image.png --aspect-ratio 9:16 --quality 18

# Format carré pour Instagram (1:1)
python whiteboard_animator.py image.png --aspect-ratio 1:1 --quality 18

# Qualité moyenne pour fichiers plus légers
python whiteboard_animator.py image.png --quality 28
```

### Ajouter un filigrane (watermark) (NOUVEAU)

```bash
# Ajouter un filigrane en bas à droite
python whiteboard_animator.py image.png --watermark logo.png

# Filigrane personnalisé (position, opacité, taille)
python whiteboard_animator.py image.png \
  --watermark logo.png \
  --watermark-position top-right \
  --watermark-opacity 0.7 \
  --watermark-scale 0.15

# Combinaison: Qualité HD 16:9 avec filigrane
python whiteboard_animator.py image.png \
  --aspect-ratio 16:9 \
  --quality 18 \
  --watermark logo.png \
  --watermark-position bottom-right \
  --watermark-opacity 0.5
```

### Export des données d'animation (JSON)

```bash
# Générer une vidéo et exporter les données JSON
python whiteboard_animator.py image.png --export-json
# Plusieurs images avec export JSON (génère un fichier JSON par image)
python whiteboard_animator.py image1.png image2.png image3.png --export-json
```

**Note:** L'option `--export-json` génère un fichier JSON contenant toutes les données de l'animation (positions, timing, frames), permettant de réutiliser ou analyser la séquence de dessin.

### Export formats avancés (NOUVEAU)

```bash
# Export en GIF animé pour le web
python whiteboard_animator.py image.png --export-formats gif

# Export multiple formats (GIF + WebM)
python whiteboard_animator.py image.png --export-formats gif webm

# Export séquence PNG pour post-production
python whiteboard_animator.py image.png --export-formats png

# Export avec transparence (WebM alpha channel)
python whiteboard_animator.py image.png --export-formats webm-alpha

# Export sans perte pour archivage
python whiteboard_animator.py image.png --export-formats lossless

# Tous les formats à la fois
python whiteboard_animator.py image.png --export-formats gif webm png lossless
```

### Presets médias sociaux (NOUVEAU)

```bash
# Lister tous les presets disponibles
python whiteboard_animator.py --list-presets

# TikTok (vertical 9:16, 1080x1920)
python whiteboard_animator.py image.png --social-preset tiktok

# YouTube standard (16:9, 1920x1080)
python whiteboard_animator.py image.png --social-preset youtube

# YouTube Shorts (vertical 9:16, 1080x1920)
python whiteboard_animator.py image.png --social-preset youtube-shorts

# Instagram Reels (vertical 9:16, 1080x1920)
python whiteboard_animator.py image.png --social-preset instagram-reel

# Instagram Feed (carré 1:1, 1080x1080)
python whiteboard_animator.py image.png --social-preset instagram-feed

# Facebook (16:9, 1280x720)
python whiteboard_animator.py image.png --social-preset facebook

# Combiner preset avec exports multiples
python whiteboard_animator.py image.png --social-preset tiktok --export-formats gif webm
```

Presets disponibles: `youtube`, `youtube-shorts`, `tiktok`, `instagram-feed`, `instagram-story`, `instagram-reel`, `facebook`, `twitter`, `linkedin`

```bash
# Générer vidéo + données JSON (une image)
python whiteboard_animator.py image.png --export-json

# Plusieurs images avec export JSON (génère un fichier JSON par image)
python whiteboard_animator.py image1.png image2.png image3.png --export-json
```

Cela génère :
- Une vidéo MP4 de l'animation (combinée si plusieurs images)
- Un fichier JSON par image contenant les données d'animation (séquence de dessin, positions de la main, etc.)

### Vérifier les valeurs recommandées

```bash
python whiteboard_animator.py image.png --get-split-lens
```

## Paramètres

### Paramètres de base
- `--split-len` : Taille de la grille pour le dessin (par défaut: 15)
- `--frame-rate` : Images par seconde (par défaut: 30)
- `--skip-rate` : Vitesse de dessin (plus grand = plus rapide, par défaut: 8)
- `--duration` : **Durée TOTALE de la slide en secondes** (animation + affichage final, par défaut: 3)
  - ⚠️ **Changement important:** `duration` représente maintenant la durée totale, pas uniquement le temps d'affichage après l'animation
  - 📖 Voir [DURATION_GUIDE.md](DURATION_GUIDE.md) pour plus de détails

### Paramètres de qualité et format (NOUVEAU)
- `--quality` : Qualité vidéo CRF (0-51, plus bas = meilleure qualité, par défaut: 18)
  - 18 = Visually lossless (qualité maximale recommandée)
  - 23 = Haute qualité (bon compromis)
  - 28 = Qualité moyenne (fichiers plus petits)
- `--aspect-ratio` : Ratio d'aspect de la vidéo (par défaut: original)
  - `original` : Conserve le ratio d'aspect de l'image source
  - `1:1` : Format carré (Instagram, profils)
  - `16:9` : Format paysage HD (YouTube, télévision)
  - `9:16` : Format vertical (Stories, Reels, TikTok)

### Paramètres de filigrane (NOUVEAU)
- `--watermark` : Chemin vers l'image de filigrane (watermark) à appliquer
- `--watermark-position` : Position du filigrane (par défaut: bottom-right)
  - Choix: `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`
- `--watermark-opacity` : Opacité du filigrane (0.0 à 1.0, par défaut: 0.5)
- `--watermark-scale` : Échelle du filigrane par rapport à la largeur de la vidéo (0.0 à 1.0, par défaut: 0.1)

### Paramètres de transition
- `--transition` : Type de transition entre les slides - choix: none, fade, wipe, push_left, push_right, iris (par défaut: none)
- `--transition-duration` : Durée de la transition en secondes (par défaut: 0.5)

### Autres paramètres
- `--config` : Fichier JSON pour une configuration personnalisée par slide (durée, vitesse, transitions, pauses, etc.)
- `--export-json` : Exporter les données d'animation au format JSON
- `--get-split-lens` : Afficher les valeurs recommandées pour split-len

### Paramètres de performance (NOUVEAU)
- `--preview` : Mode preview rapide (50% résolution, qualité réduite) pour tests
- `--quality-preset` : Préréglage de qualité
  - `preview` : Test rapide (28 CRF, 50% résolution)
  - `draft` : Brouillon (28 CRF, 75% résolution)
  - `standard` : Standard (23 CRF, 100%)
  - `high` : Haute qualité (18 CRF, 100%)
  - `ultra` : Ultra qualité (15 CRF, 100%)
- `--enable-checkpoints` : Active les points de contrôle pour reprendre les rendus
- `--resume CHECKPOINT_ID` : Reprendre un rendu depuis un checkpoint
- `--list-checkpoints` : Afficher tous les checkpoints disponibles
- `--background` : Exécuter en arrière-plan avec fichier de statut
- `--batch CONFIG1 CONFIG2 ...` : Traiter plusieurs configs en batch
- `--batch-parallel` : Traiter les configs batch en parallèle
- `--threads N` : Nombre de threads pour traitement parallèle
- `--memory-efficient` : Mode optimisation mémoire pour grandes vidéos

### Exemples d'utilisation des fonctionnalités de performance

```bash
# Test rapide avec preview
python whiteboard_animator.py --config video.json --preview

# Rendu haute qualité avec checkpoints
python whiteboard_animator.py --config video.json --quality-preset high --enable-checkpoints

# Rendu en arrière-plan
python whiteboard_animator.py --config video.json --background

# Traitement batch de plusieurs vidéos
python whiteboard_animator.py --batch video1.json video2.json video3.json

# Reprendre un rendu interrompu
python whiteboard_animator.py --list-checkpoints
python whiteboard_animator.py --resume a1b2c3d4e5f6g7h8

# Optimisation mémoire pour grande vidéo
python whiteboard_animator.py --config large_video.json --memory-efficient
```

**Voir [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md) pour plus de détails sur les optimisations de performance.**

## Configuration personnalisée par slide

Utilisez le paramètre `--config` avec un fichier JSON pour personnaliser chaque slide individuellement :

```bash
python whiteboard_animator.py slide1.png slide2.png slide3.png --config config.json
```

Le fichier de configuration permet de définir :
- **Durée d'affichage** différente pour chaque slide
- **Vitesse de dessin** (skip-rate) différente pour chaque slide
- **Type de transition** spécifique entre chaque slide
- **Durée de transition** personnalisée entre chaque slide
- **Pause avant transition** pour ajouter un temps d'attente entre les slides

### Exemple de fichier de configuration

```json
{
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
    }
  ],
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

Voir [CONFIG_FORMAT.md](CONFIG_FORMAT.md) pour la documentation complète du format de configuration.

## Formes géométriques (NOUVEAU! 🔷)

Créez des diagrammes, des schémas et des illustrations techniques avec des formes vectorielles animées :

### Formes disponibles
- **Cercles** - Formes circulaires parfaites
- **Rectangles** - Rectangles et carrés
- **Triangles** - Triangles équilatéraux
- **Polygones** - Formes personnalisées avec n'importe quel nombre de côtés
- **Lignes** - Lignes droites entre deux points
- **Flèches** - Flèches avec tête personnalisable

### 🆕 Type Flèche (Arrow Type)

Un nouveau type de couche `arrow` permet d'animer des flèches de manière progressive, comme si on les dessinait à la main :

```json
{
  "type": "arrow",
  "arrow_config": {
    "start": [200, 400],
    "end": [800, 400],
    "color": "#E74C3C",
    "fill_color": "#F1948A",
    "stroke_width": 5,
    "arrow_size": 40,
    "duration": 2.0
  },
  "z_index": 1,
  "mode": "draw"
}
```

**Différence avec les flèches de type shape:**
- **Type `arrow`**: Animation progressive naturelle, durée contrôlée
- **Type `shape` avec `shape: "arrow"`**: Dessin standard par tuiles

Voir [ARROW_TYPE_GUIDE.md](ARROW_TYPE_GUIDE.md) pour la documentation complète.

### Exemple d'utilisation

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "type": "shape",
          "shape_config": {
            "shape": "circle",
            "color": "#0066CC",
            "fill_color": "#99CCFF",
            "stroke_width": 3,
            "position": {"x": 640, "y": 360},
            "size": 100
          },
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "arrow",
            "color": "#FF6600",
            "stroke_width": 4,
            "start": [200, 400],
            "end": [1000, 400],
            "arrow_size": 30
          },
          "z_index": 2,
          "skip_rate": 8,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

Voir [SHAPES_GUIDE.md](SHAPES_GUIDE.md) pour la documentation complète des formes géométriques et [QUICKSTART_SHAPES.md](QUICKSTART_SHAPES.md) pour démarrer rapidement.

## Contrôles de caméra et animations avancées (NOUVEAU)

Whiteboard-It supporte maintenant des contrôles de caméra cinématiques et des effets d'animation avancés pour créer des vidéos plus dynamiques.

### Contrôles de caméra (par couche)

Zoomez et focalisez sur des zones spécifiques de vos couches :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "diagram.png",
          "z_index": 1,
          "camera": {
            "zoom": 1.5,
            "position": {"x": 0.5, "y": 0.5}
          }
        }
      ]
    }
  ]
}
```

### Système de caméra avancé - Séquences multiples (NOUVEAU! 🎥)

Créez des mouvements de caméra cinématiques avec plusieurs caméras et des transitions fluides :

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
          "duration": 2.5,
          "transition_duration": 1.0,
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

**Caractéristiques du système de caméra avancé:**
- ✨ Plusieurs caméras par slide avec durées individuelles
- 🎬 Transitions fluides entre caméras avec fonctions d'easing
- 📐 Taille de caméra personnalisable (ex: 2275x1280)
- 🎯 Contrôle précis du zoom et de la position
- ⚙️ Fonctions d'easing: `linear`, `ease_in`, `ease_out`, `ease_in_out`, `ease_in_cubic`, `ease_out_cubic`

📖 **Documentation complète**: [ADVANCED_CAMERA_GUIDE.md](ADVANCED_CAMERA_GUIDE.md)

### Animations post-dessin

Ajoutez des effets de zoom après le dessin de la couche :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "product.png",
          "z_index": 1,
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
  ]
}
```

**Effets disponibles:**
- `zoom_in` : Zoom progressif vers l'intérieur
- `zoom_out` : Zoom progressif vers l'extérieur

Voir [CAMERA_ANIMATION_GUIDE.md](CAMERA_ANIMATION_GUIDE.md) pour la documentation complète des contrôles de caméra et animations.

## Couches de texte dynamiques (NOUVEAU! 🆕)

Créez des animations de texte sans avoir besoin de créer des images ! Le texte est généré dynamiquement et animé avec l'effet handwriting.

### Exemple de base

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
            "text": "Bonjour!\nCeci est un texte\navec animation handwriting",
            "font": "DejaVuSans",
            "size": 48,
            "color": [0, 0, 255],
            "style": "bold",
            "line_height": 1.5,
            "align": "center"
          }
        }
      ]
    }
  ]
}
```

### Fonctionnalités des couches de texte

- **Multi-ligne** : Utilisez `\n` pour les sauts de ligne
- **Polices personnalisées** : N'importe quelle police système
- **Styles** : normal, bold, italic, bold_italic
- **Couleurs** : RGB tuples, codes hex, noms de couleurs
- **Alignement** : left, center, right
- **Position** : Positionnement absolu avec x, y
- **Animation** : Handwriting par colonnes (défaut), SVG path-based (opt-in), static, eraser
- **Animations d'entrée/sortie** : fade_in, slide_in, zoom_in, etc.

**Note:** Par défaut, le texte utilise l'animation **column-based** (non-SVG) pour une meilleure compatibilité. Pour activer l'animation SVG path-based, ajoutez `"use_svg_paths": true` dans `text_config`.

### Mélanger texte et images

```json
{
  "layers": [
    {
      "image_path": "background.png",
      "z_index": 1
    },
    {
      "type": "text",
      "z_index": 2,
      "text_config": {
        "text": "Titre sur l'image",
        "size": 64,
        "color": "#FFFFFF",
        "style": "bold"
      }
    }
  ]
}
```

**📚 Guide complet:** Voir [TEXT_LAYERS_GUIDE.md](TEXT_LAYERS_GUIDE.md) pour la documentation complète des couches de texte.

## Format d'export JSON

Voir [EXPORT_FORMAT.md](EXPORT_FORMAT.md) pour la documentation complète du format JSON.

Les données exportées incluent :
- Métadonnées (résolution, FPS, paramètres)
- Séquence de dessin frame par frame
- Positions de la main pour chaque frame
- Coordonnées des tuiles dessinées

## Exemples d'utilisation

Le dossier [examples/](examples/) contient des scripts d'exemple pour utiliser les données JSON exportées :

```bash
# Analyser une animation
python examples/use_animation_data.py animation.json

# Analyser et exporter une séquence simplifiée
python examples/use_animation_data.py animation.json --export-sequence sequence.json
```

## Cas d'utilisation du format JSON

L'export JSON permet de :
1. **Recréer l'animation** dans d'autres logiciels (After Effects, Blender, VideoScribe, etc.)
2. **Analyser la séquence** pour optimiser les paramètres
3. **Créer des animations personnalisées** en modifiant les données
4. **Intégrer dans des applications web** avec Canvas ou WebGL
5. **Générer des animations procédurales** basées sur les données

## Exemples d'utilisation avancés

### Traitement par lot avec plusieurs images

```bash
# Créer une animation combinée à partir de 3 images
python whiteboard_animator.py slide1.png slide2.png slide3.png

# Avec export JSON pour chaque image
python whiteboard_animator.py slide1.png slide2.png slide3.png --export-json

# Personnaliser la vitesse de dessin
python whiteboard_animator.py img1.png img2.png --skip-rate 15 --duration 2

# Avec transition en fondu entre les slides
python whiteboard_animator.py slide1.png slide2.png slide3.png --transition fade

# Avec configuration personnalisée par slide
python whiteboard_animator.py slide1.png slide2.png slide3.png --config my_config.json

# Configuration personnalisée + paramètres globaux
python whiteboard_animator.py slide1.png slide2.png slide3.png \
  --config my_config.json \
  --frame-rate 30 \
  --export-json
```

### Configuration personnalisée avancée

Créez un fichier `advanced_config.json` :

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
      "duration": 4,
      "skip_rate": 20
    },
    {
      "index": 2,
      "duration": 3,
      "skip_rate": 12
    }
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

Puis utilisez-le :

```bash
python whiteboard_animator.py slide1.png slide2.png slide3.png --config advanced_config.json
```

Ce fichier de configuration :
- Définit des durées et vitesses différentes pour chaque slide
- Ajoute une pause de 2 secondes après la première slide avant la transition fade
- Ajoute une pause de 1.5 secondes après la deuxième slide avant la transition iris

### Utilisation des couches multiples (layers) (NOUVEAU)

Les couches permettent de superposer plusieurs images sur une même slide, chacune avec sa position, son ordre de superposition (z-index) et sa vitesse de dessin.

Créez un fichier `layers_config.json` :

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 4,
      "layers": [
        {
          "image_path": "background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 5
        },
        {
          "image_path": "logo.png",
          "position": {"x": 50, "y": 50},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.3,
          "opacity": 0.9
        },
        {
          "image_path": "text.png",
          "position": {"x": 200, "y": 400},
          "z_index": 3,
          "skip_rate": 20,
          "opacity": 0.8
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

Puis utilisez-le (vous devez toujours fournir au moins une image en ligne de commande) :

```bash
# L'image placeholder.png définit le nombre de slides mais sera ignorée pour la slide 0
python whiteboard_animator.py placeholder.png slide2.png --config layers_config.json
```

**Fonctionnalités des couches :**
- **position** : Positionnement précis (x, y en pixels)
- **z_index** : Ordre de superposition (plus grand = au-dessus)
- **scale** : Échelle de l'image (0.5 = 50%, 1.0 = taille originale)
- **opacity** : Transparence (0.0 = invisible, 1.0 = opaque)
- **skip_rate** : Vitesse de dessin individuelle pour chaque couche

Les couches sont dessinées séquentiellement selon leur z_index, permettant de créer des animations complexes avec plusieurs éléments apparaissant l'un après l'autre sur la même scène.

**Cas d'usage :**
- **Compositions complexes** : Logo + texte + éléments graphiques sur un même fond
- **Animations par étapes** : Dessiner d'abord le fond, puis ajouter des éléments progressivement
- **Créations style "Insta Doodle"** : Superposition d'images avec positions et timing personnalisés

**🎨 Dessin progressif par couche** : Les couches sont dessinées séquentiellement tout en préservant les couches précédentes, créant un effet additif naturel similaire à VideoScribe et Doodly.

📖 **Pour plus de détails, consultez :**
- [Guide complet des couches (LAYERS_GUIDE.md)](LAYERS_GUIDE.md)
- [Guide du dessin progressif par couche (PROGRESSIVE_LAYER_DRAWING.md)](PROGRESSIVE_LAYER_DRAWING.md)


# Avec transition de type "push left" et durée personnalisée
python whiteboard_animator.py slide1.png slide2.png --transition push_left --transition-duration 1.0

# Tous les types de transitions disponibles
python whiteboard_animator.py img1.png img2.png img3.png --transition iris --transition-duration 0.8
```

### Transitions disponibles

- **none** : Pas de transition (changement instantané)
- **fade** : Fondu enchaîné entre les slides
- **wipe** : Balayage de gauche à droite
- **push_left** : Pousse la slide actuelle vers la gauche
- **push_right** : Pousse la slide actuelle vers la droite
- **iris** : Transition en cercle qui s'agrandit depuis le centre

### Cas d'usage typiques

- **Présentation animée** : Combiner plusieurs diapositives en une vidéo continue
- **Tutoriel illustré** : Dessiner étape par étape des diagrammes ou schémas
- **Story-board animé** : Transformer une série d'images en animation fluide
- **Contenu éducatif** : Créer des vidéos explicatives avec dessins successifs

## Structure du projet

```
whiteboard-it/
├── whiteboard_animator.py   # Script principal
├── data/
│   └── images/              # Images de la main
├── save_videos/             # Dossier de sortie (ignoré par git)
├── examples/                # Scripts d'exemple
│   ├── use_animation_data.py
│   └── README.md
├── CONFIG_FORMAT.md         # Documentation du format de configuration
├── EXPORT_FORMAT.md         # Documentation du format JSON d'export
├── LAYERS_GUIDE.md          # Guide complet des couches (layers)
├── TRANSITIONS.md           # Documentation des transitions
└── README.md               # Ce fichier
```

## Documentation

- **[CONFIG_FORMAT.md](CONFIG_FORMAT.md)** - Format de configuration JSON pour personnaliser les slides
- **[LAYERS_GUIDE.md](LAYERS_GUIDE.md)** - Guide complet pour utiliser les couches multiples
- **[INTELLIGENT_ERASER.md](INTELLIGENT_ERASER.md)** - Guide de la gomme intelligente pour les superpositions de couches
- **[EXPORT_FORMAT.md](EXPORT_FORMAT.md)** - Format des données d'animation exportées
- **[TRANSITIONS.md](TRANSITIONS.md)** - Documentation détaillée des transitions
- **[examples/README.md](examples/README.md)** - Exemples d'utilisation des données JSON

## Licence

MIT

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.
