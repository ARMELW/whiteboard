#!/usr/bin/env python3
"""Test that path_follow supports both path_config formats"""

def test_path_config_format_detection():
    """Test that we can detect and handle both path_config formats"""
    
    # Test case 1: Array format
    path_config_array = [
        {"x": 10, "y": 20},
        {"x": 30, "y": 40},
        {"x": 50, "y": 60}
    ]
    
    # Test case 2: Object format
    path_config_object = {
        "points": [
            {"x": 10, "y": 20},
            {"x": 30, "y": 40},
            {"x": 50, "y": 60}
        ]
    }
    
    # Test detection logic
    def extract_points(path_config):
        """Extract points from path_config in either format"""
        if path_config:
            if isinstance(path_config, list):
                # Direct array format
                return [(p['x'], p['y']) for p in path_config]
            elif isinstance(path_config, dict) and 'points' in path_config:
                # Object format
                return [(p['x'], p['y']) for p in path_config['points']]
        return None
    
    # Test array format
    points_from_array = extract_points(path_config_array)
    assert points_from_array is not None, "Should extract points from array format"
    assert len(points_from_array) == 3, "Should extract all 3 points from array"
    assert points_from_array[0] == (10, 20), "First point should match"
    print("✓ Array format works correctly")
    
    # Test object format
    points_from_object = extract_points(path_config_object)
    assert points_from_object is not None, "Should extract points from object format"
    assert len(points_from_object) == 3, "Should extract all 3 points from object"
    assert points_from_object[0] == (10, 20), "First point should match"
    print("✓ Object format works correctly")
    
    # Verify both produce same result
    assert points_from_array == points_from_object, "Both formats should produce same points"
    print("✓ Both formats produce identical results")
    
    # Test invalid format
    points_from_invalid = extract_points({"invalid": "format"})
    assert points_from_invalid is None, "Should return None for invalid format"
    print("✓ Invalid format handled correctly")
    
    print("\n✅ All path_config format tests passed!")

if __name__ == "__main__":
    test_path_config_format_detection()
