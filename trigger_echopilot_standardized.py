#!/usr/bin/env python3
"""
Standardized EchoPilot Trigger - Echo Component Implementation

This module provides a standardized interface for manually triggering the EchoPilot workflow,
implemented as an Echo component with consistent APIs and response handling.

Migrated from trigger_echopilot.py to use echo_component_base standardization.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

from echo_component_base import MemoryEchoComponent, EchoConfig, EchoResponse


class EchoPilotTriggerStandardized(MemoryEchoComponent):
    """
    Standardized EchoPilot Trigger component
    
    Provides workflow triggering capabilities with memory for tracking analysis results.
    Inherits from MemoryEchoComponent for storing analysis results and outputs.
    """
    
    def __init__(self, config: EchoConfig):
        super().__init__(config)
        
        # EchoPilot-specific configuration
        self.analysis_timeout = config.custom_params.get('analysis_timeout', 300)
        self.max_files_to_analyze = config.custom_params.get('max_files_to_analyze', 10)
        self.max_issues_per_category = config.custom_params.get('max_issues_per_category', 20)
        
        # Analysis categories
        self.analysis_categories = [
            'code_quality_issues',
            'architecture_gaps', 
            'test_coverage_gaps',
            'dependency_issues',
            'documentation_gaps'
        ]
        
    def initialize(self) -> EchoResponse:
        """Initialize the EchoPilot trigger component"""
        try:
            self._initialized = True
            self.logger.info("EchoPilot trigger initialized successfully")
            
            # Initialize analysis results storage
            for category in self.analysis_categories:
                self.store_memory(category, [])
            
            return EchoResponse(
                success=True,
                message="EchoPilot trigger component initialized",
                metadata={'categories': self.analysis_categories}
            )
        except Exception as e:
            return self.handle_error(e, "initialize")
    
    def process(self, input_data: Any, **kwargs) -> EchoResponse:
        """
        Process EchoPilot trigger request
        
        Args:
            input_data: Trigger configuration or None for default analysis
            **kwargs: Additional options like 'analysis_type', 'target_files'
        """
        try:
            # For EchoPilot trigger, None input means "run default analysis"
            # Override the base class validation for this specific case
            if input_data is not None:
                validation = self.validate_input(input_data)
                if not validation.success:
                    return validation
            
            analysis_type = kwargs.get('analysis_type', 'full')
            target_files = kwargs.get('target_files', None)
            
            self.logger.info(f"Processing EchoPilot trigger: {analysis_type}")
            
            # Run analysis
            analysis_result = self._run_analysis(analysis_type, target_files)
            if not analysis_result.success:
                return analysis_result
            
            # Store results in memory
            analysis_data = analysis_result.data
            for category in self.analysis_categories:
                if category in analysis_data:
                    store_result = self.store_memory(f"latest_{category}", analysis_data[category])
                    if not store_result.success:
                        self.logger.warning(f"Failed to store {category}: {store_result.message}")
            
            # Create issues summary
            issues_summary = self._create_issues_summary(analysis_data)
            
            return EchoResponse(
                success=True,
                data={
                    'analysis_results': analysis_data,
                    'issues_summary': issues_summary,
                    'timestamp': datetime.now().isoformat()
                },
                message=f"EchoPilot analysis completed: {analysis_type}",
                metadata={
                    'analysis_type': analysis_type,
                    'total_categories': len(self.analysis_categories),
                    'issues_found': sum(len(analysis_data.get(cat, [])) for cat in self.analysis_categories)
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "process")
    
    def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
        """
        Perform echo operation with EchoPilot trigger consideration
        
        Echoes analysis results with the provided echo value for amplification.
        """
        try:
            # For EchoPilot trigger, None data means "run default analysis and echo"
            # Process the data to get fresh analysis if needed
            process_result = self.process(data)
            
            if not process_result.success:
                return process_result
            
            # Create echoed analysis data
            echoed_data = {
                'original_analysis': process_result.data,
                'echo_value': echo_value,
                'echo_amplified_issues': self._amplify_issues_by_echo(
                    process_result.data['analysis_results'], echo_value
                ),
                'timestamp': datetime.now().isoformat()
            }
            
            # Store echoed results
            echo_key = f"echo_{datetime.now().timestamp()}"
            store_result = self.store_memory(echo_key, echoed_data)
            
            if not store_result.success:
                self.logger.warning(f"Failed to store echo results: {store_result.message}")
            
            return EchoResponse(
                success=True,
                data=echoed_data,
                message=f"EchoPilot echo analysis completed (value: {echo_value})",
                metadata={
                    'echo_value': echo_value,
                    'memory_key': echo_key,
                    'amplification_applied': echo_value > 0.5
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "echo")
    
    def _run_analysis(self, analysis_type: str = 'full', target_files: Optional[List[str]] = None) -> EchoResponse:
        """Run the EchoPilot analysis"""
        try:
            self.logger.info("Starting EchoPilot analysis...")
            
            # Create temporary file for outputs
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                output_file = f.name
            
            try:
                # Set environment variable
                env = os.environ.copy()
                env['GITHUB_OUTPUT'] = output_file
                
                # Run analysis based on type
                analysis_script = self._get_analysis_script(analysis_type, target_files)
                
                result = subprocess.run(
                    ['python3', '-c', analysis_script], 
                    env=env, 
                    capture_output=True, 
                    text=True,
                    timeout=self.analysis_timeout
                )
                
                if result.returncode != 0:
                    self.logger.warning(f"Analysis script returned {result.returncode}: {result.stderr}")
                
                # Read the outputs
                analysis_results = {}
                try:
                    with open(output_file, 'r') as f:
                        for line in f:
                            if '=' in line:
                                key, value = line.strip().split('=', 1)
                                try:
                                    analysis_results[key] = json.loads(value)
                                except json.JSONDecodeError:
                                    analysis_results[key] = value
                except Exception as e:
                    self.logger.warning(f"Error reading analysis outputs: {e}")
                
                return EchoResponse(
                    success=True,
                    data=analysis_results,
                    message="Analysis completed successfully",
                    metadata={'output_file': output_file}
                )
                
            finally:
                # Clean up
                try:
                    os.unlink(output_file)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            return EchoResponse(
                success=False,
                message=f"Analysis timed out after {self.analysis_timeout} seconds"
            )
        except Exception as e:
            return self.handle_error(e, "_run_analysis")
    
    def _get_analysis_script(self, analysis_type: str, target_files: Optional[List[str]]) -> str:
        """Get the appropriate analysis script based on type"""
        # This is a simplified version of the original script
        # In a real implementation, you might break this into separate analysis modules
        
        return f"""
