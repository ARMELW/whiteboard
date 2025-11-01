import cv2
import numpy as np
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_svg_path(path_data, sampling_rate=5):
    """
    Parse un path SVG et extrait les points.
    Supporte les commandes M, L, C, Q, A, H, V, Z
    """
    from svg.path import parse_path
    from svg.path.path import Line, CubicBezier, QuadraticBezier, Arc
    
    points = []
    path = parse_path(path_data)
    
    # Pour chaque segment du path
    for segment in path:
        if isinstance(segment, Line):
            # Ligne droite: interpoler
            start = segment.start
            end = segment.end
            num_points = max(2, int(abs(end - start) / sampling_rate))
            for i in range(num_points):
                t = i / (num_points - 1)
                point = segment.point(t)
                points.append({"x": int(point.real), "y": int(point.imag)})
        
        elif isinstance(segment, (CubicBezier, QuadraticBezier)):
            # Courbe de Bézier: échantillonner
            num_points = max(10, int(segment.length() / sampling_rate))
            for i in range(num_points):
                t = i / (num_points - 1)
                point = segment.point(t)
                points.append({"x": int(point.real), "y": int(point.imag)})
        
        elif isinstance(segment, Arc):
            # Arc: échantillonner
            num_points = max(10, int(segment.length() / sampling_rate))
            for i in range(num_points):
                t = i / (num_points - 1)
                point = segment.point(t)
                points.append({"x": int(point.real), "y": int(point.imag)})
    
    return points


def extract_from_svg(svg_path, sampling_rate=5):
    """
    Extrait les points de tous les paths SVG.
    """
    try:
        from svg.path import parse_path
    except ImportError:
        print("❌ La bibliothèque 'svg.path' n'est pas installée.")
        print("   Installe-la avec: pip install svg.path")
        return []
    
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Namespaces SVG
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        '': 'http://www.w3.org/2000/svg'
    }
    
    all_points = []
    
    # Chercher tous les éléments <path>
    for ns in ['svg:path', 'path', './/path', './/{http://www.w3.org/2000/svg}path']:
        try:
            paths = root.findall(ns, namespaces)
            if paths:
                break
        except:
            continue
    
    # Fallback: chercher sans namespace
    if not paths:
        paths = root.findall('.//path')
    
    if not paths:
        # Essayer de chercher sans namespaces
        for elem in root.iter():
            if elem.tag.endswith('path'):
                paths.append(elem)
    
    print(f"  Trouvé {len(paths)} path(s) SVG")
    
    for i, path_elem in enumerate(paths):
        path_data = path_elem.get('d')
        if path_data:
            print(f"  Extraction du path {i+1}...")
            points = parse_svg_path(path_data, sampling_rate)
            all_points.extend(points)
    
    return all_points


def extract_from_png(image_path, sampling_rate=5, reverse=False):
    """
    Extrait les points d'une image PNG/JPG via détection de contours.
    """
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        raise ValueError(f"Impossible de charger l'image: {image_path}")
    
    # Convertir en niveaux de gris
    if len(img.shape) == 3:
        if img.shape[2] == 4:  # RGBA
            gray = 255 - img[:, :, 3]
        else:  # RGB
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Binariser
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Trouver les contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) == 0:
        raise ValueError("Aucun contour trouvé dans l'image")
    
    # Prendre le plus grand contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Extraire tous les points
    all_points = []
    for point in largest_contour:
        x, y = point[0]
        all_points.append({"x": int(x), "y": int(y)})
    
    # Échantillonner
    sampled_points = all_points[::sampling_rate]
    
    if reverse:
        sampled_points = sampled_points[::-1]
    
    return sampled_points


def extract_path_points(file_path, sampling_rate=5, reverse=False):
    """
    Extrait les points d'un fichier (PNG, JPG, ou SVG).
    
    Args:
        file_path: Chemin vers le fichier
        sampling_rate: Échantillonnage (distance entre points)
        reverse: Inverser l'ordre des points
    
    Returns:
        Liste de points [{"x": ..., "y": ...}, ...]
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    
    print(f"📸 Analyse de: {file_path}")
    print(f"  Format détecté: {ext}")
    
    if ext == '.svg':
        points = extract_from_svg(file_path, sampling_rate)
    elif ext in ['.png', '.jpg', '.jpeg']:
        points = extract_from_png(file_path, sampling_rate, reverse)
    else:
        raise ValueError(f"Format non supporté: {ext} (supportés: .svg, .png, .jpg)")
    
    if not points:
        raise ValueError("Aucun point extrait")
    
    print(f"\n✅ {len(points)} points extraits")
    print(f"  Premier point: x={points[0]['x']}, y={points[0]['y']}")
    print(f"  Dernier point: x={points[-1]['x']}, y={points[-1]['y']}")
    
    return points


def analyze_endpoints(file_path):
    """
    Analyse et affiche les extrémités du dessin.
    """
    points = extract_path_points(file_path, sampling_rate=1)
    
    if len(points) < 2:
        return
    
    print(f"\n📍 Extrémités du chemin:")
    print(f"  Début: x={points[0]['x']}, y={points[0]['y']}")
    print(f"  Fin: x={points[-1]['x']}, y={points[-1]['y']}")
    
    # Trouver les points aux coins
    xs = [p['x'] for p in points]
    ys = [p['y'] for p in points]
    
    print(f"\n📐 Limites du dessin:")
    print(f"  En haut à gauche: x={min(xs)}, y={min(ys)}")
    print(f"  En bas à droite: x={max(xs)}, y={max(ys)}")


def save_path_config(points, output_file="path_config.json", comment=""):
    """
    Sauvegarde les points au format JSON.
    """
    output = {
        "_comment": comment or "Path config généré automatiquement",
        "path_config": points
    }
    
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Sauvegardé dans: {output_file}")


# EXEMPLE D'UTILISATION
if __name__ == "__main__":
    import sys
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python path_extractor.py <fichier> [sampling_rate] [--reverse]")
        print("\nExemples:")
        print("  python path_extractor.py arrow.svg")
        print("  python path_extractor.py arrow.png 5")
        print("  python path_extractor.py arrow.svg 3 --reverse")
        sys.exit(1)
    
    file_path = sys.argv[1]
    sampling_rate = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    reverse = '--reverse' in sys.argv
    
    # Extraire les points
    try:
        points = extract_path_points(file_path, sampling_rate, reverse)
        
        # Analyser
        analyze_endpoints(file_path)
        
        # Sauvegarder
        output_name = Path(file_path).stem + "_path_config.json"
        save_path_config(points, output_name, 
                        f"Extrait de {file_path} (sampling={sampling_rate})")
        
        # Aperçu
        print(f"\n📋 Aperçu des 10 premiers points:")
        for i, p in enumerate(points[:10]):
            print(f"  {i+1}. x={p['x']}, y={p['y']}")
        if len(points) > 10:
            print(f"  ... et {len(points) - 10} points de plus")
        
        print(f"\n✨ Copie le contenu de '{output_name}' dans ton config JSON!")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)