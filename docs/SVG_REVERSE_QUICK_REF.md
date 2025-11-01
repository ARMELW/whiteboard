# svg_reverse - Carte de Référence Rapide

## 🎯 Résumé en 30 Secondes

```
svg_reverse contrôle OÙ l'animation DÉMARRE
```

| Valeur | Départ | Exemple |
|--------|--------|---------|
| `false` | Début du chemin | Queue de flèche → Pointe |
| `true` | Fin du chemin | Pointe de flèche → Queue |

---

## 💡 Quand l'utiliser ?

### ✅ OUI - Utilisez svg_reverse quand :
- Vous avez des flèches pointant dans différentes directions
- Vous voulez que l'animation suive naturellement la forme visuelle
- Vous créez un diagramme de flux avec retours
- Vous animez des signatures ou écritures

### ❌ NON - N'utilisez PAS svg_reverse pour :
- Retourner/miroir l'image (→ utilisez `flipX`/`flipY`)
- Rotation de l'image (→ utilisez `rotation`)
- Inverser les couleurs (→ modifiez `shape_config`)

---

## 📋 Configuration Minimale

```json
{
  "type": "shape",
  "svg_path": "mon_image.svg",
  "svg_reverse": false
}
```

---

## 🎨 Exemples Visuels

### Flèche Normale (reverse: false)
```
    début                    fin
      ↓                       ↓
    Queue ──────────────→ Pointe
      
    Animation: ═══════════════════→
               (suit la flèche)
```

### Flèche Inversée (reverse: true)
```
    début                    fin
      ↓                       ↓  
    Queue ──────────────→ Pointe
      
    Animation: ←═══════════════════
               (part de la pointe)
```

---

## 🔧 Configuration Complète

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
    "stroke_width": 3
  },
  "z_index": 1,
  "skip_rate": 5,
  "mode": "draw"
}
```

---

## 🚀 Test Rapide

1. **Créez un fichier test.json:**
```json
{
  "output": {"path": "test.mp4", "fps": 30, "format": "16:9"},
  "slides": [{
    "duration": 5,
    "background": "#FFFFFF",
    "layers": [{
      "type": "shape",
      "svg_path": "doodle/arrow.svg",
      "svg_reverse": false,
      "mode": "draw"
    }]
  }]
}
```

2. **Lancez:**
```bash
python whiteboard_animator.py test.json
```

3. **Observez** la direction de l'animation

4. **Changez** `svg_reverse` à `true` et relancez

5. **Comparez** les deux résultats

---

## 📊 Tableau de Décision

| Ma Situation | svg_reverse |
|--------------|-------------|
| Flèche pointant → (droite) | `false` |
| Flèche pointant ← (gauche) | `true` |
| Flèche courbe ↻ (horaire) | `false` |
| Flèche courbe ↺ (antihoraire) | `true` |
| Animation suit le flux visuel | `false` |
| Animation doit partir de la fin | `true` |

---

## ❓ FAQ Express

**Q: Valeur par défaut ?**  
A: `false` (animation commence au début)

**Q: Affecte la forme visuelle ?**  
A: Non, seulement l'animation

**Q: Compatible avec tous les formats ?**  
A: Oui (SVG, PNG, JPG)

**Q: Peut-on changer en cours d'animation ?**  
A: Non, défini au moment de la création

---

## 🔗 Documentation Complète

- 📖 [SVG_REVERSE_GUIDE.md](SVG_REVERSE_GUIDE.md) - Guide détaillé (300+ lignes)
- 🎬 [arrow_direction_demo.json](../examples/arrow_direction_demo.json) - Exemple testable

---

## 💬 En Un Mot

> **`svg_reverse` = point de départ de l'animation**

---

**Dernière mise à jour:** 1er Novembre 2025
