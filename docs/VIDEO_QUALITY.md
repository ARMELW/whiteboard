# Guide de Qualité Vidéo et Formats d'Export

Ce guide explique les nouvelles fonctionnalités de qualité vidéo et d'export en différents formats.

## Qualité Vidéo (CRF)

### Qu'est-ce que le CRF ?

CRF (Constant Rate Factor) est un paramètre de qualité pour l'encodage vidéo H.264 :
- **Plage** : 0-51
- **Plus bas = meilleure qualité** (mais fichiers plus volumineux)
- **Plus haut = qualité réduite** (fichiers plus petits)

### Valeurs recommandées

| CRF | Qualité | Usage recommandé | Taille fichier |
|-----|---------|------------------|----------------|
| 18 | Visually lossless | YouTube, archives, présentations professionnelles | Grande |
| 23 | Haute qualité | Usage général, réseaux sociaux | Moyenne |
| 28 | Qualité moyenne | Brouillons, partage rapide | Petite |

### Par défaut

Le paramètre par défaut est **CRF 18** (visually lossless) pour garantir la meilleure qualité possible du rendu vidéo.

### Utilisation

```bash
# Qualité par défaut (18)
python whiteboard_animator.py image.png

# Haute qualité
python whiteboard_animator.py image.png --quality 18

# Qualité standard
python whiteboard_animator.py image.png --quality 23

# Qualité réduite (fichiers plus petits)
python whiteboard_animator.py image.png --quality 28
```

## Formats d'Export (Ratios d'Aspect)

### Ratios disponibles

#### 1. Original (par défaut)
- Conserve le ratio d'aspect de l'image source
- Redimensionne à la résolution standard la plus proche

```bash
python whiteboard_animator.py image.png --aspect-ratio original
```

#### 2. Format 16:9 (Paysage HD)
- **Résolutions** : 1920x1080 (Full HD), 1280x720 (HD)
- **Usage** : YouTube, télévision, présentations
- Ajoute des bandes blanches (letterboxing) si nécessaire

```bash
python whiteboard_animator.py image.png --aspect-ratio 16:9
```

#### 3. Format 9:16 (Vertical)
- **Résolutions** : 1080x1920, 720x1280
- **Usage** : TikTok, Instagram Reels, Stories, Shorts YouTube
- Ajoute des bandes blanches (pillarboxing) si nécessaire

```bash
python whiteboard_animator.py image.png --aspect-ratio 9:16
```

#### 4. Format 1:1 (Carré)
- **Usage** : Instagram posts, profils, contenus carrés
- Adapte l'image dans un cadre carré

```bash
python whiteboard_animator.py image.png --aspect-ratio 1:1
```

### Gestion automatique

Le système ajoute automatiquement un **padding blanc** (letterboxing ou pillarboxing) pour maintenir le ratio d'aspect cible sans déformer l'image originale.

## Filigrane (Watermark)

### Fonctionnalités

- Support des images **PNG avec transparence**
- Position configurable
- Opacité ajustable
- Taille ajustable

### Paramètres

| Paramètre | Description | Valeurs | Défaut |
|-----------|-------------|---------|--------|
| `--watermark` | Chemin vers l'image | Chemin fichier | - |
| `--watermark-position` | Position | `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center` | `bottom-right` |
| `--watermark-opacity` | Opacité | 0.0 - 1.0 | 0.5 |
| `--watermark-scale` | Échelle (% largeur vidéo) | 0.0 - 1.0 | 0.1 (10%) |

### Exemples

```bash
# Filigrane basique
python whiteboard_animator.py image.png --watermark logo.png

# Filigrane en haut à gauche, plus visible
python whiteboard_animator.py image.png \
  --watermark logo.png \
  --watermark-position top-left \
  --watermark-opacity 0.8

# Filigrane discret en bas à droite
python whiteboard_animator.py image.png \
  --watermark logo.png \
  --watermark-position bottom-right \
  --watermark-opacity 0.3 \
  --watermark-scale 0.08

# Filigrane centré, semi-transparent
python whiteboard_animator.py image.png \
  --watermark logo.png \
  --watermark-position center \
  --watermark-opacity 0.2 \
  --watermark-scale 0.3
```

