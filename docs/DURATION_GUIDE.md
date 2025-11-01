# Guide de Configuration de Durée

Ce guide explique comment contrôler la durée des animations dans Whiteboard-It, particulièrement avec les couches multiples (layers).

## 📊 Comprendre la durée

### Changement important (Octobre 2024)

Le paramètre `duration` a été modifié pour représenter la **durée TOTALE** de la slide, et non plus uniquement le temps d'affichage après l'animation.

### Avant la modification

```json
{
  "slides": [{
    "index": 0,
    "duration": 10,
    "layers": [...]
  }]
}
```

- Animation: ~2 secondes
- Affichage final: **10 secondes** (comme configuré)
- **Total vidéo: 12 secondes** ❌

**Problème:** Avec `duration: 300`, la vidéo continuait pendant 300 secondes après l'animation, créant de très longues vidéos!

### Après la modification

```json
{
  "slides": [{
    "index": 0,
    "duration": 10,
    "layers": [...]
  }]
}
```

- Animation: ~2 secondes
- Affichage final: ~8 secondes (ajusté automatiquement)
- **Total vidéo: 10 secondes** ✅

**Résultat:** La durée totale correspond exactement à ce que vous avez configuré.

## 🎯 Comment ça fonctionne

### 1. Calcul automatique du temps d'animation

Le temps d'animation dépend de plusieurs facteurs:

- **Taille de l'image:** Plus grande image = plus de temps
- **Skip rate:** Plus élevé = plus rapide
  - `skip_rate: 5` → Animation lente et détaillée
  - `skip_rate: 20` → Animation rapide
- **Nombre de couches:** Plus de couches = plus de temps total
- **Contenu de l'image:** Plus de pixels non-blancs = plus de temps

### 2. Ajustement automatique

Le système calcule:

```
Temps d'animation = (fonction de l'image, skip_rate, etc.)
Temps d'affichage final = duration - Temps d'animation
Total = max(duration, Temps d'animation)
```

### 3. Informations affichées

Pendant l'exécution, vous verrez:

```
⏱️ Animation: 1.33s (40 frames)
⏱️ Final hold: 2.67s (80 frames)
⏱️ Total duration: 4.00s
```

Si l'animation dépasse la durée configurée:

```
⏱️ Animation: 5.23s (157 frames)
⏱️ Final hold: 0.00s (0 frames)
⏱️ Total duration: 5.23s
⚠️ Warning: Animation duration (5.23s) exceeds specified duration (5s)
```

## 💡 Exemples pratiques

### Exemple 1: Durée suffisante

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ]
    }
  ]
}
```

**Résultat typique:**
- Animation: 2.5s
- Final hold: 7.5s
- Total: 10s ✅

### Exemple 2: Animation lente, durée courte

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 3,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 3
        }
      ]
    }
  ]
}
```

**Résultat typique:**
- Animation: 4.2s
- Final hold: 0s
- Total: 4.2s
- ⚠️ Avertissement affiché

