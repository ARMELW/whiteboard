# Guide d'Intégration Frontend - Corrections Shape SVG

## 📅 Date: 1er Novembre 2025

## 🎯 Résumé des Corrections

Ce document détaille les corrections apportées aux couches de type `shape` avec extraction SVG automatique, incluant le support de `svg_reverse` et `position`.

---

## 🐛 Problèmes Résolus

### 1. ❌ Problème: `svg_reverse` ne fonctionnait pas pour les fichiers SVG
**Avant:** Le paramètre `svg_reverse` était ignoré pour les fichiers SVG (fonctionnait uniquement pour PNG/JPG)

**Après:** ✅ `svg_reverse` inverse maintenant l'ordre des points extraits pour les fichiers SVG

### 2. ❌ Problème: `position` n'était pas appliqué aux shapes extraits de SVG
**Avant:** Le paramètre `position` était ignoré lors de l'extraction SVG

**Après:** ✅ `position` décale maintenant tous les points extraits du SVG

### 3. ❌ Problème: Animation path_follow ne fonctionnait pas (main invisible)
**Avant:** La shape était dessinée mais la main n'apparaissait pas pendant l'animation

**Après:** ✅ La main suit correctement le tracé de la forme pendant l'animation

---

## 🆕 Nouvelles Fonctionnalités

### 1. Support Complet de `svg_reverse` pour SVG

**Description:** Contrôle la direction de l'animation en inversant l'ordre des points du chemin SVG.

**Fonctionnement:**
- `svg_reverse: false` → L'animation démarre au **début** du chemin SVG (ex: queue de la flèche)
- `svg_reverse: true` → L'animation démarre à la **fin** du chemin SVG (ex: pointe de la flèche)

**Cas d'usage:**
- **Flèches directionnelles:** Adapter l'animation selon l'orientation de la flèche (gauche/droite)
- **Signatures:** Contrôler le sens d'écriture (début → fin ou fin → début)
- **Formes courbes:** Créer des animations qui suivent naturellement la forme visuelle

**Configuration JSON:**
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_sampling_rate": 10,
  "svg_reverse": true,
  "mode": "draw",
  "skip_rate": 5
}
```

**Paramètres:**
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `svg_reverse` | boolean | `false` | Contrôle le point de départ de l'animation (false = début du chemin, true = fin du chemin) |

**Exemple d'utilisation:**
```json
{
  "_comment": "Exemple: Deux flèches avec des animations adaptées à leur direction",
  "slides": [{
    "layers": [
      {
        "_comment": "Flèche pointant vers la droite → animation normale (queue à pointe)",
        "type": "shape",
        "svg_path": "doodle/arrow_right.svg",
        "svg_reverse": false,
        "position": {"x": 100, "y": 300},
        "shape_config": {
          "color": "#2E86DE",
          "stroke_width": 3
        },
        "mode": "draw"
      },
      {
        "_comment": "Flèche pointant vers la gauche → animation inversée (commence à la pointe)",
        "type": "shape",
        "svg_path": "doodle/arrow_left.svg",
        "svg_reverse": true,
        "position": {"x": 100, "y": 500},
        "shape_config": {
          "color": "#E84118",
          "stroke_width": 3
        },
        "mode": "draw"
      }
    ]
  }]
}
```

**💡 Astuce:** Pour une flèche courbe, utilisez `svg_reverse` pour faire correspondre le sens de l'animation avec la direction visuelle de la flèche. Cela rend l'animation plus naturelle et intuitive.

---

### 2. Support de `position` pour Shapes SVG

**Description:** Déplace une forme extraite d'un SVG vers une position spécifique sur le canvas.

**Cas d'usage:**
- Positionner plusieurs formes SVG identiques à différents endroits
- Créer des compositions avec des éléments SVG réutilisables
- Animer plusieurs instances d'une même forme

**Configuration JSON:**
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_sampling_rate": 10,
  "position": {"x": 200, "y": 150},
  "mode": "draw",
  "skip_rate": 5
}
```

**Paramètres:**
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `position.x` | number | 0 | Décalage horizontal en pixels |
| `position.y` | number | 0 | Décalage vertical en pixels |

