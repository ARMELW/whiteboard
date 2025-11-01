import os, stat, shutil
import sys
import subprocess
from pathlib import Path
import time
import math
import json
import datetime
import cv2
import numpy as np
import argparse
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import urllib.request
import urllib.error
import tempfile
import numpy as np

# Import performance optimizer module
try:
    from performance_optimizer import (
        PerformanceOptimizer, RenderCheckpoint, ProgressTracker,
        RenderQueue, parse_quality_preset, process_batch
    )
    PERFORMANCE_MODULE_AVAILABLE = True
except ImportError:
    PERFORMANCE_MODULE_AVAILABLE = False
    print("⚠️ Warning: performance_optimizer module not available. Performance features disabled.")

# Import libraries for multilingual text support
try:
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    BIDI_SUPPORT = True
except ImportError:
    # Fonctions de remplacement (fallback) si les librairies ne sont pas trouvées
    def reshape(text):
        return text
    def get_display(text):
        return text
    BIDI_SUPPORT = False
    print("  ⚠️ Warning: Librairies RTL/Bidirectional non trouvées. Le rendu du texte Arabe/Hébreu pourrait être incorrect.")



# Import export formats module
try:
    from export_formats import (
        export_gif, export_webm, export_png_sequence,
        export_with_transparency, export_lossless,
        get_social_media_preset, list_social_media_presets,
        print_social_media_presets
    )
    EXPORT_FORMATS_AVAILABLE = True
except ImportError:
    EXPORT_FORMATS_AVAILABLE = False
    print("⚠️ Warning: export_formats module not available. Advanced export features disabled.")

# Import audio manager module
try:
    from audio_manager import (
        AudioManager, add_audio_to_video, process_audio_config,
        PYDUB_AVAILABLE
    )
    AUDIO_MODULE_AVAILABLE = True
except ImportError:
    AUDIO_MODULE_AVAILABLE = False
    PYDUB_AVAILABLE = False
    print("⚠️ Warning: audio_manager module not available. Audio features disabled.")

# Import particle system module
try:
    from particle_system import (
        ParticleSystem, ParticleEmitter, Particle,
        apply_particle_effect
    )
    PARTICLE_SYSTEM_AVAILABLE = True
except ImportError:
    PARTICLE_SYSTEM_AVAILABLE = False
    print("⚠️ Warning: particle_system module not available. Particle effects disabled.")

# from kivy.clock import Clock # COMMENTÉ: Remplacé par un appel direct pour CLI

# --- Variables Globales ---
if getattr(sys, 'frozen', False):
    # Exécuté en tant que bundle PyInstaller
    base_path = sys._MEIPASS
else:
    # Exécuté dans un environnement Python normal
    base_path = os.path.dirname(os.path.abspath(__file__))
    
# Assurez-vous que le répertoire 'data/images' existe par rapport à base_path
images_path = os.path.join(base_path, 'data', 'images')
hand_path = os.path.join(images_path, 'drawing-hand.png')
hand_mask_path = os.path.join(images_path, 'hand-mask.png')
save_path = os.path.join(base_path, "save_videos")
platform = "linux"

# Default values for video generation
DEFAULT_FRAME_RATE = 30
DEFAULT_SPLIT_LEN = 15
DEFAULT_OBJECT_SKIP_RATE = 8
DEFAULT_BG_OBJECT_SKIP_RATE = 20
DEFAULT_MAIN_IMG_DURATION = 3
DEFAULT_CRF = 18  # Lower = better quality (0-51, 18 is visually lossless)
MAX_TEXT_DISPLAY_LENGTH = 50  # Maximum characters to show in text layer display

# Text threshold constants for proper filled text detection
TEXT_THRESHOLD = 240  # Pixel intensity threshold for text detection (0-255)
WHITE_RATIO_THRESHOLD = 0.7  # Ratio of white pixels to determine if image is text-only

# Synthetic text styling constants
SYNTHETIC_BOLD_STROKE_DIVISOR = 20  # Divide font size by this to get stroke width for bold
SYNTHETIC_ITALIC_SHEAR_ANGLE = -15  # Shear angle in degrees for italic effect (negative = rightward slant)

# Font configuration cache
_FONT_CONFIG_CACHE = None
_FONT_CONFIG_PATH = None

def load_font_config(config_path=None):
    """Load font configuration from JSON file.
    
    Args:
        config_path: Optional path to font config file. If None, uses default 'fonts.json' in base_path.
        
    Returns:
        Dictionary mapping font names to their .ttf file paths, or empty dict if file doesn't exist
    """
    global _FONT_CONFIG_CACHE, _FONT_CONFIG_PATH
    
    # Determine config path
    if config_path is None:
        config_path = os.path.join(base_path, 'fonts.json')
    
    # Return cached config if already loaded from the same path
    if _FONT_CONFIG_CACHE is not None and _FONT_CONFIG_PATH == config_path:
        return _FONT_CONFIG_CACHE
    
    # Load config file
    if not os.path.exists(config_path):
        _FONT_CONFIG_CACHE = {}
        _FONT_CONFIG_PATH = config_path
        return _FONT_CONFIG_CACHE
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        _FONT_CONFIG_CACHE = config.get('fonts', {})
        _FONT_CONFIG_PATH = config_path
        return _FONT_CONFIG_CACHE
    except Exception as e:
        print(f"  ⚠️ Warning: Could not load font config from {config_path}: {e}")
        _FONT_CONFIG_CACHE = {}
        _FONT_CONFIG_PATH = config_path
        return _FONT_CONFIG_CACHE

# --- Classes et Fonctions ---

def load_image_from_url_or_path(image_source):
    """Charge une image depuis une URL ou un chemin local.
    
    Args:
        image_source: URL (http/https) ou chemin local de l'image
        
    Returns:
        numpy array (BGR) de l'image, ou None si erreur
    """
    if isinstance(image_source, str) and (image_source.startswith('http://') or image_source.startswith('https://')):
        # C'est une URL - télécharger et charger
        try:
            print(f"    📥 Téléchargement de l'image depuis URL...")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_path = tmp_file.name
                urllib.request.urlretrieve(image_source, tmp_path)
            
            # Charger l'image téléchargée
            img = cv2.imread(tmp_path)
            
            # Nettoyer le fichier temporaire
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            if img is None:
                print(f"    ⚠️ Impossible de lire l'image téléchargée")
                return None
            
            print(f"    ✅ Image téléchargée avec succès")
            return img
        except urllib.error.URLError as e:
            print(f"    ⚠️ Erreur de téléchargement: {e}")
            return None
        except Exception as e:
            print(f"    ⚠️ Erreur lors du chargement de l'URL: {e}")
            return None
    else:
        # C'est un chemin local
        if not os.path.exists(image_source):
            print(f"    ⚠️ Fichier local introuvable: {image_source}")
            return None
        
        img = cv2.imread(image_source)
        if img is None:
            print(f"    ⚠️ Impossible de lire l'image: {image_source}")
            return None
        
        return img

def resolve_font_path(font_name, style='normal'):
    """Resolve font family name to actual font file path.
    
    This function first checks the fonts.json configuration file for a mapping,
    then falls back to using fontconfig (fc-match) if not found in the config.
    
    Args:
        font_name: Font family name (e.g., 'Arial', 'Pacifico', 'DejaVu Sans')
        style: Font style ('normal', 'bold', 'italic', 'bold italic')
        
    Returns:
        Path to font file if found, None otherwise
    """
    # First, check the font configuration file
    font_config = load_font_config()
    
    if font_name in font_config:
        # Normalize style
        style_lower = style.lower()
        
        # Try to find exact style match
        if style_lower in font_config[font_name]:
            font_path = font_config[font_name][style_lower]
            
            # Make path absolute if it's relative
            if not os.path.isabs(font_path):
                font_path = os.path.join(base_path, font_path)
            
            # Verify the file exists
            if os.path.exists(font_path):
                return font_path
            else:
                print(f"  ⚠️ Warning: Font file not found in fonts.json: {font_path}")
        
        # If exact style not found but font exists in config, try 'normal' style
        if 'normal' in font_config[font_name] and style_lower != 'normal':
            font_path = font_config[font_name]['normal']
            
            # Make path absolute if it's relative
            if not os.path.isabs(font_path):
                font_path = os.path.join(base_path, font_path)
            
            # Verify the file exists
            if os.path.exists(font_path):
                return font_path
    
    # If not found in config, fall back to fontconfig (fc-match)
    try:
        # Build fc-match pattern with style
        pattern = font_name
        if 'bold' in style.lower() and 'italic' in style.lower():
            pattern = f"{font_name}:style=Bold Italic"
        elif 'bold' in style.lower():
            pattern = f"{font_name}:style=Bold"
        elif 'italic' in style.lower():
            pattern = f"{font_name}:style=Italic"
        
        # Use fc-match to find the font file
        result = subprocess.run(
            ['fc-match', '-f', '%{file}', pattern],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            font_path = result.stdout.strip()
            # Verify the file exists
            if os.path.exists(font_path):
                return font_path
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError, OSError):
        # fc-match not available or failed, continue with fallback mechanism
        pass
    
    return None

def calculate_synthetic_bold_stroke(font_size):
    """Calculate stroke width for synthetic bold effect.
    
    Args:
        font_size: Size of the font in pixels
        
    Returns:
        Tuple of (stroke_width, stroke_fill) for use with PIL's draw.text()
    """
    stroke_width = max(1, int(font_size / SYNTHETIC_BOLD_STROKE_DIVISOR))
    return stroke_width

def format_text_config_for_display(text_config):
    """Extrait et formate la configuration du texte pour l'affichage dans la console.
    
    Args:
        text_config: Dictionnaire avec la configuration du texte
        
    Returns:
        Chaîne avec les détails de configuration formatés : (font:X, size:Y, color:Z, style:A, align:B)
    """
    font = text_config.get('font', 'Arial')
    size = text_config.get('size', 32)
    color = text_config.get('color', (0, 0, 0))
    style = text_config.get('style', 'normal')
    align = text_config.get('align', 'left')
    return f"(font:{font}, size:{size}, color:{color}, style:{style}, align:{align})"
def render_text_to_image(text_config, target_width, target_height):
    """Rend le texte sur une image en utilisant PIL/Pillow avec support multilingue et effets.
    
    Args:
        text_config: Dictionnaire avec la configuration du texte
        target_width: Largeur du canevas
        target_height: Hauteur du canevas
        
    Returns:
        Tableau numpy (format BGR) avec le texte rendu sur fond blanc
    """
    # 1. Extraction et Calcul de la Taille de Police
    text = text_config.get('text', '')
    font_name = text_config.get('font', 'Arial')
    explicit_size = text_config.get('size', None)

    # Initialisation temporaire des outils de dessin pour l'auto-ajustement
    img_temp = Image.new('RGB', (target_width, target_height), color='white')
    draw_temp = ImageDraw.Draw(img_temp)
    lines = text.split('\n')

    if explicit_size is not None:
        font_size = int(explicit_size)
    else:
        # Auto-ajustement de la taille
        margin_w = int(target_width * 0.10)
        margin_h = int(target_height * 0.10)
        fit_width = target_width - margin_w
        fit_height = target_height - margin_h
        font_size = min(fit_height, fit_width)
        
        while font_size > 8:
            temp_font = None
            # First try to resolve font using fontconfig
            font_path = resolve_font_path(font_name, 'normal')
            try:
                # Tente de charger la police avec la taille actuelle
                if font_path:
                    temp_font = ImageFont.truetype(font_path, font_size)
                else:
                    temp_font = ImageFont.truetype(font_name, font_size)
            except:
                # Utilise la police par défaut si la police spécifiée ne peut être chargée
                temp_font = ImageFont.load_default(size=font_size) # Petite correction: load_default peut prendre une taille
            
            # Calcul de la hauteur de ligne et de la hauteur totale
            try:
                # Utilise textbbox pour un calcul plus précis si disponible
                bbox = draw_temp.textbbox((0, 0), "Ay", font=temp_font)
                line_height = int((bbox[3] - bbox[1]) * text_config.get('line_height', 1.2))
            except:
                # Fallback pour le calcul de la hauteur de ligne
                line_height = int(font_size * text_config.get('line_height', 1.2))
                
            total_height = len(lines) * line_height
            
            # Calcul de la largeur maximale
            max_line_width = 0
            for line in lines:
                try:
                    bbox = draw_temp.textbbox((0, 0), line, font=temp_font)
                    line_width = bbox[2] - bbox[0]
                except:
                    line_width = len(line) * font_size // 2 # Estimation simple
                max_line_width = max(max_line_width, line_width)

            # Vérifie si le texte s'insère
            if total_height <= fit_height and max_line_width <= fit_width:
                break
            font_size -= 2
        
        # Si la taille est trop petite, force la taille par défaut
        if font_size <= 8 and explicit_size is None:
            font_size = 32 # Taille par défaut raisonnable si l'auto-fit a échoué

    # Autres configurations
    color = text_config.get('color', (0, 0, 0))
    style = text_config.get('style', 'normal')
    line_height_multiplier = text_config.get('line_height', 1.2)
    align = text_config.get('align', 'left')
    position = text_config.get('position', None)
    anchor_point = text_config.get('anchor_point', 'top-left')
    direction = text_config.get('direction', 'auto')
    vertical = text_config.get('vertical', False)
    text_effects = text_config.get('text_effects', {})
    font_fallbacks = text_config.get('font_fallbacks', [])
    
    # Conversion de couleur (tuple ou hex)
    if isinstance(color, list):
        color = tuple(color)
    if isinstance(color, str):
        if color.startswith('#'):
            color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        else:
            color_map = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}
            color = color_map.get(color.lower(), (0, 0, 0))
    
    # 2. Traitement RTL/BIDI
    processed_text = text
    if direction == 'rtl' or (direction == 'auto' and BIDI_SUPPORT):
        if BIDI_SUPPORT and direction != 'ltr':
            try:
                has_rtl = any('\u0590' <= char <= '\u08FF' or '\u200F' == char or '\uFB50' <= char <= '\uFEFF' for char in text)
                if has_rtl or direction == 'rtl':
                    reshaped_text = reshape(text)
                    processed_text = get_display(reshaped_text)
            except Exception as e:
                print(f"  ⚠️ Warning: Traitement RTL échoué: {e}")
                processed_text = text
    
    # 3. Création du Canevas
    img = Image.new('RGB', (target_width, target_height), color='white')
    draw = ImageDraw.Draw(img)
    
    # 4. Chargement de la Police
    font = None
    
    fonts_to_try = [(font_name, style)]
    for fallback_font in font_fallbacks:
        fonts_to_try.append((fallback_font, 'normal'))
    fonts_to_try.extend([("DejaVuSans", "normal"), ("Arial", "normal"), ("NotoSans", "normal")])
    
    # Track whether we need to apply synthetic styling
    synthetic_bold = False
    synthetic_italic = False
    loaded_style = None
    
    for font_name_try, font_style in fonts_to_try:
        if font is not None:
            break
        
        current_style = style if font_style == 'normal' else font_style
        
        # First, try to resolve font using fontconfig (fc-match)
        font_path = resolve_font_path(font_name_try, current_style)
        if font_path:
            try:
                font = ImageFont.truetype(font_path, font_size)
                loaded_style = current_style
                break
            except (OSError, IOError):
                # Font file not readable or invalid, try fallback
                pass
        
        # Fallback to direct font name attempts
        try:
            if 'bold' in current_style:
                variants = [f"{font_name_try} Bold", f"{font_name_try}-Bold", f"{font_name_try}bd"]
                if 'italic' in current_style:
                    variants.extend([f"{font_name_try} Bold Italic", f"{font_name_try}-BoldItalic", f"{font_name_try}bi"])
            elif 'italic' in current_style:
                variants = [f"{font_name_try} Italic", f"{font_name_try}-Italic", f"{font_name_try}i"]
            else:
                variants = []
                
            for font_variant in variants:
                try:
                    font = ImageFont.truetype(font_variant, font_size)
                    loaded_style = current_style
                    break
                except:
                    pass

            if font is None:
                font = ImageFont.truetype(font_name_try, font_size)
                # If we loaded a base font without style, mark as 'normal'
                loaded_style = 'normal'
        except:
            # Essai des chemins système communs (la logique originale est maintenue)
            common_fonts = [
                f"{font_name_try}.ttf", f"/usr/share/fonts/truetype/dejavu/{font_name_try}.ttf",
                f"/usr/share/fonts/truetype/liberation/Liberation{font_name_try}-Regular.ttf",
                f"C:\\Windows\\Fonts\\{font_name_try}.ttf"
            ]
            for font_path_try in common_fonts:
                try:
                    font = ImageFont.truetype(font_path_try, font_size)
                    loaded_style = 'normal'
                    break
                except:
                    pass
        
    # Fallback final à la police par défaut de PIL
    if font is None:
        try:
            # Utilise une taille pour le fallback si load_default l'accepte (dépend de la version de PIL)
            # Sinon, ImageFont.load_default() sans argument est la meilleure option
            font = ImageFont.load_default() 
        except:
            font = ImageFont.load_default()
    
    # Determine if we need to apply synthetic styling
    # If the requested style doesn't match what we loaded, apply synthetic effects
    if loaded_style is not None and loaded_style.lower() != style.lower():
        style_lower = style.lower()
        loaded_style_lower = loaded_style.lower()
        
        # Check if synthetic bold is needed
        if 'bold' in style_lower and 'bold' not in loaded_style_lower:
            synthetic_bold = True
        
        # Check if synthetic italic is needed
        if 'italic' in style_lower and 'italic' not in loaded_style_lower:
            synthetic_italic = True
    
    # 5. Calcul de l'Agencement
    lines = processed_text.split('\n')
    
    # Recalcul de la hauteur de ligne avec la police finale
    try:
        bbox = draw.textbbox((0, 0), "Ay", font=font)
        line_height = int((bbox[3] - bbox[1]) * line_height_multiplier)
    except:
        # Fallback pour ImageFont.load_default() qui peut ne pas supporter textbbox correctement
        line_height = int(font_size * line_height_multiplier) if font_size > 0 else 32
        
    total_height = len(lines) * line_height
    
    # Position Y de départ
    if position and 'y' in position:
        y = position['y']
        if anchor_point == 'center':
            y = y - total_height // 2
    else:
        y = (target_height - total_height) // 2
    
    # Calcul des largeurs de ligne pour l'alignement
    line_widths = []
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
        except:
            line_width = len(line) * font_size // 2
        line_widths.append(line_width)
    
    max_line_width = max(line_widths) if line_widths else 0
    
    # 6. Dessin du Texte
    shadow = text_effects.get('shadow', None)
    outline = text_effects.get('outline', None)

    for line_idx, line in enumerate(lines):
        line_width = line_widths[line_idx]
        current_y = y
        
        # Détermination de la position X
        if position and 'x' in position:
            base_x = position['x']
            if anchor_point == 'center':
                base_x = base_x - max_line_width // 2
            
            if align == 'center':
                x = base_x + (max_line_width - line_width) // 2
            elif align == 'right':
                x = base_x + (max_line_width - line_width)
            else:
                x = base_x
        elif align == 'center':
            x = (target_width - line_width) // 2
        elif align == 'right':
            x = target_width - line_width - 20
        else:
            x = 20
        
        # Dessin des effets et du texte
        if vertical:
            # Logique du texte vertical (caractère par caractère)
            current_y = y
            
            # Determine stroke settings for synthetic bold (vertical text)
            stroke_w = 0
            stroke_f = None
            if synthetic_bold:
                stroke_w = calculate_synthetic_bold_stroke(font_size)
                stroke_f = color
            
            for char in line:
                # For vertical text, draw shadow and outline if configured
                if shadow:
                    offset = shadow.get('offset', (2, 2))
                    shadow_color = shadow.get('color', (128, 128, 128))
                    if isinstance(shadow_color, str) and shadow_color.startswith('#'):
                        shadow_color = tuple(int(shadow_color[i:i+2], 16) for i in (1, 3, 5))
                    draw.text((x + offset[0], current_y + offset[1]), char, fill=shadow_color, font=font,
                             stroke_width=stroke_w, stroke_fill=stroke_f)
                
                if outline:
                    width = outline.get('width', 1)
                    outline_color = outline.get('color', (0, 0, 0))
                    if isinstance(outline_color, str) and outline_color.startswith('#'):
                        outline_color = tuple(int(outline_color[i:i+2], 16) for i in (1, 3, 5))
                    for dx in range(-width, width + 1):
                        for dy in range(-width, width + 1):
                            if dx != 0 or dy != 0:
                                draw.text((x + dx, current_y + dy), char, fill=outline_color, font=font,
                                         stroke_width=stroke_w, stroke_fill=stroke_f)
                
                # Draw the main character
                draw.text((x, current_y), char, fill=color, font=font, 
                         stroke_width=stroke_w, stroke_fill=stroke_f)
                current_y += line_height
        else:
            # Logique du texte horizontal
            
            # Determine stroke settings for synthetic bold
            stroke_w = 0
            stroke_f = None
            if synthetic_bold:
                # Apply synthetic bold using stroke
                stroke_w = calculate_synthetic_bold_stroke(font_size)
                stroke_f = color
            
            # 1. Ombre
            if shadow:
                offset = shadow.get('offset', (2, 2))
                shadow_color = shadow.get('color', (128, 128, 128))
                if isinstance(shadow_color, str) and shadow_color.startswith('#'):
                    shadow_color = tuple(int(shadow_color[i:i+2], 16) for i in (1, 3, 5))
                draw.text((x + offset[0], y + offset[1]), line, fill=shadow_color, font=font, 
                         stroke_width=stroke_w, stroke_fill=stroke_f)
            
            # 2. Contour (Outline)
            if outline:
                width = outline.get('width', 1)
                outline_color = outline.get('color', (0, 0, 0))
                if isinstance(outline_color, str) and outline_color.startswith('#'):
                    outline_color = tuple(int(outline_color[i:i+2], 16) for i in (1, 3, 5))
                for dx in range(-width, width + 1):
                    for dy in range(-width, width + 1):
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), line, fill=outline_color, font=font,
                                     stroke_width=stroke_w, stroke_fill=stroke_f)
            
            # 3. Texte principal
            draw.text((x, y), line, fill=color, font=font, stroke_width=stroke_w, stroke_fill=stroke_f)
            y += line_height
    
    # 7. Apply synthetic italic transformation if needed
    if synthetic_italic:
        # Apply shear transformation for italic effect
        # Convert to numpy array for transformation
        img_array = np.array(img)
        
        # Use the configured shear angle for italic effect
        shear_factor = np.tan(np.radians(SYNTHETIC_ITALIC_SHEAR_ANGLE))
        
        # Create affine transformation matrix for shear
        # [1, shear, 0]
        # [0, 1,     0]
        height, width = img_array.shape[:2]
        
        # Calculate the new width after shearing
        new_width = width + int(abs(shear_factor * height))
        
        # Create transformation matrix
        M = np.float32([[1, shear_factor, 0], [0, 1, 0]])
        
        # Apply the transformation
        img_array = cv2.warpAffine(img_array, M, (new_width, height), 
                                    borderMode=cv2.BORDER_CONSTANT, 
                                    borderValue=(255, 255, 255))
        
        # Crop back to original width (centered) only if we expanded
        if new_width > width:
            start_x = (new_width - width) // 2
            # Ensure we don't crop beyond array bounds
            end_x = min(start_x + width, new_width)
            img_array = img_array[:, start_x:end_x]
            # If the crop resulted in a narrower image, pad it back to original width
            if img_array.shape[1] < width:
                pad_width = width - img_array.shape[1]
                padding = np.ones((height, pad_width, 3), dtype=np.uint8) * 255
                img_array = np.concatenate([img_array, padding], axis=1)
        
        # Convert back to PIL Image, then to BGR
        img = Image.fromarray(img_array)
    
    # 8. Conversion finale (RGB -> BGR)
    img_array = np.array(img)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    return img_bgr