### Exemple 3: Multiples couches avec durée totale

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 5
        },
        {
          "image_path": "demo/2.jpg",
          "position": {"x": 50, "y": 50},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.5
        },
        {
          "image_path": "demo/3.jpeg",
          "position": {"x": 200, "y": 400},
          "z_index": 3,
          "skip_rate": 20,
          "opacity": 0.95
        }
      ]
    }
  ]
}
```

**Résultat typique:**
- Animation couche 1: 3.0s
- Animation couche 2: 0.5s
- Animation couche 3: 0.3s
- Total animation: 3.8s
- Final hold: 4.2s
- Total: 8.0s ✅

## 🔧 Conseils d'optimisation

### Pour contrôler la durée d'animation

1. **Utiliser skip_rate:**
   - Valeurs basses (3-8): Animation détaillée mais lente
   - Valeurs moyennes (10-15): Bon équilibre
   - Valeurs hautes (20-30): Animation rapide

2. **Ajuster la taille des images:**
   - Images plus petites = animation plus rapide
   - Utiliser le paramètre `scale` pour réduire la taille

3. **Tester et ajuster:**
   ```bash
   # Tester avec une petite durée d'abord
   python whiteboard_animator.py placeholder.png --config test.json
   # Regarder les informations de timing affichées
   # Ajuster duration et skip_rate selon le résultat
   ```

### Pour des durées prévisibles

Si vous voulez que l'animation dure exactement un temps spécifique:

1. **Première tentative:** Configurez une durée généreuse (ex: 20s)
2. **Observez:** Regardez le temps d'animation réel affiché
3. **Ajustez:** Si l'animation prend 5s, configurez `duration: 5` pour aucun hold, ou `duration: 8` pour 3s de hold

### Exemple d'itération

**Première tentative:**
```json
{"duration": 20, "skip_rate": 10}
```
Résultat: Animation 4.2s, hold 15.8s

**Ajustement:**
```json
{"duration": 6, "skip_rate": 10}
```
Résultat: Animation 4.2s, hold 1.8s ✅

Ou pour animation plus rapide:
```json
{"duration": 4, "skip_rate": 20}
```
Résultat: Animation 2.1s, hold 1.9s ✅

## 🎬 Cas d'usage courants

### Vidéo rapide pour les réseaux sociaux

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "layers": [
        {
          "image_path": "mon_image.jpg",
          "skip_rate": 20
        }
      ]
    }
  ]
}
```

### Présentation détaillée

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {
          "image_path": "slide1.jpg",
          "skip_rate": 5
        }
      ]
    }
  ]
}
```

### Animation complexe multi-couches

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "background.jpg",
          "z_index": 1,
          "skip_rate": 10
        },
        {
          "image_path": "overlay1.png",
          "position": {"x": 100, "y": 100},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.5,
          "opacity": 0.9
        },
        {
          "image_path": "overlay2.png",
          "position": {"x": 500, "y": 300},
          "z_index": 3,
          "skip_rate": 20,
          "scale": 0.3,
          "opacity": 0.95
        }
      ]
    }
  ]
}
```

## ⚙️ Configuration avancée

### Per-layer timing control

Chaque couche peut avoir son propre `skip_rate`:

```json
{
  "layers": [
    {
      "image_path": "layer1.jpg",
      "z_index": 1,
      "skip_rate": 5      // Animation lente pour le fond
    },
    {
      "image_path": "layer2.jpg",
      "z_index": 2,
      "skip_rate": 20     // Animation rapide pour l'overlay
    }
  ]
}
```

### Transitions entre slides

Utilisez la section `transitions` pour des effets entre les slides:

```json
{
  "slides": [
    {"index": 0, "duration": 8},
    {"index": 1, "duration": 8}
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

## 📝 Résumé

- **duration** = durée totale de la slide (animation + hold)
- Le système calcule automatiquement le temps d'animation
- Si l'animation dépasse la durée, elle est utilisée (avec avertissement)
- Utilisez `skip_rate` pour contrôler la vitesse d'animation
- Testez et ajustez pour obtenir le résultat souhaité
- Les informations de timing sont affichées pendant l'exécution

## 🆘 Dépannage

### Problème: Vidéo trop longue

**Solution:** Réduisez la valeur de `duration` dans votre configuration.

### Problème: Animation trop rapide

**Solution:** Réduisez `skip_rate` (valeurs plus basses = animation plus lente).

### Problème: Animation trop lente

**Solution:** Augmentez `skip_rate` ou réduisez la taille des images avec `scale`.

### Problème: Je veux aucun temps d'attente après l'animation

**Solution:** Configurez une `duration` légèrement inférieure au temps d'animation. Le système utilisera uniquement l'animation.

### Problème: Je ne sais pas quelle durée mettre

**Solution:** 
1. Configurez une durée généreuse (ex: 30s)
2. Exécutez l'animation
3. Notez le temps d'animation affiché
4. Ajustez la durée selon vos besoins