**Exemple d'utilisation:**
```json
{
  "_comment": "Trois flèches identiques à différentes positions",
  "slides": [{
    "layers": [
      {
        "type": "shape",
        "svg_path": "doodle/arrow.svg",
        "position": {"x": 100, "y": 100},
        "shape_config": {"color": "#FF0000"},
        "mode": "draw"
      },
      {
        "type": "shape",
        "svg_path": "doodle/arrow.svg",
        "position": {"x": 100, "y": 300},
        "shape_config": {"color": "#00FF00"},
        "mode": "draw"
      },
      {
        "type": "shape",
        "svg_path": "doodle/arrow.svg",
        "position": {"x": 100, "y": 500},
        "shape_config": {"color": "#0000FF"},
        "mode": "draw"
      }
    ]
  }]
}
```

---

### 3. Animation Path Follow avec Main Visible

**Description:** Les shapes extraites de SVG utilisent désormais automatiquement l'animation `path_follow` qui montre la main suivant le tracé.

**Changement automatique:**
- Avant: mode `draw` → animation tile-par-tile (sans main visible)
- Après: mode `draw` → animation `path_follow` automatique (avec main visible)

**Configuration:**
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_sampling_rate": 5,
  "mode": "draw",
  "skip_rate": 5
}
```

**Console Output attendu:**
```
📄 Auto-extraction depuis SVG: doodle/arrow.svg
🔍 Extraction des points (sampling=5, num_points=None, reverse=False)...
✅ 50 points extraits depuis SVG
🔷 Génération de forme: polygon
🔄 Utilisation automatique de path_follow pour polygon avec 50 points
```

---

## 🔧 Configuration Complète

### Template JSON Complet

```json
{
  "output": {
    "path": "output_video.mp4",
    "fps": 30,
    "format": "16:9",
    "quality": 23
  },
  "slides": [
    {
      "duration": 5,
      "background": "#ffffff",
      "layers": [
        {
          "_comment": "Shape avec toutes les options",
          "type": "shape",
          "svg_path": "doodle/arrow.svg",
          "svg_sampling_rate": 10,
          "svg_num_points": 50,
          "svg_reverse": true,
          "position": {"x": 200, "y": 150},
          "shape_config": {
            "color": "#FF0000",
            "fill_color": "#FFCCCC",
            "stroke_width": 3
          },
          "z_index": 1,
          "skip_rate": 5,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

### Tous les Paramètres Disponibles

| Paramètre | Type | Requis | Défaut | Description |
|-----------|------|--------|--------|-------------|
| `type` | string | ✅ | - | Doit être `"shape"` |
| `svg_path` | string | ✅ | - | Chemin vers le fichier SVG |
| `svg_sampling_rate` | number | ❌ | 10 | Distance entre points extraits (pixels) |
| `svg_num_points` | number | ❌ | null | Limiter le nombre de points extraits |
| `svg_reverse` | boolean | ❌ | false | Inverser l'ordre des points |
| `position.x` | number | ❌ | 0 | Décalage horizontal (pixels) |
| `position.y` | number | ❌ | 0 | Décalage vertical (pixels) |
| `shape_config.color` | string | ❌ | "#000000" | Couleur du contour (hex) |
| `shape_config.fill_color` | string | ❌ | null | Couleur de remplissage (hex) |
| `shape_config.stroke_width` | number | ❌ | 2 | Épaisseur du trait (pixels) |
| `mode` | string | ❌ | "draw" | Mode d'animation |
| `skip_rate` | number | ❌ | 5 | Vitesse d'animation (frames sautées) |
| `z_index` | number | ❌ | 1 | Ordre d'empilement |

---

## 💡 Exemples d'Intégration Frontend

### Exemple 1: Interface de Configuration Simple

```javascript
// Composant React pour configurer une shape SVG
const ShapeSVGConfig = () => {
  const [config, setConfig] = useState({
    svgPath: 'doodle/arrow.svg',
    samplingRate: 10,
    reverse: false,
    position: { x: 0, y: 0 },
    color: '#000000',
    fillColor: '#FFFFFF',
    strokeWidth: 2
  });

  const generateJSON = () => {
    return {
      type: "shape",
      svg_path: config.svgPath,
      svg_sampling_rate: config.samplingRate,
      svg_reverse: config.reverse,
      position: config.position,
      shape_config: {
        color: config.color,
        fill_color: config.fillColor,
        stroke_width: config.strokeWidth
      },
      mode: "draw",
      skip_rate: 5
    };
  };

  return (
    <div className="shape-config">
      <h3>Configuration Shape SVG</h3>
      
      <label>
        Fichier SVG:
        <input 
          type="text" 
          value={config.svgPath}
          onChange={(e) => setConfig({...config, svgPath: e.target.value})}
        />
      </label>

      <label>
        Inverser le sens:
        <input 
          type="checkbox" 
          checked={config.reverse}
          onChange={(e) => setConfig({...config, reverse: e.target.checked})}
        />
      </label>

      <label>
        Position X:
        <input 
          type="number" 
          value={config.position.x}
          onChange={(e) => setConfig({
            ...config, 
            position: {...config.position, x: parseInt(e.target.value)}
          })}
        />
      </label>

      <label>
        Position Y:
        <input 
          type="number" 
          value={config.position.y}
          onChange={(e) => setConfig({
            ...config, 
            position: {...config.position, y: parseInt(e.target.value)}
          })}
        />
      </label>

      <label>
        Couleur:
        <input 
          type="color" 
          value={config.color}
          onChange={(e) => setConfig({...config, color: e.target.value})}
        />
      </label>

      <button onClick={() => console.log(generateJSON())}>
        Générer Config JSON
      </button>
    </div>
  );
};
```

### Exemple 2: Prévisualisation Interactive

```javascript
// Composant pour prévisualiser la configuration
const ShapePreview = ({ config }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    
    const ctx = canvasRef.current.getContext('2d');
    // Dessiner un aperçu de la position et orientation
    ctx.clearRect(0, 0, 800, 600);
    
    // Dessiner un rectangle représentant la position
    ctx.strokeStyle = config.shape_config.color;
    ctx.lineWidth = config.shape_config.stroke_width;
    ctx.strokeRect(
      config.position.x - 50,
      config.position.y - 50,
      100,
      100
    );
    
    // Ajouter un indicateur de direction si reverse
    if (config.svg_reverse) {
      ctx.fillStyle = '#FF0000';
      ctx.beginPath();
      ctx.arc(config.position.x + 30, config.position.y - 30, 10, 0, 2 * Math.PI);
      ctx.fill();
      ctx.fillText('⟲', config.position.x + 25, config.position.y - 25);
    }
  }, [config]);

  return (
    <canvas 
      ref={canvasRef} 
      width={800} 
      height={600}
      style={{border: '1px solid #ccc'}}
    />
  );
};
```

### Exemple 3: Validation et Messages d'Erreur

```javascript
// Fonction de validation de la configuration
const validateShapeConfig = (config) => {
  const errors = [];

  if (!config.svg_path) {
    errors.push("Le chemin SVG est requis");
  }

  if (config.svg_sampling_rate && config.svg_sampling_rate < 1) {
    errors.push("Le taux d'échantillonnage doit être >= 1");
  }

  if (config.position) {
    if (config.position.x < 0 || config.position.x > 1920) {
      errors.push("Position X doit être entre 0 et 1920");
    }
    if (config.position.y < 0 || config.position.y > 1080) {
      errors.push("Position Y doit être entre 0 et 1080");
    }
  }

  if (config.shape_config?.stroke_width && config.shape_config.stroke_width < 1) {
    errors.push("L'épaisseur du trait doit être >= 1");
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

// Composant avec validation
const ShapeConfigWithValidation = () => {
  const [config, setConfig] = useState(defaultConfig);
  const [validation, setValidation] = useState({ valid: true, errors: [] });

  const handleChange = (newConfig) => {
    setConfig(newConfig);
    setValidation(validateShapeConfig(newConfig));
  };

  return (
    <div>
      <ShapeSVGConfig config={config} onChange={handleChange} />
      
      {!validation.valid && (
        <div className="errors">
          <h4>⚠️ Erreurs de configuration:</h4>
          <ul>
            {validation.errors.map((error, i) => (
              <li key={i}>{error}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
```

---

## 🧪 Tests et Vérification

### Test de Base

```bash
# Créer une configuration de test
cat > test_shape_svg.json << 'EOF'
{
  "output": {
    "path": "/tmp/test_shape_svg.mp4",
    "fps": 30,
    "format": "16:9"
  },
  "slides": [{
    "duration": 5,
    "background": "#ffffff",
    "layers": [{
      "type": "shape",
      "svg_path": "doodle/arrow.svg",
      "svg_sampling_rate": 10,
      "svg_reverse": true,
      "position": {"x": 200, "y": 100},
      "shape_config": {
        "color": "#FF0000",
        "fill_color": "#FFCCCC",
        "stroke_width": 3
      },
      "mode": "draw",
      "skip_rate": 5
    }]
  }]
}
EOF

# Exécuter
python whiteboard_animator.py test_shape_svg.json
```

### Vérifications Console

Lors de l'exécution, vous devriez voir:

```
📄 Auto-extraction depuis SVG: doodle/arrow.svg
🔍 Extraction des points (sampling=10, num_points=None, reverse=True)...
📍 Applying position offset: x=200, y=100
✅ 50 points extraits depuis SVG
🔷 Génération de forme: polygon
🔄 Utilisation automatique de path_follow pour polygon avec 50 points
```

### Checklist de Vérification

- [ ] Le SVG est chargé sans erreur
- [ ] Les points sont extraits correctement
- [ ] Le paramètre `svg_reverse` est appliqué (si spécifié)
- [ ] Le décalage de position est appliqué (si spécifié)
- [ ] La shape est convertie en polygon automatiquement
- [ ] L'animation path_follow est activée
- [ ] La main est visible pendant l'animation
- [ ] La couleur du contour est correcte
- [ ] La couleur de remplissage est correcte (si spécifiée)
- [ ] L'épaisseur du trait est correcte

---

## 🔄 Migration depuis Ancienne Version

### Configurations Anciennes (Avant Fix)

```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_sampling_rate": 10,
  "svg_reverse": true,
  "shape_config": {
    "color": "#FF0000"
  }
}
```

**Problèmes:**
- ❌ `svg_reverse` ignoré
- ❌ Pas de support pour `position`
- ❌ Main invisible pendant animation

### Configurations Nouvelles (Après Fix)

```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_sampling_rate": 10,
  "svg_reverse": true,
  "position": {"x": 200, "y": 100},
  "shape_config": {
    "color": "#FF0000"
  }
}
```

**Améliorations:**
- ✅ `svg_reverse` fonctionne
- ✅ Support complet de `position`
- ✅ Main visible pendant animation

### Compatibilité

**Toutes les anciennes configurations continuent de fonctionner!**

Les nouvelles fonctionnalités sont opt-in:
- Si `svg_reverse` n'est pas spécifié → `false` par défaut
- Si `position` n'est pas spécifié → `{x: 0, y: 0}` par défaut

---

## 📝 Notes Techniques

### Fichiers Modifiés

1. **path_extractor.py**
   - `extract_from_svg()`: Ajout du paramètre `reverse`
   - `extract_path_points()`: Passage du paramètre `reverse` aux fonctions SVG

2. **whiteboard_animator.py**
   - Application du décalage de position aux points extraits
   - Stockage du shape_config dans la layer pour path_follow
   - Conservation de la logique de conversion automatique polygon → path_follow

### Flux de Données

```
1. Configuration JSON
   ↓
2. Extraction SVG (path_extractor.py)
   ↓
3. Application de svg_reverse (inversion des points)
   ↓
4. Application de position (décalage des points)
   ↓
5. Création shape_config avec points décalés
   ↓
6. Stockage dans layer['shape_config']
   ↓
7. Rendu de la shape avec points décalés
   ↓
8. Détection automatique polygon + mode draw
   ↓
9. Conversion en path_follow avec path_config
   ↓
10. Animation avec main visible
```

---

## 🎨 Exemples Visuels

### Configuration de Base
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "mode": "draw"
}
```
→ Flèche dessinée de gauche à droite avec main visible

### Avec svg_reverse
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_reverse": true,
  "mode": "draw"
}
```
→ Flèche dessinée de droite à gauche avec main visible

### Avec position
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "position": {"x": 400, "y": 300},
  "mode": "draw"
}
```
→ Flèche dessinée au centre du canvas avec main visible

### Combinaison Complète
```json
{
  "type": "shape",
  "svg_path": "doodle/arrow.svg",
  "svg_reverse": true,
  "position": {"x": 400, "y": 300},
  "shape_config": {
    "color": "#FF0000",
    "fill_color": "#FFCCCC",
    "stroke_width": 5
  },
  "mode": "draw",
  "skip_rate": 3
}
```
→ Flèche rouge inversée au centre, dessinée lentement avec main visible

---

## 📚 Ressources

### Liens Utiles
- [Documentation SVG](https://developer.mozilla.org/en-US/docs/Web/SVG)
- [Guide Shape Layers](./SHAPE_FROM_SVG_GUIDE.md)
- [Guide Path Follow](./PATH_FOLLOW_GUIDE.md)

### Fichiers de Test
- `test_auto_svg_extraction.py` - Tests d'extraction automatique SVG
- `test_shape_path_follow.py` - Tests d'animation path_follow
- `examples/shape_from_svg_example.json` - Exemple complet

### Support
- Pour les bugs: créer une issue sur GitHub
- Pour les questions: voir la documentation complète
- Pour les exemples: consulter le dossier `examples/`

---

## ✅ Checklist d'Intégration Frontend

### Pour le Développeur Frontend

- [ ] Ajouter un champ `svg_reverse` (checkbox) dans le formulaire
- [ ] Ajouter des champs `position.x` et `position.y` (number inputs)
- [ ] Implémenter la validation des valeurs de position
- [ ] Ajouter une prévisualisation de la position sur canvas
- [ ] Ajouter un indicateur visuel pour `svg_reverse`
- [ ] Mettre à jour la documentation utilisateur
- [ ] Créer des exemples interactifs
- [ ] Ajouter des tooltips explicatifs
- [ ] Implémenter l'import/export de configuration
- [ ] Tester avec différents fichiers SVG

### Pour le Designer/Testeur

- [ ] Tester avec des SVG simples (flèches, formes)
- [ ] Tester avec des SVG complexes (dessins détaillés)
- [ ] Vérifier que `svg_reverse` inverse bien le sens
- [ ] Vérifier que `position` décale correctement
- [ ] Vérifier que la main est visible pendant l'animation
- [ ] Vérifier que les couleurs sont respectées
- [ ] Tester différentes valeurs de `svg_sampling_rate`
- [ ] Tester différentes valeurs de `skip_rate`
- [ ] Documenter les cas d'usage recommandés
- [ ] Créer une galerie d'exemples

---

## 🚀 Prochaines Étapes

### Améliorations Possibles

1. **Rotation des shapes**
   - Ajouter un paramètre `rotation` pour faire pivoter la shape
   - Exemple: `"rotation": 45` pour 45 degrés

2. **Échelle des shapes**
   - Ajouter un paramètre `scale` pour redimensionner
   - Exemple: `"scale": 2.0` pour doubler la taille

3. **Animation personnalisée**
   - Permettre de choisir le type d'animation
   - Exemple: `"animation_style": "smooth"` ou `"animation_style": "jittery"`

4. **Preview en temps réel**
   - Implémenter un aperçu dans le frontend
   - Montrer le tracé et le sens de dessin

5. **Bibliothèque de SVG**
   - Créer une galerie de SVG préchargés
   - Permettre l'upload de SVG personnalisés

---

**Date de dernière mise à jour:** 1er Novembre 2025  
**Version:** 1.0  
**Auteur:** Copilot & ARMELW
