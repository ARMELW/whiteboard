# Guide des Formats d'Export / Export Formats Guide

## Vue d'ensemble / Overview

Ce guide explique les nouvelles fonctionnalités d'export avancées disponibles dans Whiteboard Animator, incluant GIF animé, WebM, séquences PNG, support de transparence, et presets pour les médias sociaux.

This guide explains the advanced export features available in Whiteboard Animator, including animated GIF, WebM, PNG sequences, transparency support, and social media presets.

---

## 📦 Formats d'Export Disponibles / Available Export Formats

### 1. GIF Animé / Animated GIF

Export en format GIF animé, idéal pour le web et les réseaux sociaux.

**Utilisation / Usage:**
```bash
python whiteboard_animator.py image.png --export-formats gif
```

**Caractéristiques:**
- Format universel compatible avec tous les navigateurs
- Taille de fichier optimisée
- FPS réduit à 10 pour réduire la taille (configurable)
- Boucle infinie par défaut

**Cas d'usage:**
- Prévisualisations web
- Posts sur réseaux sociaux (Twitter, Reddit)
- Documentation et tutoriels
- Emails

---

### 2. WebM

Format vidéo moderne optimisé pour le web, avec codec VP9.

**Utilisation / Usage:**
```bash
python whiteboard_animator.py image.png --export-formats webm
```

**Caractéristiques:**
- Codec VP9 haute qualité
- Meilleure compression que MP4 pour la même qualité
- Support natif dans les navigateurs modernes
- Qualité configurable (CRF)

**Cas d'usage:**
- Vidéos web haute qualité
- Streaming web
- Animations pour sites web modernes

---

### 3. WebM avec Transparence / WebM with Alpha

Export WebM avec canal alpha pour la transparence.

**Utilisation / Usage:**
```bash
python whiteboard_animator.py image.png --export-formats webm-alpha
# ou
python whiteboard_animator.py image.png --export-formats transparent
```

**Caractéristiques:**
- Support du canal alpha (transparence)
- Codec VP9 avec format yuva420p
- Permet de superposer la vidéo sur d'autres contenus
- Idéal pour les overlays et effets spéciaux

**Cas d'usage:**
- Overlays vidéo
- Effets spéciaux web
- Intégrations web complexes
- Vidéos pour compositing

---

### 4. Séquence PNG / PNG Sequence

Export sous forme de séquence d'images PNG numérotées.

**Utilisation / Usage:**
```bash
python whiteboard_animator.py image.png --export-formats png
# ou
python whiteboard_animator.py image.png --export-formats png-sequence
```

**Caractéristiques:**
- Chaque frame sauvegardée en PNG individuel
- Numérotation automatique (frame_000001.png, frame_000002.png, etc.)
- Qualité sans perte
- Facile à manipuler frame par frame

**Cas d'usage:**
- Post-production vidéo
- Compositing dans After Effects, Premiere, etc.
- Retouche frame par frame
- Import dans d'autres logiciels d'animation

---

### 5. Export Sans Perte / Lossless Export

Export vidéo sans perte avec codec FFV1.

**Utilisation / Usage:**
```bash
python whiteboard_animator.py image.png --export-formats lossless
```

**Caractéristiques:**
- Codec FFV1 (lossless)
- Qualité parfaite (aucune perte)
- Fichiers volumineux
- Format MKV

**Cas d'usage:**
- Archivage de qualité
- Maître pour production professionnelle
- Quand la qualité prime sur la taille du fichier

---

## 📱 Presets Médias Sociaux / Social Media Presets

Des configurations pré-définies optimisées pour chaque plateforme sociale.

### Presets Disponibles / Available Presets

#### YouTube Standard
```bash
python whiteboard_animator.py image.png --social-preset youtube
```
- **Résolution:** 1920x1080 (Full HD)
- **Ratio:** 16:9
- **FPS:** 30
- **Format:** MP4 H.264

