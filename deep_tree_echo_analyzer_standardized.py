#!/usr/bin/env python3
"""
Standardized Deep Tree Echo Analyzer Component

This module provides a standardized interface for analyzing Deep Tree Echo codebase,
implemented as an Echo component with consistent APIs and response handling.

Migrated from deep_tree_echo_analyzer.py to use echo_component_base standardization.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from echo_component_base import MemoryEchoComponent, EchoConfig, EchoResponse


class DeepTreeEchoAnalyzerStandardized(MemoryEchoComponent):
    """
    Standardized Deep Tree Echo Analyzer component
    
    Provides analysis capabilities for Deep Tree Echo codebase with memory
    storage functionality. Inherits from MemoryEchoComponent for persistent storage.
    """
    
    def __init__(self, config: EchoConfig):
        super().__init__(config)
        
        # Analyzer-specific configuration
        self.repo_path = Path(config.custom_params.get('repo_path', '.'))
        self.include_legacy = config.custom_params.get('include_legacy', True)
        self.file_patterns = config.custom_params.get('file_patterns', [
            '*deep_tree_echo*.py', '*echo*.py', '*Echo*.py'
        ])
        self.exclude_patterns = config.custom_params.get('exclude_patterns', [
            'test_*', '*__pycache__*', '*.pyc'
        ])
        self.analysis_depth = config.custom_params.get('analysis_depth', 'full')  # basic, medium, full
        
        # Analysis results storage
        self.analysis_results = {}
        
        # Processing pipeline for analysis steps
        self.processing_steps = [
            ('fragment_analysis', self._analyze_fragments),
            ('architecture_analysis', self._analyze_architecture_gaps),
            ('migration_analysis', self._analyze_migration_tasks),
            ('recommendation_generation', self._generate_recommendations)
        ]
        
    def initialize(self) -> EchoResponse:
        """Initialize the Deep Tree Echo analyzer component"""
        try:
            # Validate repository path
            if not self.repo_path.exists():
                return EchoResponse(
                    success=False,
                    message=f"Repository path does not exist: {self.repo_path}"
                )
            
            # Initialize analysis structure
            self.analysis_results = {
                'fragments': [],
                'architecture_gaps': [],
                'migration_tasks': [],
                'analysis_timestamp': datetime.now().isoformat(),
                'recommendations': [],
                'config': {
                    'repo_path': str(self.repo_path),
                    'include_legacy': self.include_legacy,
                    'analysis_depth': self.analysis_depth
                }
            }
            
            self._initialized = True
            
            self.logger.info(f"Deep Tree Echo analyzer initialized for repo: {self.repo_path}")
            
            return EchoResponse(
                success=True,
                data=self.analysis_results['config'],
                message="Deep Tree Echo analyzer component initialized"
            )
        except Exception as e:
            return self.handle_error(e, "initialize")
    
    def process(self, input_data: Any, **kwargs) -> EchoResponse:
        """
        Process analysis operations
        
        Args:
            input_data: Analysis request or file list to analyze
            **kwargs: Additional options like 'analysis_type', 'target_files'
        """
        try:
            if not self._initialized:
                return EchoResponse(
                    success=False,
                    message="Component not initialized"
                )
            
            validation = self.validate_input(input_data)
            # Allow None input for full analysis
            if input_data is not None and not validation.success:
                return validation
            
            analysis_type = kwargs.get('analysis_type', self.analysis_depth)
            target_files = kwargs.get('target_files', None)
            
            self.logger.info(f"Processing Deep Tree Echo analysis: {analysis_type}")
            
            # Prepare analysis input
            analysis_input = {
                'analysis_type': analysis_type,
                'target_files': target_files,
                'input_data': input_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Execute analysis pipeline
            pipeline_result = self._execute_analysis_pipeline(analysis_input)
            
            if not pipeline_result['success']:
                return EchoResponse(
                    success=False,
                    message=pipeline_result.get('error', 'Analysis pipeline failed')
                )
            
            # Store analysis results
            analysis_key = f"analysis_{analysis_type}_{datetime.now().timestamp()}"
            self.store_memory(analysis_key, pipeline_result['data'])
            
            return EchoResponse(
                success=True,
                data=pipeline_result['data'],
                message=f"Deep Tree Echo analysis completed: {analysis_type}",
                metadata={
                    'analysis_type': analysis_type,
                    'memory_key': analysis_key,
                    'fragments_found': len(pipeline_result['data'].get('fragments', [])),
                    'gaps_identified': len(pipeline_result['data'].get('architecture_gaps', [])),
                    'tasks_generated': len(pipeline_result['data'].get('migration_tasks', []))
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "process")
    
    def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
        """
        Perform echo operation with analysis consideration
        
        Echoes analysis results with amplified insight generation based on echo value.
        """
        try:
            # Process analysis with echo-enhanced depth
            enhanced_depth = 'full' if echo_value > 0.7 else 'medium' if echo_value > 0.3 else 'basic'
            
            process_result = self.process(data, analysis_type=enhanced_depth)
            
            if not process_result.success:
                return process_result
            
            # Apply echo amplification to analysis insights
            echo_amplified_data = self._apply_echo_to_analysis(
                process_result.data, echo_value
            )
            
            # Create echoed analysis data
            echoed_data = {
                'original_analysis': process_result.data,
                'echo_value': echo_value,
                'enhanced_depth': enhanced_depth,
                'echo_amplified_insights': echo_amplified_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store echoed results
            echo_key = f"echo_{datetime.now().timestamp()}"
            store_result = self.store_memory(echo_key, echoed_data)
            
            return EchoResponse(
                success=True,
                data=echoed_data,
                message=f"Deep Tree Echo analysis echo completed (value: {echo_value})",
                metadata={
                    'echo_value': echo_value,
                    'enhanced_depth': enhanced_depth,
                    'memory_key': echo_key,
                    'insights_amplified': echo_value > 0.5
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "echo")
    
    def _execute_analysis_pipeline(self, input_data: Dict) -> Dict:
        """Execute the analysis pipeline steps"""
        try:
            current_data = input_data.copy()
            
            for step_name, step_function in self.processing_steps:
                try:
                    current_data = step_function(current_data)
                    self.logger.debug(f"Completed analysis step: {step_name}")
                except Exception as e:
                    self.logger.error(f"Failed in step {step_name}: {e}")
                    return {
                        'success': False,
                        'error': f"Pipeline failed at step {step_name}: {str(e)}"
                    }
            
            return {
                'success': True,
                'data': current_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Pipeline execution failed: {str(e)}"
            }
    
    def _analyze_fragments(self, input_data: Dict) -> Dict:
        """Analyze and categorize Deep Tree Echo fragments"""
        self.logger.info("Analyzing Deep Tree Echo fragments...")
        
        fragments = []
        
        for pattern in self.file_patterns:
            for file in self.repo_path.glob(pattern):
                if not self._should_include_file(file):
                    continue
                
                try:
                    fragment = self._analyze_single_file(file)
                    if fragment:
                        fragments.append(fragment)
                except Exception as e:
                    self.logger.warning(f"Failed to analyze {file}: {e}")
        
        # Sort fragments by complexity and relevance
        fragments.sort(key=lambda f: (f.get('complexity_score', 0), f.get('lines', 0)), reverse=True)
        
        # Update results
        input_data['fragments'] = fragments
        
        self.logger.info(f"Found {len(fragments)} Deep Tree Echo fragments")
        return input_data
    
    def _analyze_architecture_gaps(self, input_data: Dict) -> Dict:
        """Analyze architecture gaps in the codebase"""
        self.logger.info("Analyzing architecture gaps...")
        
        gaps = []
        fragments = input_data.get('fragments', [])
        
        # 1. API Inconsistency Gap
        standardized_files = [f for f in fragments if f.get('uses_echo_base', False)]
        non_standardized_files = [f for f in fragments if not f.get('uses_echo_base', False)]
        
        if len(non_standardized_files) > 0:
            gaps.append({
                'gap': 'Inconsistent APIs',
                'description': f'Found {len(non_standardized_files)} Echo components not using standardized base classes',
                'affected_files': [f['file'] for f in non_standardized_files],
                'priority': 'medium',
                'recommendation': 'Migrate components to use EchoComponent base classes for consistent APIs',
                'type': 'api_consistency'
            })
        
        # 2. Memory Fragmentation Gap
        memory_files = [f for f in fragments if 'memory' in f['file'].lower()]
        if len(memory_files) > 3:
            gaps.append({
                'gap': 'Fragmented Memory System',
                'description': f'Found {len(memory_files)} memory-related files that should be unified',
                'affected_files': [f['file'] for f in memory_files],
                'priority': 'high',
                'recommendation': 'Consolidate memory operations into unified_echo_memory.py',
                'type': 'memory_fragmentation'
            })
        
        # 3. Launch Script Multiplicity Gap
        launch_files = [f for f in fragments if 'launch' in f['file'].lower()]
        if len(launch_files) > 2:
            gaps.append({
                'gap': 'Multiple Launch Scripts',
                'description': f'Found {len(launch_files)} launch scripts that could be consolidated',
                'affected_files': [f['file'] for f in launch_files],
                'priority': 'medium',
                'recommendation': 'Consider creating a unified launcher with configuration options',
                'type': 'launch_fragmentation'
            })
        
        # 4. Test Coverage Gap
        test_files = [f for f in fragments if f['file_type'] == 'test']
        source_files = [f for f in fragments if f['file_type'] in ['core', 'extension']]
        missing_tests = []
        
        for source_file in source_files:
            source_name = Path(source_file['file']).stem
            corresponding_test = f"test_{source_name}.py"
            
            if not any(corresponding_test in test_file['file'] for test_file in test_files):
                missing_tests.append(source_file['file'])
        
        if missing_tests:
            gaps.append({
                'gap': 'Missing Test Coverage',
                'description': f'Found {len(missing_tests)} source files without corresponding tests',
                'affected_files': missing_tests[:10],  # Limit to avoid overwhelming
                'priority': 'medium',
                'recommendation': 'Add unit tests for uncovered source files',
                'type': 'test_coverage'
            })
        
        # 5. Legacy File Gap
        legacy_files = [f for f in fragments if f['status'] == 'legacy']
        if len(legacy_files) > 0:
            gaps.append({
                'gap': 'Legacy Files Present',
                'description': f'Found {len(legacy_files)} legacy files that may need cleanup or migration',
                'affected_files': [f['file'] for f in legacy_files],
                'priority': 'low',
                'recommendation': 'Review legacy files for migration or removal',
                'type': 'legacy_cleanup'
            })
        
        # Update results
        input_data['architecture_gaps'] = gaps
        
        self.logger.info(f"Identified {len(gaps)} architecture gaps")
        return input_data
    
    def _analyze_migration_tasks(self, input_data: Dict) -> Dict:
        """Generate specific migration tasks based on analysis"""
        self.logger.info("Analyzing migration tasks...")
        
        tasks = []
        gaps = input_data.get('architecture_gaps', [])
        fragments = input_data.get('fragments', [])
        
        # Generate tasks for each gap
        for gap in gaps:
            if gap['type'] == 'api_consistency':
                # Create tasks for API standardization
                for file_name in gap['affected_files'][:5]:  # Limit to 5 files per task
                    fragment = next((f for f in fragments if f['file'] == file_name), None)
                    if fragment:
                        task = {
                            'task': f'Standardize API for {file_name}',
                            'type': 'migration',
                            'priority': gap['priority'],
                            'description': f'Migrate {file_name} to use standardized Echo base classes',
                            'file': file_name,
                            'complexity': fragment.get('complexity_score', 0),
                            'estimated_effort': self._estimate_effort(fragment),
                            'steps': [
                                f'Add import: from echo_component_base import EchoComponent, EchoConfig, EchoResponse',
                                f'Update class to inherit from appropriate base class',
                                f'Implement standardized initialize(), process(), and echo() methods',
                                f'Replace custom error handling with self.handle_error()',
                                f'Add unit tests for standardized interface'
                            ]
                        }
                        tasks.append(task)
            
            elif gap['type'] == 'memory_fragmentation':
                task = {
                    'task': 'Consolidate Memory System',
                    'type': 'refactoring',
                    'priority': gap['priority'],
                    'description': 'Unify fragmented memory operations into single system',
                    'files': gap['affected_files'],
                    'complexity': 'high',
                    'estimated_effort': 'large',
                    'steps': [
                        'Analyze existing memory implementations',
                        'Design unified memory interface',
                        'Create consolidated memory component',
                        'Migrate existing memory usage',
                        'Update tests and documentation'
                    ]
                }
                tasks.append(task)
            
            elif gap['type'] == 'test_coverage':
                # Group test tasks by priority
                high_priority_files = [f for f in gap['affected_files'] 
                                     if any(frag['file'] == f and frag.get('complexity_score', 0) > 50 
                                           for frag in fragments)]
                
                if high_priority_files:
                    task = {
                        'task': 'Add Test Coverage for Core Components',
                        'type': 'testing',
                        'priority': 'high',
                        'description': f'Add unit tests for {len(high_priority_files)} core components',
                        'files': high_priority_files[:3],
                        'complexity': 'medium',
                        'estimated_effort': 'medium',
                        'steps': [
                            'Create test file structure',
                            'Implement basic test cases',
                            'Add integration tests',
                            'Ensure proper mocking',
                            'Verify test coverage metrics'
                        ]
                    }
                    tasks.append(task)
        
        # Sort tasks by priority and complexity
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        tasks.sort(key=lambda t: (priority_order.get(t['priority'], 3), t.get('complexity', 0)))
        
        # Update results
        input_data['migration_tasks'] = tasks
        
        self.logger.info(f"Generated {len(tasks)} migration tasks")
        return input_data
    
    def _generate_recommendations(self, input_data: Dict) -> Dict:
        """Generate high-level recommendations based on analysis"""
        self.logger.info("Generating recommendations...")
        
        recommendations = []
        gaps = input_data.get('architecture_gaps', [])
        tasks = input_data.get('migration_tasks', [])
        fragments = input_data.get('fragments', [])
        
        # Overall architecture recommendations
        if len(gaps) > 0:
            recommendations.append({
                'category': 'Architecture',
                'priority': 'high',
                'title': 'Implement Unified Architecture Proposal',
                'description': f'Address {len(gaps)} architecture gaps through systematic unification',
                'actions': [
                    'Prioritize API consistency migrations first',
                    'Consolidate fragmented systems progressively',
                    'Establish standardized component interfaces',
                    'Create comprehensive test coverage'
                ]
            })
        
        # Migration strategy recommendations
        high_priority_tasks = [t for t in tasks if t['priority'] == 'high']
        if high_priority_tasks:
            recommendations.append({
                'category': 'Migration Strategy',
                'priority': 'high',
                'title': 'Phased Migration Approach',
                'description': f'Execute {len(high_priority_tasks)} high-priority tasks in phases',
                'actions': [
                    'Start with simple API standardizations',
                    'Progress to medium complexity components',
                    'Address complex integrations last',
                    'Maintain backward compatibility throughout'
                ]
            })
        
        # Code quality recommendations
        complex_files = [f for f in fragments if f.get('complexity_score', 0) > 100]
        if complex_files:
            recommendations.append({
                'category': 'Code Quality',
                'priority': 'medium',
                'title': 'Refactor Complex Components',
                'description': f'Simplify {len(complex_files)} complex components for maintainability',
                'actions': [
                    'Break down large files into smaller modules',
                    'Extract reusable functionality',
                    'Improve error handling consistency',
                    'Add comprehensive documentation'
                ]
            })
        
        # Testing recommendations
        test_gaps = [gap for gap in gaps if gap['type'] == 'test_coverage']
        if test_gaps:
            recommendations.append({
                'category': 'Testing',
                'priority': 'medium',
                'title': 'Improve Test Coverage',
                'description': 'Establish comprehensive testing framework',
                'actions': [
                    'Set up automated test execution',
                    'Implement unit tests for core components',
                    'Add integration tests for system interactions',
                    'Create performance benchmarks'
                ]
            })
        
        # Update results
        input_data['recommendations'] = recommendations
        
        self.logger.info(f"Generated {len(recommendations)} recommendations")
        return input_data
    
    def _should_include_file(self, file: Path) -> bool:
        """Check if file should be included in analysis"""
        if not file.is_file():
            return False
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if file.match(pattern):
                return False
        
        # Check if legacy files should be included
        if not self.include_legacy:
            if any(marker in str(file) for marker in ['-v1', '-v2', '.backup', '.old']):
                return False
        
        return True
    
    def _analyze_single_file(self, file: Path) -> Optional[Dict]:
        """Analyze a single file and extract metadata"""
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = len(content.splitlines())
            
            # Extract structural information
            classes = re.findall(r'class\s+(\w*[Ee]cho\w*)', content)
            functions = re.findall(r'def\s+(\w*echo\w*)', content, re.IGNORECASE)
            imports = re.findall(r'(?:from|import)\s+(\w*echo\w*)', content, re.IGNORECASE)
            
            # Check for Echo base class usage
            uses_echo_base = 'echo_component_base' in content and any(
                base in content for base in ['EchoComponent', 'MemoryEchoComponent', 'ProcessingEchoComponent']
            )
            
            # Determine file type
            file_type = 'test' if file.name.startswith('test_') else 'core' if 'deep_tree_echo.py' in str(file) else 'extension'
            
            # Check if legacy
            mod_time = file.stat().st_mtime
            status = 'legacy' if mod_time < 1700000000 else 'active'  # Nov 2023 cutoff
            
            # Calculate complexity score
            complexity_score = lines + len(classes) * 10 + len(functions) * 5
            
            return {
                'file': str(file.relative_to(self.repo_path)),
                'lines': lines,
                'classes': classes,
                'functions': functions,
                'imports': imports,
                'uses_echo_base': uses_echo_base,
                'file_type': file_type,
                'status': status,
                'complexity_score': complexity_score,
                'mod_time': mod_time
            }
            
        except Exception as e:
            self.logger.warning(f"Error analyzing {file}: {e}")
            return None
    
    def _estimate_effort(self, fragment: Dict) -> str:
        """Estimate migration effort for a fragment"""
        complexity = fragment.get('complexity_score', 0)
        
        if complexity < 50:
            return 'small'
        elif complexity < 200:
            return 'medium'
        else:
            return 'large'
    
    def _apply_echo_to_analysis(self, analysis_data: Dict, echo_value: float) -> Dict:
        """Apply echo amplification to generate deeper insights"""
        if echo_value < 0.3:
            return analysis_data  # No amplification for low echo values
        
        amplified_insights = {
            'echo_value': echo_value,
            'enhanced_recommendations': [],
            'priority_adjustments': [],
            'additional_tasks': []
        }
        
        # Amplify recommendations based on echo value
        recommendations = analysis_data.get('recommendations', [])
        
        for rec in recommendations:
            if echo_value > 0.7 and rec['priority'] != 'high':
                # Elevate priority for high echo values
                enhanced_rec = rec.copy()
                enhanced_rec['priority'] = 'high'
                enhanced_rec['echo_amplified'] = True
                enhanced_rec['actions'].append('Execute with increased urgency due to echo amplification')
                amplified_insights['enhanced_recommendations'].append(enhanced_rec)
                amplified_insights['priority_adjustments'].append(f"Elevated {rec['title']} to high priority")
        
        # Generate additional tasks for high echo values
        if echo_value > 0.8:
            amplified_insights['additional_tasks'].extend([
                {
                    'task': 'Echo-Amplified Deep Analysis',
                    'description': 'Perform comprehensive system-wide consistency check',
                    'priority': 'high',
                    'echo_generated': True
                },
                {
                    'task': 'Echo-Enhanced Integration Testing',
                    'description': 'Create exhaustive integration test suite',
                    'priority': 'high',
                    'echo_generated': True
                }
            ])
        
        return amplified_insights
    
    def get_analysis_summary(self) -> EchoResponse:
        """Get a summary of the latest analysis results"""
        try:
            if not self.analysis_results:
                return EchoResponse(
                    success=False,
                    message="No analysis results available. Run analysis first."
                )
            
            summary = {
                'fragments_count': len(self.analysis_results.get('fragments', [])),
                'gaps_count': len(self.analysis_results.get('architecture_gaps', [])),
                'tasks_count': len(self.analysis_results.get('migration_tasks', [])),
                'recommendations_count': len(self.analysis_results.get('recommendations', [])),
                'analysis_timestamp': self.analysis_results.get('analysis_timestamp'),
                'top_priorities': []
            }
            
            # Extract top priority items
            gaps = self.analysis_results.get('architecture_gaps', [])
            high_priority_gaps = [g for g in gaps if g['priority'] == 'high']
            summary['top_priorities'] = [g['gap'] for g in high_priority_gaps]
            
            return EchoResponse(
                success=True,
                data=summary,
                message="Analysis summary retrieved"
            )
        except Exception as e:
            return self.handle_error(e, "get_analysis_summary")


# Factory function for easy creation
def create_deep_tree_echo_analyzer(custom_config: Dict = None) -> DeepTreeEchoAnalyzerStandardized:
    """
    Factory function to create a standardized Deep Tree Echo analyzer component.
    
    Args:
        custom_config: Optional custom configuration parameters
        
    Returns:
        Configured DeepTreeEchoAnalyzerStandardized instance
    """
    config = EchoConfig(
        component_name="DeepTreeEchoAnalyzer",
        version="1.0.0",
        echo_threshold=0.7,
        custom_params=custom_config or {}
    )
    
    return DeepTreeEchoAnalyzerStandardized(config)


# Backward compatibility class
class DeepTreeEchoAnalyzer:
    """Backward compatibility wrapper for the original API"""
    
    def __init__(self, repo_path: str = "."):
        self.analyzer = create_deep_tree_echo_analyzer({
            'repo_path': repo_path,
            'analysis_depth': 'full'
        })
        
        # Initialize the component
        init_result = self.analyzer.initialize()
        if not init_result.success:
            raise RuntimeError(f"Failed to initialize analyzer: {init_result.message}")
    
    def run_full_analysis(self) -> Dict:
        """Backward compatibility method"""
        result = self.analyzer.process(None, analysis_type='full')
        if result.success:
            return result.data
        else:
            raise RuntimeError(f"Analysis failed: {result.message}")
    
    def analyze_fragments(self) -> List[Dict]:
        """Backward compatibility method"""
        result = self.run_full_analysis()
        return result.get('fragments', [])
    
    def analyze_architecture_gaps(self) -> List[Dict]:
        """Backward compatibility method"""
        result = self.run_full_analysis()
        return result.get('architecture_gaps', [])
    
    def generate_implementation_plan(self) -> Dict:
        """Backward compatibility method"""
        result = self.run_full_analysis()
        return {
            'tasks': result.get('migration_tasks', []),
            'recommendations': result.get('recommendations', []),
            'summary': {
                'fragments': len(result.get('fragments', [])),
                'gaps': len(result.get('architecture_gaps', [])),
                'priority_tasks': len([t for t in result.get('migration_tasks', []) if t['priority'] == 'high'])
            }
        }


def main():
    """Main function for backward compatibility"""
    print("🌳 Deep Tree Echo Analysis")
    print("=" * 50)
    
    # Create and run analyzer
    analyzer = DeepTreeEchoAnalyzer()
    
    try:
        results = analyzer.run_full_analysis()
        
        print(f"✅ Analysis completed!")
        print(f"   Fragments found: {len(results.get('fragments', []))}")
        print(f"   Architecture gaps: {len(results.get('architecture_gaps', []))}")
        print(f"   Migration tasks: {len(results.get('migration_tasks', []))}")
        print(f"   Recommendations: {len(results.get('recommendations', []))}")
        
        # Show top gaps
        gaps = results.get('architecture_gaps', [])
        high_priority = [g for g in gaps if g['priority'] == 'high']
        
        if high_priority:
            print(f"\n🚨 High Priority Gaps:")
            for gap in high_priority[:3]:
                print(f"   - {gap['gap']}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())