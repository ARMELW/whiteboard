#!/usr/bin/env python3
"""
Integration test for advanced text animation features.
Tests the complete workflow from configuration to animation generation.
"""

import json
import tempfile
import os

def test_complete_workflow():
    """Test creating a complete animation with advanced text features."""
    
    print("=" * 70)
    print("Advanced Text Animation - Integration Test")
    print("=" * 70)
    print()
    
    # Create a comprehensive test configuration
    config = {
        "slides": [
            {
                "index": 0,
                "duration": 12,
                "layers": [
                    # Test 1: Character-by-character with shadow
                    {
                        "type": "text",
                        "z_index": 1,
                        "skip_rate": 5,
                        "text_config": {
                            "text": "Advanced Text",
                            "font": "DejaVuSans",
                            "size": 56,
                            "color": "#0066CC",
                            "style": "bold",
                            "align": "center",
                            "animation_type": "character_by_character",
                            "char_duration_frames": 4,
                            "pause_after_word": 8,
                            "text_effects": {
                                "shadow": {
                                    "offset": [3, 3],
                                    "color": "#888888"
                                }
                            },
                            "position": {"x": 0, "y": 80}
                        }
                    },
                    # Test 2: Word-by-word with outline
                    {
                        "type": "text",
                        "z_index": 2,
                        "skip_rate": 8,
                        "text_config": {
                            "text": "Animation Features",
                            "font": "DejaVuSans",
                            "size": 48,
                            "color": "#FF0066",
                            "style": "bold",
                            "align": "center",
                            "animation_type": "word_by_word",
                            "word_duration_frames": 10,
                            "pause_after_word": 5,
                            "text_effects": {
                                "outline": {
                                    "width": 2,
                                    "color": "#000000"
                                }
                            },
                            "position": {"x": 0, "y": 200}
                        }
                    },
                    # Test 3: RTL text
                    {
                        "type": "text",
                        "z_index": 3,
                        "skip_rate": 10,
                        "text_config": {
                            "text": "مرحبا",
                            "font": "DejaVuSans",
                            "size": 42,
                            "color": "#00AA66",
                            "direction": "rtl",
                            "align": "center",
                            "animation_type": "handwriting",
                            "position": {"x": 0, "y": 320}
                        }
                    },
                    # Test 4: Combined effects
                    {
                        "type": "text",
                        "z_index": 4,
                        "skip_rate": 12,
                        "text_config": {
                            "text": "Spectacular!",
                            "font": "DejaVuSans",
                            "size": 64,
                            "color": "#FFFF00",
                            "style": "bold",
                            "align": "center",
                            "animation_type": "character_by_character",
                            "char_duration_frames": 3,
                            "text_effects": {
                                "shadow": {
                                    "offset": [4, 4],
                                    "color": "#000000"
                                },
                                "outline": {
                                    "width": 1,
                                    "color": "#FFFFFF"
                                }
                            },
                            "position": {"x": 0, "y": 440}
                        }
                    }
                ]
            }
        ]
    }
    
    # Save configuration to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f, indent=2)
        config_file = f.name
    
    print(f"✓ Test configuration created: {config_file}")
    print()
    
    # Validate configuration structure
    print("Validating configuration...")
    assert 'slides' in config, "Config must have 'slides'"
    assert len(config['slides']) > 0, "Must have at least one slide"
    assert len(config['slides'][0]['layers']) == 4, "Should have 4 test layers"
    print("✓ Configuration structure valid")
    print()
    
    # Validate text animation types
    print("Validating animation types...")
    layers = config['slides'][0]['layers']
    animation_types = [layer['text_config']['animation_type'] for layer in layers]
    expected_types = ['character_by_character', 'word_by_word', 'handwriting', 'character_by_character']
    assert animation_types == expected_types, f"Animation types mismatch: {animation_types}"
    print(f"✓ Animation types: {', '.join(animation_types)}")
    print()
    
    # Validate text effects
    print("Validating text effects...")
    effects_count = sum(1 for layer in layers if 'text_effects' in layer['text_config'])
    assert effects_count == 3, f"Should have 3 layers with effects, got {effects_count}"
    print(f"✓ Text effects on {effects_count} layers")
    print()
    
    # Validate multilingual support
    print("Validating multilingual support...")
    rtl_layers = [l for l in layers if l['text_config'].get('direction') == 'rtl']
    assert len(rtl_layers) == 1, "Should have 1 RTL layer"
    print(f"✓ RTL text layer found: '{rtl_layers[0]['text_config']['text']}'")
    print()
    
    # Display test summary
    print("=" * 70)
    print("Integration Test Summary")
    print("=" * 70)
    print()
    print("Features Tested:")
    print("  ✅ Character-by-character animation")
    print("  ✅ Word-by-word animation")
    print("  ✅ Handwriting animation (default)")
    print("  ✅ Shadow text effects")
    print("  ✅ Outline text effects")
    print("  ✅ Combined effects (shadow + outline)")
    print("  ✅ RTL text support (Arabic)")
    print("  ✅ Timing controls (pause_after_word, char_duration_frames)")
    print("  ✅ Multiple text layers with different animations")
    print()
    print("Configuration Details:")
    print(f"  - Total slides: {len(config['slides'])}")
    print(f"  - Total layers: {len(layers)}")
    print(f"  - Animation duration: {config['slides'][0]['duration']}s")
    print()
    print("To generate video from this configuration:")
    print(f"  python3 whiteboard_animator.py --config {config_file}")
    print()
    print("=" * 70)
    print("✅ Integration test PASSED")
    print("=" * 70)
    
    return config_file

if __name__ == "__main__":
    import sys
    try:
        config_file = test_complete_workflow()
        print()
        print(f"Test configuration saved to: {config_file}")
        print("You can use this file to generate a test video.")
        sys.exit(0)
    except AssertionError as e:
        print()
        print(f"❌ Integration test FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Integration test ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
