# Guide d'utilisation des couches (Layers)

## Vue d'ensemble

La fonctionnalité de couches (layers) permet de superposer plusieurs images sur une même slide, similaire à des applications comme Insta Doodle. Chaque couche peut être positionnée précisément, avoir sa propre vitesse d'animation, et des propriétés visuelles personnalisées.

## Cas d'usage

### 1. Créer une composition complexe

Imaginez que vous voulez créer une animation avec :
- Un fond dégradé
- Un logo en haut à gauche
- Du texte explicatif en bas

Avec les couches, vous pouvez dessiner chaque élément séparément avec son propre timing.

### 2. Animation progressive

Vous pouvez dessiner d'abord le fond lentement, puis ajouter rapidement des éléments graphiques, créant un effet visuel dynamique.

### 3. Compositions multi-éléments

Créez des scènes avec plusieurs éléments superposés, chacun avec sa transparence et son échelle.

## Configuration des couches

### Structure de base

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 4,
      "layers": [
        {
          "image_path": "chemin/vers/image1.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 5,
          "scale": 1.0,
          "opacity": 1.0
        }
      ]
    }
  ]
}
```

### Propriétés des couches

#### image_path (requis)
Chemin vers l'image de la couche. Peut être absolu ou relatif au répertoire de travail.

**Exemple :**
```json
"image_path": "assets/background.png"
```

#### position (optionnel, défaut: {x: 0, y: 0})
Position de la couche sur le canvas en pixels.

**Exemple :**
```json
"position": {"x": 100, "y": 50}
```
Place l'image à 100 pixels de la gauche et 50 pixels du haut.

#### z_index (optionnel, défaut: 0)
Ordre de superposition. Plus le nombre est grand, plus la couche est au-dessus.

**Exemple :**
```json
"z_index": 1  // Fond
"z_index": 2  // Éléments intermédiaires
"z_index": 3  // Premier plan
```

Les couches sont dessinées dans l'ordre croissant de z_index.

#### skip_rate (optionnel, hérite de la slide)
Vitesse de dessin de cette couche spécifiquement. Plus le nombre est élevé, plus le dessin est rapide.

**Exemple :**
```json
"skip_rate": 5   // Dessin lent
"skip_rate": 20  // Dessin rapide
```

#### scale (optionnel, défaut: 1.0)
Échelle de l'image. 1.0 = taille originale, 0.5 = 50% de la taille, 2.0 = double taille.

**Exemple :**
```json
"scale": 0.3  // Réduit l'image à 30% de sa taille
```

#### opacity (optionnel, défaut: 1.0)
Opacité de la couche. 1.0 = complètement opaque, 0.0 = invisible.

**Exemple :**
```json
"opacity": 0.8  // 80% d'opacité (légèrement transparent)
```

#### mode (optionnel, défaut: "draw")
Mode de dessin de la couche. Détermine comment l'élément est affiché.

**Valeurs possibles :**
- `"draw"` : Mode normal avec animation de la main dessinant
- `"eraser"` : Animation avec une gomme (pour effet d'effacement)
- `"static"` : Affichage direct sans animation de dessin

**Exemple :**
```json
"mode": "eraser"  // Utilise l'animation de gomme
```

#### entrance_animation (optionnel, défaut: null)
Animation d'entrée appliquée quand la couche apparaît.

**Propriétés :**
- `type` : Type d'animation (`fade_in`, `slide_in_left`, `slide_in_right`, `slide_in_top`, `slide_in_bottom`, `zoom_in`, `none`)
- `duration` : Durée en secondes (défaut: 0.5)

**Exemple :**
```json
"entrance_animation": {
  "type": "fade_in",
  "duration": 1.0
}
```

#### exit_animation (optionnel, défaut: null)
Animation de sortie appliquée à la fin de la couche.

**Propriétés :**
- `type` : Type d'animation (`fade_out`, `slide_out_left`, `slide_out_right`, `slide_out_top`, `slide_out_bottom`, `zoom_out`, `none`)
- `duration` : Durée en secondes (défaut: 0.5)

**Exemple :**
```json
"exit_animation": {
  "type": "zoom_out",
  "duration": 0.8
}
```

#### morph (optionnel, défaut: null)
Morphing depuis la couche précédente pour une transition fluide.

**Propriétés :**
- `enabled` : Active le morphing (true/false)
- `duration` : Durée en secondes

**Exemple :**
```json
"morph": {
  "enabled": true,
  "duration": 0.5
}
```
#### type (optionnel, défaut: "image")
Type de couche. Actuellement supporte `image` et `text` (pour référence future).

**Exemple :**
```json
"type": "image"
```

#### camera (optionnel, défaut: null)
Configuration de la caméra pour zoomer et se concentrer sur des zones spécifiques.

**Propriétés :**
- `zoom` (float) : Niveau de zoom (1.0 = normal, 2.0 = zoom x2)
- `position` (object) : Point focal avec `x` et `y` (0.0-1.0, où 0.5 = centre)

**Exemple :**
```json
"camera": {
  "zoom": 1.5,
  "position": {"x": 0.5, "y": 0.3}
}
```
Ce zoom 1.5x se concentre sur la partie supérieure-centrale de la couche.

#### animation (optionnel, défaut: null)
Effets d'animation appliqués après le dessin de la couche.

**Propriétés :**
- `type` (string) : Type d'effet - `none`, `zoom_in`, `zoom_out`
- `duration` (float) : Durée de l'effet en secondes
- `start_zoom` (float) : Niveau de zoom de départ
- `end_zoom` (float) : Niveau de zoom final
- `focus_position` (object) : Point focal pendant le zoom

**Exemple zoom-in :**
```json
"animation": {
  "type": "zoom_in",
  "duration": 1.5,
  "start_zoom": 1.0,
  "end_zoom": 2.0,
  "focus_position": {"x": 0.6, "y": 0.4}
}
```
Zoome progressivement de 1.0x à 2.0x en se concentrant sur (0.6, 0.4).

## Exemples pratiques

### Exemple 1 : Logo + Texte sur fond

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
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
          "skip_rate": 20,
          "scale": 0.3
        },
        {
          "type": "text",
          "z_index": 3,
          "skip_rate": 15,
          "text_config": {
            "text": "Mon Titre\nAvec sous-titre",
            "font": "Arial",
            "size": 64,
            "color": [0, 0, 255],
            "style": "bold",
            "align": "center",
            "line_height": 1.3
          }
        }
      ]
    }
  ]
}
```