import os
import json
import re
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

def run_command(cmd, capture_output=True):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True, timeout=60)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

# Initialize analysis results
analysis_results = {{
    'code_quality_issues': [],
    'architecture_gaps': [],
    'test_coverage_gaps': [],
    'dependency_issues': [],
    'documentation_gaps': []
}}

repo_path = Path('.')

# 1. Architecture Gap Analysis (focused on API consistency)
echo_files = list(repo_path.glob('**/*echo*.py')) + list(repo_path.glob('**/*Echo*.py'))
standardized_files = []
non_standardized_files = []

for file in echo_files:
    if file.name.startswith('test_'):
        continue
    try:
        with open(file, 'r') as f:
            content = f.read()
            if 'echo_component_base' in content and ('EchoComponent' in content or 'MemoryEchoComponent' in content):
                standardized_files.append(str(file))
            else:
                non_standardized_files.append(str(file))
    except Exception:
        continue

if non_standardized_files:
    analysis_results['architecture_gaps'].append({{
        'gap': 'Inconsistent APIs',
        'description': f'Found {{len(non_standardized_files)}} Echo components not using standardized base classes',
        'files': non_standardized_files[:10],
        'priority': 'medium',
        'recommendation': 'Migrate components to use EchoComponent base classes for consistent APIs'
    }})

# 2. Test Coverage Analysis
test_files = list(repo_path.glob('**/test_*.py'))
source_files = [f for f in echo_files if not f.name.startswith('test_')]
missing_tests = []

for source_file in source_files:
    test_file_name = f"test_{{source_file.stem}}.py"
    if not any(test_file_name in str(tf) for tf in test_files):
        missing_tests.append(str(source_file))

if missing_tests:
    analysis_results['test_coverage_gaps'].append({{
        'gap': 'Missing Tests',
        'description': f'Found {{len(missing_tests)}} source files without corresponding tests',
        'files': missing_tests[:5],
        'priority': 'medium',
        'recommendation': 'Add unit tests for uncovered source files'
    }})

# Set outputs
output_file = os.environ.get('GITHUB_OUTPUT')
if output_file:
    with open(output_file, 'a') as f:
        for key, value in analysis_results.items():
            f.write(f"{{key}}={{json.dumps(value)}}\\n")