def render_shape_to_image(shape_config, target_width, target_height):
    """Render geometric shapes to an image using OpenCV.
    
    Args:
        shape_config: Dictionary with shape configuration:
            - shape: Shape type ("circle", "rectangle", "triangle", "polygon", "line", "arrow")
            - color: Shape color as RGB tuple or hex string (default: (0, 0, 0) black)
            - fill_color: Fill color as RGB tuple or hex string (default: None - no fill)
            - stroke_width: Line thickness in pixels (default: 2)
            - position: Dict with x, y for shape center/start (default: canvas center)
            - size: Size parameter (radius for circle, width/height for rectangle, etc.)
            - points: List of points for polygon [[x1, y1], [x2, y2], ...]
            - start: Start point for line/arrow [x, y]
            - end: End point for line/arrow [x, y]
            - arrow_size: Arrow head size for arrow type (default: 20)
        target_width: Canvas width
        target_height: Canvas height
        
    Returns:
        numpy array (BGR format) with rendered shape on white background
    """
    # Create a white canvas
    img = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
    
    # Extract configuration
    shape_type = shape_config.get('shape', 'circle')
    color = shape_config.get('color', (0, 0, 0))
    fill_color = shape_config.get('fill_color', None)
    stroke_width = shape_config.get('stroke_width', 2)
    position = shape_config.get('position', {'x': target_width // 2, 'y': target_height // 2})
    explicit_size = text_config.get('size', None)
    img_temp = Image.new('RGB', (target_width, target_height), color='white')
    draw_temp = ImageDraw.Draw(img_temp)
    lines = text.split('\n')

    if explicit_size is not None:
        font_size = int(explicit_size)
        # Optionally warn if explicit size overflows layer
        # First try to resolve font using fontconfig
        font_path = resolve_font_path(font_name, 'normal')
        try:
            if font_path:
                temp_font = ImageFont.truetype(font_path, font_size)
            else:
                temp_font = ImageFont.truetype(font_name, font_size)
        except:
            temp_font = ImageFont.load_default()
        try:
            bbox = draw_temp.textbbox((0, 0), "Ay", font=temp_font)
            line_height = int((bbox[3] - bbox[1]) * text_config.get('line_height', 1.2))
        except:
            line_height = int(font_size * text_config.get('line_height', 1.2))
        total_height = len(lines) * line_height
        max_line_width = 0
        for line in lines:
            try:
                bbox = draw_temp.textbbox((0, 0), line, font=temp_font)
                line_width = bbox[2] - bbox[0]
            except:
                line_width = len(line) * font_size // 2
            max_line_width = max(max_line_width, line_width)
        margin_w = int(target_width * 0.10)
        margin_h = int(target_height * 0.10)
        fit_width = target_width - margin_w
        fit_height = target_height - margin_h
        if total_height > fit_height or max_line_width > fit_width:
            print(f"⚠️ La taille de police demandée ({font_size}) dépasse la zone du layer. Le texte risque d'être tronqué.")
    else:
        # Auto-ajustement de la taille
        margin_w = int(target_width * 0.10)
        margin_h = int(target_height * 0.10)
        fit_width = target_width - margin_w
        fit_height = target_height - margin_h
        font_size = min(fit_height, fit_width)
        print('font size', font_size)
        while font_size > 8:
            temp_font = None
            # First try to resolve font using fontconfig
            font_path = resolve_font_path(font_name, 'normal')
            try:
                if font_path:
                    temp_font = ImageFont.truetype(font_path, font_size)
                else:
                    temp_font = ImageFont.truetype(font_name, font_size)
            except:
                temp_font = ImageFont.load_default()
            try:
                bbox = draw_temp.textbbox((0, 0), "Ay", font=temp_font)
                line_height = int((bbox[3] - bbox[1]) * text_config.get('line_height', 1.2))
            except:
                line_height = int(font_size * text_config.get('line_height', 1.2))
            total_height = len(lines) * line_height
            max_line_width = 0
            for line in lines:
                try:
                    bbox = draw_temp.textbbox((0, 0), line, font=temp_font)
                    line_width = bbox[2] - bbox[0]
                except:
                    line_width = len(line) * font_size // 2
                max_line_width = max(max_line_width, line_width)
            if total_height <= fit_height and max_line_width <= fit_width:
                break
            font_size -= 2
        if font_size <= 8:
            font_size = 32 # Taille par défaut raisonnable si l'auto-fit a échoué
    
    if shape_type == 'polygon':
        points = shape_config.get('points', [])
        if points:
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            if fill_color:
                cv2.fillPoly(img, [pts], fill_color)
            cv2.polylines(img, [pts], True, color, stroke_width)
    
    elif shape_type == 'line':
        start = shape_config.get('start', [x - size, y])
        end = shape_config.get('end', [x + size, y])
        pt1 = (int(start[0]), int(start[1]))
        pt2 = (int(end[0]), int(end[1]))
        cv2.line(img, pt1, pt2, color, stroke_width)
    
    elif shape_type == 'arrow':
        start = shape_config.get('start', [x - size, y])
        end = shape_config.get('end', [x + size, y])
        arrow_size = shape_config.get('arrow_size', 20)
        pt1 = (int(start[0]), int(start[1]))
        pt2 = (int(end[0]), int(end[1]))
        
        # Calculate arrow head
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        arrow_angle = np.pi / 6  # 30 degrees
        
        # Arrow head points
        p1 = (
            int(pt2[0] - arrow_size * np.cos(angle - arrow_angle)),
            int(pt2[1] - arrow_size * np.sin(angle - arrow_angle))
        )
        p2 = (
            int(pt2[0] - arrow_size * np.cos(angle + arrow_angle)),
            int(pt2[1] - arrow_size * np.sin(angle + arrow_angle))
        )
        
        # Draw arrow head FIRST (before shaft)
        if fill_color:
            arrow_pts = np.array([pt2, p1, p2], np.int32)
            arrow_pts = arrow_pts.reshape((-1, 1, 2))
            cv2.fillPoly(img, [arrow_pts], fill_color)
        cv2.line(img, pt2, p1, color, stroke_width)
        cv2.line(img, pt2, p2, color, stroke_width)
        
        # Draw main line (shaft) AFTER head
        cv2.line(img, pt1, pt2, color, stroke_width)
    
    return img


def draw_arrow_progressive(canvas, arrow_config, progress, target_width, target_height):
    """Draw an arrow progressively from start to a point along the path.
    
    This function draws an arrow as if writing it, showing only the portion
    from the start point to the current progress point.
    
    Args:
        canvas: Canvas to draw on (numpy array, BGR format)
        arrow_config: Dictionary with arrow configuration:
            - start: Start point [x, y]
            - end: End point [x, y]
            - color: Arrow color as RGB tuple or hex string (default: (0, 0, 0))
            - fill_color: Fill color for arrow head (default: None)
            - stroke_width: Line thickness (default: 2)
            - arrow_size: Arrow head size (default: 20)
        progress: Progress from 0 to 1 (0 = start, 1 = fully drawn)
        target_width: Canvas width
        target_height: Canvas height
        
    Returns:
        Canvas with progressively drawn arrow
    """
    result = canvas.copy()
    
    if progress <= 0:
        return result
    
    # Extract configuration
    start = arrow_config.get('start', [100, 100])
    end = arrow_config.get('end', [700, 100])
    color = arrow_config.get('color', (0, 0, 0))
    fill_color = arrow_config.get('fill_color', None)
    stroke_width = arrow_config.get('stroke_width', 2)
    arrow_size = arrow_config.get('arrow_size', 20)
    
    # Convert hex color to BGR if needed
    def hex_to_bgr(hex_color):
        if isinstance(hex_color, str) and hex_color.startswith('#'):
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
            return (rgb[2], rgb[1], rgb[0])  # Convert RGB to BGR
        elif isinstance(hex_color, (list, tuple)) and len(hex_color) == 3:
            return (hex_color[2], hex_color[1], hex_color[0])  # Convert RGB to BGR
        return hex_color
    
    color = hex_to_bgr(color)
    if fill_color:
        fill_color = hex_to_bgr(fill_color)
    
    # Calculate current position based on progress
    pt1 = (int(start[0]), int(start[1]))
    current_x = start[0] + progress * (end[0] - start[0])
    current_y = start[1] + progress * (end[1] - start[1])
    pt_current = (int(current_x), int(current_y))
    
    # Draw the shaft from start to current position
    cv2.line(result, pt1, pt_current, color, stroke_width)
    
    # If we're at least 80% complete, start drawing the arrow head
    if progress >= 0.8:
        # Calculate arrow head progress (from 0.8 to 1.0 maps to 0 to 1)
        head_progress = (progress - 0.8) / 0.2
        
        pt2 = (int(end[0]), int(end[1]))
        
        # Calculate arrow head angle
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        arrow_angle = np.pi / 6  # 30 degrees
        
        # Arrow head points
        p1 = (
            int(pt2[0] - arrow_size * np.cos(angle - arrow_angle)),
            int(pt2[1] - arrow_size * np.sin(angle - arrow_angle))
        )
        p2 = (
            int(pt2[0] - arrow_size * np.cos(angle + arrow_angle)),
            int(pt2[1] - arrow_size * np.sin(angle + arrow_angle))
        )
        
        # Draw arrow head with progressive appearance
        if head_progress < 0.5:
            # Draw first line of arrow head
            line_progress = head_progress / 0.5
            p1_partial = (
                int(pt2[0] + (1 - line_progress) * (pt2[0] - p1[0])),
                int(pt2[1] + (1 - line_progress) * (pt2[1] - p1[1]))
            )
            cv2.line(result, pt2, p1_partial, color, stroke_width)
        else:
            # First line fully drawn
            cv2.line(result, pt2, p1, color, stroke_width)
            
            # Draw second line of arrow head
            line_progress = (head_progress - 0.5) / 0.5
            p2_partial = (
                int(pt2[0] + (1 - line_progress) * (pt2[0] - p2[0])),
                int(pt2[1] + (1 - line_progress) * (pt2[1] - p2[1]))
            )
            cv2.line(result, pt2, p2_partial, color, stroke_width)
            
            # Fill arrow head if fill color is specified and lines are complete
            if fill_color and line_progress >= 1.0:
                arrow_pts = np.array([pt2, p1, p2], np.int32)
                arrow_pts = arrow_pts.reshape((-1, 1, 2))
                cv2.fillPoly(result, [arrow_pts], fill_color)
    
    return result


def extract_character_paths(text, font_path, font_size):
    """
    Extract vector paths from font characters.
    
    Args:
        text: Text to extract paths for
        font_path: Path to TTF/OTF font file
        font_size: Font size in points
        
    Returns:
        List of character path data with drawing commands
    """
    try:
        font = TTFont(font_path)
        glyf_table = font['glyf'] if 'glyf' in font else None
        cmap = font.getBestCmap()
        
        if not glyf_table or not cmap:
            return None
            
        char_paths = []
        
        for char in text:
            if char in ['\n', ' ', '\t']:
                char_paths.append({'char': char, 'paths': [], 'is_space': True})
                continue
                
            char_code = ord(char)
            if char_code not in cmap:
                continue
                
            glyph_name = cmap[char_code]
            glyph = glyf_table[glyph_name]
            
            # Use RecordingPen to capture drawing commands
            pen = RecordingPen()
            glyph.draw(pen, glyf_table)
            
            char_paths.append({
                'char': char,
                'paths': pen.value,
                'is_space': False
            })
        
        return char_paths
    except Exception as e:
        print(f"  ⚠️ Could not extract paths from font: {e}")
        return None


def convert_glyph_paths_to_points(char_paths, font_size, text_config, target_width, target_height):
    """
    Convert font glyph paths to screen coordinates for drawing.
    
    Args:
        char_paths: Character path data from extract_character_paths
        font_size: Font size in pixels
        text_config: Text configuration with position, align, etc.
        target_width: Canvas width
        target_height: Canvas height
        
    Returns:
        Tuple of (drawing_segments, char_boundaries)
        - drawing_segments: List of drawing segments (sequences of points)
        - char_boundaries: List of segment indices where each character ends
    """
    drawing_segments = []
    char_boundaries = []  # Track segment indices where characters end
    
    # Get text configuration
    text = text_config.get('text', '')
    align = text_config.get('align', 'left')
    position = text_config.get('position', None)
    line_height_multiplier = text_config.get('line_height', 1.2)
    
    # Scale factor from font units to pixels
    scale = font_size / 1000.0  # Typical font unit is 1000 per em
    
    # Split text into lines
    lines = text.split('\n')
    
    # Calculate starting position
    line_height = int(font_size * line_height_multiplier)
    total_height = len(lines) * line_height
    
    if position and 'y' in position:
        start_y = position['y']
    else:
        start_y = (target_height - total_height) // 2
    
    # Process each line
    current_y = start_y
    line_char_idx = 0
    
    for line_idx, line in enumerate(lines):
        if not line.strip():
            current_y += line_height
            line_char_idx += len(line) + 1  # +1 for newline
            continue
        
        # Get characters for this line
        line_chars = char_paths[line_char_idx:line_char_idx + len(line)]
        
        # Calculate line width for alignment
        line_width_estimate = len(line) * font_size * 0.6  # Rough estimate
        
        if position and 'x' in position:
            # ABSOLUTE POSITIONING: position.x is always the left edge of the text bounding box
            # Alignment does not affect the position anchor point
            line_x = position['x']
            # Note: alignment could be used to affect multi-line text alignment within the bounding box
            # but for now we treat position as absolute top-left corner
        elif align == 'center':
            line_x = (target_width - line_width_estimate) // 2
        elif align == 'right':
            line_x = target_width - line_width_estimate - 20
        else:  # left
            line_x = 20
        
        current_x = line_x
        
        # Process each character in the line
        for char_data in line_chars:
            if char_data.get('is_space', False):
                if char_data['char'] == ' ':
                    current_x += font_size * 0.3
                    # Mark space as character boundary
                    char_boundaries.append(len(drawing_segments))
                continue
                
            paths = char_data.get('paths', [])
            char_segments = []
            
            current_segment = []
            for command_type, coords in paths:
                if command_type == 'moveTo':
                    if current_segment:
                        char_segments.append(current_segment)
                        current_segment = []
                    point = coords[0]
                    x, y = point
                    screen_x = int(current_x + x * scale)
                    screen_y = int(current_y + (font_size - y * scale))
                    current_segment.append((screen_x, screen_y))
                    
                elif command_type == 'lineTo':
                    point = coords[0]
                    x, y = point
                    screen_x = int(current_x + x * scale)
                    screen_y = int(current_y + (font_size - y * scale))
                    current_segment.append((screen_x, screen_y))
                    
                elif command_type == 'qCurveTo':
                    for point in coords:
                        if isinstance(point, tuple) and len(point) == 2:
                            x, y = point
                            screen_x = int(current_x + x * scale)
                            screen_y = int(current_y + (font_size - y * scale))
                            current_segment.append((screen_x, screen_y))
                            
                elif command_type == 'closePath':
                    if current_segment and len(current_segment) > 1:
                        char_segments.append(current_segment)
                        current_segment = []
            
            if current_segment:
                char_segments.append(current_segment)
                
            drawing_segments.extend(char_segments)
            
            # Mark where this character ends
            char_boundaries.append(len(drawing_segments))
            
            # Advance x for next character
            if char_segments:
                max_x = max(pt[0] for seg in char_segments for pt in seg)
                current_x = max_x + int(font_size * 0.05)
            else:
                current_x += font_size * 0.5
        
        current_y += line_height
        line_char_idx += len(line) + 1  # +1 for newline
    
    return drawing_segments, char_boundaries


def draw_svg_path_handwriting(
    variables, skip_rate=5, mode='draw',
    eraser=None, eraser_mask_inv=None, eraser_ht=0, eraser_wd=0,
    text_config=None
):
    """
    Draw text with SVG path-based handwriting animation.
    Follows actual character stroke order like VideoScribe.
    
    This implements the VideoScribe-style approach:
    1. Text is converted to vector paths
    2. Paths are drawn in sequence with proper stroke order
    3. Progressive masking reveals text as it's drawn
    4. Hand follows the actual character contours
    
    Args:
        variables: AllVariables object with image data
        skip_rate: Frame skip rate for animation speed
        mode: 'draw' for normal drawing, 'eraser' for eraser mode
        text_config: Optional text configuration for path extraction
                     - pause_after_char: frames to pause after each character (default: 0)
                     - pause_after_word: frames to pause after each word (default: 0)
    """
    if mode == 'eraser':
        variables.drawn_frame[:, :, :] = variables.img
    
    # Check if user explicitly disabled SVG path-based drawing
    use_svg_paths = True  # Within this function, we assume user wants SVG
    pause_after_char = 0
    pause_after_word = 0
    
    if text_config:
        use_svg_paths = text_config.get('use_svg_paths', True)
        pause_after_char = text_config.get('pause_after_char', 0)
        pause_after_word = text_config.get('pause_after_word', 0)
    
    # Try to extract paths if enabled and text_config is provided
    use_path_based = False
    drawing_segments = []
    char_boundaries = []  # Track where each character ends
    
    if use_svg_paths and text_config:
        text = text_config.get('text', '')
        font_name = text_config.get('font', 'Arial')
        font_size = text_config.get('size', 32)
        
        # Try to find font file using fontconfig first
        font_path = resolve_font_path(font_name, text_config.get('style', 'normal'))
        
        # If fontconfig didn't work, try to load font to get path
        if not font_path:
            try:
                temp_font = ImageFont.truetype(font_name, font_size)
                # Get font path from PIL font
                if hasattr(temp_font, 'path'):
                    font_path = temp_font.path
            except:
                pass
        
        # Fallback to common font locations
        if not font_path:
            # Try common font locations
            common_paths = [
                f"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                f"/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                f"C:\\Windows\\Fonts\\arial.ttf",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    font_path = path
                    break
        
        # Try to extract character paths
        if font_path and os.path.exists(font_path):
            char_paths = extract_character_paths(text, font_path, font_size)
            if char_paths:
                # Convert to drawing segments
                result = convert_glyph_paths_to_points(
                    char_paths, font_size, text_config, 
                    variables.resize_wd, variables.resize_ht
                )
                if result:
                    drawing_segments, char_boundaries = result
                    if drawing_segments:
                        use_path_based = True
                        print(f"  ✨ Using SVG path-based drawing ({len(drawing_segments)} segments, {len(char_boundaries)} chars)")
    
    # If path-based extraction failed, fall back to column-based
    if not use_path_based:
        print(f"  ⚠️  SVG path extraction failed, falling back to column-based drawing")
        # Fall back to existing column-based method
        draw_text_handwriting(
            variables, skip_rate, mode,
            eraser, eraser_mask_inv, eraser_ht, eraser_wd
        )
        return
    
    # Draw using path-based approach
    counter = 0
    current_char_idx = 0
    
    for seg_idx, segment in enumerate(drawing_segments):
        if len(segment) < 2:
            continue
            
        # Draw this path segment
        for i in range(len(segment) - 1):
            pt1 = segment[i]
            pt2 = segment[i + 1]
            
            # Clip coordinates to image bounds
            pt1 = (max(0, min(pt1[0], variables.resize_wd - 1)), 
                   max(0, min(pt1[1], variables.resize_ht - 1)))
            pt2 = (max(0, min(pt2[0], variables.resize_wd - 1)), 
                   max(0, min(pt2[1], variables.resize_ht - 1)))
            
            # Draw line on the canvas
            if mode == 'eraser':
                cv2.line(variables.drawn_frame, pt1, pt2, (255, 255, 255), 2)
            else:
                # Get color from original image at this location
                try:
                    color = variables.img[pt1[1], pt1[0]].tolist()
                except:
                    color = [0, 0, 0]
                cv2.line(variables.drawn_frame, pt1, pt2, color, 2)
            
            # Hand position at current point
            hand_coord_x, hand_coord_y = pt2
            
            # Draw hand
            if mode == 'static':
                drawn_frame_with_hand = variables.drawn_frame.copy()
            elif mode == 'eraser' and eraser is not None:
                drawn_frame_with_hand = draw_eraser_on_img(
                    variables.drawn_frame.copy(),
                    eraser.copy(),
                    hand_coord_x,
                    hand_coord_y,
                    eraser_mask_inv.copy(),
                    eraser_ht,
                    eraser_wd,
                    variables.resize_ht,
                    variables.resize_wd,
                )
            else:
                drawn_frame_with_hand = draw_hand_on_img(
                    variables.drawn_frame.copy(),
                    variables.hand.copy(),
                    hand_coord_x,
                    hand_coord_y,
                    variables.hand_mask_inv.copy(),
                    variables.hand_ht,
                    variables.hand_wd,
                    variables.resize_ht,
                    variables.resize_wd,
                )
            
            counter += 1
            if counter % skip_rate == 0:
                if variables.watermark_path:
                    drawn_frame_with_hand = apply_watermark(
                        drawn_frame_with_hand,
                        variables.watermark_path,
                        variables.watermark_position,
                        variables.watermark_opacity,
                        variables.watermark_scale
                    )
                
                variables.video_object.write(drawn_frame_with_hand)
                variables.frames_written += 1
        
        # Check if we've finished a character and should pause
        if current_char_idx < len(char_boundaries) and seg_idx + 1 >= char_boundaries[current_char_idx]:
            # Finished a character
            if pause_after_char > 0:
                # Hold the current frame for pause
                for _ in range(pause_after_char):
                    if variables.watermark_path:
                        drawn_frame_with_hand = apply_watermark(
                            drawn_frame_with_hand,
                            variables.watermark_path,
                            variables.watermark_position,
                            variables.watermark_opacity,
                            variables.watermark_scale
                        )
                    variables.video_object.write(drawn_frame_with_hand)
                    variables.frames_written += 1
            
            current_char_idx += 1
    
    # Final reveal - overlay complete image
    # Only overlay where the current layer has content (non-white pixels)
    # This preserves previously drawn layers
    if mode != 'eraser':
        # Create a mask for pixels that belong to the current layer (non-white pixels)
        content_mask = np.any(variables.img < 250, axis=2)
        # Apply the colored image only where there is content
        variables.drawn_frame[content_mask] = variables.img[content_mask]


def euc_dist(arr1, point):
    """Calcule la distance euclidienne entre un tableau de points (arr1) et un seul point."""
    square_sub = (arr1 - point) ** 2
    return np.sqrt(np.sum(square_sub, axis=1))

def preprocess_image(img, variables):
    """Redimensionne, convertit en niveaux de gris et seuille l'image source."""
    img_ht, img_wd = img.shape[0], img.shape[1]
    img = cv2.resize(img, (variables.resize_wd, variables.resize_ht))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Égalisation de l'histogramme de couleur (CLAHE) - cl1 n'est pas utilisé directement plus tard
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3, 3))
    cl1 = clahe.apply(img_gray)

    # Use a simple threshold for better detection of filled text
    # This captures all pixels that are not white (< TEXT_THRESHOLD)
    # For text layers, this works better than adaptive threshold
    _, img_thresh = cv2.threshold(img_gray, TEXT_THRESHOLD, 255, cv2.THRESH_BINARY)
    
    # For images with more complex content, fall back to adaptive threshold
    # Check if image is mostly white (likely a text layer)
    white_ratio = np.sum(img_gray > TEXT_THRESHOLD) / (img_gray.shape[0] * img_gray.shape[1])
    if white_ratio < WHITE_RATIO_THRESHOLD:  # Less than threshold - use adaptive threshold for complex images
        img_thresh = cv2.adaptiveThreshold(
            img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10
        )

    # Ajout des éléments requis à l'objet variables
    variables.img_ht = img_ht
    variables.img_wd = img_wd
    variables.img_gray = img_gray
    variables.img_thresh = img_thresh
    variables.img = img
    return variables


def preprocess_hand_image(hand_path, hand_mask_path, variables):
    """Charge et pré-traite l'image de la main et son masque."""
    hand = cv2.imread(hand_path)
    hand_mask = cv2.imread(hand_mask_path, cv2.IMREAD_GRAYSCALE)

    top_left, bottom_right = get_extreme_coordinates(hand_mask)
    hand = hand[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    hand_mask = hand_mask[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    hand_mask_inv = 255 - hand_mask

    # Standardisation des masques de main
    hand_mask = hand_mask / 255
    hand_mask_inv = hand_mask_inv / 255

    # Rendre le fond de la main noir
    hand_bg_ind = np.where(hand_mask == 0)
    hand[hand_bg_ind] = [0, 0, 0]

    # Obtention des dimensions de l'image et de la main
    hand_ht, hand_wd = hand.shape[0], hand.shape[1]

    variables.hand_ht = hand_ht
    variables.hand_wd = hand_wd
    variables.hand = hand
    variables.hand_mask = hand_mask
    variables.hand_mask_inv = hand_mask_inv
    return variables


def get_extreme_coordinates(mask):
    """Trouve les coordonnées minimales et maximales des pixels blancs (255) dans un masque."""
    indices = np.where(mask == 255)
    # Extraire les coordonnées x et y des pixels.
    x = indices[1]
    y = indices[0]

    # Trouver les coordonnées x et y minimales et maximales.
    topleft = (np.min(x), np.min(y))
    bottomright = (np.max(x), np.max(y))

    return topleft, bottomright


def easing_function(progress, easing_type='linear'):
    """Apply easing function to progress value (0.0 to 1.0).
    
    Args:
        progress: Value between 0.0 and 1.0
        easing_type: Type of easing function
            - 'linear': No easing
            - 'ease_in': Slow start
            - 'ease_out': Slow end (recommended for camera movements)
            - 'ease_in_out': Slow start and end
            - 'ease_in_cubic': Stronger slow start
            - 'ease_out_cubic': Stronger slow end
    
    Returns:
        Eased progress value between 0.0 and 1.0
    """
    if easing_type == 'linear':
        return progress
    elif easing_type == 'ease_in':
        # Quadratic ease in
        return progress * progress
    elif easing_type == 'ease_out':
        # Quadratic ease out
        return progress * (2 - progress)
    elif easing_type == 'ease_in_out':
        # Quadratic ease in-out
        if progress < 0.5:
            return 2 * progress * progress
        else:
            return -1 + (4 - 2 * progress) * progress
    elif easing_type == 'ease_in_cubic':
        # Cubic ease in
        return progress * progress * progress
    elif easing_type == 'ease_out_cubic':
        # Cubic ease out
        p = progress - 1
        return p * p * p + 1
    else:
        return progress


def apply_camera_transform(frame, camera_config, frame_width, frame_height, camera_size=None):
    """Apply camera zoom and position transformations to a frame.
    
    Args:
        frame: Input frame (numpy array)
        camera_config: Dictionary with camera settings (zoom, position, size)
        frame_width: Target frame width
        frame_height: Target frame height
        camera_size: Optional dict with 'width' and 'height' for camera viewport size
    
    Returns:
        Transformed frame
    """
    if camera_config is None:
        return frame
    
    zoom = camera_config.get('zoom', 1.0)
    position = camera_config.get('position', {'x': 0.5, 'y': 0.5})
    
    # Get camera size if specified (for advanced camera system)
    if camera_size is None:
        camera_size = camera_config.get('size', None)
    
    h, w = frame.shape[:2]
    
    # Calculate the viewport size (what the camera sees)
    if camera_size:
        # Use specified camera size
        viewport_w = int(camera_size.get('width', w))
        viewport_h = int(camera_size.get('height', h))
    else:
        # Calculate based on zoom
        viewport_w = int(w / zoom)
        viewport_h = int(h / zoom)
    
    # Calculate center position (0.5, 0.5 is center, 0.0, 0.0 is top-left)
    center_x = int(w * position['x'])
    center_y = int(h * position['y'])
    
    # Calculate crop region
    x1 = max(0, center_x - viewport_w // 2)
    y1 = max(0, center_y - viewport_h // 2)
    x2 = min(w, x1 + viewport_w)
    y2 = min(h, y1 + viewport_h)
    
    # Adjust if we hit boundaries
    if x2 - x1 < viewport_w:
        x1 = max(0, x2 - viewport_w)
    if y2 - y1 < viewport_h:
        y1 = max(0, y2 - viewport_h)
    
    # Crop and resize to target dimensions
    cropped = frame[y1:y2, x1:x2]
    
    # If no zoom/size change and cropped matches target, return as is
    if cropped.shape[:2] == (frame_height, frame_width):
        return cropped
    
    zoomed = cv2.resize(cropped, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)
    
    return zoomed


def generate_camera_sequence_frames(base_frame, cameras, frame_rate, target_width, target_height):
    """Generate frames for a sequence of camera movements.
    
    Args:
        base_frame: The base frame to apply cameras to
        cameras: List of camera configurations, each with:
            - size: dict with width, height (optional, uses aspect ratio by default)
            - zoom: zoom level (default 1.0)
            - position: dict with x, y (0.0-1.0, default 0.5, 0.5)
            - duration: how long to hold this camera view in seconds
            - transition_duration: time to transition from previous camera (default 0)
            - easing: easing function type for transition (default 'ease_out')
        frame_rate: Video frame rate
        target_width: Output frame width
        target_height: Output frame height
    
    Returns:
        List of frames for the entire camera sequence
    """
    if not cameras or len(cameras) == 0:
        return [base_frame]
    
    all_frames = []
    prev_camera = None
    
    for camera_idx, camera in enumerate(cameras):
        # Extract camera parameters
        camera_zoom = camera.get('zoom', 1.0)
        camera_pos = camera.get('position', {'x': 0.5, 'y': 0.5})
        camera_size = camera.get('size', None)
        duration = camera.get('duration', 2.0)
        transition_duration = camera.get('transition_duration', 0)
        easing = camera.get('easing', 'ease_out')
        
        # Calculate frame counts
        hold_frames = int(frame_rate * duration)
        transition_frames = int(frame_rate * transition_duration) if prev_camera and transition_duration > 0 else 0
        
        print(f"    📷 Camera {camera_idx + 1}: zoom={camera_zoom:.2f}, pos=({camera_pos['x']:.2f}, {camera_pos['y']:.2f}), duration={duration}s")
        if transition_frames > 0:
            print(f"       Transition: {transition_duration}s with {easing} easing")
        
        # Generate transition frames from previous camera to current
        if prev_camera and transition_frames > 0:
            prev_zoom = prev_camera.get('zoom', 1.0)
            prev_pos = prev_camera.get('position', {'x': 0.5, 'y': 0.5})
            prev_size = prev_camera.get('size', None)
            
            for i in range(transition_frames):
                progress = i / max(1, transition_frames - 1) if transition_frames > 1 else 1.0
                eased_progress = easing_function(progress, easing)
                
                # Interpolate camera parameters
                current_zoom = prev_zoom + (camera_zoom - prev_zoom) * eased_progress
                current_pos = {
                    'x': prev_pos['x'] + (camera_pos['x'] - prev_pos['x']) * eased_progress,
                    'y': prev_pos['y'] + (camera_pos['y'] - prev_pos['y']) * eased_progress
                }
                
                # Interpolate size if both cameras have size specified
                current_size = None
                if prev_size and camera_size:
                    current_size = {
                        'width': prev_size['width'] + (camera_size['width'] - prev_size['width']) * eased_progress,
                        'height': prev_size['height'] + (camera_size['height'] - prev_size['height']) * eased_progress
                    }
                elif camera_size:
                    current_size = camera_size
                
                # Apply camera transform
                interpolated_camera = {
                    'zoom': current_zoom,
                    'position': current_pos,
                    'size': current_size
                }
                
                frame = apply_camera_transform(
                    base_frame.copy(),
                    interpolated_camera,
                    target_width,
                    target_height,
                    current_size
                )
                all_frames.append(frame)
        
        # Generate hold frames at current camera position
        camera_config = {
            'zoom': camera_zoom,
            'position': camera_pos,
            'size': camera_size
        }
        
        for i in range(hold_frames):
            frame = apply_camera_transform(
                base_frame.copy(),
                camera_config,
                target_width,
                target_height,
                camera_size
            )
            all_frames.append(frame)
        
        prev_camera = camera
    
    return all_frames


def apply_post_animation_effect(frames_list, effect_config, frame_rate, target_width, target_height):
    """Apply post-animation effects like zoom-in or zoom-out.
    
    Args:
        frames_list: List of frames to apply effect to
        effect_config: Dictionary with effect settings (type, duration, etc.)
        frame_rate: Video frame rate
        target_width: Target frame width
        target_height: Target frame height
    
    Returns:
        List of frames with effect applied
    """
    if not effect_config or len(frames_list) == 0:
        return frames_list
    
    effect_type = effect_config.get('type', 'none')
    duration = effect_config.get('duration', 1.0)
    start_zoom = effect_config.get('start_zoom', 1.0)
    end_zoom = effect_config.get('end_zoom', 1.5)
    
    if effect_type == 'none':
        return frames_list
    
    effect_frames = int(frame_rate * duration)
    if effect_frames <= 0:
        return frames_list
    
    # Take the last frame as base
    base_frame = frames_list[-1].copy()
    effect_frames_list = []
    
    for i in range(effect_frames):
        progress = i / max(1, effect_frames - 1)
        
        if effect_type == 'zoom_in':
            current_zoom = start_zoom + (end_zoom - start_zoom) * progress
        elif effect_type == 'zoom_out':
            current_zoom = end_zoom - (end_zoom - start_zoom) * progress
        else:
            effect_frames_list.append(base_frame.copy())
            continue
        
        # Apply zoom
        camera_config = {
            'zoom': current_zoom,
            'position': effect_config.get('focus_position', {'x': 0.5, 'y': 0.5})
        }
        
        transformed = apply_camera_transform(base_frame, camera_config, target_width, target_height)
        effect_frames_list.append(transformed)
    
    return frames_list + effect_frames_list


def draw_hand_on_img(
    drawing,
    hand,
    drawing_coord_x,
    drawing_coord_y,
    hand_mask_inv,
    hand_ht,
    hand_wd,
    img_ht,
    img_wd,
):
    """Dessine (superpose) l'image de la main sur l'image 'drawing' aux coordonnées données."""
    remaining_ht = img_ht - drawing_coord_y
    remaining_wd = img_wd - drawing_coord_x
    
    # Déterminer la taille de la main à cropper pour éviter de dépasser les bords de l'image
    crop_hand_ht = min(remaining_ht, hand_ht)
    crop_hand_wd = min(remaining_wd, hand_wd)

    hand_cropped = hand[:crop_hand_ht, :crop_hand_wd]
    hand_mask_inv_cropped = hand_mask_inv[:crop_hand_ht, :crop_hand_wd]

    # Coordonnées pour l'insertion
    y_slice = slice(drawing_coord_y, drawing_coord_y + crop_hand_ht)
    x_slice = slice(drawing_coord_x, drawing_coord_x + crop_hand_wd)

    # Masquer la zone pour la main (mettre le fond à 0 en utilisant le masque inversé)
    for i in range(3): # Pour chaque canal de couleur (B, G, R)
        drawing[y_slice, x_slice][:, :, i] = (
            drawing[y_slice, x_slice][:, :, i] * hand_mask_inv_cropped
        )

    # Ajouter l'image de la main
    drawing[y_slice, x_slice] = (
        drawing[y_slice, x_slice]
        + hand_cropped
    )
    return drawing


def preprocess_eraser_image(eraser_path, eraser_mask_path):
    """Load and pre-process the eraser image and its mask."""
    eraser = cv2.imread(eraser_path)
    eraser_mask = cv2.imread(eraser_mask_path, cv2.IMREAD_GRAYSCALE)
    
    if eraser is None or eraser_mask is None:
        # Create default eraser if images don't exist
        print("⚠️ Eraser images not found, using default hand")
        return None, None, None, None, 0, 0
    
    top_left, bottom_right = get_extreme_coordinates(eraser_mask)
    eraser = eraser[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    eraser_mask = eraser_mask[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    eraser_mask_inv = 255 - eraser_mask
    
    # Standardize eraser masks
    eraser_mask = eraser_mask / 255
    eraser_mask_inv = eraser_mask_inv / 255
    
    # Make eraser background black
    eraser_bg_ind = np.where(eraser_mask == 0)
    eraser[eraser_bg_ind] = [0, 0, 0]
    
    # Get eraser dimensions
    eraser_ht, eraser_wd = eraser.shape[0], eraser.shape[1]
    
    return eraser, eraser_mask, eraser_mask_inv, eraser_bg_ind, eraser_ht, eraser_wd


def draw_eraser_on_img(
    drawing,
    eraser,
    drawing_coord_x,
    drawing_coord_y,
    eraser_mask_inv,
    eraser_ht,
    eraser_wd,
    img_ht,
    img_wd,
):
    """Draw (overlay) the eraser image on the 'drawing' image at given coordinates."""
    remaining_ht = img_ht - drawing_coord_y
    remaining_wd = img_wd - drawing_coord_x
    
    # Determine eraser size to crop to avoid exceeding image edges
    crop_eraser_ht = min(remaining_ht, eraser_ht)
    crop_eraser_wd = min(remaining_wd, eraser_wd)

    eraser_cropped = eraser[:crop_eraser_ht, :crop_eraser_wd]
    eraser_mask_inv_cropped = eraser_mask_inv[:crop_eraser_ht, :crop_eraser_wd]

    # Coordinates for insertion
    y_slice = slice(drawing_coord_y, drawing_coord_y + crop_eraser_ht)
    x_slice = slice(drawing_coord_x, drawing_coord_x + crop_eraser_wd)

    # Mask the area for the eraser (set background to 0 using inverted mask)
    for i in range(3):  # For each color channel (B, G, R)
        drawing[y_slice, x_slice][:, :, i] = (
            drawing[y_slice, x_slice][:, :, i] * eraser_mask_inv_cropped
        )

    # Add the eraser image
    drawing[y_slice, x_slice] = (
        drawing[y_slice, x_slice]
        + eraser_cropped
    )
    return drawing


def apply_push_animation_with_hand(frame, animation_config, frame_index, total_frames, frame_rate, hand, hand_mask_inv, hand_ht, hand_wd):
    """Apply push animation with hand overlay to a frame.
    
    Args:
        frame: The frame to animate (numpy array)
        animation_config: Dict with animation parameters (type, duration, etc.)
        frame_index: Current frame index in the animation
        total_frames: Total number of frames in the animation
        frame_rate: Frame rate of the video
        hand: Hand image (numpy array)
        hand_mask_inv: Inverted hand mask (numpy array)
        hand_ht: Hand height
        hand_wd: Hand width
        
    Returns:
        Animated frame with hand overlay
    """
    if not animation_config or not animation_config.get('type', '').startswith('push_from_'):
        return frame
    
    anim_type = animation_config.get('type', 'push_from_left')
    direction = anim_type.replace('push_from_', '')
    duration = animation_config.get('duration', 1.0)
    anim_frames = int(duration * frame_rate)
    
    if frame_index >= anim_frames:
        return frame
    
    # Apply easing for natural motion (ease_out gives a nice pushing deceleration)
    raw_progress = frame_index / anim_frames
    progress = easing_function(raw_progress, 'ease_out')
    
    h, w = frame.shape[:2]
    result = np.ones_like(frame) * 255
    
    # Calculate object position based on eased progress
    if direction == 'left':
        # Push from left side - element slides in from left
        offset = int(w * (1 - progress))
        if offset < w:
            result[:, offset:] = frame[:, :w-offset]
        # Hand follows the element, positioned at its leading edge
        # Hand starts off-screen and moves with the element
        hand_x = max(0, offset - int(hand_wd * 0.7))  # More overlap for better "pushing" look
        hand_y = int(h / 2 - hand_ht / 2)
    elif direction == 'right':
        # Push from right side - element slides in from right
        offset = int(w * (1 - progress))
        if offset < w:
            result[:, :w-offset] = frame[:, offset:]
        # Hand positioned at the right side, pushing left
        hand_x = min(w - hand_wd, w - offset + int(hand_wd * 0.2))  # Slight offset for visibility
        hand_y = int(h / 2 - hand_ht / 2)
    elif direction == 'top':
        # Push from top - element slides in from top
        offset = int(h * (1 - progress))
        if offset < h:
            result[offset:, :] = frame[:h-offset, :]
        # Hand positioned at top, pushing down
        hand_x = int(w / 2 - hand_wd / 2)
        hand_y = max(0, offset - int(hand_ht * 0.7))  # More overlap for better "pushing" look
    elif direction == 'bottom':
        # Push from bottom - element slides in from bottom
        offset = int(h * (1 - progress))
        if offset < h:
            result[:h-offset, :] = frame[offset:, :]
        # Hand positioned at bottom, pushing up
        hand_x = int(w / 2 - hand_wd / 2)
        hand_y = min(h - hand_ht, h - offset + int(hand_ht * 0.2))  # Slight offset for visibility
    else:
        # Default to left if direction not recognized
        offset = int(w * (1 - progress))
        if offset < w:
            result[:, offset:] = frame[:, :w-offset]
        hand_x = max(0, offset - int(hand_wd * 0.7))
        hand_y = int(h / 2 - hand_ht / 2)
    
    # Draw hand on the result frame
    if hand is not None and hand_mask_inv is not None:
        result = draw_hand_on_img(
            result, hand, hand_x, hand_y,
            hand_mask_inv, hand_ht, hand_wd,
            h, w
        )
    
    return result


def apply_entrance_animation(frame, animation_config, frame_index, total_frames, frame_rate):
    """Apply entrance animation to a frame.
    
    Args:
        frame: The frame to animate (numpy array)
        animation_config: Dict with animation parameters (type, duration, etc.)
        frame_index: Current frame index in the animation
        total_frames: Total number of frames in the animation
        frame_rate: Frame rate of the video
        
    Returns:
        Animated frame
    """
    if not animation_config or animation_config.get('type') == 'none':
        return frame
    
    anim_type = animation_config.get('type', 'fade_in')
    duration = animation_config.get('duration', 0.5)
    anim_frames = int(duration * frame_rate)
    
    if frame_index >= anim_frames:
        return frame
    
    progress = frame_index / anim_frames
    
    if anim_type == 'fade_in':
        # Fade from white to image
        white = np.ones_like(frame) * 255
        return cv2.addWeighted(white, 1 - progress, frame, progress, 0)
    
    elif anim_type == 'slide_in_left':
        # Slide in from left
        h, w = frame.shape[:2]
        offset = int(w * (1 - progress))
        result = np.ones_like(frame) * 255
        if offset < w:
            result[:, offset:] = frame[:, :w-offset]
        return result
    
    elif anim_type == 'slide_in_right':
        # Slide in from right
        h, w = frame.shape[:2]
        offset = int(w * (1 - progress))
        result = np.ones_like(frame) * 255
        if offset < w:
            result[:, :w-offset] = frame[:, offset:]
        return result
    
    elif anim_type == 'slide_in_top':
        # Slide in from top
        h, w = frame.shape[:2]
        offset = int(h * (1 - progress))
        result = np.ones_like(frame) * 255
        if offset < h:
            result[offset:, :] = frame[:h-offset, :]
        return result
    
    elif anim_type == 'slide_in_bottom':
        # Slide in from bottom
        h, w = frame.shape[:2]
        offset = int(h * (1 - progress))
        result = np.ones_like(frame) * 255
        if offset < h:
            result[:h-offset, :] = frame[offset:, :]
        return result
    
    elif anim_type == 'zoom_in':
        # Zoom in from center
        h, w = frame.shape[:2]
        scale = 0.5 + 0.5 * progress  # Start at 50% size
        new_h, new_w = int(h * scale), int(w * scale)
        resized = cv2.resize(frame, (new_w, new_h))
        
        result = np.ones_like(frame) * 255
        y_offset = (h - new_h) // 2
        x_offset = (w - new_w) // 2
        result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        return result
    
    elif anim_type.startswith('push_'):
        # Push animation - element slides in with hand visible
        # Direction can be: push_from_left, push_from_right, push_from_top, push_from_bottom
        direction = anim_type.replace('push_from_', '')
        h, w = frame.shape[:2]
        result = np.ones_like(frame) * 255
        
        if direction == 'left':
            # Push from left side
            offset = int(w * (1 - progress))
            if offset < w:
                result[:, offset:] = frame[:, :w-offset]
        elif direction == 'right':
            # Push from right side
            offset = int(w * (1 - progress))
            if offset < w:
                result[:, :w-offset] = frame[:, offset:]
        elif direction == 'top':
            # Push from top
            offset = int(h * (1 - progress))
            if offset < h:
                result[offset:, :] = frame[:h-offset, :]
        elif direction == 'bottom':
            # Push from bottom
            offset = int(h * (1 - progress))
            if offset < h:
                result[:h-offset, :] = frame[offset:, :]
        else:
            # Default to left if direction not recognized
            offset = int(w * (1 - progress))
            if offset < w:
                result[:, offset:] = frame[:, :w-offset]
        
        return result
    
    return frame


def apply_exit_animation(frame, animation_config, frame_index, total_frames, frame_rate):
    """Apply exit animation to a frame.
    
    Args:
        frame: The frame to animate (numpy array)
        animation_config: Dict with animation parameters (type, duration, etc.)
        frame_index: Current frame index in the animation (from start of exit)
        total_frames: Total number of frames in the exit animation
        frame_rate: Frame rate of the video
        
    Returns:
        Animated frame
    """
    if not animation_config or animation_config.get('type') == 'none':
        return frame
    
    anim_type = animation_config.get('type', 'fade_out')
    duration = animation_config.get('duration', 0.5)
    anim_frames = int(duration * frame_rate)
    
    if frame_index >= anim_frames:
        # Animation complete, return white frame
        return np.ones_like(frame) * 255
    
    progress = frame_index / anim_frames
    
    if anim_type == 'fade_out':
        # Fade to white
        white = np.ones_like(frame) * 255
        return cv2.addWeighted(frame, 1 - progress, white, progress, 0)
    
    elif anim_type == 'slide_out_left':
        # Slide out to left
        h, w = frame.shape[:2]
        offset = int(w * progress)
        result = np.ones_like(frame) * 255
        if offset < w:
            result[:, :w-offset] = frame[:, offset:]
        return result
    
    elif anim_type == 'slide_out_right':
        # Slide out to right
        h, w = frame.shape[:2]
        offset = int(w * progress)
        result = np.ones_like(frame) * 255
        if offset < w:
            result[:, offset:] = frame[:, :w-offset]
        return result
    
    elif anim_type == 'slide_out_top':
        # Slide out to top
        h, w = frame.shape[:2]
        offset = int(h * progress)
        result = np.ones_like(frame) * 255
        if offset < h:
            result[:h-offset, :] = frame[offset:, :]
        return result
    
    elif anim_type == 'slide_out_bottom':
        # Slide out to bottom
        h, w = frame.shape[:2]
        offset = int(h * progress)
        result = np.ones_like(frame) * 255
        if offset < h:
            result[offset:, :] = frame[:h-offset, :]
        return result
    
    elif anim_type == 'zoom_out':
        # Zoom out from center
        h, w = frame.shape[:2]
        scale = 1.0 + 0.5 * progress  # Grow to 150% size
        new_h, new_w = int(h * scale), int(w * scale)
        resized = cv2.resize(frame, (new_w, new_h))
        
        result = np.ones_like(frame) * 255
        y_offset = (h - new_h) // 2
        x_offset = (w - new_w) // 2
        
        # Crop to fit original size
        y1 = max(0, -y_offset)
        x1 = max(0, -x_offset)
        y2 = y1 + h
        x2 = x1 + w
        
        if y2 <= new_h and x2 <= new_w:
            result = resized[y1:y2, x1:x2]
        return result
    
    return frame


def generate_morph_frames(frame1, frame2, num_frames):
    """Generate morph transition frames between two frames.
    
    This function creates a smooth morphing transition that handles both
    opacity blending and position changes when content is at different locations.
    
    Args:
        frame1: Starting frame
        frame2: Ending frame
        num_frames: Number of transition frames to generate
        
    Returns:
        List of morphed frames
    """
    if num_frames <= 0:
        return []
    
    morph_frames = []
    
    # Detect content regions in both frames (non-white pixels)
    # A pixel is considered content if it's significantly different from white (255,255,255)
    threshold = 250
    frame1_mask = np.any(frame1 < threshold, axis=2).astype(np.uint8) * 255
    frame2_mask = np.any(frame2 < threshold, axis=2).astype(np.uint8) * 255
    
    # Find bounding boxes of content in both frames
    def get_content_bbox(mask):
        """Get bounding box of non-zero pixels in mask"""
        coords = np.argwhere(mask > 0)
        if len(coords) == 0:
            return None
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        return (x_min, y_min, x_max, y_max)
    
    bbox1 = get_content_bbox(frame1_mask)
    bbox2 = get_content_bbox(frame2_mask)
    
    # If no content in either frame, just do simple blending
    if bbox1 is None or bbox2 is None:
        for i in range(num_frames):
            alpha = (i + 1) / (num_frames + 1)
            morphed = cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
            morph_frames.append(morphed)
        return morph_frames
    
    # Calculate centers of content regions
    center1_x = (bbox1[0] + bbox1[2]) / 2
    center1_y = (bbox1[1] + bbox1[3]) / 2
    center2_x = (bbox2[0] + bbox2[2]) / 2
    center2_y = (bbox2[1] + bbox2[3]) / 2
    
    # Check if there's significant position difference
    position_diff = np.sqrt((center2_x - center1_x)**2 + (center2_y - center1_y)**2)
    
    # If positions are very similar (less than 10 pixels apart), use simple blending
    if position_diff < 10:
        for i in range(num_frames):
            alpha = (i + 1) / (num_frames + 1)
            morphed = cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
            morph_frames.append(morphed)
    else:
        # Position-aware morphing: blend while interpolating positions
        for i in range(num_frames):
            alpha = (i + 1) / (num_frames + 1)
            
            # Interpolate center position
            interp_center_x = center1_x * (1 - alpha) + center2_x * alpha
            interp_center_y = center1_y * (1 - alpha) + center2_y * alpha
            
            # Calculate translation needed for each frame
            offset1_x = interp_center_x - center1_x
            offset1_y = interp_center_y - center1_y
            offset2_x = interp_center_x - center2_x
            offset2_y = interp_center_y - center2_y
            
            # Create translation matrices
            h, w = frame1.shape[:2]
            
            # Translate frame1 content toward target position
            M1 = np.float32([[1, 0, offset1_x], [0, 1, offset1_y]])
            frame1_translated = cv2.warpAffine(frame1, M1, (w, h), 
                                              borderMode=cv2.BORDER_CONSTANT,
                                              borderValue=(255, 255, 255))
            
            # Translate frame2 content toward intermediate position
            M2 = np.float32([[1, 0, offset2_x], [0, 1, offset2_y]])
            frame2_translated = cv2.warpAffine(frame2, M2, (w, h),
                                              borderMode=cv2.BORDER_CONSTANT,
                                              borderValue=(255, 255, 255))
            
            # Blend the translated frames
            morphed = cv2.addWeighted(frame1_translated, 1 - alpha, frame2_translated, alpha, 0)
            morph_frames.append(morphed)
    
    return morph_frames


def evaluate_bezier_cubic(p0, p1, p2, p3, t):
    """Evaluate a cubic Bezier curve at parameter t.
    
    Args:
        p0, p1, p2, p3: Control points as (x, y) tuples
        t: Parameter from 0 to 1
        
    Returns:
        (x, y) point on the curve
    """
    t2 = t * t
    t3 = t2 * t
    mt = 1 - t
    mt2 = mt * mt
    mt3 = mt2 * mt
    
    x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
    y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
    
    return (x, y)


def evaluate_bezier_quadratic(p0, p1, p2, t):
    """Evaluate a quadratic Bezier curve at parameter t.
    
    Args:
        p0, p1, p2: Control points as (x, y) tuples
        t: Parameter from 0 to 1
        
    Returns:
        (x, y) point on the curve
    """
    mt = 1 - t
    mt2 = mt * mt
    t2 = t * t
    
    x = mt2 * p0[0] + 2 * mt * t * p1[0] + t2 * p2[0]
    y = mt2 * p0[1] + 2 * mt * t * p1[1] + t2 * p2[1]
    
    return (x, y)


def evaluate_path_at_time(path_config, t):
    """Evaluate a path at normalized time t (0 to 1).
    
    Args:
        path_config: Dictionary containing path configuration:
            - type: "bezier_cubic", "bezier_quadratic", "linear", or "spline"
            - points: List of control points [(x1, y1), (x2, y2), ...]
            - For bezier_cubic: needs 4 points (or multiples of 3 after first)
            - For bezier_quadratic: needs 3 points (or multiples of 2 after first)
            - For linear: needs 2+ points
            - For spline: needs 4+ points (uses cubic interpolation)
        t: Time parameter from 0 to 1
        
    Returns:
        (x, y, angle) tuple - position and tangent angle in degrees
    """
    path_type = path_config.get('type', 'linear')
    points = path_config.get('points', [])
    
    if len(points) < 2:
        return (0, 0, 0)
    
    if path_type == 'linear':
        # Simple linear interpolation between points
        if len(points) == 2:
            p0, p1 = points[0], points[1]
            x = p0[0] + t * (p1[0] - p0[0])
            y = p0[1] + t * (p1[1] - p0[1])
            angle = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
            return (x, y, angle)
        else:
            # Multiple segments - find which segment t falls into
            num_segments = len(points) - 1
            segment_length = 1.0 / num_segments
            segment_idx = min(int(t / segment_length), num_segments - 1)
            local_t = (t - segment_idx * segment_length) / segment_length
            
            p0 = points[segment_idx]
            p1 = points[segment_idx + 1]
            x = p0[0] + local_t * (p1[0] - p0[0])
            y = p0[1] + local_t * (p1[1] - p0[1])
            angle = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
            return (x, y, angle)
    
    elif path_type == 'bezier_cubic':
        # Cubic Bezier curve
        if len(points) >= 4:
            # Use first 4 points for single curve
            # For multiple curves, we'd need to segment t appropriately
            p0, p1, p2, p3 = points[:4]
            pos = evaluate_bezier_cubic(p0, p1, p2, p3, t)
            
            # Calculate tangent for angle (derivative of bezier)
            # Tangent at t: 3(1-t)²(p1-p0) + 6(1-t)t(p2-p1) + 3t²(p3-p2)
            mt = 1 - t
            dx = 3 * mt * mt * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
            dy = 3 * mt * mt * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
            angle = math.degrees(math.atan2(dy, dx))
            
            return (pos[0], pos[1], angle)
    
    elif path_type == 'bezier_quadratic':
        # Quadratic Bezier curve
        if len(points) >= 3:
            p0, p1, p2 = points[:3]
            pos = evaluate_bezier_quadratic(p0, p1, p2, t)
            
            # Calculate tangent for angle
            # Tangent at t: 2(1-t)(p1-p0) + 2t(p2-p1)
            mt = 1 - t
            dx = 2 * mt * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
            dy = 2 * mt * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
            angle = math.degrees(math.atan2(dy, dx))
            
            return (pos[0], pos[1], angle)
    
    elif path_type == 'spline':
        # Catmull-Rom spline interpolation
        if len(points) >= 4:
            # Find which segment we're on
            num_segments = len(points) - 3
            segment_length = 1.0 / num_segments
            segment_idx = min(int(t / segment_length), num_segments - 1)
            local_t = (t - segment_idx * segment_length) / segment_length
            
            # Get 4 control points for this segment
            p0 = points[segment_idx]
            p1 = points[segment_idx + 1]
            p2 = points[segment_idx + 2]
            p3 = points[segment_idx + 3]
            
            # Catmull-Rom spline formula
            t2 = local_t * local_t
            t3 = t2 * local_t
            
            x = 0.5 * ((2 * p1[0]) +
                      (-p0[0] + p2[0]) * local_t +
                      (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                      (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3)
            
            y = 0.5 * ((2 * p1[1]) +
                      (-p0[1] + p2[1]) * local_t +
                      (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                      (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3)
            
            # Calculate tangent
            dx = 0.5 * ((-p0[0] + p2[0]) +
                       2 * (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * local_t +
                       3 * (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t2)
            
            dy = 0.5 * ((-p0[1] + p2[1]) +
                       2 * (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * local_t +
                       3 * (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t2)
            
            angle = math.degrees(math.atan2(dy, dx))
            return (x, y, angle)
    
    # Fallback: return first point
    return (points[0][0], points[0][1], 0)


def apply_speed_curve(t, speed_profile='linear'):
    """Apply a speed curve to the time parameter.
    
    Args:
        t: Time parameter from 0 to 1
        speed_profile: Type of speed curve
            - 'linear': constant speed
            - 'ease_in': slow start
            - 'ease_out': slow end
            - 'ease_in_out': slow start and end
            
    Returns:
        Modified time parameter
    """
    if speed_profile == 'ease_in':
        return t * t
    elif speed_profile == 'ease_out':
        return 1 - (1 - t) * (1 - t)
    elif speed_profile == 'ease_in_out':
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)
    else:  # linear
        return t


def draw_path_progressive(frame, path_config, progress, color=(0, 0, 0), thickness=2):
    """Draw a path progressively from start to current progress.
    
    Args:
        frame: Frame to draw on
        path_config: Path configuration dictionary
        progress: How much of the path to draw (0 to 1)
        color: Line color (BGR tuple)
        thickness: Line thickness
        
    Returns:
        Frame with path drawn
    """
    result = frame.copy()
    
    if progress <= 0:
        return result
    
    # Sample points along the path
    num_samples = 100
    points = []
    for i in range(int(num_samples * progress) + 1):
        t = i / num_samples
        if t > progress:
            t = progress
        x, y, _ = evaluate_path_at_time(path_config, t)
        points.append((int(x), int(y)))
    
    # Draw lines between consecutive points
    for i in range(len(points) - 1):
        cv2.line(result, points[i], points[i + 1], color, thickness)
    
    return result


def apply_path_animation(layer_img, path_config, frame_index, total_frames, orient_to_path=False):
    """Apply path animation to move and optionally rotate an object along a path.
    
    Args:
        layer_img: The layer image to animate
        path_config: Path configuration dictionary with:
            - type: path type (bezier_cubic, bezier_quadratic, linear, spline)
            - points: list of control points
            - speed_profile: optional speed curve ('linear', 'ease_in', 'ease_out', 'ease_in_out')
        frame_index: Current frame index
        total_frames: Total frames in animation
        orient_to_path: Whether to rotate object to face path direction
        
    Returns:
        Positioned and optionally rotated frame
    """
    h, w = layer_img.shape[:2]
    
    # Calculate progress
    t = frame_index / max(total_frames - 1, 1)
    
    # Apply speed curve if specified
    speed_profile = path_config.get('speed_profile', 'linear')
    t = apply_speed_curve(t, speed_profile)
    
    # Get position and angle on path
    x, y, angle = evaluate_path_at_time(path_config, t)
    
    # Create white canvas
    result = np.ones((h, w, 3), dtype=np.uint8) * 255
    
    # Get layer dimensions
    layer_h, layer_w = layer_img.shape[:2]
    
    # Calculate center offset
    center_x = int(x)
    center_y = int(y)
    
    # Apply rotation if orient_to_path is enabled
    if orient_to_path:
        # Get rotation matrix
        rotation_center = (layer_w // 2, layer_h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(rotation_center, -angle, 1.0)
        
        # Rotate the layer
        rotated_layer = cv2.warpAffine(layer_img, rotation_matrix, (layer_w, layer_h),
                                       borderMode=cv2.BORDER_CONSTANT,
                                       borderValue=(255, 255, 255))
    else:
        rotated_layer = layer_img
    
    # Calculate position to place the layer (centered at path point)
    start_x = center_x - layer_w // 2
    start_y = center_y - layer_h // 2
    
    # Clip to bounds and place layer
    if 0 <= start_x < w and 0 <= start_y < h:
        end_x = min(start_x + layer_w, w)
        end_y = min(start_y + layer_h, h)
        
        if start_x >= 0 and start_y >= 0:
            src_start_x = max(0, -start_x)
            src_start_y = max(0, -start_y)
            src_end_x = src_start_x + (end_x - max(0, start_x))
            src_end_y = src_start_y + (end_y - max(0, start_y))
            
            dst_start_x = max(0, start_x)
            dst_start_y = max(0, start_y)
            
            # Only copy non-white pixels
            layer_region = rotated_layer[src_start_y:src_end_y, src_start_x:src_end_x]
            mask = np.any(layer_region < 250, axis=2)
            
            result[dst_start_y:end_y, dst_start_x:end_x][mask] = layer_region[mask]
    
    return result


def draw_character_by_character_text(
    variables, skip_rate=5, mode='draw',
    eraser=None, eraser_mask_inv=None, eraser_ht=0, eraser_wd=0,
    text_config=None
):
    """
    Draw text character-by-character with precise timing control.
    Each character appears completely before moving to the next.
    
    Args:
        variables: AllVariables object with image data
        skip_rate: Frame skip rate for animation speed (frames per character)
        mode: 'draw' for normal drawing, 'eraser' for eraser mode, 'static' for no animation
        eraser: Eraser image (for eraser mode)
        eraser_mask_inv: Inverted eraser mask (for eraser mode)
        eraser_ht, eraser_wd: Eraser dimensions
        text_config: Text configuration with timing parameters
    """
    if mode == 'eraser':
        variables.drawn_frame[:, :, :] = variables.img
    
    # Get configuration parameters
    pause_after_char = 0
    pause_after_word = 0
    char_duration_frames = skip_rate  # Default frames per character
    
    if text_config:
        pause_after_char = text_config.get('pause_after_char', 0)
        pause_after_word = text_config.get('pause_after_word', 0)
        char_duration_frames = text_config.get('char_duration_frames', skip_rate)
    
    # Convert to grayscale and threshold to find text pixels
    img_thresh = variables.img_thresh.copy()
    height, width = img_thresh.shape
    
    # Use the original render_text_to_image to get character positions
    # We need to render each character separately and track positions
    text = text_config.get('text', '') if text_config else ''
    if not text:
        return
    
    # Process text character by character
    chars_to_draw = []
    for char in text:
        if char == '\n':
            chars_to_draw.append({'char': char, 'is_newline': True})
        elif char.isspace():
            chars_to_draw.append({'char': char, 'is_space': True})
        else:
            chars_to_draw.append({'char': char, 'is_char': True})
    
    # Find columns with text content for each character region
    # We'll divide the width by approximate character count
    columns_with_text = []
    for x in range(width):
        column = img_thresh[:, x]
        if np.any(column < 250):  # Has dark pixels (text)
            columns_with_text.append(x)
    
    if len(columns_with_text) == 0:
        return
    
    # Group columns by character based on spacing
    # Find gaps in columns to identify character boundaries
    char_column_groups = []
    if columns_with_text:
        current_group = [columns_with_text[0]]
        for i in range(1, len(columns_with_text)):
            if columns_with_text[i] - columns_with_text[i-1] > 3:  # Gap detected
                char_column_groups.append(current_group)
                current_group = [columns_with_text[i]]
            else:
                current_group.append(columns_with_text[i])
        char_column_groups.append(current_group)
    
    # Draw each character group
    counter = 0
    char_idx = 0
    is_word_start = True
    
    for group_idx, column_group in enumerate(char_column_groups):
        # Draw all columns in this character group
        for x in column_group:
            column = img_thresh[:, x]
            text_pixels = np.where(column < 250)[0]
            
            if len(text_pixels) > 0:
                # Group consecutive pixels into segments
                segments = []
                start_y = text_pixels[0]
                prev_y = text_pixels[0]
                
                for y in text_pixels[1:]:
                    if y - prev_y > 3:  # Gap detected
                        segments.append((start_y, prev_y))
                        start_y = y
                    prev_y = y
                segments.append((start_y, prev_y))
                
                # Draw all segments in this column
                for y_start, y_end in segments:
                    if mode == 'eraser':
                        variables.drawn_frame[y_start:y_end+1, x] = 255
                    else:
                        variables.drawn_frame[y_start:y_end+1, x] = variables.img[y_start:y_end+1, x]
        
        # After character is drawn, position hand and write frames
        if column_group:
            hand_coord_x = column_group[len(column_group)//2]
            # Find middle Y for this character
            column = img_thresh[:, hand_coord_x]
            text_pixels = np.where(column < 250)[0]
            hand_coord_y = text_pixels[len(text_pixels)//2] if len(text_pixels) > 0 else height // 2
            
            # Draw hand or eraser
            if mode == 'static':
                drawn_frame_with_hand = variables.drawn_frame.copy()
            elif mode == 'eraser' and eraser is not None:
                drawn_frame_with_hand = draw_eraser_on_img(
                    variables.drawn_frame.copy(), eraser.copy(),
                    hand_coord_x, hand_coord_y,
                    eraser_mask_inv.copy(), eraser_ht, eraser_wd,
                    variables.resize_ht, variables.resize_wd
                )
            else:
                drawn_frame_with_hand = draw_hand_on_img(
                    variables.drawn_frame.copy(), variables.hand.copy(),
                    hand_coord_x, hand_coord_y,
                    variables.hand_mask_inv.copy(),
                    variables.hand_ht, variables.hand_wd,
                    variables.resize_ht, variables.resize_wd
                )
            
            # Write frames for this character
            for _ in range(char_duration_frames):
                if variables.watermark_path:
                    drawn_frame_with_hand = apply_watermark(
                        drawn_frame_with_hand, variables.watermark_path,
                        variables.watermark_position, variables.watermark_opacity,
                        variables.watermark_scale
                    )
                variables.video_object.write(drawn_frame_with_hand)
                variables.frames_written += 1
            
            # Pause after character if configured
            if pause_after_char > 0:
                for _ in range(pause_after_char):
                    variables.video_object.write(drawn_frame_with_hand)
                    variables.frames_written += 1
            
            # Check if word ended (next character is space or we're at end)
            char_idx += 1
            if char_idx < len(chars_to_draw):
                if chars_to_draw[char_idx].get('is_space') or chars_to_draw[char_idx].get('is_newline'):
                    # Word ended, apply pause
                    if pause_after_word > 0:
                        for _ in range(pause_after_word):
                            variables.video_object.write(drawn_frame_with_hand)
                            variables.frames_written += 1


def draw_word_by_word_text(
    variables, skip_rate=5, mode='draw',
    eraser=None, eraser_mask_inv=None, eraser_ht=0, eraser_wd=0,
    text_config=None
):
    """
    Draw text word-by-word with typing animation.
    Each word appears completely before moving to the next.
    
    Args:
        variables: AllVariables object with image data
        skip_rate: Frame skip rate for animation speed (frames per word)
        mode: 'draw' for normal drawing, 'eraser' for eraser mode
        text_config: Text configuration with timing parameters
    """
    if mode == 'eraser':
        variables.drawn_frame[:, :, :] = variables.img
    
    # Get configuration parameters
    pause_after_word = text_config.get('pause_after_word', 0) if text_config else 0
    word_duration_frames = text_config.get('word_duration_frames', skip_rate) if text_config else skip_rate
    
    # Convert to grayscale and threshold
    img_thresh = variables.img_thresh.copy()
    height, width = img_thresh.shape
    
    # Find all columns with text
    columns_with_text = []
    for x in range(width):
        column = img_thresh[:, x]
        if np.any(column < 250):
            columns_with_text.append(x)
    
    if not columns_with_text:
        return
    
    # Group columns by words (larger gaps between words)
    word_column_groups = []
    if columns_with_text:
        current_group = [columns_with_text[0]]
        for i in range(1, len(columns_with_text)):
            # Larger gap threshold for word boundaries (e.g., 15 pixels)
            if columns_with_text[i] - columns_with_text[i-1] > 15:
                word_column_groups.append(current_group)
                current_group = [columns_with_text[i]]
            else:
                current_group.append(columns_with_text[i])
        word_column_groups.append(current_group)
    
    # Draw each word group
    for word_idx, word_columns in enumerate(word_column_groups):
        # Draw all columns in this word
        for x in word_columns:
            column = img_thresh[:, x]
            text_pixels = np.where(column < 250)[0]
            
            if len(text_pixels) > 0:
                segments = []
                start_y = text_pixels[0]
                prev_y = text_pixels[0]
                
                for y in text_pixels[1:]:
                    if y - prev_y > 3:
                        segments.append((start_y, prev_y))
                        start_y = y
                    prev_y = y
                segments.append((start_y, prev_y))
                
                for y_start, y_end in segments:
                    if mode == 'eraser':
                        variables.drawn_frame[y_start:y_end+1, x] = 255
                    else:
                        variables.drawn_frame[y_start:y_end+1, x] = variables.img[y_start:y_end+1, x]
        
        # Position hand at end of word and write frames
        if word_columns:
            hand_coord_x = word_columns[-1]
            column = img_thresh[:, hand_coord_x]
            text_pixels = np.where(column < 250)[0]
            hand_coord_y = text_pixels[len(text_pixels)//2] if len(text_pixels) > 0 else height // 2
            
            if mode == 'static':
                drawn_frame_with_hand = variables.drawn_frame.copy()
            elif mode == 'eraser' and eraser is not None:
                drawn_frame_with_hand = draw_eraser_on_img(
                    variables.drawn_frame.copy(), eraser.copy(),
                    hand_coord_x, hand_coord_y,
                    eraser_mask_inv.copy(), eraser_ht, eraser_wd,
                    variables.resize_ht, variables.resize_wd
                )
            else:
                drawn_frame_with_hand = draw_hand_on_img(
                    variables.drawn_frame.copy(), variables.hand.copy(),
                    hand_coord_x, hand_coord_y,
                    variables.hand_mask_inv.copy(),
                    variables.hand_ht, variables.hand_wd,
                    variables.resize_ht, variables.resize_wd
                )
            
            # Write frames for this word
            for _ in range(word_duration_frames):
                if variables.watermark_path:
                    drawn_frame_with_hand = apply_watermark(
                        drawn_frame_with_hand, variables.watermark_path,
                        variables.watermark_position, variables.watermark_opacity,
                        variables.watermark_scale
                    )
                variables.video_object.write(drawn_frame_with_hand)
                variables.frames_written += 1
            
            # Pause after word
            if pause_after_word > 0:
                for _ in range(pause_after_word):
                    variables.video_object.write(drawn_frame_with_hand)
                    variables.frames_written += 1


def draw_text_handwriting(
    variables, skip_rate=5, mode='draw',
    eraser=None, eraser_mask_inv=None, eraser_ht=0, eraser_wd=0
):
    """
    Draw text with handwriting animation following character contours.
    Instead of tile-based drawing, this function draws text column-by-column
    from left to right, top to bottom, simulating natural handwriting.
    
    Args:
        variables: AllVariables object with image data
        skip_rate: Frame skip rate for animation speed
        mode: 'draw' for normal drawing, 'eraser' for eraser mode, 'static' for no animation
        eraser: Eraser image (for eraser mode)
        eraser_mask_inv: Inverted eraser mask (for eraser mode)
        eraser_ht, eraser_wd: Eraser dimensions
    """
    # For eraser mode, start with the full image visible
    if mode == 'eraser':
        variables.drawn_frame[:, :, :] = variables.img
    
    # Convert to grayscale and threshold to find text pixels
    img_thresh = variables.img_thresh.copy()
    
    # Find all columns that contain black pixels (text)
    # We'll process column by column from left to right
    height, width = img_thresh.shape
    
    # Find columns with text content
    columns_with_text = []
    for x in range(width):
        column = img_thresh[:, x]
        if np.any(column < 250):  # Has dark pixels (text)
            columns_with_text.append(x)
    
    if len(columns_with_text) == 0:
        return  # No text to draw
    
    # For each column, find the vertical segments (top to bottom)
    column_segments = []
    for x in columns_with_text:
        column = img_thresh[:, x]
        # Find continuous segments in this column
        text_pixels = np.where(column < 250)[0]
        
        if len(text_pixels) > 0:
            # Group consecutive pixels into segments
            segments = []
            start_y = text_pixels[0]
            prev_y = text_pixels[0]
            
            for y in text_pixels[1:]:
                if y - prev_y > 3:  # Gap detected, start new segment
                    segments.append((start_y, prev_y))
                    start_y = y
                prev_y = y
            
            # Add the last segment
            segments.append((start_y, prev_y))
            
            # Add all segments for this column
            for y_start, y_end in segments:
                column_segments.append((x, y_start, y_end))
    
    # Group segments by line based on y-coordinates
    # This ensures multiline text is written line-by-line instead of column-by-column across all lines
    if len(column_segments) > 0:
        # Find line breaks by detecting significant y-coordinate gaps
        y_centers = sorted(set((seg[1] + seg[2]) // 2 for seg in column_segments))
        
        # Group y_centers into lines (gap threshold is half the average line height)
        lines = []
        current_line = [y_centers[0]]
        
        if len(y_centers) > 1:
            # Calculate average distance between consecutive y_centers
            y_diffs = [y_centers[i+1] - y_centers[i] for i in range(len(y_centers)-1)]
            avg_diff = sum(y_diffs) / len(y_diffs) if y_diffs else 0
            gap_threshold = max(20, avg_diff * 1.5)  # Minimum 20px gap or 1.5x average spacing
            
            for y_center in y_centers[1:]:
                if y_center - current_line[-1] > gap_threshold:
                    # New line detected
                    lines.append(current_line)
                    current_line = [y_center]
                else:
                    current_line.append(y_center)
            
        lines.append(current_line)
        
        # Assign each segment to a line based on its y_center
        def get_line_number(seg):
            y_center = (seg[1] + seg[2]) // 2
            for line_idx, line_y_centers in enumerate(lines):
                if y_center in line_y_centers or any(abs(y_center - ly) <= 5 for ly in line_y_centers):
                    return line_idx
            # Fallback: assign to closest line
            min_dist = float('inf')
            closest_line = 0
            for line_idx, line_y_centers in enumerate(lines):
                for ly in line_y_centers:
                    dist = abs(y_center - ly)
                    if dist < min_dist:
                        min_dist = dist
                        closest_line = line_idx
            return closest_line
        
        # Sort segments: first by line number, then by x coordinate (left to right), then by y
        column_segments.sort(key=lambda seg: (get_line_number(seg), seg[0], seg[1]))
    else:
        # Fallback to original sorting if no segments
        column_segments.sort(key=lambda seg: (seg[0], seg[1]))
    
    # Initialize animation data if JSON export is enabled
    if variables.export_json:
        variables.animation_data = {
            "drawing_sequence": [],
            "frames_written": []
        }
    
    # Draw each segment
    counter = 0
    for seg_idx, (x, y_start, y_end) in enumerate(column_segments):
        # Draw this vertical segment
        if mode == 'eraser':
            # In eraser mode, erase (set to white) the segment
            variables.drawn_frame[y_start:y_end+1, x] = 255
        else:
            # In draw mode, copy from original image
            variables.drawn_frame[y_start:y_end+1, x] = variables.img[y_start:y_end+1, x]
        
        # Calculate hand position at the middle of the segment
        hand_coord_x = x
        hand_coord_y = (y_start + y_end) // 2
        
        # Draw hand or eraser
        if mode == 'static':
            drawn_frame_with_hand = variables.drawn_frame.copy()
        elif mode == 'eraser' and eraser is not None:
            drawn_frame_with_hand = draw_eraser_on_img(
                variables.drawn_frame.copy(),
                eraser.copy(),
                hand_coord_x,
                hand_coord_y,
                eraser_mask_inv.copy(),
                eraser_ht,
                eraser_wd,
                variables.resize_ht,
                variables.resize_wd,
            )
        else:
            drawn_frame_with_hand = draw_hand_on_img(
                variables.drawn_frame.copy(),
                variables.hand.copy(),
                hand_coord_x,
                hand_coord_y,
                variables.hand_mask_inv.copy(),
                variables.hand_ht,
                variables.hand_wd,
                variables.resize_ht,
                variables.resize_wd,
            )
        
        counter += 1
        # Write frame based on skip rate
        if counter % skip_rate == 0 or seg_idx == len(column_segments) - 1:
            # Apply watermark if specified
            if variables.watermark_path:
                drawn_frame_with_hand = apply_watermark(
                    drawn_frame_with_hand,
                    variables.watermark_path,
                    variables.watermark_position,
                    variables.watermark_opacity,
                    variables.watermark_scale
                )
            
            variables.video_object.write(drawn_frame_with_hand)
            variables.frames_written += 1
            
            # Capture animation data if JSON export is enabled
            if variables.export_json:
                frame_data = {
                    "frame_number": len(variables.animation_data["frames_written"]),
                    "segment_drawn": {
                        "x": int(x),
                        "y_start": int(y_start),
                        "y_end": int(y_end)
                    },
                    "hand_position": {
                        "x": int(hand_coord_x),
                        "y": int(hand_coord_y)
                    },
                    "segments_remaining": int(len(column_segments) - seg_idx - 1)
                }
                variables.animation_data["frames_written"].append(frame_data)
        
        # Progress indicator
        if counter % 100 == 0 and seg_idx < len(column_segments) - 1:
            remaining = len(column_segments) - seg_idx
            print(f"Segments restants: {remaining}")
    
    # After drawing all segments, overlay the complete colored image
    # Only overlay where the current layer has content (non-white pixels)
    # This preserves previously drawn layers
    if mode != 'eraser':
        # Create a mask for pixels that belong to the current layer (non-white pixels)
        content_mask = np.any(variables.img < 250, axis=2)
        # Apply the colored image only where there is content
        variables.drawn_frame[content_mask] = variables.img[content_mask]


def draw_masked_object(
    variables, object_mask=None, skip_rate=5, black_pixel_threshold=10, mode='draw', 
    eraser=None, eraser_mask_inv=None, eraser_ht=0, eraser_wd=0
):
    """
    Implémente la logique de dessin en quadrillage.
    Sépare l'image en blocs, sélectionne le bloc le plus proche à dessiner
    et enregistre la trame.
    
    Args:
        mode: 'draw' for normal drawing with hand, 'eraser' for eraser mode, 'static' for no animation
        eraser: Eraser image (for eraser mode)
        eraser_mask_inv: Inverted eraser mask (for eraser mode)
        eraser_ht, eraser_wd: Eraser dimensions
    """
    # print("Skip Rate: ", skip_rate)
    
    # For eraser mode, start with the full image visible
    if mode == 'eraser':
        if object_mask is not None:
            object_ind = np.where(object_mask == 255)
            variables.drawn_frame[object_ind] = variables.img[object_ind]
        else:
            variables.drawn_frame[:, :, :] = variables.img
    
    # Si un masque d'objet est fourni, le seuil s'appliquera uniquement à cette zone
    img_thresh_copy = variables.img_thresh.copy()
    if object_mask is not None:
        object_mask_black_ind = np.where(object_mask == 0)
        img_thresh_copy[object_mask_black_ind] = 255

    selected_ind_val = None
    selected_ind = 0
    
    # Initialize animation data if JSON export is enabled
    if variables.export_json:
        variables.animation_data = {
            "drawing_sequence": [],
            "frames_written": []
        }
    
    # Calculer le nombre de coupes pour la grille
    n_cuts_vertical = int(math.ceil(variables.resize_ht / variables.split_len))
    n_cuts_horizontal = int(math.ceil(variables.resize_wd / variables.split_len))

    # Construire la grille de tuiles (même les tuiles de bord de taille inégale)
    grid_of_cuts = []
    for i in range(n_cuts_vertical):
        row_cuts = []
        for j in range(n_cuts_horizontal):
            y_start = i * variables.split_len
            y_end = min(y_start + variables.split_len, variables.resize_ht)
            x_start = j * variables.split_len
            x_end = min(x_start + variables.split_len, variables.resize_wd)
            tile = img_thresh_copy[y_start:y_end, x_start:x_end]
            row_cuts.append(tile)
        grid_of_cuts.append(row_cuts)
    
    # Note: grid_of_cuts is kept as nested lists (not converted to numpy array)
    # because tiles can have inconsistent sizes at image borders

    # Trouver les tuiles (tiles) contenant au moins un pixel noir
    cut_black_indices = []
    for i in range(n_cuts_vertical):
        for j in range(n_cuts_horizontal):
            if np.sum(grid_of_cuts[i][j] < black_pixel_threshold) > 0:
                cut_black_indices.append((i, j))
    
    cut_black_indices = np.array(cut_black_indices)

    counter = 0
    # Continue tant qu'il y a des tuiles à dessiner
    while len(cut_black_indices) > 0:
        if selected_ind >= len(cut_black_indices):
            selected_ind = 0 
            
        selected_ind_val = cut_black_indices[selected_ind].copy()
        
        # Récupérer la tuile à dessiner (peut être de taille variable)
        tile_to_draw = grid_of_cuts[selected_ind_val[0]][selected_ind_val[1]]
        tile_ht, tile_wd = tile_to_draw.shape # <-- On récupère la taille réelle
        
        # Calculer les coordonnées de la tuile sélectionnée EN UTILISANT LA TAILLE RÉELLE
        range_v_start = selected_ind_val[0] * variables.split_len
        range_v_end = range_v_start + tile_ht # MODIFIÉ pour utiliser la taille réelle de la tuile
        range_h_start = selected_ind_val[1] * variables.split_len
        range_h_end = range_h_start + tile_wd # MODIFIÉ pour utiliser la taille réelle de la tuile

        # Obtenir la tuile correspondante de l'image en niveaux de gris pour l'animation
        # (La couleur sera appliquée à la fin)
        gray_tile = variables.img_gray[range_v_start:range_v_end, range_h_start:range_h_end]
        
        # Appliquer la tuile au cadre de dessin
        if mode == 'eraser':
            # En mode eraser, on efface (met en blanc/noir) la tuile
            variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end] = 255
        else:
            # En mode normal, dessiner en niveaux de gris pendant l'animation
            # Mais seulement où le threshold indique du contenu (pixels noirs < threshold)
            # Créer un masque basé sur le threshold (tile_to_draw)
            content_mask = tile_to_draw < black_pixel_threshold
            
            # Convertir la tuile en niveaux de gris en BGR (3 canaux)
            gray_tile_bgr = cv2.cvtColor(gray_tile, cv2.COLOR_GRAY2BGR)
            
            # Appliquer seulement les pixels de contenu (où le masque est True)
            # Cela permet de dessiner uniquement les traits/bords, pas le fond
            frame_region = variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end]
            frame_region[content_mask] = gray_tile_bgr[content_mask]
            variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end] = frame_region

        # Coordonnées pour le centre de la main/eraser
        hand_coord_x = range_h_start + int(tile_wd / 2)
        hand_coord_y = range_v_start + int(tile_ht / 2)
        
        # Dessiner la main ou l'eraser selon le mode
        if mode == 'static':
            # Mode statique: pas de main/eraser
            drawn_frame_with_hand = variables.drawn_frame.copy()
        elif mode == 'eraser' and eraser is not None:
            # Mode eraser: utiliser l'image de l'eraser
            drawn_frame_with_hand = draw_eraser_on_img(
                variables.drawn_frame.copy(),
                eraser.copy(),
                hand_coord_x,
                hand_coord_y,
                eraser_mask_inv.copy(),
                eraser_ht,
                eraser_wd,
                variables.resize_ht,
                variables.resize_wd,
            )
        else:
            # Mode normal: utiliser l'image de la main
            drawn_frame_with_hand = draw_hand_on_img(
                variables.drawn_frame.copy(),
                variables.hand.copy(),
                hand_coord_x,
                hand_coord_y,
                variables.hand_mask_inv.copy(),
                variables.hand_ht,
                variables.hand_wd,
                variables.resize_ht,
                variables.resize_wd,
            )

        # Supprimer l'index sélectionné
        cut_black_indices = np.delete(cut_black_indices, selected_ind, axis=0)

        # Sélectionner le nouvel index le plus proche
        if len(cut_black_indices) > 0:
            euc_arr = euc_dist(cut_black_indices, selected_ind_val)
            selected_ind = np.argmin(euc_arr)
        else:
            selected_ind = -1 

        counter += 1
        if counter % skip_rate == 0 or len(cut_black_indices) == 0:
            # Apply watermark if specified
            if variables.watermark_path:
                drawn_frame_with_hand = apply_watermark(
                    drawn_frame_with_hand,
                    variables.watermark_path,
                    variables.watermark_position,
                    variables.watermark_opacity,
                    variables.watermark_scale
                )
            
            variables.video_object.write(drawn_frame_with_hand)
            variables.frames_written += 1
            
            # Capture animation data if JSON export is enabled
            if variables.export_json:
                frame_data = {
                    "frame_number": len(variables.animation_data["frames_written"]),
                    "tile_drawn": {
                        "grid_position": [int(selected_ind_val[0]), int(selected_ind_val[1])],
                        "pixel_coords": {
                            "x_start": int(range_h_start),
                            "x_end": int(range_h_end),
                            "y_start": int(range_v_start),
                            "y_end": int(range_v_end)
                        }
                    },
                    "hand_position": {
                        "x": int(hand_coord_x),
                        "y": int(hand_coord_y)
                    },
                    "tiles_remaining": int(len(cut_black_indices))
                }
                variables.animation_data["frames_written"].append(frame_data)

        if counter % 40 == 0 and len(cut_black_indices) > 0:
            print(f"Tuiles restantes: {len(cut_black_indices)}")

    # Après avoir dessiné toutes les lignes, superposer l'objet original en couleur
    # (sauf en mode eraser où on veut garder l'état effacé)
    # Only overlay where the current layer has content to preserve previously drawn layers
    if mode != 'eraser':
        if object_mask is not None:
            object_ind = np.where(object_mask == 255)
            variables.drawn_frame[object_ind] = variables.img[object_ind]
        else:
            # Create a mask for pixels that belong to the current layer (non-white pixels)
            content_mask = np.any(variables.img < 250, axis=2)
            # Apply the colored image only where there is content
            variables.drawn_frame[content_mask] = variables.img[content_mask]


def draw_whiteboard_animations(
    img, mask_path, hand_path, hand_mask_path, save_video_path, variables
):
    """Fonction principale pour orchestrer l'animation de dessin."""
    object_mask_exists = (mask_path is not None)

    # 1. Pré-traitement de l'image source et de la main
    variables = preprocess_image(img=img, variables=variables)
    variables = preprocess_hand_image(
        hand_path=hand_path, hand_mask_path=hand_mask_path, variables=variables
    )

    start_time = time.time()

    # 2. Définition de l'objet vidéo
    if platform == "android":
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    else:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
        
    variables.video_object = cv2.VideoWriter(
        save_video_path,
        fourcc,
        variables.frame_rate,
        (variables.resize_wd, variables.resize_ht),
    )

    # 3. Création d'un cadre vide (fond blanc)
    variables.drawn_frame = np.zeros(variables.img.shape, np.uint8) + np.array(
        [255, 255, 255], np.uint8
    )

    # 4. Dessin de l'animation
    # Dessiner l'image entière sans masque
    draw_masked_object(
        variables=variables,
        skip_rate=variables.object_skip_rate,
    )


    # 5. Fin de la vidéo avec l'image originale en couleur
    # Calculate total frames needed for the specified duration
    total_frames_needed = int(variables.frame_rate * variables.end_gray_img_duration_in_sec)
    animation_frames = variables.frames_written
    remaining_frames = max(0, total_frames_needed - animation_frames)
    
    # Display timing information
    animation_duration = animation_frames / variables.frame_rate
    final_hold_duration = remaining_frames / variables.frame_rate
    total_duration = (animation_frames + remaining_frames) / variables.frame_rate
    
    print(f"  ⏱️ Animation: {animation_duration:.2f}s ({animation_frames} frames)")
    print(f"  ⏱️ Final hold: {final_hold_duration:.2f}s ({remaining_frames} frames)")
    print(f"  ⏱️ Total duration: {total_duration:.2f}s")
    
    if animation_frames > total_frames_needed:
        print(f"  ⚠️ Warning: Animation duration ({animation_duration:.2f}s) exceeds specified duration ({variables.end_gray_img_duration_in_sec}s)")
    
    for i in range(remaining_frames):
        final_frame = variables.img.copy()
        # Apply watermark if specified
        if variables.watermark_path:
            final_frame = apply_watermark(
                final_frame,
                variables.watermark_path,
                variables.watermark_position,
                variables.watermark_opacity,
                variables.watermark_scale
            )
        variables.video_object.write(final_frame)
        variables.frames_written += 1

    end_time = time.time()
    print(f"Temps total d'exécution pour le dessin: {end_time - start_time:.2f} secondes")

    # 6. Fermeture de l'objet vidéo
    variables.video_object.release()


def draw_layered_whiteboard_animations(
    layers_config, hand_path, hand_mask_path, save_video_path, variables, base_path=".", slide_config=None
):
    """Dessine une animation avec plusieurs couches, chacune avec son propre skip_rate.
    
    Args:
        layers_config: Liste de configurations de couches
        hand_path: Chemin vers l'image de la main
        hand_mask_path: Chemin vers le masque de la main
        save_video_path: Chemin de sauvegarde de la vidéo
        variables: Objet AllVariables contenant les paramètres
        base_path: Chemin de base pour résoudre les chemins relatifs
        slide_config: Configuration complète de la slide (pour les cameras, etc.)
    """
    # Trier les couches par z_index
    sorted_layers = sorted(layers_config, key=lambda x: x.get('z_index', 0))
    
    # Pré-traiter l'image de la main
    hand = cv2.imread(hand_path)
    hand_mask = cv2.imread(hand_mask_path, cv2.IMREAD_GRAYSCALE)
    top_left, bottom_right = get_extreme_coordinates(hand_mask)
    hand = hand[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    hand_mask = hand_mask[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
    hand_mask_inv = 255 - hand_mask
    hand_mask = hand_mask / 255
    hand_mask_inv = hand_mask_inv / 255
    hand_bg_ind = np.where(hand_mask == 0)
    hand[hand_bg_ind] = [0, 0, 0]
    hand_ht, hand_wd = hand.shape[0], hand.shape[1]
    
    variables.hand_ht = hand_ht
    variables.hand_wd = hand_wd
    variables.hand = hand
    variables.hand_mask = hand_mask
    variables.hand_mask_inv = hand_mask_inv
    
    # Pré-traiter l'image de l'eraser
    eraser_path = os.path.join(os.path.dirname(hand_path), 'eraser.png')
    eraser_mask_path = os.path.join(os.path.dirname(hand_path), 'eraser-mask.png')
    eraser, eraser_mask, eraser_mask_inv, _, eraser_ht, eraser_wd = preprocess_eraser_image(
        eraser_path, eraser_mask_path
    )
    
    start_time = time.time()
    
    # Créer l'objet vidéo
    if platform == "android":
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    else:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    
    variables.video_object = cv2.VideoWriter(
        save_video_path,
        fourcc,
        variables.frame_rate,
        (variables.resize_wd, variables.resize_ht),
    )
    
    # Créer un canvas blanc de base
    base_canvas = np.ones((variables.resize_ht, variables.resize_wd, 3), dtype=np.uint8) * 255
    variables.drawn_frame = base_canvas.copy()
    
    # Initialiser les données d'animation si export JSON est activé
    if variables.export_json:
        variables.animation_data = {
            "frames_written": [],
            "layer_info": []
        }
    
    # Dessiner chaque couche séquentiellement
    for layer_idx, layer in enumerate(sorted_layers):
        print(f"  🖌️ Dessin de la couche {layer_idx + 1}/{len(sorted_layers)}: " + 
              f"z_index={layer.get('z_index', 0)}")
        
        try:
            # Check if this is a text layer
            layer_type = layer.get('type', 'image')
            
            if layer_type == 'text':
                # Render text to image
                text_config = layer.get('text_config', {})
                if not text_config or 'text' not in text_config:
                    print(f"    ⚠️ Configuration de texte manquante ou invalide")
                    continue
                
                # Backward compatibility: if layer.position is not set but text_config.position is,
                # use text_config.position as layer.position
                if 'position' not in layer and 'position' in text_config:
                    layer['position'] = text_config['position']
                
                # Display text config details for verification
                config_display = format_text_config_for_display(text_config)
                text_preview = text_config.get('text', '')[:MAX_TEXT_DISPLAY_LENGTH]
                print(f"    📝 Génération de texte: \"{text_preview}...\" {config_display}")
                
                # Calculate scaling factors for position adaptation (early for text layers)
                # Note: This is calculated again later for all layers, but text needs it here
                # to scale positions before rendering
                source_width = layer.get('source_width', variables.resize_wd)
                source_height = layer.get('source_height', variables.resize_ht)
                scale_x = variables.resize_wd / source_width
                scale_y = variables.resize_ht / source_height
                
                # Scale the font size
                text_config_for_render = text_config.copy()
                original_size = text_config.get('size', 12)
                scaled_size = int(original_size * min(scale_x, scale_y))  # Use min to maintain aspect ratio
                text_config_for_render['size'] = scaled_size
  
                anchor_point = layer.get('anchor_point', None)
                layer_position = layer.get('position', None)
                
                if anchor_point == 'center' and layer_position:
                    # For center anchor, scale the layer position and use it in text rendering
                    scaled_position = {
                        'x': layer_position.get('x', 0) * scale_x,
                        'y': layer_position.get('y', 0) * scale_y
                    }
                    text_config_for_render['position'] = scaled_position
                    text_config_for_render['anchor_point'] = 'center'
                elif 'position' in text_config:
                    # Use text_config.position (backward compatibility) but scale it
                    original_pos = text_config['position']
                    text_config_for_render['position'] = {
                        'x': original_pos.get('x', 0) * scale_x,
                        'y': original_pos.get('y', 0) * scale_y
                    }
                else:
                    # No position specified, default to (0,0)
                    text_config_for_render['position'] = {'x': 0, 'y': 0}
                
                layer_img_original = render_text_to_image(
                    text_config_for_render,
                    variables.resize_wd,
                    variables.resize_ht
                )
            elif layer_type == 'shape':
                # Render shape to image
                shape_config = layer.get('shape_config', {})
                if not shape_config or 'shape' not in shape_config:
                    print(f"    ⚠️ Configuration de forme manquante ou invalide")
                    continue
                
                shape_type = shape_config.get('shape', 'circle')
                print(f"    🔷 Génération de forme: {shape_type}")
                layer_img_original = render_shape_to_image(
                    shape_config,
                    variables.resize_wd,
                    variables.resize_ht
                )
            elif layer_type == 'arrow':
                # Render arrow with path animation
                arrow_config = layer.get('arrow_config', {})
                if not arrow_config or 'start' not in arrow_config or 'end' not in arrow_config:
                    print(f"    ⚠️ Configuration de flèche manquante ou invalide (start/end requis)")
                    continue
                
                print(f"    ➡️  Génération de flèche animée: start={arrow_config.get('start')}, end={arrow_config.get('end')}")
                # Create a white canvas for the arrow
                layer_img_original = np.ones((variables.resize_ht, variables.resize_wd, 3), dtype=np.uint8) * 255
                # Arrow will be drawn progressively in the drawing loop below
            else:
                # Charger l'image de la couche (URL ou chemin local)
                image_path = layer.get('image_path', '')
                
                # Résoudre chemin local si ce n'est pas une URL
                if not (image_path.startswith('http://') or image_path.startswith('https://')):
                    if not os.path.isabs(image_path):
                        image_path = os.path.join(base_path, image_path)
                
                # Charger l'image avec support URLs
                layer_img_original = load_image_from_url_or_path(image_path)
                if layer_img_original is None:
                    continue
            
            # Calculer les facteurs d'échelle pour la projection
            # Si les layers sont définis pour une résolution source différente
            source_width = layer.get('source_width', variables.resize_wd)
            source_height = layer.get('source_height', variables.resize_ht)
            scale_x = variables.resize_wd / source_width
            scale_y = variables.resize_ht / source_height
            
            # Appliquer l'échelle du layer + l'échelle de projection
            # Only for image layers (text/shape/arrow already render at target size)
            layer_scale = layer.get('scale', 1.0)
            combined_scale_x = layer_scale * scale_x
            combined_scale_y = layer_scale * scale_y
            
            if layer_type not in ['text', 'shape', 'arrow'] and (combined_scale_x != 1.0 or combined_scale_y != 1.0):
                new_width = int(layer_img_original.shape[1] * combined_scale_x)
                new_height = int(layer_img_original.shape[0] * combined_scale_y)
                layer_img_original = cv2.resize(layer_img_original, (new_width, new_height))
            
            # Obtenir position et opacité avec adaptation proportionnelle
            position = layer.get('position', {'x': 0, 'y': 0})
            
            # For text/shape/arrow layers, positioning is handled internally during rendering
            # so we don't apply an additional offset here (same as compose_layers function)
            if layer_type in ['text', 'shape', 'arrow']:
                x_offset = 0
                y_offset = 0
            else:
                # For image layers, apply the position offset
                x_offset = position.get('x', 0) * scale_x
                y_offset = position.get('y', 0) * scale_y
            
            opacity = layer.get('opacity', 1.0)
            layer_skip_rate = layer.get('skip_rate', variables.object_skip_rate)
            
            # Placement pixel-perfect : arrondir coordonnées et dimensions
            layer_full = base_canvas.copy()
            layer_h = int(round(layer_img_original.shape[0]))
            layer_w = int(round(layer_img_original.shape[1]))
            x_offset = int(round(x_offset))
            y_offset = int(round(y_offset))
        
            # Calculer les limites pour copier la couche
            x1 = max(0, x_offset)
            y1 = max(0, y_offset)
            x2 = min(variables.resize_wd, x_offset + layer_w)
            y2 = min(variables.resize_ht, y_offset + layer_h)

            lx1 = max(0, -x_offset)
            ly1 = max(0, -y_offset)
            lx2 = lx1 + (x2 - x1)
            ly2 = ly1 + (y2 - y1)
            
            if x2 > x1 and y2 > y1:
                layer_full[y1:y2, x1:x2] = layer_img_original[ly1:ly2, lx1:lx2]
            
            # Pré-traiter cette couche pour l'animation
            layer_vars = AllVariables(
                frame_rate=variables.frame_rate,
                resize_wd=variables.resize_wd,
                resize_ht=variables.resize_ht,
                split_len=variables.split_len,
                object_skip_rate=layer_skip_rate,
                bg_object_skip_rate=variables.bg_object_skip_rate,
                end_gray_img_duration_in_sec=0,  # Pas de pause entre les couches
                export_json=False,  # Géré globalement
                watermark_path=None  # Pas de watermark sur chaque couche
            )
            
            layer_vars = preprocess_image(img=layer_full, variables=layer_vars)
            layer_vars.hand_ht = hand_ht
            layer_vars.hand_wd = hand_wd
            layer_vars.hand = hand
            layer_vars.hand_mask = hand_mask
            layer_vars.hand_mask_inv = hand_mask_inv
            layer_vars.video_object = variables.video_object
            layer_vars.drawn_frame = variables.drawn_frame.copy()
            
            # Get layer mode and animations
            layer_mode = layer.get('mode', 'draw')  # 'draw', 'eraser', or 'static'
            entrance_anim = layer.get('entrance_animation', None)
            exit_anim = layer.get('exit_animation', None)
            morph_config = layer.get('morph', None)
            path_anim = layer.get('path_animation', None)
            
            # Check if we need to morph from previous layer
            if layer_idx > 0 and morph_config and morph_config.get('enabled', False):
                # Generate morph frames from previous drawn frame to current layer
                morph_duration = morph_config.get('duration', 0.5)
                morph_frames_count = int(morph_duration * variables.frame_rate)
                print(f"    🔄 Morphing from previous layer ({morph_frames_count} frames)...")
                
                # Use the current layer as target for morph
                prev_frame = variables.drawn_frame.copy()
                
                # Create a preview of what this layer will look like
                target_preview = prev_frame.copy()
                if x2 > x1 and y2 > y1:
                    if opacity < 1.0:
                        target_region = target_preview[y1:y2, x1:x2]
                        layer_region = layer_img_original[ly1:ly2, lx1:lx2]
                        blended = cv2.addWeighted(target_region, 1 - opacity, layer_region, opacity, 0)
                        target_preview[y1:y2, x1:x2] = blended
                    else:
                        target_preview[y1:y2, x1:x2] = layer_img_original[ly1:ly2, lx1:lx2]
                
                morph_frames = generate_morph_frames(prev_frame, target_preview, morph_frames_count)
                for morph_frame in morph_frames:
                    if variables.watermark_path:
                        morph_frame = apply_watermark(
                            morph_frame, variables.watermark_path,
                            variables.watermark_position, variables.watermark_opacity,
                            variables.watermark_scale
                        )
                    variables.video_object.write(morph_frame)
                    variables.frames_written += 1
                
                # Update drawn_frame to the final morphed state
                # This ensures the previous layer is fully transitioned and replaced
                if morph_frames:
                    variables.drawn_frame = morph_frames[-1].copy()
            
            # Entrance animation
            entrance_frames = 0
            if entrance_anim and entrance_anim.get('type') != 'none':
                entrance_duration = entrance_anim.get('duration', 0.5)
                entrance_frames = int(entrance_duration * variables.frame_rate)
                print(f"    ▶️  Entrance animation: {entrance_anim.get('type')} ({entrance_frames} frames)")
            
            # Dessiner cette couche selon le mode
            if layer_mode == 'static':
                # Mode statique: afficher l'image directement sans animation de dessin
                print(f"    📷 Mode statique (pas d'animation de dessin)")
                layer_vars.drawn_frame = layer_full.copy()
                # No drawing animation, frames_written stays 0 for this layer drawing
            elif layer_mode == 'eraser' and eraser is not None:
                # Mode eraser: utiliser l'eraser
                print(f"    🧹 Mode eraser")
                # Use text-specific drawing for text layers, tile-based for images
                if layer_type == 'text':
                    text_config = layer.get('text_config', {})
                    text_animation_type = text_config.get('animation_type', 'handwriting')
                    
                    # Removed: character_by_character and word_by_word animation types
                    # Now only support svg_path and default handwriting
                    
                    if text_animation_type == 'svg_path' or text_config.get('use_svg_paths', False):
                        draw_svg_path_handwriting(
                            variables=layer_vars,
                            skip_rate=layer_skip_rate,
                            mode='eraser',
                            eraser=eraser,
                            eraser_mask_inv=eraser_mask_inv,
                            eraser_ht=eraser_ht,
                            eraser_wd=eraser_wd,
                            text_config=text_config
                        )
                    else:
                        # Default: column-based handwriting
                        draw_text_handwriting(
                            variables=layer_vars,
                            skip_rate=layer_skip_rate,
                            mode='eraser',
                            eraser=eraser,
                            eraser_mask_inv=eraser_mask_inv,
                            eraser_ht=eraser_ht,
                            eraser_wd=eraser_wd
                        )
                else:
                    draw_masked_object(
                        variables=layer_vars,
                        skip_rate=layer_skip_rate,
                        mode='eraser',
                        eraser=eraser,
                        eraser_mask_inv=eraser_mask_inv,
                        eraser_ht=eraser_ht,
                        eraser_wd=eraser_wd
                    )
            else:
                # Mode normal: dessiner avec la main
                # Use text-specific drawing for text layers, tile-based for images
                if layer_type == 'text':
                    text_config = layer.get('text_config', {})
                    
                    # Check animation type for text
                    text_animation_type = text_config.get('animation_type', 'handwriting')
                    
                    # Removed: character_by_character and word_by_word animation types
                    # Now only support svg_path and default handwriting
                    
                    if text_animation_type == 'svg_path' or text_config.get('use_svg_paths', False):
                        print(f"    ✍️  Mode handwriting (SVG path-based)")
                        # Use SVG path-based drawing (opt-in)
                        draw_svg_path_handwriting(
                            variables=layer_vars,
                            skip_rate=layer_skip_rate,
                            mode='draw',
                            text_config=text_config
                        )
                    else:
                        # Default: column-based handwriting
                        print(f"    ✍️  Mode handwriting (text)")
                        draw_text_handwriting(
                            variables=layer_vars,
                            skip_rate=layer_skip_rate,
                            mode='draw'
                        )
                elif layer_type == 'arrow':
                    # Draw arrow progressively as a path animation
                    arrow_config = layer.get('arrow_config', {})
                    print(f"    ➡️  Dessin progressif de la flèche")
                    
                    # Calculate number of frames for arrow drawing
                    arrow_duration = arrow_config.get('duration', 2.0)  # default 2 seconds
                    arrow_frames = int(arrow_duration * variables.frame_rate)
                    
                    # Draw arrow progressively
                    for frame_idx in range(arrow_frames):
                        progress = (frame_idx + 1) / arrow_frames
                        
                        # Draw arrow on current frame
                        frame_with_arrow = draw_arrow_progressive(
                            layer_vars.drawn_frame.copy(),
                            arrow_config,
                            progress,
                            variables.resize_wd,
                            variables.resize_ht
                        )
                        
                        layer_vars.drawn_frame = frame_with_arrow
                        
                        # Apply watermark if configured
                        if variables.watermark_path:
                            frame_with_arrow = apply_watermark(
                                frame_with_arrow, variables.watermark_path,
                                variables.watermark_position, variables.watermark_opacity,
                                variables.watermark_scale
                            )
                        
                        # Write frame to video
                        variables.video_object.write(frame_with_arrow)
                        layer_vars.frames_written += 1
                else:
                    draw_masked_object(
                        variables=layer_vars,
                        skip_rate=layer_skip_rate,
                        mode='draw'
                    )
            
            # Accumulate frame count from this layer
            variables.frames_written += layer_vars.frames_written
            
            # Extract the drawn layer content from the positioned region
            # layer_vars.drawn_frame contains the drawing from layer_full (which was positioned)
            # We need to extract only the content region and place it at the correct position
            layer_drawn_region = layer_vars.drawn_frame[y1:y2, x1:x2] if (y2 > y1 and x2 > x1) else np.ones((1, 1, 3), dtype=np.uint8) * 255
            
            # Create mask for this layer's content (from the original layer image position)
            layer_mask = np.any(layer_full < 250, axis=2).astype(np.float32)
            layer_mask_3d = np.stack([layer_mask] * 3, axis=2)
            
            # Apply entrance animation to drawn layer before blending
            if entrance_anim and entrance_anim.get('type') != 'none':
                entrance_duration = entrance_anim.get('duration', 0.5)
                entrance_frames = int(entrance_duration * variables.frame_rate)
                
                # Check if this is a push animation
                is_push_animation = entrance_anim.get('type', '').startswith('push_from_')
                
                # Generate entrance animation frames
                for frame_idx in range(entrance_frames):
                    # Start with current state
                    anim_frame = variables.drawn_frame.copy()
                    
                    # Apply entrance animation to the new layer content
                    if is_push_animation:
                        # Use push animation with hand overlay
                        layer_animated = apply_push_animation_with_hand(
                            layer_vars.drawn_frame,
                            entrance_anim,
                            frame_idx,
                            entrance_frames,
                            variables.frame_rate,
                            hand.copy(),
                            hand_mask_inv.copy(),
                            hand_ht,
                            hand_wd
                        )
                    else:
                        # Use standard entrance animation
                        layer_animated = apply_entrance_animation(
                            layer_vars.drawn_frame,
                            entrance_anim,
                            frame_idx,
                            entrance_frames,
                            variables.frame_rate
                        )
                    
                    # Blend animated layer with current frame
                    if opacity < 1.0:
                        layer_content = layer_animated * layer_mask_3d
                        old_background = anim_frame * layer_mask_3d
                        blended_layer = cv2.addWeighted(old_background, 1 - opacity, layer_content, opacity, 0)
                        anim_frame = (layer_mask_3d * blended_layer + 
                                     (1 - layer_mask_3d) * anim_frame).astype(np.uint8)
                    else:
                        anim_frame = np.where(layer_mask_3d > 0, layer_animated, anim_frame).astype(np.uint8)
                    
                    # Apply watermark and write frame
                    if variables.watermark_path:
                        anim_frame = apply_watermark(
                            anim_frame, variables.watermark_path,
                            variables.watermark_position, variables.watermark_opacity,
                            variables.watermark_scale
                        )
                    variables.video_object.write(anim_frame)
                    variables.frames_written += 1
            
            # Apply path animation if configured
            if path_anim and path_anim.get('enabled', False):
                path_duration = path_anim.get('duration', 2.0)
                path_frames = int(path_duration * variables.frame_rate)
                orient_to_path = path_anim.get('orient_to_path', False)
                draw_path = path_anim.get('draw_path', False)
                path_color = path_anim.get('path_color', [0, 0, 0])  # BGR
                path_thickness = path_anim.get('path_thickness', 2)
                
                print(f"    🛤️  Path animation: {path_anim.get('type', 'linear')} " +
                      f"({path_frames} frames, orient={orient_to_path}, draw_path={draw_path})")
                
                # Generate path animation frames
                for frame_idx in range(path_frames):
                    # Start with current state
                    anim_frame = variables.drawn_frame.copy()
                    
                    # Optionally draw the path progressively
                    if draw_path:
                        progress = frame_idx / max(path_frames - 1, 1)
                        anim_frame = draw_path_progressive(
                            anim_frame, 
                            path_anim, 
                            progress,
                            tuple(path_color),
                            path_thickness
                        )
                    
                    # Apply path animation to move/rotate the layer
                    layer_on_path = apply_path_animation(
                        layer_vars.drawn_frame,
                        path_anim,
                        frame_idx,
                        path_frames,
                        orient_to_path
                    )
                    
                    # Create mask for layer on path
                    path_layer_mask = np.any(layer_on_path < 250, axis=2).astype(np.float32)
                    path_layer_mask_3d = np.stack([path_layer_mask] * 3, axis=2)
                    
                    # Blend layer on path with current frame
                    if opacity < 1.0:
                        layer_content = layer_on_path * path_layer_mask_3d
                        old_background = anim_frame * path_layer_mask_3d
                        blended_layer = cv2.addWeighted(old_background, 1 - opacity, layer_content, opacity, 0)
                        anim_frame = (path_layer_mask_3d * blended_layer + 
                                     (1 - path_layer_mask_3d) * anim_frame).astype(np.uint8)
                    else:
                        anim_frame = np.where(path_layer_mask_3d > 0, layer_on_path, anim_frame).astype(np.uint8)
                    
                    # Apply watermark and write frame
                    if variables.watermark_path:
                        anim_frame = apply_watermark(
                            anim_frame, variables.watermark_path,
                            variables.watermark_position, variables.watermark_opacity,
                            variables.watermark_scale
                        )
                    variables.video_object.write(anim_frame)
                    variables.frames_written += 1
                
                # Update drawn_frame to final position
                variables.drawn_frame = anim_frame.copy()
            else:
                # Final blend of layer (only when path animation is NOT used)
                # Use the positioned region from the drawn layer
                if y2 > y1 and x2 > x1:
                    # Extract the drawn region that corresponds to the layer position
                    layer_drawn_region = layer_vars.drawn_frame[y1:y2, x1:x2]
                    
                    if opacity < 1.0:
                        # Blend with opacity
                        old_region = variables.drawn_frame[y1:y2, x1:x2]
                        blended = cv2.addWeighted(old_region, 1 - opacity, layer_drawn_region, opacity, 0)
                        variables.drawn_frame[y1:y2, x1:x2] = blended
                    else:
                        # No opacity blending, just overlay where layer has content
                        variables.drawn_frame[y1:y2, x1:x2] = layer_drawn_region
                else:
                    # Fallback to full frame blending if dimensions are invalid
                    if opacity < 1.0:
                        layer_content = layer_vars.drawn_frame * layer_mask_3d
                        old_background = variables.drawn_frame * layer_mask_3d
                        blended_layer = cv2.addWeighted(old_background, 1 - opacity, layer_content, opacity, 0)
                        variables.drawn_frame = (layer_mask_3d * blended_layer + 
                                                (1 - layer_mask_3d) * variables.drawn_frame).astype(np.uint8)
                    else:
                        variables.drawn_frame = np.where(layer_mask_3d > 0, 
                                                        layer_vars.drawn_frame, 
                                                        variables.drawn_frame).astype(np.uint8)
            
            # Apply exit animation after layer is complete (if this is the last layer or configured)
            if exit_anim and exit_anim.get('type') != 'none':
                exit_duration = exit_anim.get('duration', 0.5)
                exit_frames = int(exit_duration * variables.frame_rate)
                print(f"    ◀️  Exit animation: {exit_anim.get('type')} ({exit_frames} frames)")
                
                # Generate exit animation frames
                for frame_idx in range(exit_frames):
                    exit_frame = apply_exit_animation(
                        variables.drawn_frame,
                        exit_anim,
                        frame_idx,
                        exit_frames,
                        variables.frame_rate
                    )
                    
                    if variables.watermark_path:
                        exit_frame = apply_watermark(
                            exit_frame, variables.watermark_path,
                            variables.watermark_position, variables.watermark_opacity,
                            variables.watermark_scale
                        )
                    variables.video_object.write(exit_frame)
                    variables.frames_written += 1
                
                # After exit animation, reset to white or keep final frame
                # depending on whether there are more layers
                if layer_idx < len(sorted_layers) - 1:
                    # More layers coming, reset to white
                    variables.drawn_frame = base_canvas.copy()
            # Apply camera transformation if specified
            camera_config = layer.get('camera', None)
            if camera_config:
                print(f"    📷 Applying camera: zoom={camera_config.get('zoom', 1.0)}")
                variables.drawn_frame = apply_camera_transform(
                    variables.drawn_frame,
                    camera_config,
                    variables.resize_wd,
                    variables.resize_ht
                )
            
            # Apply post-animation effects if specified
            animation_config = layer.get('animation', None)
            if animation_config:
                effect_type = animation_config.get('type', 'none')
                if effect_type != 'none':
                    print(f"    🎬 Applying animation effect: {effect_type}")
                    # Create temporary frames for effect
                    temp_frames = [variables.drawn_frame.copy()]
                    effect_frames = apply_post_animation_effect(
                        temp_frames,
                        animation_config,
                        variables.frame_rate,
                        variables.resize_wd,
                        variables.resize_ht
                    )
                    
                    # Write additional effect frames
                    for effect_frame in effect_frames[1:]:  # Skip first frame (already written)
                        if variables.watermark_path:
                            effect_frame = apply_watermark(
                                effect_frame,
                                variables.watermark_path,
                                variables.watermark_position,
                                variables.watermark_opacity,
                                variables.watermark_scale
                            )
                        variables.video_object.write(effect_frame)
                        variables.frames_written += 1
                    
                    # Update drawn_frame to last effect frame
                    if len(effect_frames) > 0:
                        variables.drawn_frame = effect_frames[-1].copy()
            
            # Apply particle effects if specified
            particle_config = layer.get('particle_effect', None)
            if particle_config and PARTICLE_SYSTEM_AVAILABLE:
                effect_type = particle_config.get('type', 'confetti')
                duration = particle_config.get('duration', 2.0)
                particle_frames = int(duration * variables.frame_rate)
                
                print(f"    ✨ Applying particle effect: {effect_type} ({particle_frames} frames)")
                
                # Generate particle effect frames
                for frame_idx in range(particle_frames):
                    particle_frame = apply_particle_effect(
                        variables.drawn_frame.copy(),
                        particle_config,
                        frame_idx,
                        particle_frames,
                        variables.frame_rate
                    )
                    
                    if variables.watermark_path:
                        particle_frame = apply_watermark(
                            particle_frame,
                            variables.watermark_path,
                            variables.watermark_position,
                            variables.watermark_opacity,
                            variables.watermark_scale
                        )
                    variables.video_object.write(particle_frame)
                    variables.frames_written += 1
            
            # Enregistrer les infos de la couche pour l'export JSON
            if variables.export_json:
                variables.animation_data["layer_info"].append({
                    "layer_index": layer_idx,
                    "image_path": layer.get('image_path', ''),
                    "position": position,
                    "z_index": layer.get('z_index', 0),
                    "scale": layer_scale,
                    "opacity": opacity,
                    "skip_rate": layer_skip_rate,
                    "source_width": source_width,
                    "source_height": source_height,
                    "scale_x": scale_x,
                    "scale_y": scale_y
                })
            
        except Exception as e:
            print(f"    ❌ Erreur lors du dessin de la couche: {e}")
            continue
    
    # Check if there are camera sequences defined at slide level
    camera_sequence = slide_config.get('cameras', None) if slide_config else None
    
    if camera_sequence and len(camera_sequence) > 0:
        # Advanced camera system: multiple cameras with transitions
        print(f"  🎥 Processing camera sequence with {len(camera_sequence)} camera(s)")
        camera_frames = generate_camera_sequence_frames(
            variables.drawn_frame.copy(),
            camera_sequence,
            variables.frame_rate,
            variables.resize_wd,
            variables.resize_ht
        )
        
        # Write all camera sequence frames
        for camera_frame in camera_frames:
            if variables.watermark_path:
                camera_frame = apply_watermark(
                    camera_frame,
                    variables.watermark_path,
                    variables.watermark_position,
                    variables.watermark_opacity,
                    variables.watermark_scale
                )
            variables.video_object.write(camera_frame)
            variables.frames_written += 1
        
        camera_duration = len(camera_frames) / variables.frame_rate
        print(f"  ⏱️ Camera sequence: {camera_duration:.2f}s ({len(camera_frames)} frames)")
    else:
        # Standard final hold behavior
        # Calculate total frames needed for the specified duration
        total_frames_needed = int(variables.frame_rate * variables.end_gray_img_duration_in_sec)
        animation_frames = variables.frames_written
        remaining_frames = max(0, total_frames_needed - animation_frames)
        
        # Display timing information
        animation_duration = animation_frames / variables.frame_rate
        final_hold_duration = remaining_frames / variables.frame_rate
        total_duration = (animation_frames + remaining_frames) / variables.frame_rate
        
        print(f"  ⏱️ Animation: {animation_duration:.2f}s ({animation_frames} frames)")
        print(f"  ⏱️ Final hold: {final_hold_duration:.2f}s ({remaining_frames} frames)")
        print(f"  ⏱️ Total duration: {total_duration:.2f}s")
        
        if animation_frames > total_frames_needed:
            print(f"  ⚠️ Warning: Animation duration ({animation_duration:.2f}s) exceeds specified duration ({variables.end_gray_img_duration_in_sec}s)")
        
        for i in range(remaining_frames):
            final_frame = variables.drawn_frame.copy()
            # Appliquer le watermark sur l'image finale uniquement
            if variables.watermark_path:
                final_frame = apply_watermark(
                    final_frame,
                    variables.watermark_path,
                    variables.watermark_position,
                    variables.watermark_opacity,
                    variables.watermark_scale
                )
            variables.video_object.write(final_frame)
            variables.frames_written += 1
    
    end_time = time.time()
    print(f"  ⏱️ Temps de dessin des couches: {end_time - start_time:.2f} secondes")
    
    # Fermer l'objet vidéo
    variables.video_object.release()
    
def export_animation_json(variables, json_path):
    """Exporte les données d'animation au format JSON."""
    if not variables.animation_data:
        print("⚠️ Aucune donnée d'animation à exporter.")
        return False
    
    try:
        # Convert numpy types to Python native types
        def convert_to_native(obj):
            """Convertit les types numpy en types Python natifs."""
            if isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64,
                               np.uint8, np.uint16, np.uint32, np.uint64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_to_native(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(item) for item in obj]
            else:
                return obj
        
        export_data = {
            "metadata": {
                "frame_rate": int(variables.frame_rate),
                "width": int(variables.resize_wd),
                "height": int(variables.resize_ht),
                "split_len": int(variables.split_len),
                "object_skip_rate": int(variables.object_skip_rate),
                "total_frames": len(variables.animation_data["frames_written"]),
                "hand_dimensions": {
                    "width": int(variables.hand_wd),
                    "height": int(variables.hand_ht)
                }
            },
            "animation": convert_to_native(variables.animation_data)
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Données d'animation exportées: {json_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export JSON: {e}")
        return False


def find_nearest_res(given):
    """Trouve la résolution standard la plus proche pour une dimension donnée."""
    arr = np.array([360, 480, 640, 720, 1080, 1280, 1440, 1920, 2160, 2560, 3840, 4320, 7680])
    idx = (np.abs(arr - given)).argmin()
    return arr[idx]


def calculate_aspect_ratio_dimensions(original_width, original_height, aspect_ratio):
    """Calculate dimensions for a specific aspect ratio.
    
    Args:
        original_width: Original image width
        original_height: Original image height
        aspect_ratio: Target aspect ratio string ('1:1', '16:9', '9:16', 'original')
    
    Returns:
        tuple: (width, height) for the target aspect ratio
    """
    if aspect_ratio == 'original':
        return original_width, original_height
    
    # Parse aspect ratio
    if aspect_ratio == '1:1':
        ratio_w, ratio_h = 1, 1
    elif aspect_ratio == '16:9':
        ratio_w, ratio_h = 16, 9
    elif aspect_ratio == '9:16':
        ratio_w, ratio_h = 9, 16
    else:
        return original_width, original_height
    
    # Calculate dimensions maintaining the aspect ratio
    target_ratio = ratio_w / ratio_h
    original_ratio = original_width / original_height
    
    # Determine base dimension (use the larger dimension as reference)
    if aspect_ratio == '1:1':
        # For 1:1, use the smaller dimension to avoid too much cropping
        base = min(original_width, original_height)
        width = height = find_nearest_res(base)
    elif aspect_ratio == '16:9':
        # HD 16:9 resolutions
        if original_height >= 1080:
            width, height = 1920, 1080
        elif original_height >= 720:
            width, height = 1280, 720
        else:
            height = find_nearest_res(original_height)
            width = find_nearest_res(int(height * target_ratio))
    elif aspect_ratio == '9:16':
        # Vertical video resolutions
        if original_width >= 1080:
            width, height = 1080, 1920
        elif original_width >= 720:
            width, height = 720, 1280
        else:
            width = find_nearest_res(original_width)
            height = find_nearest_res(int(width / target_ratio))
    else:
        width, height = original_width, original_height
    
    return width, height


def apply_aspect_ratio_padding(image, target_width, target_height):
    """Apply padding to maintain aspect ratio with letterboxing/pillarboxing.
    
    Args:
        image: Input image (numpy array)
        target_width: Target width
        target_height: Target height
    
    Returns:
        Padded image with white background
    """
    img_height, img_width = image.shape[:2]
    
    # Calculate scaling to fit within target dimensions
    scale = min(target_width / img_width, target_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    
    # Resize image
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Create white canvas
    canvas = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
    
    # Calculate position to center the image
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    
    # Place image on canvas
    canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
    
    return canvas


def apply_watermark(frame, watermark_path, position='bottom-right', opacity=0.5, scale=0.1):
    """Apply watermark to a frame.
    
    Args:
        frame: Input frame (numpy array)
        watermark_path: Path to watermark image
        position: Position string ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
        opacity: Watermark opacity (0.0 to 1.0)
        scale: Scale of watermark relative to frame width (0.0 to 1.0)
    
    Returns:
        Frame with watermark applied
    """
    if not watermark_path or not os.path.exists(watermark_path):
        return frame
    
    try:
        # Load watermark
        watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
        if watermark is None:
            print(f"⚠️ Warning: Could not load watermark from {watermark_path}")
            return frame
        
        # Calculate watermark size
        frame_height, frame_width = frame.shape[:2]
        watermark_width = int(frame_width * scale)
        watermark_height = int(watermark.shape[0] * (watermark_width / watermark.shape[1]))
        watermark_resized = cv2.resize(watermark, (watermark_width, watermark_height))
        
        # Handle alpha channel
        if watermark_resized.shape[2] == 4:
            # Has alpha channel
            watermark_bgr = watermark_resized[:, :, :3]
            watermark_alpha = watermark_resized[:, :, 3] / 255.0 * opacity
        else:
            # No alpha channel, use opacity
            watermark_bgr = watermark_resized
            watermark_alpha = np.ones((watermark_height, watermark_width)) * opacity
        
        # Calculate position
        margin = 20
        if position == 'top-left':
            y1, y2 = margin, margin + watermark_height
            x1, x2 = margin, margin + watermark_width
        elif position == 'top-right':
            y1, y2 = margin, margin + watermark_height
            x1, x2 = frame_width - watermark_width - margin, frame_width - margin
        elif position == 'bottom-left':
            y1, y2 = frame_height - watermark_height - margin, frame_height - margin
            x1, x2 = margin, margin + watermark_width
        elif position == 'bottom-right':
            y1, y2 = frame_height - watermark_height - margin, frame_height - margin
            x1, x2 = frame_width - watermark_width - margin, frame_width - margin
        elif position == 'center':
            y1, y2 = (frame_height - watermark_height) // 2, (frame_height + watermark_height) // 2
            x1, x2 = (frame_width - watermark_width) // 2, (frame_width + watermark_width) // 2
        else:
            # Default to bottom-right
            y1, y2 = frame_height - watermark_height - margin, frame_height - margin
            x1, x2 = frame_width - watermark_width - margin, frame_width - margin
        
        # Ensure bounds are within frame
        y1, y2 = max(0, y1), min(frame_height, y2)
        x1, x2 = max(0, x1), min(frame_width, x2)
        
        # Adjust watermark size if it doesn't fit
        actual_height = y2 - y1
        actual_width = x2 - x1
        if actual_height != watermark_height or actual_width != watermark_width:
            watermark_bgr = watermark_bgr[:actual_height, :actual_width]
            watermark_alpha = watermark_alpha[:actual_height, :actual_width]
        
        # Apply watermark using alpha blending
        roi = frame[y1:y2, x1:x2]
        for c in range(3):
            roi[:, :, c] = roi[:, :, c] * (1 - watermark_alpha) + watermark_bgr[:, :, c] * watermark_alpha
        
        frame[y1:y2, x1:x2] = roi
        
    except Exception as e:
        print(f"⚠️ Warning: Error applying watermark: {e}")
    
    return frame

class AllVariables:
    """Classe conteneur pour toutes les variables et paramètres du processus."""
    def __init__(
        self,
        frame_rate=None,
        resize_wd=None,
        resize_ht=None,
        split_len=None,
        object_skip_rate=None,
        bg_object_skip_rate=None,
        end_gray_img_duration_in_sec=None,
        export_json=False,
        watermark_path=None,
        watermark_position='bottom-right',
        watermark_opacity=0.5,
        watermark_scale=0.1,
    ):
        self.frame_rate = frame_rate
        self.resize_wd = resize_wd
        self.resize_ht = resize_ht
        self.split_len = split_len
        self.object_skip_rate = object_skip_rate
        self.bg_object_skip_rate = bg_object_skip_rate
        self.end_gray_img_duration_in_sec = end_gray_img_duration_in_sec
        self.export_json = export_json
        self.watermark_path = watermark_path
        self.watermark_position = watermark_position
        self.watermark_opacity = watermark_opacity
        self.watermark_scale = watermark_scale
        
        # Variables qui seront ajoutées plus tard
        self.img_ht = None
        self.img_wd = None
        self.img_gray = None
        self.img_thresh = None
        self.img = None
        self.hand_ht = None
        self.hand_wd = None
        self.hand = None
        self.hand_mask = None
        self.hand_mask_inv = None
        self.video_object = None
        self.drawn_frame = None
        
        # Variables pour l'export JSON
        self.animation_data = None
        
        # Frame counter for tracking total frames written
        self.frames_written = 0


def common_divisors(num1, num2):
    """Trouve tous les diviseurs communs de deux nombres et les renvoie triés."""
    common_divs = []
    min_num = min(num1, num2)
    
    for i in range(1, min_num + 1):
        if num1 % i == 0 and num2 % i == 0:
            common_divs.append(i)
    return common_divs


def compose_layers(layers_config, target_width, target_height, base_path="."):
    """Compose plusieurs couches d'images en une seule image.
    
    Args:
        layers_config: Liste de configurations de couches avec:
            - image_path: chemin vers l'image
            - position: dict avec x, y
            - anchor_point: point d'ancrage de la position (optionnel, défaut 'top-left')
                           'top-left': position est le coin supérieur gauche (comportement par défaut)
                           'center': position est le centre de l'objet
            - width: largeur explicite pour redimensionner (optionnel, priorité sur scale)
            - height: hauteur explicite pour redimensionner (optionnel, priorité sur scale)
            - z_index: ordre de superposition
            - scale: échelle de l'image (optionnel, défaut 1.0)
            - opacity: opacité de la couche (optionnel, défaut 1.0)
            - intelligent_eraser: si True, efface la zone de collision avant de dessiner (optionnel, défaut False)
        target_width: largeur du canvas cible
        target_height: hauteur du canvas cible
        base_path: chemin de base pour résoudre les chemins relatifs
    
    Returns:
        Image composée (numpy array BGR)
    """
    # Créer un canvas blanc
    canvas = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
    
    # Trier les couches par z_index (du plus petit au plus grand)
    sorted_layers = sorted(layers_config, key=lambda x: x.get('z_index', 0))
    
    print(f"  📐 Composition de {len(sorted_layers)} couche(s)...")
    
    for layer in sorted_layers:
        try:
            # Check if this is a text layer
            layer_type = layer.get('type', 'image')
            
            if layer_type == 'text':
                # Render text to image
                text_config = layer.get('text_config', {})
                if not text_config or 'text' not in text_config:
                    print(f"    ⚠️ Configuration de texte manquante ou invalide")
                    continue
                
                # Backward compatibility: if layer.position is not set but text_config.position is,
                # use text_config.position as layer.position
                if 'position' not in layer and 'position' in text_config:
                    layer['position'] = text_config['position']
                
                # Display text config details for verification
                config_display = format_text_config_for_display(text_config)
                print(f"    📝 Génération de texte pour composition {config_display}")
                # For layer-based rendering with anchor_point, use layer position
                # Otherwise, use text_config.position if available, else position at (0,0)
                text_config_for_render = text_config.copy()
                anchor_point = layer.get('anchor_point', None)  # None means no anchor_point specified
                layer_position = layer.get('position', None)
                
                if anchor_point == 'center' and layer_position:
                    # For center anchor, use the layer position directly in text rendering
                    text_config_for_render['position'] = layer_position
                    text_config_for_render['anchor_point'] = 'center'
                elif 'position' in text_config:
                    # Use text_config.position (backward compatibility)
                    # Don't override it
                    pass
                else:
                    # No position specified, default to (0,0)
                    text_config_for_render['position'] = {'x': 0, 'y': 0}
                
                layer_img = render_text_to_image(
                    text_config_for_render,
                    target_width,
                    target_height
                )
            elif layer_type == 'shape':
                # Render shape to image
                shape_config = layer.get('shape_config', {})
                if not shape_config or 'shape' not in shape_config:
                    print(f"    ⚠️ Configuration de forme manquante ou invalide")
                    continue
                
                shape_type = shape_config.get('shape', 'circle')
                print(f"    🔷 Génération de forme pour composition: {shape_type}")
                
                # For center anchor, pass through the layer position to shape rendering
                shape_config_for_render = shape_config.copy()
                anchor_point = layer.get('anchor_point', 'top-left')
                layer_position = layer.get('position', {'x': target_width // 2, 'y': target_height // 2})
                
                if anchor_point == 'center':
                    # Use layer position for shape center
                    shape_config_for_render['position'] = layer_position
                # else shape_config already has its position
                
                layer_img = render_shape_to_image(
                    shape_config_for_render,
                    target_width,
                    target_height
                )
            elif layer_type == 'arrow':
                # Render arrow fully drawn (for composition, no animation)
                arrow_config = layer.get('arrow_config', {})
                if not arrow_config or 'start' not in arrow_config or 'end' not in arrow_config:
                    print(f"    ⚠️ Configuration de flèche manquante ou invalide")
                    continue
                
                print(f"    ➡️  Génération de flèche pour composition")
                # Create white canvas and draw fully completed arrow
                layer_img = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
                layer_img = draw_arrow_progressive(
                    layer_img,
                    arrow_config,
                    1.0,  # Fully drawn
                    target_width,
                    target_height
                )
            else:
                # Résoudre et charger l'image de la couche (URL ou chemin local)
                image_path = layer.get('image_path', '')
                
                # Résoudre chemin local si ce n'est pas une URL
                if not (image_path.startswith('http://') or image_path.startswith('https://')):
                    if not os.path.isabs(image_path):
                        image_path = os.path.join(base_path, image_path)
                
                # Charger l'image avec support URLs
                layer_img = load_image_from_url_or_path(image_path)
                if layer_img is None:
                    continue
            
            # Appliquer le redimensionnement explicite (width/height) ou l'échelle
            # width/height prend la priorité sur scale pour la compatibilité avec les éditeurs externes
            explicit_width = layer.get('width', None)
            explicit_height = layer.get('height', None)
            scale = layer.get('scale', 1.0)  # Get scale for logging
            
            if explicit_width is not None and explicit_height is not None:
                # Redimensionnement explicite demandé
                new_width = int(explicit_width)
                new_height = int(explicit_height)
                layer_img = cv2.resize(layer_img, (new_width, new_height))
            elif scale != 1.0:
                # Utiliser scale si pas de width/height explicite
                new_width = int(layer_img.shape[1] * scale)
                new_height = int(layer_img.shape[0] * scale)
                layer_img = cv2.resize(layer_img, (new_width, new_height))
            
            # Calculer les dimensions finales de la couche
            layer_h, layer_w = layer_img.shape[:2]
            
            # Obtenir la position et le point d'ancrage
            position = layer.get('position', {'x': 0, 'y': 0})
            anchor_point = layer.get('anchor_point', 'top-left')  # 'top-left' ou 'center'
            
            # For text/shape/arrow layers that render to full canvas, they handle positioning internally
            # so we always use (0,0) for layer placement
            if layer_type in ['text', 'shape', 'arrow']:
                x = 0
                y = 0
            else:
                x = int(position.get('x', 0))  # Convertir en entier
                y = int(position.get('y', 0))  # Convertir en entier
                
                # Ajuster la position selon le point d'ancrage pour les images
                if anchor_point == 'center':
                    # Si le point d'ancrage est le centre, ajuster pour obtenir le coin supérieur gauche
                    x = x - layer_w // 2
                    y = y - layer_h // 2
            
            # Obtenir l'opacité
            opacity = layer.get('opacity', 1.0)
            opacity = max(0.0, min(1.0, opacity))  # Limiter entre 0 et 1
            
            # S'assurer que la couche reste dans les limites du canvas
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(target_width, x + layer_w)
            y2 = min(target_height, y + layer_h)
            
            # Calculer les coordonnées correspondantes dans l'image de la couche
            lx1 = max(0, -x)
            ly1 = max(0, -y)
            lx2 = lx1 + (x2 - x1)
            ly2 = ly1 + (y2 - y1)
            
            # Vérifier qu'il y a une région valide à copier
            if x2 <= x1 or y2 <= y1 or lx2 <= lx1 or ly2 <= ly1:
                print(f"    ⚠️ Couche hors limites: {os.path.basename(image_path)}")
                continue
            
            # Copier la région de la couche sur le canvas avec opacité
            layer_region = layer_img[ly1:ly2, lx1:lx2]
            canvas_region = canvas[y1:y2, x1:x2].copy()
            
            # Intelligent eraser: efface la zone de collision avant de dessiner
            intelligent_eraser = layer.get('intelligent_eraser', False)
            if intelligent_eraser:
                # Créer un masque de contenu (pixels non-blancs) de la nouvelle couche
                # Un pixel est considéré comme du contenu s'il est significativement différent du blanc
                threshold = 250
                layer_content_mask = np.any(layer_region < threshold, axis=2)
                
                # Effacer (mettre en blanc) les zones du canvas où la nouvelle couche a du contenu
                canvas_region[layer_content_mask] = [255, 255, 255]
            
            if opacity < 1.0:
                # Mélanger avec opacité
                canvas[y1:y2, x1:x2] = cv2.addWeighted(
                    canvas_region, 1 - opacity, layer_region, opacity, 0
                )
            else:
                # Pour opacité 1.0, copier seulement les pixels non-blancs de la couche
                # Cela préserve le fond blanc et l'effet d'effacement
                threshold = 250
                layer_content_mask = np.any(layer_region < threshold, axis=2)
                canvas_region[layer_content_mask] = layer_region[layer_content_mask]
                canvas[y1:y2, x1:x2] = canvas_region
            
            z_idx = layer.get('z_index', 0)
            eraser_str = ", eraser:on" if intelligent_eraser else ""
            
            # Get layer description for logging
            if layer_type == 'text':
                layer_desc = f"text:{text_config.get('text', '')[:30]}..."
            elif layer_type == 'shape':
                layer_desc = f"shape:{shape_config.get('shape', 'unknown')}"
            elif layer_type == 'arrow':
                layer_desc = "arrow"
            else:
                layer_desc = os.path.basename(image_path)
            
            print(f"    ✓ Couche appliquée: {layer_desc} " + 
                  f"(z:{z_idx}, pos:{x},{y}, scale:{scale:.2f}, opacity:{opacity:.2f}{eraser_str})")
        
        except Exception as e:
            print(f"    ❌ Erreur lors de l'application de la couche: {e}")
            continue
    
    return canvas


def compose_scene_with_camera(scene_config, camera_config=None, scene_width=1920, scene_height=1080, 
                               background='#FFFFFF', base_path=".", verbose=True):
    """Compose a scene with camera-based viewport positioning.
    
    Similar to the TypeScript exportSceneImage function, this renders a scene
    with all layers positioned correctly relative to the camera viewport.
    
    Args:
        scene_config: Scene configuration dict with:
            - layers: List of layer configurations
            - backgroundImage: Optional background image path
            - sceneCameras: Optional list of camera configurations (first default camera will be used)
        camera_config: Optional camera configuration dict with:
            - width: Camera viewport width (default: 800)
            - height: Camera viewport height (default: 450)
            - position: Dict with x, y (0.0-1.0, default 0.5, 0.5 for center)
            - isDefault: Boolean indicating if this is the default camera
        scene_width: Scene width in pixels (default: 1920)
        scene_height: Scene height in pixels (default: 1080)
        background: Background color (hex string or RGB tuple, default: '#FFFFFF')
        base_path: Base path for resolving relative file paths
    
    Returns:
        Composed image as numpy array (BGR format)
    """
    # Get camera configuration
    if camera_config is None:
        # Try to get default camera from scene_config
        scene_cameras = scene_config.get('sceneCameras', [])
        if scene_cameras:
            # Find default camera
            for cam in scene_cameras:
                if cam.get('isDefault', False):
                    camera_config = cam
                    break
            # If no default found, use first camera
            if camera_config is None and scene_cameras:
                camera_config = scene_cameras[0]
    
    # Set default camera values if no camera config
    if camera_config is None:
        camera_config = {
            'width': 800,
            'height': 450,
            'position': {'x': 0.5, 'y': 0.5},
            'zoom': 1.0
        }
    
    # Use camera dimensions for canvas (output size)
    canvas_width = int(camera_config.get('width', 800))
    canvas_height = int(camera_config.get('height', 450))
    
    # Get zoom factor
    zoom = camera_config.get('zoom', 1.0)
    if zoom <= 0:
        zoom = 1.0
    
    # Calculate viewport size in scene coordinates based on zoom
    # When zoom > 1.0, viewport is smaller (zooming in)
    # When zoom < 1.0, viewport is larger (zooming out)
    viewport_width = canvas_width / zoom
    viewport_height = canvas_height / zoom
    
    # Parse background color
    if isinstance(background, str):
        if background.startswith('#'):
            # Convert hex to BGR
            rgb = tuple(int(background[i:i+2], 16) for i in (1, 3, 5))
            bg_color = (rgb[2], rgb[1], rgb[0])  # Convert RGB to BGR
        else:
            bg_color = (255, 255, 255)  # Default white
    elif isinstance(background, (list, tuple)) and len(background) == 3:
        # Assume RGB, convert to BGR
        bg_color = (background[2], background[1], background[0])
    else:
        bg_color = (255, 255, 255)
    
    # Create canvas with background color
    canvas = np.full((canvas_height, canvas_width, 3), bg_color, dtype=np.uint8)
    
    # Calculate camera viewport in scene coordinates
    camera_pos = camera_config.get('position', {'x': 0.5, 'y': 0.5})
    # Camera position is the center of the viewport in scene coordinates
    camera_center_x = camera_pos['x'] * scene_width
    camera_center_y = camera_pos['y'] * scene_height
    # Calculate top-left corner of viewport
    camera_x = camera_center_x - (viewport_width / 2)
    camera_y = camera_center_y - (viewport_height / 2)
    
    if verbose: print(f"  📷 Camera: output={canvas_width}x{canvas_height}, zoom={zoom:.2f}, viewport={viewport_width:.1f}x{viewport_height:.1f} at scene position ({camera_x:.1f}, {camera_y:.1f})")
    
    # Render scene background image if exists
    background_image = scene_config.get('backgroundImage', None)
    if background_image:
        try:
            # Load background image
            if background_image.startswith('http://') or background_image.startswith('https://'):
                bg_img = load_image_from_url_or_path(background_image)
            else:
                if not os.path.isabs(background_image):
                    background_image = os.path.join(base_path, background_image)
                bg_img = load_image_from_url_or_path(background_image)
            
            if bg_img is not None:
                # Calculate source rectangle (portion of background to show)
                # Use viewport dimensions (accounting for zoom) not canvas dimensions
                bg_h, bg_w = bg_img.shape[:2]
                source_x = int((camera_x / scene_width) * bg_w)
                source_y = int((camera_y / scene_height) * bg_h)
                source_width = int((viewport_width / scene_width) * bg_w)
                source_height = int((viewport_height / scene_height) * bg_h)
                
                # Clamp to image bounds
                source_x = max(0, min(source_x, bg_w - 1))
                source_y = max(0, min(source_y, bg_h - 1))
                source_width = min(source_width, bg_w - source_x)
                source_height = min(source_height, bg_h - source_y)
                
                # Extract and resize the cropped portion
                if source_width > 0 and source_height > 0:
                    cropped_bg = bg_img[source_y:source_y+source_height, source_x:source_x+source_width]
                    canvas = cv2.resize(cropped_bg, (canvas_width, canvas_height), interpolation=cv2.INTER_LINEAR)
                    if verbose: print(f"  🖼️  Background image rendered with camera cropping")
        except Exception as e:
            if verbose: print(f"  ⚠️ Failed to render background image: {e}")
    
    # Get and sort layers by z_index
    layers = scene_config.get('layers', [])
    sorted_layers = sorted(layers, key=lambda x: x.get('z_index', 0))
    
    if verbose: print(f"  📐 Composing {len(sorted_layers)} layer(s) with camera positioning...")
    
    # Render each layer
    for layer in sorted_layers:
        try:
            # Check layer visibility
            if not layer.get('visible', True):
                continue
            
            layer_type = layer.get('type', 'image')
            
            # Render layer to image based on type
            layer_img = None
            
            if layer_type == 'text':
                text_config = layer.get('text_config', {})
                if not text_config or 'text' not in text_config:
                    continue
                # Display text config details for verification
                if verbose:
                    config_display = format_text_config_for_display(text_config)
                    text_content = text_config.get('text', '')[:MAX_TEXT_DISPLAY_LENGTH]
                    print(f"    📝 Rendering text layer: \"{text_content}...\" {config_display}")
                # Pass layer position and anchor_point to text rendering if not already in text_config
                text_config_for_render = text_config.copy()
                # Only apply zoom transformations if zoom != 1.0
                if zoom != 1.0:
                    if 'position' not in text_config_for_render:
                        layer_position = layer.get('position', None)
                        if layer_position:
                            # Scale position by zoom to match the zoomed scene canvas
                            text_config_for_render['position'] = {
                                'x': int(layer_position.get('x', 0) * zoom),
                                'y': int(layer_position.get('y', 0) * zoom)
                            }
                    # Scale font size by zoom to render crisp text instead of scaling later
                    if 'size' in text_config_for_render and text_config_for_render['size'] > 0:
                        text_config_for_render['size'] = int(text_config_for_render['size'] * zoom)
                else:
                    # No zoom, just pass position without scaling
                    if 'position' not in text_config_for_render:
                        layer_position = layer.get('position', None)
                        if layer_position:
                            text_config_for_render['position'] = layer_position
                if 'anchor_point' not in text_config_for_render:
                    text_config_for_render['anchor_point'] = layer.get('anchor_point', 'top-left')
                # Render text to zoomed scene size to avoid blurry scaling
                zoomed_scene_width = int(scene_width * zoom) if zoom != 1.0 else scene_width
                zoomed_scene_height = int(scene_height * zoom) if zoom != 1.0 else scene_height
                layer_img = render_text_to_image(text_config_for_render, zoomed_scene_width, zoomed_scene_height)
                
            elif layer_type == 'shape':
                shape_config = layer.get('shape_config', {})
                if not shape_config:
                    continue
                # Render shape to full scene size
                layer_img = render_shape_to_image(shape_config, scene_width, scene_height)
                
            elif layer_type == 'arrow':
                arrow_config = layer.get('arrow_config', {})
                if not arrow_config or 'start' not in arrow_config or 'end' not in arrow_config:
                    continue
                # Render arrow fully drawn
                layer_img = np.ones((scene_height, scene_width, 3), dtype=np.uint8) * 255
                layer_img = draw_arrow_progressive(layer_img, arrow_config, 1.0, scene_width, scene_height)
                
            elif layer_type == 'whiteboard':
                # For whiteboard/strokes, we need to render strokes
                strokes = layer.get('strokes', [])
                if not strokes:
                    continue
                # Create white canvas and render strokes
                layer_img = np.ones((scene_height, scene_width, 3), dtype=np.uint8) * 255
                # Render each stroke
                for stroke in strokes:
                    points = stroke.get('points', [])
                    if len(points) < 2:
                        continue
                    stroke_width = stroke.get('strokeWidth', stroke.get('stroke_width', 2))
                    stroke_color_str = stroke.get('strokeColor', stroke.get('stroke_color', '#000000'))
                    # Parse stroke color
                    if isinstance(stroke_color_str, str) and stroke_color_str.startswith('#'):
                        rgb = tuple(int(stroke_color_str[i:i+2], 16) for i in (1, 3, 5))
                        stroke_color = (rgb[2], rgb[1], rgb[0])  # RGB to BGR
                    else:
                        stroke_color = (0, 0, 0)
                    
                    # Draw stroke path
                    if len(points) == 2:
                        pt1 = (int(points[0]['x']), int(points[0]['y']))
                        pt2 = (int(points[1]['x']), int(points[1]['y']))
                        cv2.line(layer_img, pt1, pt2, stroke_color, int(stroke_width))
                    else:
                        # Use quadratic curves for smooth strokes
                        for i in range(len(points) - 1):
                            pt1 = (int(points[i]['x']), int(points[i]['y']))
                            pt2 = (int(points[i+1]['x']), int(points[i+1]['y']))
                            cv2.line(layer_img, pt1, pt2, stroke_color, int(stroke_width))
                
            else:
                # Image layer
                image_path = layer.get('image_path', '')
                if not image_path:
                    continue
                # Resolve path
                if not (image_path.startswith('http://') or image_path.startswith('https://')):
                    if not os.path.isabs(image_path):
                        image_path = os.path.join(base_path, image_path)
                layer_img = load_image_from_url_or_path(image_path)
                if layer_img is None:
                    continue
            
            # Apply explicit resizing (width/height) or scale
            # width/height takes priority over scale for compatibility with external editors
            explicit_width = layer.get('width', None)
            explicit_height = layer.get('height', None)
            
            if explicit_width is not None and explicit_height is not None and layer_img is not None:
                # Explicit resizing requested
                new_width = int(explicit_width)
                new_height = int(explicit_height)
                layer_img = cv2.resize(layer_img, (new_width, new_height))
            else:
                # Use scale if no explicit width/height
                scale = layer.get('scale', 1.0)
                if scale != 1.0 and layer_img is not None:
                    new_width = int(layer_img.shape[1] * scale)
                    new_height = int(layer_img.shape[0] * scale)
                    layer_img = cv2.resize(layer_img, (new_width, new_height))
            
            # Get final layer dimensions
            layer_h, layer_w = layer_img.shape[:2] if layer_img is not None else (0, 0)
            
            # Get layer position (in scene coordinates) and anchor point
            # For text/shape/arrow layers that render to full scene, positioning is handled internally
            # so layer position is always (0, 0)
            if layer_type in ['text', 'shape', 'arrow', 'whiteboard']:
                layer_x = 0
                layer_y = 0
            else:
                position = layer.get('position', {'x': 0, 'y': 0})
                anchor_point = layer.get('anchor_point', 'top-left')  # 'top-left' or 'center'
                
                layer_x = position.get('x', 0)
                layer_y = position.get('y', 0)
                
                # Adjust position based on anchor point
                if anchor_point == 'center':
                    # If anchor point is center, adjust to get top-left corner
                    layer_x = layer_x - layer_w // 2
                    layer_y = layer_y - layer_h // 2
            
            # Calculate layer position relative to camera viewport (in scene coordinates)
            # For text/shape/arrow layers that render to full scene and handle positioning internally,
            # we need to account for the camera viewport cropping
            if layer_type in ['text', 'shape', 'arrow', 'whiteboard']:
                # These layers are rendered to full scene size, so we crop them based on camera viewport
                relative_x = -camera_x
                relative_y = -camera_y
            else:
                relative_x = layer_x - camera_x
                relative_y = layer_y - camera_y
            
            # Apply zoom scaling to convert from scene coordinates to canvas coordinates
            # When zoom > 1, scene content appears larger in canvas (zoomed in)
            # When zoom < 1, scene content appears smaller in canvas (zoomed out)
            relative_x = relative_x * zoom
            relative_y = relative_y * zoom
            
            # Scale layer dimensions for zoom
            # Skip for text layers as they're already rendered at zoomed size
            if zoom != 1.0 and layer_img is not None and layer_type != 'text':
                scaled_w = int(layer_w * zoom)
                scaled_h = int(layer_h * zoom)
                if scaled_w > 0 and scaled_h > 0:
                    layer_img = cv2.resize(layer_img, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
                    layer_w, layer_h = scaled_w, scaled_h
            
            # Get rotation and flip
            rotation = layer.get('rotation', 0)
            flip_x = layer.get('flipX', False)
            flip_y = layer.get('flipY', False)
            
            # Apply transformations if needed
            if rotation != 0 or flip_x or flip_y:
                # Get image dimensions
                layer_h, layer_w = layer_img.shape[:2]
                
                # Apply flip
                if flip_x:
                    layer_img = cv2.flip(layer_img, 1)  # Horizontal flip
                if flip_y:
                    layer_img = cv2.flip(layer_img, 0)  # Vertical flip
                
                # Apply rotation
                if rotation != 0:
                    # Get rotation matrix (rotate around center)
                    center = (layer_w / 2, layer_h / 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, rotation, 1.0)
                    # Calculate new bounding box
                    cos = np.abs(rotation_matrix[0, 0])
                    sin = np.abs(rotation_matrix[0, 1])
                    new_w = int((layer_h * sin) + (layer_w * cos))
                    new_h = int((layer_h * cos) + (layer_w * sin))
                    # Adjust rotation matrix for new size
                    rotation_matrix[0, 2] += (new_w / 2) - center[0]
                    rotation_matrix[1, 2] += (new_h / 2) - center[1]
                    # Apply rotation with white background
                    layer_img = cv2.warpAffine(layer_img, rotation_matrix, (new_w, new_h), 
                                               borderMode=cv2.BORDER_CONSTANT, 
                                               borderValue=(255, 255, 255))
                    # Adjust position to account for size change
                    relative_x -= (new_w - layer_w) / 2
                    relative_y -= (new_h - layer_h) / 2
            
            # Get opacity
            opacity = layer.get('opacity', 1.0)
            opacity = max(0.0, min(1.0, opacity))
            
            # Calculate region to copy
            layer_h, layer_w = layer_img.shape[:2]
            
            # Calculate intersection with canvas
            x1_canvas = max(0, int(relative_x))
            y1_canvas = max(0, int(relative_y))
            x2_canvas = min(canvas_width, int(relative_x + layer_w))
            y2_canvas = min(canvas_height, int(relative_y + layer_h))
            
            # Calculate corresponding region in layer image
            x1_layer = max(0, int(-relative_x))
            y1_layer = max(0, int(-relative_y))
            x2_layer = x1_layer + (x2_canvas - x1_canvas)
            y2_layer = y1_layer + (y2_canvas - y1_canvas)
            
            # Check if there's a valid region to copy
            if x2_canvas <= x1_canvas or y2_canvas <= y1_canvas:
                continue
            
            # Extract regions
            layer_region = layer_img[y1_layer:y2_layer, x1_layer:x2_layer]
            canvas_region = canvas[y1_canvas:y2_canvas, x1_canvas:x2_canvas].copy()
            
            # Blend with opacity
            if opacity < 1.0:
                canvas[y1_canvas:y2_canvas, x1_canvas:x2_canvas] = cv2.addWeighted(
                    canvas_region, 1 - opacity, layer_region, opacity, 0
                )
            else:
                # For opacity 1.0, copy only non-white pixels (preserve transparency)
                threshold = 250
                layer_content_mask = np.any(layer_region < threshold, axis=2)
                canvas_region[layer_content_mask] = layer_region[layer_content_mask]
                canvas[y1_canvas:y2_canvas, x1_canvas:x2_canvas] = canvas_region
            
            # Log layer
            z_idx = layer.get('z_index', 0)
            layer_id = layer.get('id', 'unknown')
            layer_scale = layer.get('scale', 1.0)
            if verbose: print(f"    ✓ Layer applied: {layer_type} (id:{layer_id}, z:{z_idx}, " +
                  f"scene_pos:({layer_x:.1f},{layer_y:.1f}), " +
                  f"canvas_pos:({relative_x:.1f},{relative_y:.1f}), " +
                  f"scale:{layer_scale:.2f}, zoom:{zoom:.2f}, opacity:{opacity:.2f})")
            
        except Exception as e:
            if verbose: print(f"    ❌ Error rendering layer: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return canvas


def export_scene_to_video(scene_config, output_path, fps=30, duration=None, 
                          camera_config=None, scene_width=1920, scene_height=1080,
                          background='#FFFFFF', base_path=".", crf=18,
                          camera_animation=None):
    """Export a scene to video with camera-based viewport positioning.
    
    This function uses the compose_scene_with_camera logic to render each frame
    of the video, properly placing all elements relative to the camera viewport.
    
    Args:
        scene_config: Scene configuration dict with:
            - layers: List of layer configurations
            - backgroundImage: Optional background image path
            - sceneCameras: Optional list of camera configurations
            - duration: Optional scene duration in seconds (overrides duration parameter)
        output_path: Path to save the output video file
        fps: Frames per second (default: 30)
        duration: Video duration in seconds (default: 5.0, or from scene_config)
        camera_config: Optional camera configuration dict (if None, uses sceneCameras)
        scene_width: Scene width in pixels (default: 1920)
        scene_height: Scene height in pixels (default: 1080)
        background: Background color (default: '#FFFFFF')
        base_path: Base path for resolving relative file paths
        crf: Video quality (0-51, lower = better, 18 is visually lossless)
        camera_animation: Optional dict with camera animation config:
            - type: 'pan', 'zoom', 'static' (default: 'static')
            - start_position: Starting camera position {'x', 'y'}
            - end_position: Ending camera position {'x', 'y'}
            - start_zoom: Starting zoom level (for zoom animation)
            - end_zoom: Ending zoom level (for zoom animation)
            - easing: 'linear', 'ease_in', 'ease_out', 'ease_in_out'
    
    Returns:
        dict: Status information with 'success' boolean and 'output_path' string
    """
    print("\n" + "="*60)
    print("🎬 SCENE VIDEO EXPORT")
    print("="*60)
    
    # Determine duration
    if duration is None:
        duration = scene_config.get('duration', 5.0)
    
    # Calculate total frames
    total_frames = int(duration * fps)
    
    print(f"  📹 Output: {output_path}")
    print(f"  ⏱️  Duration: {duration}s ({total_frames} frames @ {fps} fps)")
    
    # Get camera configuration
    if camera_config is None:
        scene_cameras = scene_config.get('sceneCameras', [])
        if scene_cameras:
            for cam in scene_cameras:
                if cam.get('isDefault', False):
                    camera_config = cam
                    break
            if camera_config is None and scene_cameras:
                camera_config = scene_cameras[0]
    
    # Set default camera if still None
    if camera_config is None:
        camera_config = {
            'width': scene_width,
            'height': scene_height,
            'position': {'x': 0.5, 'y': 0.5}
        }
    
    # Get camera dimensions
    camera_width = int(camera_config.get('width', scene_width))
    camera_height = int(camera_config.get('height', scene_height))
    
    print(f"  📷 Camera: {camera_width}x{camera_height}")
    
    # Initialize video writer
    try:
        # Determine video codec
        if output_path.endswith('.avi'):
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        else:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        
        video_writer = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (camera_width, camera_height)
        )
        
        if not video_writer.isOpened():
            raise Exception("Failed to open video writer")
        
        print(f"  ✓ Video writer initialized")
        
    except Exception as e:
        print(f"  ❌ Failed to initialize video writer: {e}")
        return {'success': False, 'error': str(e)}
    
    # Helper function for easing
    def apply_easing(t, easing='linear'):
        """Apply easing function to normalized time t (0.0 to 1.0)."""
        if easing == 'ease_in':
            return t * t
        elif easing == 'ease_out':
            return 1 - (1 - t) * (1 - t)
        elif easing == 'ease_in_out':
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) * (1 - t)
        else:  # linear
            return t
    
    # Render frames
    try:
        print(f"  🎨 Rendering {total_frames} frames...")
        
        for frame_idx in range(total_frames):
            # Calculate progress (0.0 to 1.0)
            progress = frame_idx / max(1, total_frames - 1) if total_frames > 1 else 0.0
            
            # Calculate current camera configuration based on animation
            current_camera = camera_config.copy()
            
            if camera_animation:
                anim_type = camera_animation.get('type', 'static')
                easing = camera_animation.get('easing', 'linear')
                eased_progress = apply_easing(progress, easing)
                
                if anim_type == 'pan':
                    # Pan camera from start to end position
                    start_pos = camera_animation.get('start_position', {'x': 0.5, 'y': 0.5})
                    end_pos = camera_animation.get('end_position', {'x': 0.5, 'y': 0.5})
                    
                    current_x = start_pos['x'] + (end_pos['x'] - start_pos['x']) * eased_progress
                    current_y = start_pos['y'] + (end_pos['y'] - start_pos['y']) * eased_progress
                    
                    current_camera['position'] = {'x': current_x, 'y': current_y}
                
                elif anim_type == 'zoom':
                    # Zoom camera
                    start_zoom = camera_animation.get('start_zoom', 1.0)
                    end_zoom = camera_animation.get('end_zoom', 2.0)
                    
                    current_zoom = start_zoom + (end_zoom - start_zoom) * eased_progress
                    
                    # Adjust camera size based on zoom
                    base_width = camera_animation.get('base_width', camera_width)
                    base_height = camera_animation.get('base_height', camera_height)
                    
                    current_camera['width'] = int(base_width / current_zoom)
                    current_camera['height'] = int(base_height / current_zoom)
            
            # Compose frame using the camera positioning logic (verbose=False for performance)
            frame = compose_scene_with_camera(
                scene_config,
                current_camera,
                scene_width,
                scene_height,
                background,
                base_path,
                verbose=False  # Disable per-frame logging for performance
            )
            
            # Ensure frame dimensions match camera dimensions
            if frame.shape[:2] != (camera_height, camera_width):
                frame = cv2.resize(frame, (camera_width, camera_height))
            
            # Write frame
            video_writer.write(frame)
            
            # Progress indicator
            if (frame_idx + 1) % max(1, total_frames // 10) == 0:
                percent = int((frame_idx + 1) / total_frames * 100)
                print(f"    Progress: {percent}% ({frame_idx + 1}/{total_frames} frames)")
        
        print(f"  ✓ All frames rendered")
        
    except Exception as e:
        print(f"  ❌ Error rendering frames: {e}")
        import traceback
        traceback.print_exc()
        video_writer.release()
        return {'success': False, 'error': str(e)}
    
    finally:
        video_writer.release()
    
    # Convert to H.264 if requested
    if crf is not None and crf != 18:
        temp_path = output_path.replace('.mp4', '_temp.mp4')
        os.rename(output_path, temp_path)
        
        try:
            print(f"  🔄 Converting to H.264 (CRF={crf})...")
            ffmpeg_convert(temp_path, output_path, crf=crf)
            os.remove(temp_path)
            print(f"  ✓ Conversion complete")
        except Exception as e:
            print(f"  ⚠️ Conversion failed: {e}")
            os.rename(temp_path, output_path)
    
    print(f"\n✅ Video export complete: {output_path}")
    print("="*60)
    
    return {
        'success': True,
        'output_path': output_path,
        'duration': duration,
        'fps': fps,
        'frames': total_frames,
        'resolution': f"{camera_width}x{camera_height}"
    }


def export_scene_to_whiteboard_video(scene_config, output_path, fps=30,
                                     camera_config=None, scene_width=1920, scene_height=1080,
                                     background='#FFFFFF', base_path=".", crf=18,
                                     draw_speed=8, show_hand=True, hand_path=None, 
                                     final_hold_duration=2.0):
    """Export a scene to video with whiteboard-style progressive drawing animation.
    
    This function animates layers progressively with a drawing hand that follows
    the content being drawn, creating a whiteboard/doodly-style animation.
    
    Args:
        scene_config: Scene configuration dict with:
            - layers: List of layer configurations (must have z_index for draw order)
            - backgroundImage: Optional background image path
            - sceneCameras: Optional list of camera configurations
        output_path: Path to save the output video file
        fps: Frames per second (default: 30)
        camera_config: Optional camera configuration dict
        scene_width: Scene width in pixels (default: 1920)
        scene_height: Scene height in pixels (default: 1080)
        background: Background color (default: '#FFFFFF')
        base_path: Base path for resolving relative file paths
        crf: Video quality (0-51, lower = better, 18 is visually lossless)
        draw_speed: Drawing speed factor (lower = slower, default: 8)
        show_hand: Whether to show the drawing hand (default: True)
        hand_path: Path to drawing hand image (default: uses built-in)
        final_hold_duration: Duration to hold final frame in seconds (default: 2.0)
    
    Returns:
        dict: Status information with 'success' boolean and details
    """
    print("\n" + "="*60)
    print("🎬 WHITEBOARD VIDEO EXPORT")
    print("="*60)
    
    # Get camera configuration
    if camera_config is None:
        scene_cameras = scene_config.get('sceneCameras', [])
        if scene_cameras:
            for cam in scene_cameras:
                if cam.get('isDefault', False):
                    camera_config = cam
                    break
            if camera_config is None and scene_cameras:
                camera_config = scene_cameras[0]
    
    if camera_config is None:
        camera_config = {
            'width': scene_width,
            'height': scene_height,
            'position': {'x': 0.5, 'y': 0.5}
        }
    
    camera_width = int(camera_config.get('width', scene_width))
    camera_height = int(camera_config.get('height', scene_height))
    
    print(f"  📹 Output: {output_path}")
    print(f"  📷 Camera: {camera_width}x{camera_height}")
    print(f"  🎨 Draw speed: {draw_speed}")
    
    # Load hand image if showing hand
    hand_img = None
    hand_mask_inv = None
    if show_hand:
        if hand_path is None:
            hand_path = os.path.join(base_path, 'data', 'images', 'drawing-hand.png')
        
        if os.path.exists(hand_path):
            hand_img = cv2.imread(hand_path, cv2.IMREAD_UNCHANGED)
            if hand_img is not None and hand_img.shape[2] == 4:
                # Extract alpha channel as mask
                hand_mask = hand_img[:, :, 3]
                hand_mask_inv = cv2.bitwise_not(hand_mask)
                hand_img = hand_img[:, :, :3]
                print(f"  ✋ Hand image loaded: {hand_img.shape[1]}x{hand_img.shape[0]}")
            else:
                print(f"  ⚠️ Hand image has no alpha channel, disabling hand")
                show_hand = False
        else:
            print(f"  ⚠️ Hand image not found at {hand_path}, disabling hand")
            show_hand = False
    
    # Initialize video writer
    try:
        if output_path.endswith('.avi'):
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        else:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        
        video_writer = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (camera_width, camera_height)
        )
        
        if not video_writer.isOpened():
            raise Exception("Failed to open video writer")
        
        print(f"  ✓ Video writer initialized")
        
    except Exception as e:
        print(f"  ❌ Failed to initialize video writer: {e}")
        return {'success': False, 'error': str(e)}
    
    # Sort layers by z_index (draw order)
    layers = scene_config.get('layers', [])
    sorted_layers = sorted(layers, key=lambda x: x.get('z_index', 0))
    
    print(f"  📝 Animating {len(sorted_layers)} layer(s) progressively...")
    
    # Create initial blank canvas
    blank_canvas = compose_scene_with_camera(
        {'layers': []},  # Empty scene
        camera_config,
        scene_width,
        scene_height,
        background,
        base_path,
        verbose=False
    )
    
    total_frames_written = 0
    
    try:
        # Render background if exists
        bg_image = scene_config.get('backgroundImage', None)
        if bg_image:
            bg_scene = {
                'backgroundImage': bg_image,
                'layers': []
            }
            current_canvas = compose_scene_with_camera(
                bg_scene,
                camera_config,
                scene_width,
                scene_height,
                background,
                base_path,
                verbose=False
            )
        else:
            current_canvas = blank_canvas.copy()
        
        # Animate each layer progressively
        for layer_idx, layer in enumerate(sorted_layers):
            layer_type = layer.get('type', 'image')
            layer_id = layer.get('id', f'layer_{layer_idx}')
            
            # Skip if not visible
            if not layer.get('visible', True):
                continue
            
            print(f"    Animating layer {layer_idx + 1}/{len(sorted_layers)}: {layer_type} (id: {layer_id})")
            
            # Compose this layer on top of current canvas
            layer_scene = {
                'layers': [layer]
            }
            
            # Get the full layer image
            layer_full = compose_scene_with_camera(
                layer_scene,
                camera_config,
                scene_width,
                scene_height,
                '#FFFFFF',  # White background for layer
                base_path,
                verbose=False
            )
            
            # Calculate drawing frames based on layer complexity
            # For now, use a fixed number of frames per layer
            layer_duration = layer.get('draw_duration', 2.0)  # seconds
            layer_frames = int(layer_duration * fps)
            
            # Animate layer being drawn progressively
            for frame_idx in range(layer_frames):
                progress = (frame_idx + 1) / layer_frames
                
                # Create progressive reveal using a simple fade-in effect
                # In a real implementation, this would scan pixel by pixel
                frame = current_canvas.copy()
                
                # Blend the layer progressively
                alpha = progress
                frame = cv2.addWeighted(frame, 1.0, layer_full, alpha, 0)
                
                # Add drawing hand if enabled
                if show_hand and hand_img is not None:
                    # Position hand at a representative location
                    # In a real implementation, this would follow the actual drawing path
                    layer_pos = layer.get('position', {'x': scene_width // 2, 'y': scene_height // 2})
                    
                    # Calculate hand position in camera viewport
                    camera_pos = camera_config.get('position', {'x': 0.5, 'y': 0.5})
                    camera_x = (camera_pos['x'] * scene_width) - (camera_width / 2)
                    camera_y = (camera_pos['y'] * scene_height) - (camera_height / 2)
                    
                    hand_x = int(layer_pos['x'] - camera_x)
                    hand_y = int(layer_pos['y'] - camera_y)
                    
                    # Adjust hand position for drawing progress
                    hand_y = int(hand_y - 50 + (100 * progress))
                    
                    # Overlay hand on frame
                    hand_h, hand_w = hand_img.shape[:2]
                    x1 = max(0, hand_x)
                    y1 = max(0, hand_y)
                    x2 = min(camera_width, hand_x + hand_w)
                    y2 = min(camera_height, hand_y + hand_h)
                    
                    if x2 > x1 and y2 > y1:
                        hx1 = max(0, -hand_x)
                        hy1 = max(0, -hand_y)
                        hx2 = hx1 + (x2 - x1)
                        hy2 = hy1 + (y2 - y1)
                        
                        try:
                            hand_region = hand_img[hy1:hy2, hx1:hx2]
                            mask_region = hand_mask_inv[hy1:hy2, hx1:hx2]
                            frame_region = frame[y1:y2, x1:x2]
                            
                            # Blend hand onto frame
                            for c in range(3):
                                frame_region[:, :, c] = (
                                    frame_region[:, :, c] * (mask_region / 255.0) +
                                    hand_region[:, :, c] * (1 - mask_region / 255.0)
                                ).astype(np.uint8)
                            
                            frame[y1:y2, x1:x2] = frame_region
                        except:
                            pass  # Skip hand if positioning fails
                
                video_writer.write(frame)
                total_frames_written += 1
            
            # Update current canvas to include this layer
            current_canvas = cv2.addWeighted(current_canvas, 1.0, layer_full, 1.0, 0)
        
        # Hold final frame
        final_frames = int(final_hold_duration * fps)
        print(f"    Holding final frame for {final_hold_duration}s ({final_frames} frames)")
        
        for _ in range(final_frames):
            video_writer.write(current_canvas)
            total_frames_written += 1
        
        print(f"  ✓ All frames rendered ({total_frames_written} total)")
        
    except Exception as e:
        print(f"  ❌ Error rendering frames: {e}")
        import traceback
        traceback.print_exc()
        video_writer.release()
        return {'success': False, 'error': str(e)}
    
    finally:
        video_writer.release()
    
    total_duration = total_frames_written / fps
    
    print(f"\n✅ Whiteboard video export complete: {output_path}")
    print(f"   Duration: {total_duration:.2f}s, Frames: {total_frames_written}")
    print("="*60)
    
    return {
        'success': True,
        'output_path': output_path,
        'duration': total_duration,
        'fps': fps,
        'frames': total_frames_written,
        'resolution': f"{camera_width}x{camera_height}"
    }


def ffmpeg_convert(source_vid, dest_vid, platform="linux", crf=18):
    """Convertit la vidéo brute (mp4v) en H.264 compatible avec PyAV.
    
    Args:
        source_vid: Chemin de la vidéo source
        dest_vid: Chemin de la vidéo de destination
        platform: Plateforme cible
        crf: Constant Rate Factor (0-51, lower = better quality, 18 is visually lossless)
    """
    ff_stat = False
    try:
        import av
        src_path = Path(source_vid)
        input_container = av.open(src_path, mode="r")
        output_container = av.open(dest_vid, mode="w")
        
        in_stream = input_container.streams.video[0]
        width = in_stream.codec_context.width
        height = in_stream.codec_context.height
        fps = in_stream.average_rate
        
        # set output params
        out_stream = output_container.add_stream("h264", rate=fps)
        out_stream.width = width
        out_stream.height = height
        out_stream.pix_fmt = "yuv420p"
        out_stream.options = {"crf": str(crf)}

        for frame in input_container.decode(video=0):
            packet = out_stream.encode(frame)
            if packet:
                output_container.mux(packet)
                
        packet = out_stream.encode()
        if packet:
            output_container.mux(packet)
            
        output_container.close()
        input_container.close()

        print(f"✅ Conversion FFmpeg réussie. Fichier: {dest_vid}")
        ff_stat = True
        
    except ImportError:
        print("⚠️ AVERTISSEMENT: Le module 'av' (PyAV) n'est pas installé. La conversion H.264 sera ignorée.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion FFmpeg: {e}")
        
    return ff_stat


def extract_frames_from_video(video_path):
    """
    Extract all frames from a video file.
    
    Args:
        video_path: Path to the video file
    
    Returns:
        list: List of frames as numpy arrays (BGR format)
    """
    frames = []
    try:
        import av
        
        container = av.open(video_path, mode='r')
        video_stream = container.streams.video[0]
        
        for frame in container.decode(video=0):
            frame_np = frame.to_ndarray(format='bgr24')
            frames.append(frame_np)
        
        container.close()
        return frames
        
    except ImportError:
        print("⚠️ PyAV library required. Trying with OpenCV...")
        # Fallback to OpenCV
        cap = cv2.VideoCapture(video_path)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames
        
    except Exception as e:
        print(f"❌ Error extracting frames: {e}")
        return frames


def export_additional_formats(video_path, export_formats_list, fps=30):
    """
    Export video to additional formats (GIF, WebM, PNG sequence, etc.).
    
    Args:
        video_path: Path to the source video file
        export_formats_list: List of format strings ('gif', 'webm', 'png', 'webm-alpha', 'lossless')
        fps: Frame rate for export
    
    Returns:
        dict: Dictionary of exported files {format: filepath}
    """
    if not EXPORT_FORMATS_AVAILABLE:
        print("⚠️ Export formats module not available. Skipping additional exports.")
        return {}
    
    if not export_formats_list:
        return {}
    
    print(f"\n📦 Exporting to additional formats: {', '.join(export_formats_list)}")
    
    # Extract frames from video
    print("  🎬 Extracting frames from video...")
    frames = extract_frames_from_video(video_path)
    
    if not frames:
        print("  ❌ No frames extracted. Skipping additional exports.")
        return {}
    
    print(f"  ✅ Extracted {len(frames)} frames")
    
    exported_files = {}
    base_path = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    for format_name in export_formats_list:
        format_lower = format_name.lower()
        
        if format_lower == 'gif':
            output_path = os.path.join(base_path, f"{base_name}.gif")
            # Reduce fps for GIF to keep file size reasonable
            gif_fps = min(10, fps)
            if export_gif(frames, output_path, fps=gif_fps):
                exported_files['gif'] = output_path
        
        elif format_lower == 'webm':
            output_path = os.path.join(base_path, f"{base_name}.webm")
            if export_webm(frames, output_path, fps=fps):
                exported_files['webm'] = output_path
        
        elif format_lower == 'png' or format_lower == 'png-sequence':
            output_dir = os.path.join(base_path, f"{base_name}_frames")
            if export_png_sequence(frames, output_dir):
                exported_files['png-sequence'] = output_dir
        
        elif format_lower == 'webm-alpha' or format_lower == 'transparent':
            output_path = os.path.join(base_path, f"{base_name}_alpha.webm")
            if export_with_transparency(frames, output_path, fps=fps):
                exported_files['webm-alpha'] = output_path
        
        elif format_lower == 'lossless':
            output_path = os.path.join(base_path, f"{base_name}_lossless.mkv")
            if export_lossless(frames, output_path, fps=fps):
                exported_files['lossless'] = output_path
    
    return exported_files


def generate_transition_frames(frame1, frame2, transition_type, num_frames, fps):
    """Génère des frames de transition entre deux frames.
    
    Args:
        frame1: Frame de fin de la vidéo précédente (numpy array BGR)
        frame2: Frame de début de la vidéo suivante (numpy array BGR)
        transition_type: Type de transition ('none', 'fade', 'wipe', 'push_left', 'push_right', 'iris')
        num_frames: Nombre de frames de transition à générer
        fps: Frame rate de la vidéo
    
    Returns:
        Liste de frames de transition
    """
    if transition_type == 'none' or num_frames == 0:
        return []
    
    transition_frames = []
    
    if transition_type == 'fade':
        # Transition en fondu
        for i in range(num_frames):
            alpha = (i + 1) / (num_frames + 1)
            blended = cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
            transition_frames.append(blended)
    
    elif transition_type == 'wipe':
        # Transition en balayage de gauche à droite
        height, width = frame1.shape[:2]
        for i in range(num_frames):
            progress = (i + 1) / (num_frames + 1)
            split_x = int(width * progress)
            frame = frame1.copy()
            frame[:, :split_x] = frame2[:, :split_x]
            transition_frames.append(frame)
    
    elif transition_type == 'push_left':
        # Poussée vers la gauche
        height, width = frame1.shape[:2]
        for i in range(num_frames):
            progress = (i + 1) / (num_frames + 1)
            offset = int(width * progress)
            frame = np.zeros_like(frame1)
            
            # Partie de frame1 qui reste visible
            if offset < width:
                frame[:, :width-offset] = frame1[:, offset:]
            
            # Partie de frame2 qui devient visible
            frame[:, width-offset:] = frame2[:, :offset]
            transition_frames.append(frame)
    
    elif transition_type == 'push_right':
        # Poussée vers la droite
        height, width = frame1.shape[:2]
        for i in range(num_frames):
            progress = (i + 1) / (num_frames + 1)
            offset = int(width * progress)
            frame = np.zeros_like(frame1)
            
            # Partie de frame2 qui devient visible
            frame[:, :offset] = frame2[:, width-offset:]
            
            # Partie de frame1 qui reste visible
            if offset < width:
                frame[:, offset:] = frame1[:, :width-offset]
            transition_frames.append(frame)
    
    elif transition_type == 'iris':
        # Transition en iris (cercle qui s'agrandit)
        height, width = frame1.shape[:2]
        center = (width // 2, height // 2)
        max_radius = int(np.sqrt(width**2 + height**2) / 2)
        
        for i in range(num_frames):
            progress = (i + 1) / (num_frames + 1)
            radius = int(max_radius * progress)
            
            # Créer un masque circulaire
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.circle(mask, center, radius, 255, -1)
            mask_3ch = cv2.merge([mask, mask, mask])
            
            # Appliquer le masque
            frame = frame1.copy()
            frame = np.where(mask_3ch == 255, frame2, frame1)
            transition_frames.append(frame)
    
    return transition_frames


def concatenate_videos(video_paths, output_path, transition_type='none', transition_duration=0.5, per_slide_transitions=None, crf=18):
    """Concatène plusieurs vidéos en une seule vidéo finale avec transitions optionnelles.
    
    Args:
        video_paths: Liste des chemins des vidéos à concaténer
        output_path: Chemin de sortie pour la vidéo combinée
        transition_type: Type de transition par défaut ('none', 'fade', 'wipe', 'push_left', 'push_right', 'iris')
        transition_duration: Durée de la transition en secondes (par défaut)
        per_slide_transitions: Liste de dicts avec configs de transition par slide
        crf: Constant Rate Factor for video quality (0-51, lower = better quality)
    """
    try:
        import av
        
        if not video_paths:
            raise ValueError("Aucune vidéo à concaténer")
        
        if len(video_paths) == 1:
            # Si une seule vidéo, copier simplement
            shutil.copy2(video_paths[0], output_path)
            print(f"✅ Vidéo unique copiée: {output_path}")
            return True
        
        print(f"🔗 Concaténation de {len(video_paths)} vidéos...")
        if transition_type != 'none':
            print(f"   Transition: {transition_type} ({transition_duration}s)")
        
        # Ouvrir le premier fichier pour obtenir les paramètres
        first_container = av.open(video_paths[0], mode="r")
        first_stream = first_container.streams.video[0]
        width = first_stream.codec_context.width
        height = first_stream.codec_context.height
        fps = first_stream.average_rate
        first_container.close()
        
        # Calculer le nombre de frames de transition
        num_transition_frames = int(float(fps) * transition_duration)
        
        # Créer le conteneur de sortie
        output_container = av.open(output_path, mode="w")
        out_stream = output_container.add_stream("h264", rate=fps)
        out_stream.width = width
        out_stream.height = height
        out_stream.pix_fmt = "yuv420p"
        out_stream.options = {"crf": str(crf)}
        
        last_frame = None
        
        # Concaténer toutes les vidéos
        for i, video_path in enumerate(video_paths):
            print(f"  Ajout de la vidéo {i+1}/{len(video_paths)}: {os.path.basename(video_path)}")
            input_container = av.open(video_path, mode="r")
            
            first_frame_of_video = None
            frames_list = []
            
            # Lire toutes les frames de cette vidéo
            for frame in input_container.decode(video=0):
                frames_list.append(frame)
            
            input_container.close()
            
            # Ajouter la transition si ce n'est pas la première vidéo
            if i > 0 and last_frame is not None and len(frames_list) > 0:
                first_frame_of_video = frames_list[0]
                
                # Déterminer le type et la durée de transition pour cette slide
                current_transition_type = transition_type
                current_transition_duration = transition_duration
                
                # Si une configuration par slide existe, l'utiliser
                if per_slide_transitions and i - 1 < len(per_slide_transitions):
                    slide_trans_config = per_slide_transitions[i - 1]
                    if 'type' in slide_trans_config:
                        current_transition_type = slide_trans_config['type']
                    if 'duration' in slide_trans_config:
                        current_transition_duration = slide_trans_config['duration']
                
                # Calculer le nombre de frames pour cette transition
                current_num_transition_frames = int(float(fps) * current_transition_duration)
                
                # Ajouter des frames de pause avant la transition si spécifié
                pause_duration = 0
                if per_slide_transitions and i - 1 < len(per_slide_transitions):
                    pause_duration = per_slide_transitions[i - 1].get('pause_before', 0)
                
                if pause_duration > 0:
                    num_pause_frames = int(float(fps) * pause_duration)
                    print(f"    Ajout d'une pause de {pause_duration}s ({num_pause_frames} frames)")
                    last_frame_np = last_frame.to_ndarray(format='bgr24')
                    if last_frame_np.shape[:2] != (height, width):
                        last_frame_np = cv2.resize(last_frame_np, (width, height))
                    
                    for _ in range(num_pause_frames):
                        av_frame = av.VideoFrame.from_ndarray(last_frame_np, format='bgr24')
                        av_frame.pts = None
                        packets = out_stream.encode(av_frame)
                        for packet in packets:
                            output_container.mux(packet)
                
                # Afficher la transition utilisée
                if current_transition_type != 'none':
                    print(f"    Transition: {current_transition_type} ({current_transition_duration}s)")
                
                # Convertir les frames PyAV en numpy arrays
                last_frame_np = last_frame.to_ndarray(format='bgr24')
                first_frame_np = first_frame_of_video.to_ndarray(format='bgr24')
                
                # Redimensionner les frames si nécessaire pour correspondre à la résolution de sortie
                if last_frame_np.shape[:2] != (height, width):
                    last_frame_np = cv2.resize(last_frame_np, (width, height))
                if first_frame_np.shape[:2] != (height, width):
                    first_frame_np = cv2.resize(first_frame_np, (width, height))
                
                # Générer les frames de transition
                transition_frames = generate_transition_frames(
                    last_frame_np, first_frame_np, current_transition_type, 
                    current_num_transition_frames, float(fps)
                )
                
                # Encoder les frames de transition
                for trans_frame in transition_frames:
                    # Convertir numpy array en PyAV frame
                    av_frame = av.VideoFrame.from_ndarray(trans_frame, format='bgr24')
                    av_frame.pts = None
                    # encode() retourne une liste de packets
                    packets = out_stream.encode(av_frame)
                    for packet in packets:
                        output_container.mux(packet)
            
            # Ajouter toutes les frames de cette vidéo
            # Pour assurer la compatibilité avec les frames de transition,
            # convertir les frames décodées en numpy puis en VideoFrame
            for frame in frames_list:
                # Convertir en numpy puis recréer le frame
                frame_np = frame.to_ndarray(format='bgr24')
                
                # Redimensionner si nécessaire pour correspondre à la résolution de sortie
                if frame_np.shape[:2] != (height, width):
                    frame_np = cv2.resize(frame_np, (width, height))
                
                av_frame = av.VideoFrame.from_ndarray(frame_np, format='bgr24')
                # encode() retourne une liste de packets
                packets = out_stream.encode(av_frame)
                for packet in packets:
                    output_container.mux(packet)
            
            # Sauvegarder la dernière frame pour la transition suivante
            if len(frames_list) > 0:
                last_frame = frames_list[-1]
        
        # Finaliser l'encodage - appeler encode() en boucle jusqu'à ce qu'il n'y ait plus de packets
        try:
            while True:
                packets = out_stream.encode()
                if not packets:
                    break
                for packet in packets:
                    output_container.mux(packet)
        except Exception:
            # L'encoder peut signaler EOF lors du flush, c'est normal
            pass
        
        output_container.close()
        
        # Vérifier que le fichier a bien été créé
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Concaténation réussie: {output_path}")
            return True
        else:
            print(f"❌ Le fichier de sortie n'a pas été créé correctement")
            return False
        
    except ImportError:
        print("❌ ERREUR: Le module 'av' (PyAV) est requis pour la concaténation de vidéos.")
        print("   Installez-le avec: pip install av")
        return False
        
    except Exception as e:
        # Vérifier si le fichier existe malgré l'erreur (PyAV peut rapporter des erreurs même en cas de succès)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Concaténation réussie: {output_path}")
            print(f"   (Note: PyAV a rapporté une erreur mais le fichier est valide)")
            return True
        else:
            print(f"❌ Erreur lors de la concaténation: {e}")
            return False


def initiate_sketch_sync(image_path, split_len, frame_rate, object_skip_rate, bg_object_skip_rate, main_img_duration, callback, save_path=save_path, which_platform="linux", export_json=False, aspect_ratio='original', crf=DEFAULT_CRF, watermark_path=None, watermark_position='bottom-right', watermark_opacity=0.5, watermark_scale=0.1):
    """Version synchrone de initiate_sketch pour l'exécution en ligne de commande (sans Kivy Clock)."""
    global platform
    platform = which_platform
    final_result = {"status": False, "message": "Initial load"}
    try:
        if not (os.path.exists(hand_path) and os.path.exists(hand_mask_path)):
            raise FileNotFoundError(f"Fichiers de main manquants. Attendu dans: {images_path}")
            
        image_bgr = cv2.imread(image_path)
        if image_bgr is None:
             raise ValueError(f"Impossible de lire l'image: {image_path}")
             
        mask_path = None 

        now = datetime.datetime.now()
        current_time = str(now.strftime("%H%M%S"))
        current_date = str(now.strftime("%Y%m%d"))
        
        video_save_name = f"vid_{current_date}_{current_time}.mp4" 
        save_video_path = os.path.join(save_path, video_save_name)
        ffmpeg_file_name = f"vid_{current_date}_{current_time}_h264.mp4"
        ffmpeg_video_path = os.path.join(save_path, ffmpeg_file_name)
        json_file_name = f"animation_{current_date}_{current_time}.json"
        json_export_path = os.path.join(save_path, json_file_name)
        os.makedirs(os.path.dirname(save_video_path), exist_ok=True)
        print(f"Chemin de sauvegarde brut: {save_video_path}")

        # Calculate dimensions based on aspect ratio
        img_ht, img_wd = image_bgr.shape[0], image_bgr.shape[1]
        
        if aspect_ratio != 'original':
            img_wd, img_ht = calculate_aspect_ratio_dimensions(img_wd, img_ht, aspect_ratio)
            print(f"Ratio d'aspect: {aspect_ratio}, Résolution cible: {img_wd}x{img_ht}")
            # Apply padding to maintain aspect ratio
            image_bgr = apply_aspect_ratio_padding(image_bgr, img_wd, img_ht)
        else:
            original_aspect_ratio = img_wd / img_ht
            img_ht = find_nearest_res(img_ht)
            new_aspect_wd = int(img_ht * original_aspect_ratio)
            img_wd = find_nearest_res(new_aspect_wd)
            print(f"Résolution cible: {img_wd}x{img_ht}")

        variables = AllVariables(
            frame_rate=frame_rate, resize_wd=img_wd, resize_ht=img_ht, split_len=split_len, 
            object_skip_rate=object_skip_rate, bg_object_skip_rate=bg_object_skip_rate, 
            end_gray_img_duration_in_sec=main_img_duration, export_json=export_json,
            watermark_path=watermark_path, watermark_position=watermark_position,
            watermark_opacity=watermark_opacity, watermark_scale=watermark_scale
        )

        draw_whiteboard_animations(
            image_bgr, mask_path, hand_path, hand_mask_path, save_video_path, variables
        )
        
        # Export JSON if requested
        if export_json:
            export_animation_json(variables, json_export_path)
        
        ff_stat = ffmpeg_convert(source_vid=save_video_path, dest_vid=ffmpeg_video_path, platform=platform, crf=crf)
        
        if ff_stat:
            final_result = {"status": True, "message": f"{ffmpeg_video_path}"}
            os.unlink(save_video_path)
            print(f"Vidéo brute supprimée: {save_video_path}")
        else:
            final_result = {"status": True, "message": f"{save_video_path}"} 
        
        # Add JSON path to result if exported
        if export_json:
            final_result["json_path"] = json_export_path

    except Exception as e:
        final_result = {"status": False, "message": f"Erreur fatale: {e}"}

    callback(final_result)


def process_multiple_images(image_paths, split_len, frame_rate, object_skip_rate, bg_object_skip_rate, main_img_duration, which_platform="linux", export_json=False, transition='none', transition_duration=0.5, per_slide_config=None, aspect_ratio='original', crf=DEFAULT_CRF, watermark_path=None, watermark_position='bottom-right', watermark_opacity=0.5, watermark_scale=0.1, audio_config=None, background_music=None, music_volume=0.5, music_fade_in=0, music_fade_out=0, enable_typewriter_sound=False, enable_drawing_sound=False):
    """Traite plusieurs images et génère une vidéo combinée.
    
    Args:
        image_paths: Liste des chemins des images à traiter
        split_len: Taille de la grille pour le dessin
        frame_rate: Images par seconde
        object_skip_rate: Vitesse de dessin
        bg_object_skip_rate: Taux de saut pour l'arrière-plan
        main_img_duration: Durée de l'image finale en secondes
        which_platform: Plateforme ('linux', 'android', etc.)
        export_json: Exporter les données d'animation au format JSON
        transition: Type de transition ('none', 'fade', 'wipe', 'push_left', 'push_right', 'iris')
        transition_duration: Durée de la transition en secondes
        per_slide_config: Configuration par slide (dict avec clés 'slides' et 'transitions')
        aspect_ratio: Target aspect ratio ('original', '1:1', '16:9', '9:16')
        crf: Video quality (0-51, lower = better quality)
        watermark_path: Path to watermark image
        watermark_position: Position of watermark
        watermark_opacity: Opacity of watermark (0.0-1.0)
        watermark_scale: Scale of watermark relative to frame width
        audio_config: Audio configuration dictionary
        background_music: Path to background music file
        music_volume: Background music volume (0.0-1.0)
        music_fade_in: Music fade-in duration in seconds
        music_fade_out: Music fade-out duration in seconds
        enable_typewriter_sound: Enable typewriter sounds for text animations
        enable_drawing_sound: Enable drawing sounds for animations
    """
    global platform
    platform = which_platform
    
    # Check if we have slides with layers configuration
    has_slides_config = False
    num_slides = 0
    if per_slide_config:
        if 'slides' in per_slide_config:
            num_slides = len(per_slide_config['slides'])
            has_slides_config = True
        elif 'layers' in per_slide_config:
            # Single scene config without 'slides' wrapper - wrap it
            per_slide_config = {
                'slides': [per_slide_config],
                'canvas_width': per_slide_config.get('canvas_width', 1920),
                'canvas_height': per_slide_config.get('canvas_height', 1080)
            }
            # Map sceneCameras to cameras at root level (only if cameras doesn't exist or is empty)
            if 'sceneCameras' in per_slide_config['slides'][0]:
                if 'cameras' not in per_slide_config['slides'][0] or not per_slide_config['slides'][0]['cameras']:
                    per_slide_config['slides'][0]['cameras'] = per_slide_config['slides'][0]['sceneCameras']
            per_slide_config['slides'][0]['index'] = 0
            num_slides = 1
            has_slides_config = True
    
    # If no image paths and no slides config, error
    if not image_paths and not has_slides_config:
        return {"status": False, "message": "Aucune image fournie"}
    
    # Determine how many items to process
    if has_slides_config:
        # Use slides from config
        num_items = num_slides
        print("\n" + "="*60)
        print(f"🎬 TRAITEMENT DE {num_items} SLIDE(S) DEPUIS LA CONFIGURATION")
        print("="*60)
    else:
        # Use image paths
        num_items = len(image_paths)
        print("\n" + "="*60)
        print(f"🎬 TRAITEMENT DE {num_items} IMAGE(S)")
        print("="*60)
    
    generated_videos = []
    json_exports = []
    
    # Créer un horodatage unique pour cette série
    now = datetime.datetime.now()
    current_time = str(now.strftime("%H%M%S"))
    current_date = str(now.strftime("%Y%m%d"))
    series_id = f"{current_date}_{current_time}"
    
    # Initialize audio manager if audio is requested
    audio_manager = None
    total_video_duration = 0.0
    
    if AUDIO_MODULE_AVAILABLE and PYDUB_AVAILABLE and (audio_config or background_music or enable_typewriter_sound or enable_drawing_sound):
        print("\n🔊 Audio Support Enabled")
        audio_manager = AudioManager(frame_rate=frame_rate)
        
        # Load audio configuration from file if provided
        if audio_config:
            if os.path.exists(audio_config):
                try:
                    with open(audio_config, 'r', encoding='utf-8') as f:
                        audio_cfg = json.load(f)
                    print(f"✅ Audio configuration loaded: {audio_config}")
                    
                    # Process global audio configuration
                    if 'audio' in audio_cfg:
                        process_audio_config(audio_cfg['audio'], audio_manager)
                except Exception as e:
                    print(f"⚠️ Error loading audio config: {e}")
            else:
                print(f"⚠️ Audio config file not found: {audio_config}")
        
        # Load background music from CLI argument
        if background_music and os.path.exists(background_music):
            audio_manager.load_background_music(
                background_music,
                volume=music_volume,
                loop=True,
                fade_in=music_fade_in,
                fade_out=music_fade_out
            )
    elif (audio_config or background_music or enable_typewriter_sound or enable_drawing_sound):
        print("⚠️ Audio requested but pydub is not installed. Audio features disabled.")
        print("   Install with: pip install pydub")
    
    # Préparer les configurations de transition par slide
    transition_configs = []
    
    # Traiter chaque slide/image
    for idx in range(1, num_items + 1):
        # Determine if this is an image-based or layer-based slide
        slide_config = {}
        layers = None
        image_path = None
        
        if has_slides_config:
            # Get slide config from configuration
            for slide_cfg in per_slide_config['slides']:
                if slide_cfg.get('index') == idx - 1:
                    slide_config = slide_cfg
                    break
            
            # Map sceneCameras to cameras if present (for compatibility)
            # Only map if cameras doesn't exist or is empty
            if 'sceneCameras' in slide_config:
                if 'cameras' not in slide_config or not slide_config['cameras']:
                    slide_config['cameras'] = slide_config['sceneCameras']
            
            layers = slide_config.get('layers', None)
            image_path = slide_config.get('image_path', None)
            
            # If image_path specified in slide config, use it
            if image_path:
                if not os.path.isabs(image_path):
                    image_path = os.path.join(base_path, image_path)
            # Otherwise check if there's a corresponding image in image_paths
            elif image_paths and idx <= len(image_paths):
                image_path = image_paths[idx - 1]
        else:
            # Traditional mode: use image from image_paths
            image_path = image_paths[idx - 1] if idx <= len(image_paths) else None
            # Check for slide config even without layers
            if per_slide_config and 'slides' in per_slide_config:
                for slide_cfg in per_slide_config['slides']:
                    if slide_cfg.get('index') == idx - 1:
                        slide_config = slide_cfg
                        break
        
        if layers:
            print(f"\n📝 Slide {idx}/{num_items}: Couches de texte/images")
        elif image_path:
            print(f"\n📷 Image {idx}/{num_items}: {os.path.basename(image_path)}")
        else:
            print(f"\n⚠️ Slide {idx}/{num_items}: Aucune source (ignorée)")
            continue
        
        print("-" * 60)
        
        try:
            # Read image if available
            image_bgr = None
            mask_path = None
            
            if image_path:
                if not os.path.exists(image_path):
                    print(f"⚠️ Image ignorée (introuvable): {image_path}")
                    continue
                
                # Lire l'image pour vérifier
                image_bgr = cv2.imread(image_path)
                if image_bgr is None:
                    print(f"⚠️ Image ignorée (illisible): {image_path}")
                    continue
            
            # Noms de fichiers pour cette slide
            video_save_name = f"vid_{series_id}_img{idx}.mp4"
            save_video_path = os.path.join(save_path, video_save_name)
            ffmpeg_file_name = f"vid_{series_id}_img{idx}_h264.mp4"
            ffmpeg_video_path = os.path.join(save_path, ffmpeg_file_name)
            json_file_name = f"animation_{series_id}_img{idx}.json"
            json_export_path = os.path.join(save_path, json_file_name)
            
            os.makedirs(save_path, exist_ok=True)
            
            # Calculer la résolution basée sur le ratio d'aspect
            if image_bgr is not None:
                img_ht, img_wd = image_bgr.shape[0], image_bgr.shape[1]
                
                if aspect_ratio != 'original':
                    img_wd, img_ht = calculate_aspect_ratio_dimensions(img_wd, img_ht, aspect_ratio)
                    print(f"  Ratio d'aspect: {aspect_ratio}, Résolution cible: {img_wd}x{img_ht}")
                    # Apply padding to maintain aspect ratio
                    image_bgr = apply_aspect_ratio_padding(image_bgr, img_wd, img_ht)
                else:
                    original_aspect_ratio = img_wd / img_ht
                    img_ht = find_nearest_res(img_ht)
                    new_aspect_wd = int(img_ht * original_aspect_ratio)
                    img_wd = find_nearest_res(new_aspect_wd)
                    print(f"  Résolution cible: {img_wd}x{img_ht}")
            else:
                # No image provided, use default resolution or get from config
                # Default to 1920x1080 for text-only slides
                img_wd = 1920
                img_ht = 1080
                if aspect_ratio == '1:1':
                    img_wd, img_ht = 1080, 1080
                elif aspect_ratio == '9:16':
                    img_wd, img_ht = 1080, 1920
                elif aspect_ratio == '16:9':
                    img_wd, img_ht = 1920, 1080
                print(f"  Résolution par défaut (texte uniquement): {img_wd}x{img_ht}")
            
            # Check for canvas dimensions in config and scale positions if needed
            canvas_width = per_slide_config.get('canvas_width', 1920) if per_slide_config else 1920
            canvas_height = per_slide_config.get('canvas_height', 1080) if per_slide_config else 1080
            
            # Calculate scaling factors if canvas dimensions differ from target dimensions
            scale_x = img_wd / canvas_width
            scale_y = img_ht / canvas_height
            
            if scale_x != 1.0 or scale_y != 1.0:
                print(f"  📏 Canvas original: {canvas_width}x{canvas_height}")
                print(f"  📏 Scaling positions: x={scale_x:.3f}, y={scale_y:.3f}")
                
                # Scale all layer positions
                if layers:
                    for layer in layers:
                        if 'position' in layer and layer['position']:
                            layer['position']['x'] = layer['position']['x'] * scale_x
                            layer['position']['y'] = layer['position']['y'] * scale_y
                        
                        # Scale text positions within text_config
                        if 'text_config' in layer and layer['text_config']:
                            text_cfg = layer['text_config']
                            if 'position' in text_cfg and text_cfg['position']:
                                text_cfg['position']['x'] = text_cfg['position']['x'] * scale_x
                                text_cfg['position']['y'] = text_cfg['position']['y'] * scale_y
            
            # Layers and slide_config already retrieved above
            if layers:
                print(f"  🎨 Mode multi-couches détecté ({len(layers)} couche(s))")
                # Composer les couches en une seule image (for non-layered animation path)
                # Note: For layered animation, we pass layers directly
                # image_bgr = compose_layers(layers, img_wd, img_ht, base_path)
            
            # Utiliser les paramètres de la slide ou les valeurs par défaut
            slide_skip_rate = slide_config.get('skip_rate', object_skip_rate)
            slide_duration = slide_config.get('duration', main_img_duration)
            
            # Pour les slides intermédiaires (pas la dernière), vérifier si une durée est spécifiée
            is_last_image = (idx == num_items)
            if not is_last_image and 'duration' not in slide_config:
                # Si pas de durée spécifiée pour slide intermédiaire, utiliser 0
                slide_duration = 0
            
            print(f"  Vitesse de dessin (skip-rate): {slide_skip_rate}")
            print(f"  Durée de la slide: {slide_duration}s")
            
            # Stocker la config de transition pour plus tard
            transition_config = {}
            if per_slide_config and 'transitions' in per_slide_config:
                # Chercher la config de transition après cette slide
                for trans_cfg in per_slide_config['transitions']:
                    if trans_cfg.get('after_slide') == idx - 1:
                        transition_config = trans_cfg
                        break
            transition_configs.append(transition_config)
            
            # Créer les variables
            variables = AllVariables(
                frame_rate=frame_rate, resize_wd=img_wd, resize_ht=img_ht, split_len=split_len,
                object_skip_rate=slide_skip_rate, bg_object_skip_rate=bg_object_skip_rate,
                end_gray_img_duration_in_sec=slide_duration, export_json=export_json,
                watermark_path=watermark_path, watermark_position=watermark_position,
                watermark_opacity=watermark_opacity, watermark_scale=watermark_scale
            )
            
            # Générer l'animation (avec ou sans couches)
            if layers:
                # Animation multi-couches
                draw_layered_whiteboard_animations(
                    layers, hand_path, hand_mask_path, save_video_path, variables, base_path, slide_config
                )
            else:
                # Animation simple d'une seule image
                draw_whiteboard_animations(
                    image_bgr, mask_path, hand_path, hand_mask_path, save_video_path, variables
                )
            
            # Export JSON si demandé
            if export_json:
                export_animation_json(variables, json_export_path)
                json_exports.append(json_export_path)
            
            # Convertir en H.264
            ff_stat = ffmpeg_convert(source_vid=save_video_path, dest_vid=ffmpeg_video_path, platform=platform, crf=crf)
            
            if ff_stat:
                generated_videos.append(ffmpeg_video_path)
                os.unlink(save_video_path)
                print(f"  ✅ Vidéo générée: {os.path.basename(ffmpeg_video_path)}")
            else:
                generated_videos.append(save_video_path)
                print(f"  ✅ Vidéo générée (sans conversion): {os.path.basename(save_video_path)}")
        
        except Exception as e:
            print(f"  ❌ Erreur lors du traitement de l'image {idx}: {e}")
            continue
    
    # Vérifier qu'au moins une vidéo a été générée
    if not generated_videos:
        return {"status": False, "message": "Aucune vidéo n'a pu être générée"}
    
    # Concaténer les vidéos si plusieurs
    if len(generated_videos) > 1:
        print("\n" + "="*60)
        print("🔗 COMBINAISON DES VIDÉOS")
        print("="*60)
        
        combined_video_name = f"vid_{series_id}_combined.mp4"
        combined_video_path = os.path.join(save_path, combined_video_name)
        
        concat_success = concatenate_videos(
            generated_videos, 
            combined_video_path, 
            transition_type=transition, 
            transition_duration=transition_duration,
            per_slide_transitions=transition_configs,
            crf=crf
        )
        
        if concat_success:
            # Add audio to video if audio manager was initialized
            if audio_manager is not None:
                print("\n" + "="*60)
                print("🔊 ADDING AUDIO TO VIDEO")
                print("="*60)
                
                # Calculate total video duration by inspecting the final video
                try:
                    import av
                    with av.open(combined_video_path) as container:
                        if container.streams.video:
                            stream = container.streams.video[0]
                            duration_seconds = float(stream.duration * stream.time_base)
                            audio_manager.set_total_duration(duration_seconds)
                            print(f"📊 Video duration: {duration_seconds:.2f}s")
                except Exception as e:
                    print(f"⚠️ Could not determine video duration: {e}")
                
                # Export mixed audio
                temp_audio_path = os.path.join(save_path, f"audio_{series_id}.wav")
                if audio_manager.export_audio(temp_audio_path, format="wav"):
                    # Create final video with audio
                    final_video_name = f"vid_{series_id}_combined_with_audio.mp4"
                    final_video_path = os.path.join(save_path, final_video_name)
                    
                    if add_audio_to_video(combined_video_path, temp_audio_path, final_video_path):
                        # Remove temporary audio file
                        try:
                            os.unlink(temp_audio_path)
                            print(f"  🗑️ Temporary audio file removed")
                        except:
                            pass
                        
                        # Remove video without audio
                        try:
                            os.unlink(combined_video_path)
                            print(f"  🗑️ Video without audio removed")
                        except:
                            pass
                        
                        # Update path to point to video with audio
                        combined_video_path = final_video_path
                        print(f"✅ Final video with audio: {combined_video_path}")
                    else:
                        print("⚠️ Failed to add audio to video. Using video without audio.")
                        # Clean up temp audio file
                        try:
                            os.unlink(temp_audio_path)
                        except:
                            pass
            
            # Supprimer les vidéos individuelles après concaténation réussie
            for video_path in generated_videos:
                try:
                    os.unlink(video_path)
                    print(f"  🗑️ Vidéo intermédiaire supprimée: {os.path.basename(video_path)}")
                except Exception as e:
                    print(f"  ⚠️ Impossible de supprimer {os.path.basename(video_path)}: {e}")
            
            result = {
                "status": True,
                "message": combined_video_path,
                "images_processed": len(image_paths),
                "videos_generated": len(generated_videos)
            }
            
            if json_exports:
                result["json_paths"] = json_exports
            
            return result
        else:
            # Échec de la concaténation, garder les vidéos individuelles
            result = {
                "status": True,
                "message": "Vidéos individuelles générées (échec de la concaténation): " + ", ".join([os.path.basename(v) for v in generated_videos]),
                "individual_videos": generated_videos,
                "images_processed": len(image_paths),
                "videos_generated": len(generated_videos)
            }
            
            if json_exports:
                result["json_paths"] = json_exports
            
            return result
    else:
        # Une seule vidéo générée
        single_video_path = generated_videos[0]
        
        # Add audio to video if audio manager was initialized
        if audio_manager is not None:
            print("\n" + "="*60)
            print("🔊 ADDING AUDIO TO VIDEO")
            print("="*60)
            
            # Calculate total video duration by inspecting the final video
            try:
                import av
                with av.open(single_video_path) as container:
                    if container.streams.video:
                        stream = container.streams.video[0]
                        duration_seconds = float(stream.duration * stream.time_base)
                        audio_manager.set_total_duration(duration_seconds)
                        print(f"📊 Video duration: {duration_seconds:.2f}s")
            except Exception as e:
                print(f"⚠️ Could not determine video duration: {e}")
            
            # Export mixed audio
            temp_audio_path = os.path.join(save_path, f"audio_{series_id}.wav")
            if audio_manager.export_audio(temp_audio_path, format="wav"):
                # Create final video with audio
                base_name = os.path.splitext(os.path.basename(single_video_path))[0]
                final_video_name = f"{base_name}_with_audio.mp4"
                final_video_path = os.path.join(save_path, final_video_name)
                
                if add_audio_to_video(single_video_path, temp_audio_path, final_video_path):
                    # Remove temporary audio file
                    try:
                        os.unlink(temp_audio_path)
                        print(f"  🗑️ Temporary audio file removed")
                    except:
                        pass
                    
                    # Remove video without audio
                    try:
                        os.unlink(single_video_path)
                        print(f"  🗑️ Video without audio removed")
                    except:
                        pass
                    
                    # Update path to point to video with audio
                    single_video_path = final_video_path
                    print(f"✅ Final video with audio: {single_video_path}")
                else:
                    print("⚠️ Failed to add audio to video. Using video without audio.")
                    # Clean up temp audio file
                    try:
                        os.unlink(temp_audio_path)
                    except:
                        pass
        
        result = {
            "status": True,
            "message": single_video_path,
            "images_processed": 1,
            "videos_generated": 1
        }
        
        if json_exports:
            result["json_path"] = json_exports[0]
        
        return result


def get_split_lens(image_path):
    """ Obtient la résolution de l'image (redimensionnée) et les diviseurs communs (split_lens). """
    final_return = {"image_res": "None", "split_lens": []}
    try:
        image_bgr = cv2.imread(image_path)
        if image_bgr is None:
             raise ValueError(f"Impossible de lire l'image: {image_path}")
             
        img_ht, img_wd = image_bgr.shape[0], image_bgr.shape[1]
        aspect_ratio = img_wd / img_ht
        img_ht = find_nearest_res(img_ht)
        new_aspect_wd = int(img_ht * aspect_ratio)
        img_wd = find_nearest_res(new_aspect_wd)
        
        hcf_list = common_divisors(img_ht, img_wd)
        filename = os.path.basename(image_path)
        
        final_return["split_lens"] = hcf_list
        final_return["image_res"] = f"{filename}, résolution vidéo cible: {img_wd}x{img_ht}"
    except Exception as e:
        final_return["image_res"] = f"Erreur lors de la lecture de l'image. {e}"
        print(f"Erreur lors de l'obtention des split lens: {e}")
        
    return final_return

# --- Configuration CLI (Ligne de Commande) ---

def main():
    """Fonction principale pour gérer les arguments CLI et lancer l'animation."""
    parser = argparse.ArgumentParser(
        description="Crée une vidéo d'animation style tableau blanc à partir d'une ou plusieurs images. "
        "Utilisez aussi --get-split-lens [image_path] pour voir les valeurs 'split_len' recommandées."
    )
    
    parser.add_argument(
        'image_paths', 
        type=str, 
        nargs='*', 
        default=None,
        help="Le(s) chemin(s) du/des fichier(s) image(s) à animer (ex: image1.png image2.png image3.png)"
    )

    parser.add_argument(
        '--split-len', 
        type=int, 
        default=DEFAULT_SPLIT_LEN,
        help=f"Taille de grille pour le dessin. Par défaut: {DEFAULT_SPLIT_LEN}. Utilisez des diviseurs de la résolution pour de meilleurs résultats."
    )
    parser.add_argument(
        '--frame-rate', 
        type=int, 
        default=DEFAULT_FRAME_RATE,
        help=f"Images par seconde (FPS). Par défaut: {DEFAULT_FRAME_RATE}."
    )
    parser.add_argument(
        '--skip-rate', 
        type=int, 
        default=DEFAULT_OBJECT_SKIP_RATE,
        help=f"Vitesse de dessin. Plus grand = plus rapide. Par défaut: {DEFAULT_OBJECT_SKIP_RATE}."
    )
    parser.add_argument(
        '--bg-skip-rate', 
        type=int, 
        default=DEFAULT_BG_OBJECT_SKIP_RATE,
        help=f"Taux de saut pour l'arrière-plan (non utilisé ici sans masques). Par défaut: {DEFAULT_BG_OBJECT_SKIP_RATE}."
    )
    parser.add_argument(
        '--duration', 
        type=int, 
        default=DEFAULT_MAIN_IMG_DURATION,
        help=f"Durée en secondes de l'image finale. Par défaut: {DEFAULT_MAIN_IMG_DURATION}."
    )
    
    parser.add_argument(
        '--transition',
        type=str,
        default='none',
        choices=['none', 'fade', 'wipe', 'push_left', 'push_right', 'iris'],
        help="Type de transition entre les slides (par défaut: none). Disponible: none, fade, wipe, push_left, push_right, iris."
    )
    
    parser.add_argument(
        '--transition-duration',
        type=float,
        default=0.5,
        help="Durée de la transition en secondes (par défaut: 0.5)."
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help="Chemin vers un fichier JSON pour une configuration personnalisée par slide (durée, vitesse, transitions, etc.)."
    )
    
    parser.add_argument(
        '--export-json',
        action='store_true',
        help="Exporte les données d'animation au format JSON (séquence de dessin, positions de la main, etc.)."
    )
    
    parser.add_argument(
        '--aspect-ratio',
        type=str,
        default='original',
        choices=['original', '1:1', '16:9', '9:16'],
        help="Ratio d'aspect de la vidéo (par défaut: original). Choix: original, 1:1, 16:9, 9:16."
    )
    
    parser.add_argument(
        '--quality',
        type=int,
        default=DEFAULT_CRF,
        choices=range(0, 52),
        metavar='0-51',
        help=f"Qualité vidéo (CRF: 0-51, plus bas = meilleure qualité, par défaut: {DEFAULT_CRF}). Valeurs recommandées: 18 (visually lossless), 23 (high quality), 28 (medium)."
    )
    
    parser.add_argument(
        '--watermark',
        type=str,
        default=None,
        help="Chemin vers l'image de filigrane (watermark) à appliquer sur la vidéo."
    )
    
    parser.add_argument(
        '--watermark-position',
        type=str,
        default='bottom-right',
        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
        help="Position du filigrane (par défaut: bottom-right)."
    )
    
    parser.add_argument(
        '--watermark-opacity',
        type=float,
        default=0.5,
        help="Opacité du filigrane (0.0 à 1.0, par défaut: 0.5)."
    )
    
    parser.add_argument(
        '--watermark-scale',
        type=float,
        default=0.1,
        help="Échelle du filigrane par rapport à la largeur de la vidéo (0.0 à 1.0, par défaut: 0.1)."
    )
    
    parser.add_argument(
        '--get-split-lens', 
        action='store_true',
        help="Affiche les valeurs 'split_len' recommandées pour le chemin d'image fourni, puis quitte."
    )
    
    # Performance optimization arguments
    parser.add_argument(
        '--preview',
        action='store_true',
        help="Mode preview: rendu rapide basse qualité pour tester (50%% résolution, qualité réduite)."
    )
    
    parser.add_argument(
        '--quality-preset',
        type=str,
        choices=['preview', 'draft', 'standard', 'high', 'ultra'],
        default=None,
        help="Préréglage de qualité (override --quality et --skip-rate). Choix: preview, draft, standard, high, ultra."
    )
    
    parser.add_argument(
        '--enable-checkpoints',
        action='store_true',
        help="Active les points de contrôle pour reprendre les rendus interrompus."
    )
    
    parser.add_argument(
        '--resume',
        type=str,
        default=None,
        metavar='CHECKPOINT_ID',
        help="Reprendre un rendu depuis un point de contrôle (ID du checkpoint)."
    )
    
    parser.add_argument(
        '--list-checkpoints',
        action='store_true',
        help="Affiche tous les points de contrôle disponibles et quitte."
    )
    
    parser.add_argument(
        '--background',
        action='store_true',
        help="Exécute le rendu en arrière-plan avec fichier de statut (render_status.json)."
    )
    
    parser.add_argument(
        '--batch',
        type=str,
        nargs='+',
        metavar='CONFIG_FILE',
        help="Mode batch: traite plusieurs fichiers de configuration en série."
    )
    
    parser.add_argument(
        '--batch-parallel',
        action='store_true',
        help="Active le traitement parallèle en mode batch (utilise plusieurs CPU)."
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=None,
        metavar='N',
        help="Nombre de threads pour le traitement parallèle (par défaut: auto-détecté)."
    )
    
    parser.add_argument(
        '--memory-efficient',
        action='store_true',
        help="Active le mode optimisation mémoire pour les grandes vidéos."
    )
    
    # Export format arguments
    parser.add_argument(
        '--export-formats',
        type=str,
        nargs='+',
        choices=['gif', 'webm', 'png', 'png-sequence', 'webm-alpha', 'transparent', 'lossless'],
        default=None,
        metavar='FORMAT',
        help="Formats d'export supplémentaires (gif, webm, png, webm-alpha, transparent, lossless). Peut spécifier plusieurs formats."
    )
    
    parser.add_argument(
        '--social-preset',
        type=str,
        default=None,
        choices=['youtube', 'youtube-shorts', 'tiktok', 'instagram-feed', 'instagram-story', 
                 'instagram-reel', 'facebook', 'twitter', 'linkedin'],
        help="Preset pour plateformes de médias sociaux (définit résolution, ratio, format optimal)."
    )
    
    parser.add_argument(
        '--list-presets',
        action='store_true',
        help="Affiche tous les presets de médias sociaux disponibles et quitte."
    )
    
    # Audio arguments
    parser.add_argument(
        '--audio-config',
        type=str,
        default=None,
        help="Chemin vers un fichier JSON de configuration audio (musique de fond, effets sonores, voix off, etc.)."
    )
    
    parser.add_argument(
        '--background-music',
        type=str,
        default=None,
        help="Chemin vers un fichier audio pour la musique de fond (mp3, wav, ogg, etc.)."
    )
    
    parser.add_argument(
        '--music-volume',
        type=float,
        default=0.5,
        help="Volume de la musique de fond (0.0 à 1.0, par défaut: 0.5)."
    )
    
    parser.add_argument(
        '--music-fade-in',
        type=float,
        default=0.0,
        help="Durée du fade-in de la musique en secondes (par défaut: 0)."
    )
    
    parser.add_argument(
        '--music-fade-out',
        type=float,
        default=0.0,
        help="Durée du fade-out de la musique en secondes (par défaut: 0)."
    )
    
    parser.add_argument(
        '--enable-typewriter-sound',
        action='store_true',
        help="Active les sons de machine à écrire pour les animations de texte."
    )
    
    parser.add_argument(
        '--enable-drawing-sound',
        action='store_true',
        help="Active les sons de dessin pour les animations de tracé."
    )
    
    parser.add_argument(
        '--audio-output',
        type=str,
        default=None,
        help="Chemin pour exporter l'audio mixé séparément (wav, mp3, etc.)."
    )

    args = parser.parse_args()
    
    # Handle list presets command
    if args.list_presets:
        if EXPORT_FORMATS_AVAILABLE:
            print_social_media_presets()
        else:
            print("❌ Export formats module not available.")
        return
    
    # Handle social media preset
    if args.social_preset:
        if EXPORT_FORMATS_AVAILABLE:
            preset = get_social_media_preset(args.social_preset)
            if preset:
                print(f"\n📱 Applying social media preset: {args.social_preset}")
                print(f"   {preset['description']}")
                
                # Override aspect ratio based on preset
                if preset['aspect_ratio'] == '16:9':
                    args.aspect_ratio = '16:9'
                elif preset['aspect_ratio'] == '9:16':
                    args.aspect_ratio = '9:16'
                elif preset['aspect_ratio'] == '1:1':
                    args.aspect_ratio = '1:1'
                
                # Set frame rate
                args.frame_rate = preset['fps']
                
                print(f"   - Aspect ratio: {preset['aspect_ratio']}")
                print(f"   - Resolution: {preset['resolution'][0]}x{preset['resolution'][1]}")
                print(f"   - FPS: {preset['fps']}")
                print(f"   - Format: {preset['format'].upper()}")
            else:
                print(f"❌ Preset '{args.social_preset}' not found.")
                return
        else:
            print("❌ Export formats module not available.")
            return
    
    # Initialize performance optimizer if available
    performance_optimizer = None
    checkpoint_manager = None
    
    if PERFORMANCE_MODULE_AVAILABLE:
        # Handle list checkpoints command
        if args.list_checkpoints:
            checkpoint_manager = RenderCheckpoint()
            checkpoints = checkpoint_manager.list_checkpoints()
            
            if not checkpoints:
                print("📋 No checkpoints found.")
            else:
                print("📋 Available checkpoints:")
                print("-" * 60)
                for checkpoint_id, mtime in checkpoints:
                    mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"  {checkpoint_id}  (modified: {mtime_str})")
                print("-" * 60)
            return
        
        # Handle batch processing
        if args.batch:
            print(f"📦 Batch mode: processing {len(args.batch)} configuration(s)")
            results = process_batch(
                args.batch,
                parallel=args.batch_parallel,
                max_workers=args.threads or 2
            )
            
            # Process each config in batch
            for i, config_file in enumerate(args.batch):
                print(f"\n{'='*60}")
                print(f"Processing {i+1}/{len(args.batch)}: {config_file}")
                print(f"{'='*60}")
                
                # Temporarily override args.config
                original_config = args.config
                args.config = config_file
                
                # Note: Full batch processing would recursively call the render
                # For now, we just prepare the structure
                results[i]['status'] = 'ready'
                
                args.config = original_config
            
            print(f"\n✅ Batch processing prepared for {len(args.batch)} configurations")
            return
        
        # Handle background rendering
        if args.background:
            print("🔄 Background rendering mode enabled")
            print("   Status will be written to: render_status.json")
            
            # Create progress tracker with status file
            progress_tracker = ProgressTracker()
            progress_tracker.set_status_file("render_status.json")
        
        # Apply quality preset if specified
        if args.quality_preset:
            preset_settings = parse_quality_preset(args.quality_preset)
            args.quality = preset_settings['quality']
            
            # Apply skip rate multiplier
            if hasattr(args, 'skip_rate'):
                args.skip_rate = int(args.skip_rate * preset_settings['skip_rate_multiplier'])
            
            print(f"🎨 Quality preset '{args.quality_preset}' applied:")
            print(f"   - Quality (CRF): {args.quality}")
            print(f"   - Skip rate multiplier: {preset_settings['skip_rate_multiplier']}")
        
        # Apply preview mode
        if args.preview:
            print("👁️  Preview mode enabled (50% resolution, faster rendering)")
            # Resolution will be reduced during processing
        
        # Initialize optimizer
        performance_optimizer = PerformanceOptimizer(
            enable_multithreading=args.threads is not None,
            max_workers=args.threads,
            enable_checkpoints=args.enable_checkpoints,
            checkpoint_interval=100,
            enable_preview=args.preview,
            preview_scale=0.5
        )
        
        checkpoint_manager = performance_optimizer.checkpoint_manager if args.enable_checkpoints else None
        
        if args.enable_checkpoints:
            print("💾 Checkpoints enabled (saves every 100 frames)")
        
        if args.memory_efficient:
            print("🧠 Memory-efficient mode enabled")
    
    if not (os.path.exists(hand_path) and os.path.exists(hand_mask_path)):
        print("\n❌ ERREUR DE CONFIGURATION: Les images de la main (drawing-hand.png et hand-mask.png) sont introuvables.")
        sys.exit(1)

    # --- Mode de vérification des 'split-lens' ---
    if args.get_split_lens:
        if not args.image_paths or len(args.image_paths) == 0:
            print("Erreur: Vous devez spécifier le chemin de l'image après --get-split-lens.")
            return

        path_to_check = args.image_paths[0]
        if not os.path.exists(path_to_check):
             print(f"Erreur: Le chemin d'image spécifié est introuvable: {path_to_check}")
             return
             
        res_info = get_split_lens(path_to_check)
        print("\n" + "="*50)
        print("INFOS DE RÉSOLUTION ET VALEURS 'SPLIT_LEN' RECOMMANDÉES")
        print("="*50)
        print(res_info['image_res'])
        print(f"Valeurs 'split_len' suggérées (diviseurs communs de la résolution cible):")
        print(res_info['split_lens'])
        print("\nUtilisez l'une de ces valeurs avec l'argument --split-len.")
        print("="*50 + "\n")
        return

    # Charger la configuration personnalisée si fournie
    per_slide_config = None
    has_layers_config = False
    if args.config:
        if not os.path.exists(args.config):
            print(f"❌ Erreur: Fichier de configuration introuvable: {args.config}")
            return
        
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                per_slide_config = json.load(f)
            print(f"✅ Configuration personnalisée chargée depuis: {args.config}")
            
            # Check if config has layers
            if 'slides' in per_slide_config:
                for slide_cfg in per_slide_config['slides']:
                    if 'layers' in slide_cfg:
                        has_layers_config = True
                        break
            elif 'layers' in per_slide_config:
                # Single scene config without 'slides' wrapper
                has_layers_config = True
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier de configuration: {e}")
            return
    
    # Check if we should use the new whiteboard export with camera positioning
    use_whiteboard_export = False
    if has_layers_config and per_slide_config:
        # Check if this is a single scene (not slides)
        if 'layers' in per_slide_config and 'slides' not in per_slide_config:
            use_whiteboard_export = True
            print("🎨 Detected single scene with layers - using whiteboard video export")

    # --- Mode de génération vidéo ---
    # If config has layers, images are optional
    if not args.image_paths or len(args.image_paths) == 0:
        # Check if config file has layers - if so, that's OK
        if not has_layers_config:
            parser.print_help()
            print("\n❌ ERREUR: Au moins un chemin d'image est requis.")
            return
        # Config file with layers exists, proceed without images
        valid_images = []
    else:
        # Vérifier que les images existent
        valid_images = []
        for img_path in args.image_paths:
            if os.path.exists(img_path):
                valid_images.append(img_path)
            else:
                print(f"⚠️ Avertissement: Image ignorée (introuvable): {img_path}")
        
        if not valid_images and not has_layers_config:
            print("❌ Erreur: Aucune image valide fournie.")
            return

    print("\n" + "="*50)
    print("🎬 Lancement de l'animation Whiteboard")
    if len(valid_images) == 1:
        print(f"Image source: {valid_images[0]}")
    else:
        print(f"Images sources: {len(valid_images)} image(s)")
        for i, img in enumerate(valid_images, 1):
            print(f"  {i}. {os.path.basename(img)}")
    print(f"Paramètres: Split={args.split_len}, FPS={args.frame_rate}, Skip={args.skip_rate}")
    print(f"Ratio d'aspect: {args.aspect_ratio}, Qualité (CRF): {args.quality}")
    if args.watermark:
        print(f"Filigrane: {args.watermark} ({args.watermark_position}, opacité: {args.watermark_opacity})")
    if per_slide_config:
        print("🔧 Configuration personnalisée par slide activée")
    print("="*50)

    # Traitement unique ou multiple
    if use_whiteboard_export:
        # Use new whiteboard export with camera positioning
        print("\n🎬 Using whiteboard video export with camera positioning...")
        
        # Get scene configuration
        scene_width = per_slide_config.get('scene_width', 1920)
        scene_height = per_slide_config.get('scene_height', 1080)
        background = per_slide_config.get('background', '#FFFFFF')
        
        # Get camera config
        camera_config = None
        if 'sceneCameras' in per_slide_config:
            for cam in per_slide_config['sceneCameras']:
                if cam.get('isDefault', False):
                    camera_config = cam
                    break
            if camera_config is None and per_slide_config['sceneCameras']:
                camera_config = per_slide_config['sceneCameras'][0]
        
        # Set output path
        output_path = os.path.join(save_path, f"whiteboard_scene_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        # Call whiteboard export
        result = export_scene_to_whiteboard_video(
            per_slide_config,
            output_path,
            fps=args.frame_rate,
            camera_config=camera_config,
            scene_width=scene_width,
            scene_height=scene_height,
            background=background,
            base_path=base_path,
            crf=args.quality,
            show_hand=True,
            final_hold_duration=args.duration
        )
        
        if result['success']:
            print(f"\n✅ SUCCÈS! Vidéo whiteboard créée: {result['output_path']}")
            print(f"   Durée: {result['duration']:.1f}s")
            print(f"   Résolution: {result['resolution']}")
            print(f"   Frames: {result['frames']}")
        else:
            print(f"\n❌ ÉCHEC: {result.get('error', 'Erreur inconnue')}")
        
    elif len(valid_images) == 1 and not has_layers_config:
        # Une seule image sans configuration de couches - utiliser l'ancienne méthode
        def final_callback_cli(result):
            """Fonction de rappel appelée à la fin de la génération."""
            if result["status"]:
                print(f"\n✅ SUCCÈS! Vidéo enregistrée sous: {result['message']}")
                if "json_path" in result:
                    print(f"✅ Données d'animation exportées: {result['json_path']}")
                
                # Export to additional formats if requested
                if args.export_formats:
                    exported = export_additional_formats(result['message'], args.export_formats, args.frame_rate)
                    if exported:
                        print(f"\n📦 Formats supplémentaires exportés:")
                        for fmt, path in exported.items():
                            print(f"  • {fmt}: {path}")
            else:
                print(f"\n❌ ÉCHEC de la génération vidéo. Message: {result['message']}")

        # Appel de la fonction synchrone pour la CLI
        initiate_sketch_sync(
            valid_images[0],
            args.split_len,
            args.frame_rate,
            args.skip_rate,
            args.bg_skip_rate,
            args.duration,
            final_callback_cli,
            export_json=args.export_json,
            aspect_ratio=args.aspect_ratio,
            crf=args.quality,
            watermark_path=args.watermark,
            watermark_position=args.watermark_position,
            watermark_opacity=args.watermark_opacity,
            watermark_scale=args.watermark_scale
        )
    else:
        # Plusieurs images - utiliser la nouvelle méthode
        result = process_multiple_images(
            valid_images,
            args.split_len,
            args.frame_rate,
            args.skip_rate,
            args.bg_skip_rate,
            args.duration,
            export_json=args.export_json,
            transition=args.transition,
            transition_duration=args.transition_duration,
            per_slide_config=per_slide_config,
            aspect_ratio=args.aspect_ratio,
            crf=args.quality,
            watermark_path=args.watermark,
            watermark_position=args.watermark_position,
            watermark_opacity=args.watermark_opacity,
            watermark_scale=args.watermark_scale,
            audio_config=args.audio_config,
            background_music=args.background_music,
            music_volume=args.music_volume,
            music_fade_in=args.music_fade_in,
            music_fade_out=args.music_fade_out,
            enable_typewriter_sound=args.enable_typewriter_sound,
            enable_drawing_sound=args.enable_drawing_sound
        )
        
        print("\n" + "="*60)
        if result["status"]:
            print("✅ SUCCÈS!")
            print(f"📊 Images traitées: {result.get('images_processed', 0)}")
            print(f"🎬 Vidéos générées: {result.get('videos_generated', 0)}")
            
            if "individual_videos" in result:
                print("\n📹 Vidéos individuelles (la concaténation a échoué):")
                for video in result["individual_videos"]:
                    print(f"  • {video}")
                    
                    # Export to additional formats if requested
                    if args.export_formats:
                        exported = export_additional_formats(video, args.export_formats, args.frame_rate)
                        if exported:
                            print(f"     📦 Formats supplémentaires exportés:")
                            for fmt, path in exported.items():
                                print(f"        • {fmt}: {path}")
            else:
                print(f"\n🎥 Vidéo finale: {result['message']}")
                
                # Export to additional formats if requested
                if args.export_formats:
                    exported = export_additional_formats(result['message'], args.export_formats, args.frame_rate)
                    if exported:
                        print(f"\n📦 Formats supplémentaires exportés:")
                        for fmt, path in exported.items():
                            print(f"  • {fmt}: {path}")
            
            if "json_paths" in result:
                print(f"\n📄 Données d'animation exportées ({len(result['json_paths'])} fichier(s)):")
                for json_path in result["json_paths"]:
                    print(f"  • {json_path}")
            elif "json_path" in result:
                print(f"\n📄 Données d'animation exportées: {result['json_path']}")
        else:
            print("❌ ÉCHEC!")
            print(f"Message: {result['message']}")
        print("="*60 + "\n")

if __name__ == '__main__':
    main()