**Résultat :**
1. Le fond est dessiné lentement (skip_rate: 5)
2. Le logo apparaît ensuite rapidement en haut à gauche, réduit à 30%
3. Le texte est "écrit" avec animation de handwriting au centre

### Exemple 2 : Diagramme avec annotations

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 3,
      "layers": [
        {
          "image_path": "diagram.png",
          "position": {"x": 100, "y": 100},
          "z_index": 1,
          "skip_rate": 10
        },
        {
          "image_path": "arrow1.png",
          "position": {"x": 300, "y": 200},
          "z_index": 2,
          "skip_rate": 30
        },
        {
          "image_path": "arrow2.png",
          "position": {"x": 400, "y": 300},
          "z_index": 2,
          "skip_rate": 30
        },
        {
          "image_path": "label1.png",
          "position": {"x": 350, "y": 180},
          "z_index": 3,
          "skip_rate": 40
        }
      ]
    }
  ]
}
```

**Résultat :**
1. Le diagramme principal est dessiné
2. Deux flèches apparaissent rapidement
3. Une étiquette apparaît très rapidement par-dessus

### Exemple 3 : Modes avancés avec animations (NOUVEAU)
### Exemple 3 : Contrôles de caméra et animations (NOUVEAU)

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "duration": 10,
      "layers": [
        {
          "image_path": "scene.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "image_path": "error.png",
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
          "skip_rate": 12,
          "mode": "draw",
          "morph": {
            "enabled": true,
            "duration": 0.5
          "camera": {
            "zoom": 1.5,
            "position": {"x": 0.5, "y": 0.4}
          },
          "animation": {
            "type": "zoom_in",
            "duration": 2.0,
            "start_zoom": 1.5,
            "end_zoom": 2.5,
            "focus_position": {"x": 0.6, "y": 0.4}
          }
        }
      ]
    }
  ]
}
```

**Résultat :**
1. La scène est dessinée avec un zoom de caméra de 1.5x
2. La caméra se concentre sur la partie supérieure-centrale (0.5, 0.4)
3. Après le dessin, un zoom-in progressif de 1.5x à 2.5x est appliqué
4. Le focus se déplace légèrement vers (0.6, 0.4) pendant le zoom

**Cas d'usage :**
- Présentation de produits avec zoom sur les détails
- Tutoriels avec focus sur des zones spécifiques
- Effets cinématiques et dramatiques

