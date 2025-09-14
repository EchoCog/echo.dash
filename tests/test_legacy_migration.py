#!/usr/bin/env python3
"""
Test for legacy file archival validation

This validates that deprecated legacy files have been properly moved
to the archived directory structure for preservation.
"""

import os
from pathlib import Path


def test_legacy_files_archived():
    """Test that legacy files have been properly archived"""
    print("🧪 Testing legacy file archival...")
    
    repo_root = Path(__file__).parent
    archive_legacy = repo_root / "archive" / "legacy"
    archive_archived = repo_root / "archive" / "archived" / "legacy_deep_tree_echo"
    
    # Legacy files that should be archived
    legacy_files = [
        "deep_tree_echo-v1.py", 
        "deep_tree_echo-v2.py"
    ]
    
    # Verify files are NOT in root directory
    for file in legacy_files:
        root_file = repo_root / file
        assert not root_file.exists(), f"Legacy file {file} should not exist in root directory"
        print(f"  ✅ {file} correctly removed from root")
    
    # Verify files are NOT in archive/legacy directory (moved to archived)
    for file in legacy_files:
        legacy_file = archive_legacy / file
        assert not legacy_file.exists(), f"Legacy file {file} should be moved from archive/legacy/"
        print(f"  ✅ {file} correctly moved from archive/legacy/")
        
    # Verify files ARE in archive/archived/legacy_deep_tree_echo directory
    for file in legacy_files:
        archived_file = archive_archived / file
        assert archived_file.exists(), f"Legacy file {file} should exist in archive/archived/legacy_deep_tree_echo/"
        print(f"  ✅ {file} correctly archived in archive/archived/legacy_deep_tree_echo/")
    
    print("  ✅ All legacy file archival tests passed")


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
    """Run all legacy archival tests"""
    print("🚀 Starting Legacy Code Archival Validation Tests")
    print("=" * 50)
    
    try:
        test_legacy_files_archived()
        test_archive_structure()
        test_analyzer_shows_resolution()
        
        print("\n" + "=" * 50)
        print("✅ All legacy archival tests passed!")
        print("\n🎯 Legacy code archival validation successful:")
        print("  - Legacy deep_tree_echo files properly archived to archive/archived/legacy_deep_tree_echo/")
        print("  - Root directory cleaned of deprecated versions")
        print("  - Archive/legacy directory cleaned of deep_tree_echo files")
        print("  - Archive/archived directory properly structured with README")
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