print(f"Analysis complete. Found {{len(analysis_results['architecture_gaps'])}} architecture gaps")
"""
    
    def _create_issues_summary(self, analysis_data: Dict) -> Dict:
        """Create a summary of issues from analysis data"""
        summary = {
            'total_issues': 0,
            'by_category': {},
            'priority_breakdown': {'high': 0, 'medium': 0, 'low': 0}
        }
        
        for category in self.analysis_categories:
            issues = analysis_data.get(category, [])
            count = len(issues)
            summary['by_category'][category] = count
            summary['total_issues'] += count
            
            # Count by priority
            for issue in issues:
                priority = issue.get('priority', 'medium')
                if priority in summary['priority_breakdown']:
                    summary['priority_breakdown'][priority] += 1
        
        return summary
    
    def _amplify_issues_by_echo(self, analysis_results: Dict, echo_value: float) -> Dict:
        """Amplify issue priorities based on echo value"""
        if echo_value < 0.3:
            return analysis_results  # No amplification for low echo values
        
        amplified = {}
        for category, issues in analysis_results.items():
            amplified[category] = []
            for issue in issues:
                amplified_issue = issue.copy()
                
                # Amplify priority based on echo value
                current_priority = issue.get('priority', 'medium')
                if echo_value > 0.7 and current_priority == 'medium':
                    amplified_issue['priority'] = 'high'
                    amplified_issue['echo_amplified'] = True
                elif echo_value > 0.5 and current_priority == 'low':
                    amplified_issue['priority'] = 'medium'
                    amplified_issue['echo_amplified'] = True
                
                amplified[category].append(amplified_issue)
        
        return amplified
    
    def get_latest_analysis_results(self) -> EchoResponse:
        """Get the latest stored analysis results"""
        try:
            results = {}
            for category in self.analysis_categories:
                memory_result = self.retrieve_memory(f"latest_{category}")
                if memory_result.success:
                    results[category] = memory_result.data
                else:
                    results[category] = []
            
            return EchoResponse(
                success=True,
                data=results,
                message="Retrieved latest analysis results"
            )
        except Exception as e:
            return self.handle_error(e, "get_latest_analysis_results")
    
    def get_analysis_history(self, limit: int = 10) -> EchoResponse:
        """Get analysis history from memory"""
        try:
            history = []
            
            # Get all echo keys (analysis history)
            for key in self.memory_store.keys():
                if key.startswith('echo_'):
                    memory_result = self.retrieve_memory(key)
                    if memory_result.success:
                        history.append({
                            'key': key,
                            'timestamp': memory_result.data.get('timestamp'),
                            'echo_value': memory_result.data.get('echo_value'),
                            'analysis_summary': memory_result.data.get('original_analysis', {}).get('issues_summary', {})
                        })
            
            # Sort by timestamp and limit
            history = sorted(history, key=lambda x: x['timestamp'] or '', reverse=True)[:limit]
            
            return EchoResponse(
                success=True,
                data=history,
                message=f"Retrieved {len(history)} analysis history entries",
                metadata={'total_entries': len(history)}
            )
        except Exception as e:
            return self.handle_error(e, "get_analysis_history")


# Factory function for easy creation
def create_echopilot_trigger(custom_config: Dict = None) -> EchoPilotTriggerStandardized:
    """
    Factory function to create a standardized EchoPilot trigger component.
    
    Args:
        custom_config: Optional custom configuration parameters
        
    Returns:
        Configured EchoPilotTriggerStandardized instance
    """
    config = EchoConfig(
        component_name="EchoPilotTrigger",
        version="1.0.0",
        echo_threshold=0.6,
        custom_params=custom_config or {}
    )
    
    return EchoPilotTriggerStandardized(config)


# Backward compatibility function
def main():
    """Main function for backward compatibility with original trigger_echopilot.py"""
    print("🚀 EchoPilot Standardized Trigger")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create and initialize component
    trigger = create_echopilot_trigger({'analysis_timeout': 300})
    
    # Initialize
    init_result = trigger.initialize()
    if not init_result.success:
        print(f"❌ Initialization failed: {init_result.message}")
        return 1
    
    print("✅ EchoPilot trigger initialized")
    
    # Run analysis
    print("🔍 Running analysis...")
    analysis_result = trigger.process(None, analysis_type='full')
    
    if analysis_result.success:
        data = analysis_result.data
        print("✅ Analysis completed successfully!")
        print(f"📊 Issues Summary:")
        
        issues_summary = data.get('issues_summary', {})
        print(f"  - Total issues: {issues_summary.get('total_issues', 0)}")
        
        for category, count in issues_summary.get('by_category', {}).items():
            if count > 0:
                print(f"  - {category.replace('_', ' ').title()}: {count}")
        
        priority_breakdown = issues_summary.get('priority_breakdown', {})
        print(f"  - Priority breakdown: High: {priority_breakdown.get('high', 0)}, "
              f"Medium: {priority_breakdown.get('medium', 0)}, Low: {priority_breakdown.get('low', 0)}")
    else:
        print(f"❌ Analysis failed: {analysis_result.message}")
        return 1
    
    print(f"\n✅ EchoPilot run complete!")
    return 0


if __name__ == "__main__":
    exit(main())