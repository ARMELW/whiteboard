# Guide: Paramètre svg_reverse

## 📋 Vue d'Ensemble

Le paramètre `svg_reverse` contrôle le **point de départ de l'animation** pour les formes extraites de fichiers SVG. C'est un outil essentiel pour adapter l'animation à la direction visuelle de vos formes, particulièrement pour les flèches.

---

## 🎯 Fonctionnement

### Comportement de Base

```
svg_reverse: false (défaut)
└─→ L'animation démarre au DÉBUT du chemin SVG

svg_reverse: true
└─→ L'animation démarre à la FIN du chemin SVG
```

### Exemple Visuel

Imaginez une flèche courbe pointant vers la droite :

```
Queue ──────────────────→ Pointe
 (début)                   (fin)

svg_reverse: false
Animation: Queue → Pointe ✓ Naturel!

svg_reverse: true  
Animation: Pointe → Queue
```

---

## 💡 Cas d'Usage Principaux

### 1. Flèches Directionnelles

**Problème:** Vous avez des flèches pointant dans différentes directions sur le même slide.

**Solution:** Utilisez `svg_reverse` pour adapter l'animation à chaque flèche.

```json
{
  "layers": [
    {
      "_comment": "Flèche pointant vers la droite",
      "type": "shape",
      "svg_path": "arrow.svg",
      "svg_reverse": false,
      "position": {"x": 100, "y": 300}
    },
    {
      "_comment": "Flèche pointant vers la gauche", 
      "type": "shape",
      "svg_path": "arrow.svg",
      "svg_reverse": true,
      "position": {"x": 100, "y": 500}
    }
  ]
}
```

### 2. Formes Courbes

Pour une forme courbe, `svg_reverse` permet de suivre naturellement le flux visuel :

```json
{
  "_comment": "Courbe S - commence par le haut ou par le bas selon vos besoins",
  "type": "shape",
  "svg_path": "s_curve.svg",
  "svg_reverse": true
}
```

### 3. Signatures et Écriture

Contrôlez si la signature s'écrit du début à la fin ou vice versa :

```json
{
  "_comment": "Signature écrite à l'envers pour un effet spécial",
  "type": "shape",
  "svg_path": "signature.svg",
  "svg_reverse": true
}
```

---

## 🔧 Configuration Complète

### Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `svg_reverse` | boolean | `false` | Contrôle le point de départ de l'animation |

### Exemple Complet

```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_sampling_rate": 10,
  "svg_num_points": 80,
  "svg_reverse": false,
  "position": {"x": 200, "y": 300},
  "shape_config": {
    "color": "#3498DB",
    "fill_color": "#AED6F1",
    "stroke_width": 3
  },
  "z_index": 1,
  "skip_rate": 5,
  "mode": "draw"
}
```

---

## 🎨 Exemples Pratiques

### Exemple 1: Workflow avec Flèches

Créez un diagramme de workflow où les flèches s'animent dans le sens de lecture :

```json
{
  "slides": [{
    "layers": [
      {
        "_comment": "Étape 1 → Étape 2",
        "type": "shape",
        "svg_path": "arrow_right.svg",
        "svg_reverse": false,
        "position": {"x": 300, "y": 400}
      },
      {
        "_comment": "Étape 2 → Étape 1 (retour)",
        "type": "shape", 
        "svg_path": "arrow_left.svg",
        "svg_reverse": true,
        "position": {"x": 300, "y": 600}
      }
    ]
  }]
}
```

### Exemple 2: Animation Circulaire

Pour une flèche circulaire (↻), contrôlez si elle tourne dans le sens horaire ou antihoraire :

```json
{
  "_comment": "Flèche circulaire - sens horaire",
  "type": "shape",
  "svg_path": "circular_arrow.svg",
  "svg_reverse": false
}
```

### Exemple 3: Diagramme avec Retours

```json
{
  "layers": [
    {
      "_comment": "Flux principal (gauche → droite)",
      "svg_reverse": false
    },
    {
      "_comment": "Boucle de retour (droite → gauche)",
      "svg_reverse": true
    }
  ]
}
```

---

## ⚙️ Implémentation Technique

### Comment ça Marche

1. Les points sont extraits du SVG dans leur ordre original
2. Si `svg_reverse: true`, l'ordre des points est inversé
3. L'animation suit les points dans l'ordre (normal ou inversé)

### Code Interne

```python
# path_extractor.py
if reverse:
    all_points = all_points[::-1]  # Inverse l'ordre des points
```

### Ordre d'Exécution

```
1. Extraction des points SVG → [p1, p2, p3, ..., pN]
2. Application de svg_reverse → [pN, ..., p3, p2, p1] (si true)
3. Application de svg_num_points (échantillonnage)
4. Animation suit les points dans l'ordre final
```

