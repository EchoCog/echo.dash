#!/usr/bin/env python3
"""
Test for legacy file cleanup validation

This validates that deprecated legacy files have been completely removed
and are no longer present anywhere in the repository.
"""

import os
from pathlib import Path


def test_legacy_files_removed():
    """Test that legacy files have been completely removed"""
    print("🧪 Testing legacy file cleanup...")
    
    repo_root = Path(__file__).parent
    archive_legacy = repo_root / "archive" / "legacy"
    
    # Legacy files that should be completely removed
    legacy_files = [
        "deep_tree_echo-v1.py", 
        "deep_tree_echo-v2.py"
    ]
    
    # Verify files are NOT in root directory
    for file in legacy_files:
        root_file = repo_root / file
        assert not root_file.exists(), f"Legacy file {file} should not exist in root directory"
        print(f"  ✅ {file} correctly removed from root")
    
    # Verify files are NOT in archive/legacy directory (completely cleaned up)
    for file in legacy_files:
        archived_file = archive_legacy / file
        assert not archived_file.exists(), f"Legacy file {file} should be completely removed"
        print(f"  ✅ {file} completely removed (not even archived)")
    
    print("  ✅ All legacy file cleanup tests passed")


def test_archive_structure():
    """Test that archive directory has correct structure"""
    print("🧪 Testing archive directory structure...")
    
    repo_root = Path(__file__).parent
    archive_dir = repo_root / "archive"
    legacy_dir = archive_dir / "legacy"
    
    # Verify directories exist
    assert archive_dir.exists(), "Archive directory should exist"
    assert legacy_dir.exists(), "Archive/legacy directory should exist"
    
    # Verify legacy directory is now empty (or only contains non-deep-tree-echo files)
    if legacy_dir.exists():
        legacy_contents = list(legacy_dir.iterdir())
        deep_tree_echo_files = [f for f in legacy_contents if f.name.startswith('deep_tree_echo')]
        assert len(deep_tree_echo_files) == 0, "No deep_tree_echo legacy files should remain"
        print(f"  ✅ Legacy directory clean of deep_tree_echo files")
    
    print("  ✅ Archive structure tests passed")


def test_analyzer_shows_resolution():
    """Test that analyzer shows legacy code retention as resolved"""
    print("🧪 Testing analyzer gap resolution...")
    
    repo_root = Path(__file__).parent
    
    # Import and run the analyzer
    import sys
    sys.path.insert(0, str(repo_root))
    
    from deep_tree_echo_analyzer import DeepTreeEchoAnalyzer
    
    analyzer = DeepTreeEchoAnalyzer(repo_root)
    gaps = analyzer.identify_architecture_gaps()
    
    # Check that Legacy Code Retention gap is marked as resolved
    legacy_gaps = [gap for gap in gaps if gap['gap'] == 'Legacy Code Retention']
    
    if legacy_gaps:
        # If gap still exists, it should be marked as resolved
        legacy_gap = legacy_gaps[0]
        assert legacy_gap.get('priority') == 'resolved', "Legacy Code Retention gap should be marked as resolved"
        print("  ✅ Analyzer correctly shows legacy code retention as resolved")
    else:
        print("  ✅ Analyzer no longer reports legacy code retention gap")


def run_all_tests():
    """Run all legacy cleanup tests"""
    print("🚀 Starting Legacy Code Cleanup Validation Tests")
    print("=" * 50)
    
    try:
        test_legacy_files_removed()
        test_archive_structure()
        test_analyzer_shows_resolution()
        
        print("\n" + "=" * 50)
        print("✅ All legacy cleanup tests passed!")
        print("\n🎯 Legacy code cleanup validation successful:")
        print("  - Legacy deep_tree_echo files completely removed")
        print("  - Root directory cleaned of deprecated versions")
        print("  - Archive/legacy directory cleaned of deep_tree_echo files")
        print("  - Analyzer shows legacy code retention as resolved")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    import sys
    sys.exit(0 if success else 1)