#### YouTube Shorts
```bash
python whiteboard_animator.py image.png --social-preset youtube-shorts
```
- **Résolution:** 1080x1920 (vertical)
- **Ratio:** 9:16
- **FPS:** 30
- **Format:** MP4 H.264

#### TikTok
```bash
python whiteboard_animator.py image.png --social-preset tiktok
```
- **Résolution:** 1080x1920 (vertical)
- **Ratio:** 9:16
- **FPS:** 30
- **Format:** MP4 H.264

#### Instagram Feed (Carré)
```bash
python whiteboard_animator.py image.png --social-preset instagram-feed
```
- **Résolution:** 1080x1080 (carré)
- **Ratio:** 1:1
- **FPS:** 30
- **Format:** MP4 H.264

#### Instagram Story / Reels
```bash
python whiteboard_animator.py image.png --social-preset instagram-story
# ou
python whiteboard_animator.py image.png --social-preset instagram-reel
```
- **Résolution:** 1080x1920 (vertical)
- **Ratio:** 9:16
- **FPS:** 30
- **Format:** MP4 H.264

#### Facebook
```bash
python whiteboard_animator.py image.png --social-preset facebook
```
- **Résolution:** 1280x720 (HD)
- **Ratio:** 16:9
- **FPS:** 30
- **Format:** MP4 H.264

#### Twitter / X
```bash
python whiteboard_animator.py image.png --social-preset twitter
```
- **Résolution:** 1280x720 (HD)
- **Ratio:** 16:9
- **FPS:** 30
- **Format:** MP4 H.264

#### LinkedIn
```bash
python whiteboard_animator.py image.png --social-preset linkedin
```
- **Résolution:** 1920x1080 (Full HD)
- **Ratio:** 16:9
- **FPS:** 30
- **Format:** MP4 H.264

### Lister Tous les Presets / List All Presets
```bash
python whiteboard_animator.py --list-presets
```

---

## 🔄 Exports Multiples / Multiple Exports

Vous pouvez exporter vers plusieurs formats en une seule commande:

```bash
python whiteboard_animator.py image.png --export-formats gif webm png
```

Ceci générera:
- `vid_YYYYMMDD_HHMMSS_h264.mp4` (vidéo principale)
- `vid_YYYYMMDD_HHMMSS_h264.gif` (version GIF)
- `vid_YYYYMMDD_HHMMSS_h264.webm` (version WebM)
- `vid_YYYYMMDD_HHMMSS_h264_frames/` (séquence PNG)

---

## 💡 Exemples Pratiques / Practical Examples

### Exemple 1: Post Instagram complet
```bash
# Génère une vidéo optimisée pour Instagram Reels + GIF pour preview
python whiteboard_animator.py image.png \
  --social-preset instagram-reel \
  --export-formats gif \
  --quality 23
```

### Exemple 2: Vidéo YouTube avec backup lossless
```bash
# Vidéo YouTube + version sans perte pour archivage
python whiteboard_animator.py image.png \
  --social-preset youtube \
  --export-formats lossless
```

### Exemple 3: Pack complet multi-plateforme
```bash
# Génère tous les formats pour distribution
python whiteboard_animator.py image.png \
  --aspect-ratio 16:9 \
  --export-formats gif webm png \
  --quality 20
```

### Exemple 4: Overlay transparent pour site web
```bash
# Vidéo avec transparence pour intégration web
python whiteboard_animator.py image.png \
  --export-formats webm-alpha \
  --aspect-ratio 1:1
```

### Exemple 5: Post-production professionnelle
```bash
# Export séquence PNG pour édition dans After Effects
python whiteboard_animator.py image.png \
  --export-formats png lossless \
  --quality 18 \
  --frame-rate 30
```

---

## ⚙️ Compatibilité et Dépendances / Compatibility and Dependencies

### Dépendances Requises / Required Dependencies