---

## 🚨 Points d'Attention

### ⚠️ Ne Pas Confondre Avec

`svg_reverse` n'est **PAS** :
- ❌ Une rotation de l'image (utilisez CSS/transformations pour ça)
- ❌ Un miroir horizontal/vertical (utilisez `flipX`/`flipY`)
- ❌ Une inversion des couleurs

`svg_reverse` **EST** :
- ✅ Un contrôle de la direction d'animation
- ✅ Un changement de point de départ du tracé
- ✅ Une inversion de l'ordre des points du chemin

### 💡 Bonnes Pratiques

1. **Testez d'abord sans reverse** : Voyez l'animation par défaut
2. **Ajoutez reverse si nécessaire** : Si l'animation ne suit pas le flux visuel
3. **Documentez vos choix** : Ajoutez des commentaires dans votre JSON

```json
{
  "_comment": "reverse=true car la flèche pointe vers la gauche",
  "svg_reverse": true
}
```

---

## 🎓 Tutoriel Pas-à-Pas

### Étape 1: Créez votre SVG

Créez une flèche dans votre éditeur SVG préféré (Inkscape, Figma, etc.).

### Étape 2: Testez l'animation par défaut

```json
{
  "type": "shape",
  "svg_path": "my_arrow.svg",
  "svg_reverse": false
}
```

### Étape 3: Observez le résultat

- L'animation suit-elle naturellement la forme visuelle ?
- Si oui → Gardez `svg_reverse: false` ✓
- Si non → Passez à l'étape 4

### Étape 4: Inversez si nécessaire

```json
{
  "type": "shape",
  "svg_path": "my_arrow.svg",
  "svg_reverse": true
}
```

### Étape 5: Affinez avec d'autres paramètres

```json
{
  "type": "shape",
  "svg_path": "my_arrow.svg",
  "svg_reverse": true,
  "svg_sampling_rate": 8,
  "svg_num_points": 60,
  "skip_rate": 5
}
```

---

## 📊 Tableau de Décision

| Situation | svg_reverse | Explication |
|-----------|-------------|-------------|
| Flèche → droite | `false` | Animation suit naturellement |
| Flèche ← gauche | `true` | Animation inversée pour suivre |
| Courbe ↺ horaire | `false` | Commence au début de la courbe |
| Courbe ↻ antihoraire | `true` | Commence à la fin |
| Signature normale | `false` | Écrit du début à la fin |
| Signature "rewind" | `true` | Effet spécial d'écriture inversée |

---

## 🔗 Ressources Complémentaires

- [SHAPE_SVG_INTEGRATION_GUIDE.md](../SHAPE_SVG_INTEGRATION_GUIDE.md) - Guide complet des shapes SVG
- [SHAPE_FROM_SVG_GUIDE.md](../SHAPE_FROM_SVG_GUIDE.md) - Extraction de formes depuis SVG
- [PATH_FOLLOW_GUIDE.md](../PATH_FOLLOW_GUIDE.md) - Mode d'animation path_follow
- [examples/arrow_direction_demo.json](../examples/arrow_direction_demo.json) - Exemple pratique

---

## ❓ FAQ

### Q: Puis-je utiliser svg_reverse avec des PNG ?
**R:** Oui ! Le paramètre fonctionne aussi pour les PNG/JPG. Il inverse l'ordre des points extraits du contour.

### Q: Est-ce que svg_reverse affecte la couleur ou le style ?
**R:** Non, `svg_reverse` affecte uniquement l'ordre des points d'animation. Les couleurs et styles sont définis dans `shape_config`.

### Q: Puis-je animer deux fois la même flèche avec reverse différent ?
**R:** Oui ! Créez deux layers avec le même SVG mais `svg_reverse` différent.

### Q: Comment savoir quel sens est "naturel" pour mon SVG ?
**R:** Testez avec `svg_reverse: false` d'abord. Si l'animation ne suit pas le flux visuel de votre forme, passez à `true`.

---

## 🎬 Exemple de Démonstration

Un exemple complet est disponible dans `examples/arrow_direction_demo.json`. Ce fichier montre :

1. Explication du concept svg_reverse
2. Animation avec svg_reverse: false
3. Animation avec svg_reverse: true
4. Cas d'usage pratique avec plusieurs flèches

Pour le tester :

```bash
python whiteboard_animator.py examples/arrow_direction_demo.json
```

---

## 📝 Notes de Version

| Version | Date | Changements |
|---------|------|-------------|
| 1.0 | 2025-11-01 | Documentation complète de svg_reverse |

---

**Auteur:** Documentation générée suite à clarification utilisateur  
**Dernière mise à jour:** 1er Novembre 2025