### Exemple 4 : Révélation cinématique avec zoom-out

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "full_scene.png",
          "z_index": 1,
          "skip_rate": 10,
          "camera": {
            "zoom": 2.5,
            "position": {"x": 0.5, "y": 0.5}
          },
          "animation": {
            "type": "zoom_out",
            "duration": 2.5,
            "start_zoom": 2.5,
            "end_zoom": 1.0,
            "focus_position": {"x": 0.5, "y": 0.5}
          }
        }
      ]
    }
  ]
}
```

**Résultat :**
1. La scène de fond est dessinée normalement avec la main
2. Un élément "error" est effacé avec l'animation d'une gomme et apparaît en fondu
3. Un logo apparaît statiquement (sans main) avec un effet zoom-in, puis disparaît en fondu
4. Du texte apparaît avec un morphing fluide depuis la couche précédente

**Détails des nouveautés :**
- **Mode `eraser`** : Utilise l'image d'une gomme au lieu de la main pour créer un effet d'effacement
- **Mode `static`** : Affiche l'image directement sans animation de dessin (idéal pour logos, watermarks)
- **Entrance/Exit animations** : Ajoutent des effets d'apparition et de disparition
- **Morph** : Crée une transition fluide en morphing entre deux couches

### Exemple 4 : Slides multiples avec et sans couches
1. La scène commence très zoomée (2.5x)
2. Le dessin est animé avec ce zoom important
3. Après le dessin, un zoom-out révèle progressivement la scène complète
4. Effet de "grande révélation" dramatique

### Exemple 5 : Slides multiples avec et sans couches

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 4,
      "layers": [
        {
          "image_path": "intro_bg.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8
        },
        {
          "image_path": "intro_logo.png",
          "position": {"x": 250, "y": 200},
          "z_index": 2,
          "skip_rate": 20,
          "scale": 0.5
        }
      ]
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
      "duration": 0.8
    }
  ]
}
```

**Utilisation :**
```bash
python whiteboard_animator.py placeholder.png content.png --config config.json
```

**Résultat :**
- Slide 0 : Composition de 2 couches (intro avec logo)
- Transition fade
- Slide 1 : Image unique (content.png) dessinée normalement

## Commandes d'utilisation

### Avec une seule slide contenant des couches

```bash
python whiteboard_animator.py placeholder.png --config layers_config.json
```

**Note :** Vous devez fournir au moins une image en ligne de commande pour définir le nombre de slides, mais cette image sera ignorée pour les slides configurées avec des couches.

### Avec plusieurs slides

```bash
python whiteboard_animator.py slide1.png slide2.png slide3.png --config config.json
```

Les slides avec configuration de couches utiliseront les couches définies, les autres utiliseront l'image fournie en ligne de commande.

### Avec transitions et paramètres additionnels

```bash
python whiteboard_animator.py img1.png img2.png \
  --config layers_config.json \
  --transition fade \
  --frame-rate 30 \
  --export-json
```

## Conseils et astuces

### 1. Organisation des fichiers
Organisez vos images de couches dans un dossier dédié :
```
projet/
├── layers/
│   ├── background.png
│   ├── element1.png
│   └── element2.png
├── config.json
└── placeholder.png
```

### 2. Vitesses de dessin
- **Fond (z_index: 1)** : skip_rate 5-10 (lent, donne du poids)
- **Éléments principaux (z_index: 2)** : skip_rate 10-20 (normal)
- **Détails/annotations (z_index: 3+)** : skip_rate 20-40 (rapide)

### 3. Transparence
Utilisez l'opacité pour créer des effets de superposition subtils :
- Logo d'arrière-plan : opacity 0.3-0.5
- Éléments normaux : opacity 0.8-1.0

### 4. Échelle
Utilisez scale pour éviter de redimensionner les images manuellement :
- Logos : 0.2-0.4
- Icônes : 0.3-0.6
- Images complètes : 0.8-1.0

### 5. Résolution cible
Les positions sont en pixels par rapport à la résolution cible calculée. Utilisez `--get-split-lens` pour connaître la résolution :
```bash
python whiteboard_animator.py image.png --get-split-lens
```

### 6. Contrôles de caméra (NOUVEAU)
**Niveaux de zoom recommandés :**
- Vue d'ensemble : zoom 1.0-1.2
- Focus modéré : zoom 1.3-1.8
- Gros plan : zoom 2.0-3.0

**Position de focus :**
- Centre : `{"x": 0.5, "y": 0.5}`
- Haut à gauche : `{"x": 0.25, "y": 0.25}`
- Bas à droite : `{"x": 0.75, "y": 0.75}`

### 7. Animations post-dessin (NOUVEAU)
**Durées recommandées :**
- Effet subtil : 1.0-1.5 secondes
- Effet normal : 1.5-2.5 secondes
- Effet dramatique : 2.5-4.0 secondes

**Zoom-in :** Utilisez pour attirer l'attention sur un détail après le dessin
**Zoom-out :** Utilisez pour révéler le contexte complet après un gros plan

### 8. Combinaison caméra + animation
Pour un effet cinématique maximal :
1. Commencez avec un `camera.zoom` initial
2. Ajoutez une `animation` pour un effet progressif
3. Assurez-vous que `start_zoom` de l'animation correspond au `camera.zoom`

## Dépannage