```bash
pip install Pillow opencv-python numpy av
```

- **Pillow**: Pour export GIF
- **opencv-python**: Pour manipulation d'images et PNG
- **PyAV (av)**: Pour WebM, lossless, et transparence
- **numpy**: Pour traitement des frames

### Support des Formats par Plateforme

| Format | Windows | macOS | Linux |
|--------|---------|-------|-------|
| GIF | ✅ | ✅ | ✅ |
| WebM | ✅ | ✅ | ✅ |
| PNG Sequence | ✅ | ✅ | ✅ |
| WebM Alpha | ✅ | ✅ | ✅ |
| Lossless (FFV1) | ✅ | ✅ | ✅ |

---

## 🎯 Choix du Format / Choosing the Right Format

### Pour le Web / For Web
- **GIF**: Compatibilité maximale, animations courtes
- **WebM**: Meilleure qualité/taille, navigateurs modernes
- **WebM Alpha**: Overlays et effets spéciaux

### Pour les Médias Sociaux / For Social Media
- Utilisez les **presets** appropriés (--social-preset)
- Ajoutez **GIF** pour preview rapide
- **MP4** reste le format principal

### Pour la Post-Production / For Post-Production
- **PNG Sequence**: Maximum de flexibilité
- **Lossless**: Qualité maximale pour maître
- **MP4 CRF 18**: Bon compromis qualité/taille

### Pour le Partage / For Sharing
- **MP4**: Format universel
- **GIF**: Preview et partage rapide
- **WebM**: Web moderne

---

## 📊 Comparaison des Tailles de Fichiers / File Size Comparison

Pour une vidéo de 10 secondes à 1920x1080:

| Format | Taille Approximative | Qualité | Cas d'usage |
|--------|---------------------|---------|-------------|
| MP4 (CRF 23) | ~5 MB | Élevée | Standard |
| WebM (CRF 10) | ~4 MB | Élevée | Web moderne |
| GIF | ~3-8 MB | Moyenne | Web universel |
| PNG Sequence | ~150-300 MB | Maximale | Post-production |
| Lossless (FFV1) | ~200-400 MB | Parfaite | Archivage |
| WebM Alpha | ~6-10 MB | Élevée | Transparence |

---

## 🔧 Résolution des Problèmes / Troubleshooting

### Le module 'av' n'est pas installé
```bash
pip install av
```

### Erreur lors de l'export GIF
Assurez-vous que Pillow est installé:
```bash
pip install --upgrade Pillow
```

### Fichier WebM trop volumineux
Ajustez la qualité:
```bash
python whiteboard_animator.py image.png --export-formats webm --quality 15
```

### Séquence PNG prend trop d'espace
- Utilisez une résolution plus faible
- Réduisez le nombre de frames (augmentez --skip-rate)
- Compressez après export

---

## 📚 Voir Aussi / See Also

- [VIDEO_QUALITY.md](VIDEO_QUALITY.md) - Guide de qualité vidéo
- [EXPORT_FORMAT.md](EXPORT_FORMAT.md) - Format d'export JSON
- [README.md](README.md) - Documentation principale
- [CONFIG_FORMAT.md](CONFIG_FORMAT.md) - Format de configuration

---

## 🆕 Nouveautés de cette Mise à Jour

Cette mise à jour ajoute les fonctionnalités suivantes:

✅ **Export GIF animé** - Format universel pour le web
✅ **Export WebM** - Codec VP9 moderne
✅ **Séquences PNG** - Pour post-production
✅ **Support de transparence** - WebM avec canal alpha
✅ **Export sans perte** - FFV1 lossless
✅ **Presets médias sociaux** - 9 plateformes supportées
✅ **Exports multiples** - Plusieurs formats en une commande

Toutes ces fonctionnalités s'intègrent parfaitement avec les fonctionnalités existantes (transitions, couches, effets de caméra, etc.).
