#!/usr/bin/env python3
"""
EchoPilot Trigger - Unified Interface

This module provides the primary interface for triggering EchoPilot workflows.
It uses the standardized Echo component implementation internally while maintaining
backward compatibility with legacy usage patterns.

This is now the unified implementation that replaces the legacy script.
The old implementation is preserved in trigger_echopilot_legacy.py for reference.
"""

# Primary interface - use standardized implementation
from trigger_echopilot_standardized import (
    EchoPilotTriggerStandardized,
    create_echopilot_trigger,
    main as standardized_main
)

# For backward compatibility, expose the old interface
import json
from pathlib import Path
from datetime import datetime

# Global instance for backward compatibility
_global_trigger = None

def _get_global_trigger():
    """Get or create the global trigger instance for backward compatibility"""
    global _global_trigger
    if _global_trigger is None:
        _global_trigger = create_echopilot_trigger({
            'analysis_timeout': 300,
            'max_files_to_analyze': 10
        })
        _global_trigger.initialize()
    return _global_trigger

def run_analysis():
    """
    Legacy interface: Run the analysis step
    
    Returns:
        dict: Analysis outputs in legacy format
    """
    trigger = _get_global_trigger()
    result = trigger.process(None, analysis_type='full')
    
    if result.success:
        # Convert to legacy format
        analysis_results = result.data.get('analysis_results', {})
        outputs = {}
        
        for category in ['code_quality_issues', 'architecture_gaps', 'test_coverage_gaps', 
                        'dependency_issues', 'documentation_gaps']:
            outputs[category] = json.dumps(analysis_results.get(category, []))
        
        return outputs
    else:
        print(f"❌ Analysis failed: {result.message}")
        return {}

def create_issues(outputs):
    """
    Legacy interface: Create GitHub issues based on analysis results
    
    Args:
        outputs (dict): Analysis outputs from run_analysis()
        
    Returns:
        int: Number of issues that would be created
    """
    print("\n🔧 Creating GitHub Issues...")
    print("=" * 50)
    
    # Parse outputs (they're JSON strings in legacy format)
    def parse_output(output_str):
        try:
            return json.loads(output_str) if output_str else []
        except json.JSONDecodeError:
            print(f"Failed to parse output: {output_str[:200]}...")
            return []
    
    code_quality_issues = parse_output(outputs.get('code_quality_issues', '[]'))
    architecture_gaps = parse_output(outputs.get('architecture_gaps', '[]'))
    test_coverage_gaps = parse_output(outputs.get('test_coverage_gaps', '[]'))
    dependency_issues = parse_output(outputs.get('dependency_issues', '[]'))
    documentation_gaps = parse_output(outputs.get('documentation_gaps', '[]'))
    
    print(f"📊 Analysis Results:")
    print(f"  - Code Quality Issues: {len(code_quality_issues)}")
    print(f"  - Architecture Gaps: {len(architecture_gaps)}")
    print(f"  - Test Coverage Gaps: {len(test_coverage_gaps)}")
    print(f"  - Dependency Issues: {len(dependency_issues)}")
    print(f"  - Documentation Gaps: {len(documentation_gaps)}")
    
    # Simulate issue creation (same logic as legacy)
    issues_created = 0
    
    # Architecture gaps (high priority)
    for gap in architecture_gaps:
        title = f"🏗️ {gap['gap']}"
        print(f"✅ Would create issue: {title}")
        print(f"   Description: {gap['description']}")
        print(f"   Priority: {gap['priority']}")
        print(f"   Recommendation: {gap['recommendation']}")
        print()
        issues_created += 1
    
    # Documentation gaps
    for gap in documentation_gaps:
        title = f"📚 {gap['gap']}"
        print(f"✅ Would create issue: {title}")
        print(f"   Description: {gap['description']}")
        print(f"   Priority: {gap['priority']}")
        print()
        issues_created += 1
    
    # Test coverage gaps
    for gap in test_coverage_gaps:
        title = f"🧪 {gap['gap']}"
        print(f"✅ Would create issue: {title}")
        print(f"   Description: {gap['description']}")
        print(f"   Priority: {gap['priority']}")
        print()
        issues_created += 1
    
    # Dependency issues
    for issue_data in dependency_issues:
        title = f"📦 {issue_data['gap']}"
        print(f"✅ Would create issue: {title}")
        print(f"   Description: {issue_data['description']}")
        print(f"   Priority: {issue_data['priority']}")
        print()
        issues_created += 1
    
    # Code quality issues (batch them if there are many)
    if code_quality_issues:
        # Group by file to avoid spam
        issues_by_file = {}
        for issue in code_quality_issues:
            file = issue.get('file', 'unknown')
            if file not in issues_by_file:
                issues_by_file[file] = []
            issues_by_file[file].append(issue)

        for file, issues in list(issues_by_file.items())[:5]:  # Limit to 5 files
            title = f"🔧 Code Quality Issues in {Path(file).name}"
            print(f"✅ Would create issue: {title}")
            print(f"   File: {file}")
            print(f"   Issues Found: {len(issues)}")
            print(f"   Sample issues:")
            for issue in issues[:3]:
                if 'message' in issue:
                    print(f"     - Line {issue.get('line', 'N/A')}: {issue.get('message', 'Unknown issue')}")
                elif 'issue' in issue:
                    print(f"     - Line {issue.get('line', 'N/A')}: {issue.get('issue', 'Unknown issue')}")
                else:
                    print(f"     - Line {issue.get('line', 'N/A')}: {issue.get('pattern', 'Unknown pattern')}")
            print()
            issues_created += 1
    
    if issues_created > 0:
        print(f"🎉 Would create {issues_created} issues for dtecho to work on!")
    else:
        print("✅ No issues found! Your codebase appears to be in good shape.")
        print("💡 Consider running manual code reviews or adding more comprehensive tests.")
    
    return issues_created

def main():
    """
    Main function - provides legacy compatibility while using standardized implementation
    """
    # Use the standardized main function which provides the same interface
    # but with enhanced features
    return standardized_main()

# Export the standardized classes for advanced usage
EchoComponent = EchoPilotTriggerStandardized
create_trigger = create_echopilot_trigger

if __name__ == "__main__":
    main()