### Les couches ne s'affichent pas
- Vérifiez que les chemins d'images sont corrects
- Assurez-vous que les positions ne placent pas les couches hors du canvas
- Vérifiez que l'opacité n'est pas à 0

### Les couches sont dans le mauvais ordre
- Vérifiez les valeurs de z_index
- Souvenez-vous : plus petit z_index = dessiné en premier (derrière)

### Les images sont trop grandes/petites
- Utilisez la propriété `scale` pour ajuster
- Vérifiez la résolution cible de votre vidéo

### Performance lente
- Augmentez les valeurs de skip_rate
- Réduisez la résolution des images de couches
- Utilisez --split-len plus grand (ex: 30 au lieu de 15)

### Zoom de caméra pixelisé
- Utilisez des images source en haute résolution
- Réduisez le niveau de zoom (restez sous 2.5x si possible)
- Évitez de zoomer sur des images basse résolution

### Animation de zoom saccadée
- Augmentez le frame rate (ex: --frame-rate 30 ou 60)
- Réduisez la différence entre start_zoom et end_zoom
- Augmentez la durée de l'animation

### Focus de caméra incorrect
- Vérifiez que les coordonnées sont entre 0.0 et 1.0
- Rappelez-vous : (0.5, 0.5) est le centre exact
- Testez différentes positions par incréments de 0.1

## Limitations

1. **Nombre de couches** : Pas de limite technique, mais gardez-le raisonnable (< 10) pour la performance
2. **Formats d'image** : PNG recommandé pour la transparence
3. **Taille des images** : Proportionnelle à la résolution cible pour de meilleurs résultats
4. **Position** : Les coordonnées négatives ou hors canvas seront tronquées
5. **Mode eraser** : L'image de la gomme doit exister dans `data/images/eraser.png`
6. **Animations** : Les animations d'entrée/sortie augmentent la durée totale de la slide
7. **Morphing** : Ne fonctionne qu'entre couches consécutives d'une même slide

## Fonctionnalités avancées

### Types de couches

**Type `image` (défaut)** :
- Utilise une image existante (PNG, JPG, etc.)
- Nécessite `image_path` pour spécifier le fichier

**Type `text`** :
- Génère dynamiquement du texte
- Nécessite `text_config` avec le texte et les paramètres
- Support multi-ligne avec `\n`
- Supporte différentes polices, tailles, couleurs et styles
- Animation de handwriting automatique

**Exemple de couche texte :**
```json
{
  "type": "text",
  "z_index": 2,
  "skip_rate": 12,
  "text_config": {
    "text": "Bonjour!\nCeci est un texte\nsur plusieurs lignes",
    "font": "DejaVuSans",
    "size": 48,
    "color": "#FF0000",
    "style": "bold",
    "line_height": 1.5,
    "align": "center"
  }
}
```

### Modes de dessin

**Mode `draw` (défaut)** :
- Animation classique avec la main qui dessine
- Recommandé pour le contenu principal
- Fonctionne avec les types `image` et `text`

**Mode `eraser`** :
- Utilise une gomme au lieu de la main
- Idéal pour simuler un effet d'effacement ou de révélation
- L'image de la gomme doit être présente dans `data/images/`

**Mode `static`** :
- Pas d'animation de dessin
- L'image apparaît directement (avec animations d'entrée/sortie si configurées)
- Idéal pour logos, watermarks, ou éléments décoratifs

### Animations d'entrée et de sortie

Les animations peuvent être combinées avec tous les modes :
- **Entrée** : `fade_in`, `slide_in_*`, `zoom_in`
- **Sortie** : `fade_out`, `slide_out_*`, `zoom_out`

**Conseil** : Utilisez des animations courtes (0.5-1.5s) pour un effet professionnel.

### Morphing entre couches

Le morphing crée une transition fluide entre deux couches :
- Active automatiquement entre la couche N-1 et N
- Fonctionne mieux entre images de contenu similaire
- Durée recommandée : 0.3-0.8 secondes
5. **Zoom de caméra** : Le zoom ne peut pas ajouter de détails au-delà de la résolution originale
6. **Animations** : Les effets de zoom peuvent augmenter le temps de rendu et la taille du fichier
7. **Type text** : ✅ Désormais implémenté ! Utilisez `type: "text"` avec `text_config` pour générer du texte dynamique

## Ressources complémentaires

- **Guide complet des contrôles de caméra** : [CAMERA_ANIMATION_GUIDE.md](CAMERA_ANIMATION_GUIDE.md)
- **Format de configuration** : [CONFIG_FORMAT.md](CONFIG_FORMAT.md)
- **Exemples pratiques** : Voir le dossier `examples/` pour des configurations prêtes à l'emploi

## Support et contributions

Pour des questions ou suggestions concernant les couches, ouvrez une issue sur GitHub.