### Création d'un filigrane

Pour créer un filigrane PNG avec transparence :

```python
import cv2
import numpy as np

# Créer une image avec canal alpha (transparence)
watermark = np.zeros((100, 300, 4), dtype=np.uint8)

# Ajouter du texte blanc
cv2.putText(watermark, 'Mon Logo', (10, 60), 
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255, 255), 3)

# Définir la transparence (canal alpha)
watermark[:, :, 3] = 200  # 0-255, 200 = semi-transparent

# Sauvegarder
cv2.imwrite('mon_logo.png', watermark)
```

## Exemples de Cas d'Usage

### 1. Vidéo YouTube professionnelle

```bash
python whiteboard_animator.py presentation.png \
  --aspect-ratio 16:9 \
  --quality 18 \
  --watermark logo.png \
  --watermark-position bottom-right \
  --watermark-opacity 0.6
```

**Résultat** : Vidéo 1920x1080 en qualité maximale avec logo discret

### 2. Stories Instagram/TikTok

```bash
python whiteboard_animator.py story.png \
  --aspect-ratio 9:16 \
  --quality 23 \
  --watermark brand.png \
  --watermark-position top-right \
  --watermark-scale 0.12
```

**Résultat** : Vidéo verticale 1080x1920 optimisée pour mobile

### 3. Post Instagram carré

```bash
python whiteboard_animator.py post.png \
  --aspect-ratio 1:1 \
  --quality 23 \
  --watermark watermark.png
```

**Résultat** : Vidéo carrée pour feed Instagram

### 4. Plusieurs images avec qualité uniforme

```bash
python whiteboard_animator.py slide1.png slide2.png slide3.png \
  --aspect-ratio 16:9 \
  --quality 18 \
  --transition fade \
  --watermark logo.png \
  --watermark-opacity 0.5
```

**Résultat** : Présentation multi-slides en HD avec transitions et logo

## Comparaison de Taille de Fichier

Pour une vidéo de 1 minute à 1920x1080 :

| CRF | Qualité | Taille approximative |
|-----|---------|---------------------|
| 18 | Visually lossless | ~50-70 MB |
| 23 | Haute qualité | ~20-30 MB |
| 28 | Qualité moyenne | ~10-15 MB |

**Note** : Les tailles varient selon le contenu (complexité, mouvement, couleurs)

## Conseils

### Pour la meilleure qualité
- Utilisez `--quality 18`
- Utilisez le format natif de votre plateforme cible
- Activez `--aspect-ratio 16:9` pour YouTube

### Pour des fichiers plus légers
- Utilisez `--quality 28` pour les brouillons
- Utilisez `--quality 23` pour un bon compromis

### Pour les réseaux sociaux
- **YouTube** : `--aspect-ratio 16:9 --quality 18`
- **TikTok/Reels** : `--aspect-ratio 9:16 --quality 23`
- **Instagram** : `--aspect-ratio 1:1 --quality 23`
- **Twitter/X** : `--aspect-ratio 16:9 --quality 23`

### Pour le filigrane
- Utilisez des PNG avec transparence pour un meilleur rendu
- Gardez `--watermark-opacity` entre 0.3 et 0.7 pour lisibilité
- Utilisez `--watermark-scale` entre 0.08 et 0.15 selon le logo
- Position `bottom-right` est la plus discrète et professionnelle

## Résolution des Problèmes

### Le filigrane n'apparaît pas
- Vérifiez que le chemin du fichier est correct
- Assurez-vous que le fichier est un PNG valide
- Augmentez `--watermark-opacity` (ex: 0.8)

### La qualité est insuffisante
- Réduisez la valeur `--quality` (essayez 18 ou 15)
- Vérifiez que l'image source est de bonne qualité
- Utilisez un format d'aspect approprié

### Les fichiers sont trop volumineux
- Augmentez `--quality` (essayez 28 ou 30)
- Réduisez la durée avec `--duration`
- Augmentez `--skip-rate` pour des animations plus rapides

### L'aspect ratio ne correspond pas
- Vérifiez que vous utilisez le bon format pour votre plateforme
- Les bandes blanches sont normales pour maintenir le ratio
- Recadrez l'image source si vous voulez éviter le padding
