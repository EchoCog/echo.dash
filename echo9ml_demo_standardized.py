#!/usr/bin/env python3
"""
Standardized Echo9ml Demo Component

This module provides a standardized interface for demonstrating the Deep Tree Echo
persona evolution system, implemented as an Echo component with consistent APIs.

Migrated from echo9ml_demo.py to use echo_component_base standardization.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

from echo_component_base import MemoryEchoComponent, EchoConfig, EchoResponse

# Import echo9ml system (with error handling for missing dependencies)
try:
    from echo9ml import create_echo9ml_system, PersonaTraitType
    ECHO9ML_AVAILABLE = True
except ImportError:
    ECHO9ML_AVAILABLE = False
    PersonaTraitType = None


class Echo9mlDemoStandardized(MemoryEchoComponent):
    """
    Standardized Echo9ml Demo component
    
    Provides demonstration capabilities for the Deep Tree Echo persona evolution system
    with memory for storing demo results and learning progressions.
    """
    
    def __init__(self, config: EchoConfig):
        super().__init__(config)
        
        # Demo-specific configuration
        self.demo_types = config.custom_params.get('demo_types', ['basic', 'learning', 'creativity', 'adaptation'])
        self.save_results = config.custom_params.get('save_results', True)
        self.results_file = config.custom_params.get('results_file', 'echo9ml_demo_results.json')
        
        # Initialize echo9ml system if available
        self.echo9ml_system = None
        self.demo_results = {}
        
    def initialize(self) -> EchoResponse:
        """Initialize the Echo9ml demo component"""
        try:
            if not ECHO9ML_AVAILABLE:
                return EchoResponse(
                    success=False,
                    message="Echo9ml system not available - missing dependencies"
                )
            
            # Initialize echo9ml system
            self.echo9ml_system = create_echo9ml_system()
            self._initialized = True
            
            self.logger.info("Echo9ml demo initialized with persona: {}".format(
                self.echo9ml_system.persona_kernel.name
            ))
            
            # Store initial state
            initial_state = self._get_persona_state()
            self.store_memory('initial_state', initial_state)
            
            return EchoResponse(
                success=True,
                data=initial_state,
                message="Echo9ml demo component initialized",
                metadata={
                    'persona_name': self.echo9ml_system.persona_kernel.name,
                    'demo_types_available': self.demo_types
                }
            )
        except Exception as e:
            return self.handle_error(e, "initialize")
    
    def process(self, input_data: Any, **kwargs) -> EchoResponse:
        """
        Process Echo9ml demo request
        
        Args:
            input_data: Demo configuration or experience data
            **kwargs: Additional options like 'demo_type', 'experience_data'
        """
        try:
            if not self._initialized:
                return EchoResponse(
                    success=False,
                    message="Component not initialized"
                )
            
            validation = self.validate_input(input_data)
            if not validation.success:
                return validation
            
            demo_type = kwargs.get('demo_type', 'basic')
            
            self.logger.info(f"Processing Echo9ml demo: {demo_type}")
            
            # Execute appropriate demo based on type
            if demo_type == 'basic':
                result = self._demonstrate_basic_usage(input_data)
            elif demo_type == 'learning':
                result = self._demonstrate_learning_progression(input_data)
            elif demo_type == 'creativity':
                result = self._demonstrate_creativity(input_data)
            elif demo_type == 'adaptation':
                result = self._demonstrate_adaptation(input_data)
            elif demo_type == 'experience':
                result = self._process_custom_experience(input_data)
            else:
                return EchoResponse(
                    success=False,
                    message=f"Unknown demo type: {demo_type}. Available: {self.demo_types}"
                )
            
            if not result.success:
                return result
            
            # Store demo results
            demo_key = f"demo_{demo_type}_{datetime.now().timestamp()}"
            self.store_memory(demo_key, result.data)
            
            # Update results collection
            if demo_type not in self.demo_results:
                self.demo_results[demo_type] = []
            self.demo_results[demo_type].append(result.data)
            
            return EchoResponse(
                success=True,
                data=result.data,
                message=f"Echo9ml demo completed: {demo_type}",
                metadata={
                    'demo_type': demo_type,
                    'memory_key': demo_key,
                    'total_demos_run': len(self.demo_results.get(demo_type, []))
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "process")
    
    def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
        """
        Perform echo operation with Echo9ml demo consideration
        
        Echoes demo results with persona evolution based on echo value.
        """
        try:
            # Process the data to get fresh demo results
            process_result = self.process(data, demo_type='experience')
            
            if not process_result.success:
                return process_result
            
            # Apply echo value to persona evolution
            echo_amplified_data = self._apply_echo_to_persona(
                process_result.data, echo_value
            )
            
            # Create echoed demo data
            echoed_data = {
                'original_demo': process_result.data,
                'echo_value': echo_value,
                'echo_amplified_evolution': echo_amplified_data,
                'persona_state_post_echo': self._get_persona_state(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Store echoed results
            echo_key = f"echo_{datetime.now().timestamp()}"
            store_result = self.store_memory(echo_key, echoed_data)
            
            return EchoResponse(
                success=True,
                data=echoed_data,
                message=f"Echo9ml demo echo completed (value: {echo_value})",
                metadata={
                    'echo_value': echo_value,
                    'memory_key': echo_key,
                    'persona_evolution_applied': echo_value > 0.3
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "echo")
    
    def _demonstrate_basic_usage(self, input_data: Any) -> EchoResponse:
        """Demonstrate basic echo9ml system usage"""
        try:
            demo_data = {
                'type': 'basic_usage',
                'initial_traits': dict(self.echo9ml_system.persona_kernel.traits),
                'tensor_shape': self.echo9ml_system.tensor_encoding.tensor_shape,
                'experience_processed': None,
                'results': {}
            }
            
            # Process a default experience or use provided data
            if isinstance(input_data, dict) and 'experience' in input_data:
                experience = input_data['experience']
            else:
                experience = {
                    "type": "learning",
                    "content": "Understanding tensor mathematics",
                    "success": 0.8,
                    "importance": 0.7,
                    "novelty": 0.6
                }
            
            demo_data['experience_processed'] = experience
            
            # Process the experience
            result = self.echo9ml_system.process_experience(experience)
            demo_data['results'] = result
            
            # Get updated state
            demo_data['final_traits'] = dict(self.echo9ml_system.persona_kernel.traits)
            
            # Calculate changes
            trait_changes = {}
            for trait, final_value in demo_data['final_traits'].items():
                initial_value = demo_data['initial_traits'][trait]
                trait_changes[trait.value] = final_value - initial_value
            demo_data['trait_changes'] = trait_changes
            
            return EchoResponse(
                success=True,
                data=demo_data,
                message="Basic usage demonstration completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_demonstrate_basic_usage")
    
    def _demonstrate_learning_progression(self, input_data: Any) -> EchoResponse:
        """Demonstrate persona evolution through learning progression"""
        try:
            # Use provided learning stages or default ones
            if isinstance(input_data, dict) and 'learning_stages' in input_data:
                learning_stages = input_data['learning_stages']
            else:
                learning_stages = [
                    {"stage": "Beginner", "success": 0.3, "difficulty": 0.9, "novelty": 0.9},
                    {"stage": "Learning", "success": 0.5, "difficulty": 0.7, "novelty": 0.7},
                    {"stage": "Improving", "success": 0.7, "difficulty": 0.6, "novelty": 0.5},
                    {"stage": "Competent", "success": 0.8, "difficulty": 0.5, "novelty": 0.3},
                    {"stage": "Expert", "success": 0.9, "difficulty": 0.4, "novelty": 0.1}
                ]
            
            demo_data = {
                'type': 'learning_progression',
                'initial_traits': dict(self.echo9ml_system.persona_kernel.traits),
                'learning_stages': learning_stages,
                'progression_results': [],
                'evolution_summary': {}
            }
            
            # Track key traits
            initial_reasoning = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.BRANCHES]
            initial_memory = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.ROOTS]
            
            # Process each learning stage
            for stage_data in learning_stages:
                experience = {
                    "type": "learning",
                    "content": f"{stage_data['stage']} level learning",
                    "success": stage_data["success"],
                    "difficulty": stage_data.get("difficulty", 0.5),
                    "novelty": stage_data.get("novelty", 0.5),
                    "importance": 0.8,
                    "traits_used": [PersonaTraitType.BRANCHES, PersonaTraitType.ROOTS, PersonaTraitType.GROWTH]
                }
                
                result = self.echo9ml_system.process_experience(experience)
                
                reasoning = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.BRANCHES]
                memory = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.ROOTS]
                
                stage_result = {
                    'stage': stage_data['stage'],
                    'experience': experience,
                    'reasoning_value': reasoning,
                    'memory_value': memory,
                    'reasoning_change': reasoning - initial_reasoning,
                    'memory_change': memory - initial_memory,
                    'process_result': result
                }
                
                demo_data['progression_results'].append(stage_result)
            
            # Calculate evolution summary
            final_reasoning = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.BRANCHES]
            final_memory = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.ROOTS]
            
            demo_data['evolution_summary'] = {
                'total_reasoning_improvement': final_reasoning - initial_reasoning,
                'total_memory_improvement': final_memory - initial_memory,
                'stages_completed': len(learning_stages),
                'final_traits': dict(self.echo9ml_system.persona_kernel.traits)
            }
            
            return EchoResponse(
                success=True,
                data=demo_data,
                message=f"Learning progression demonstration completed ({len(learning_stages)} stages)"
            )
            
        except Exception as e:
            return self.handle_error(e, "_demonstrate_learning_progression")
    
    def _demonstrate_creativity(self, input_data: Any) -> EchoResponse:
        """Demonstrate creative capabilities"""
        try:
            creative_experiences = [
                {
                    "type": "creative",
                    "content": "Generating novel artistic concepts",
                    "success": 0.7,
                    "novelty": 0.9,
                    "importance": 0.6,
                    "traits_used": [PersonaTraitType.CANOPY, PersonaTraitType.LEAVES, PersonaTraitType.GROWTH]
                },
                {
                    "type": "creative",
                    "content": "Innovative problem solving approach", 
                    "success": 0.8,
                    "novelty": 0.8,
                    "importance": 0.7,
                    "traits_used": [PersonaTraitType.BRANCHES, PersonaTraitType.CANOPY]
                },
                {
                    "type": "creative",
                    "content": "Cross-domain pattern recognition",
                    "success": 0.9,
                    "novelty": 0.7,
                    "importance": 0.8,
                    "traits_used": [PersonaTraitType.CANOPY, PersonaTraitType.NETWORK, PersonaTraitType.BRANCHES]
                }
            ]
            
            demo_data = {
                'type': 'creativity_demonstration',
                'initial_creativity': self.echo9ml_system.persona_kernel.traits[PersonaTraitType.CANOPY],
                'creative_experiences': [],
                'creativity_evolution': {}
            }
            
            for experience in creative_experiences:
                result = self.echo9ml_system.process_experience(experience)
                creativity_value = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.CANOPY]
                
                demo_data['creative_experiences'].append({
                    'experience': experience,
                    'result': result,
                    'creativity_after': creativity_value
                })
            
            demo_data['creativity_evolution'] = {
                'initial_creativity': demo_data['initial_creativity'],
                'final_creativity': self.echo9ml_system.persona_kernel.traits[PersonaTraitType.CANOPY],
                'total_improvement': (self.echo9ml_system.persona_kernel.traits[PersonaTraitType.CANOPY] - 
                                    demo_data['initial_creativity'])
            }
            
            return EchoResponse(
                success=True,
                data=demo_data,
                message="Creativity demonstration completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_demonstrate_creativity")
    
    def _demonstrate_adaptation(self, input_data: Any) -> EchoResponse:
        """Demonstrate adaptive capabilities"""
        try:
            # Simulate changing environment requiring adaptation
            adaptation_scenarios = [
                {
                    "scenario": "Environment change",
                    "difficulty": 0.8,
                    "novelty": 0.9,
                    "success_threshold": 0.6
                },
                {
                    "scenario": "Resource constraints", 
                    "difficulty": 0.7,
                    "novelty": 0.6,
                    "success_threshold": 0.7
                },
                {
                    "scenario": "New requirements",
                    "difficulty": 0.6,
                    "novelty": 0.8,
                    "success_threshold": 0.8
                }
            ]
            
            demo_data = {
                'type': 'adaptation_demonstration',
                'initial_adaptability': self.echo9ml_system.persona_kernel.traits[PersonaTraitType.GROWTH],
                'adaptation_results': [],
                'adaptation_summary': {}
            }
            
            for scenario in adaptation_scenarios:
                experience = {
                    "type": "adaptation",
                    "content": f"Adapting to {scenario['scenario']}",
                    "difficulty": scenario['difficulty'],
                    "novelty": scenario['novelty'],
                    "success": min(0.9, scenario['success_threshold'] + 
                                 self.echo9ml_system.persona_kernel.traits[PersonaTraitType.GROWTH] * 0.3),
                    "importance": 0.8,
                    "traits_used": [PersonaTraitType.GROWTH, PersonaTraitType.BRANCHES, PersonaTraitType.TRUNK]
                }
                
                result = self.echo9ml_system.process_experience(experience)
                adaptability_after = self.echo9ml_system.persona_kernel.traits[PersonaTraitType.GROWTH]
                
                demo_data['adaptation_results'].append({
                    'scenario': scenario,
                    'experience': experience,
                    'result': result,
                    'adaptability_after': adaptability_after
                })
            
            demo_data['adaptation_summary'] = {
                'initial_adaptability': demo_data['initial_adaptability'],
                'final_adaptability': self.echo9ml_system.persona_kernel.traits[PersonaTraitType.GROWTH],
                'total_improvement': (self.echo9ml_system.persona_kernel.traits[PersonaTraitType.GROWTH] -
                                    demo_data['initial_adaptability']),
                'scenarios_completed': len(adaptation_scenarios)
            }
            
            return EchoResponse(
                success=True,
                data=demo_data,
                message="Adaptation demonstration completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_demonstrate_adaptation")
    
    def _process_custom_experience(self, input_data: Any) -> EchoResponse:
        """Process a custom experience provided by the user"""
        try:
            if not isinstance(input_data, dict):
                return EchoResponse(
                    success=False,
                    message="Custom experience must be a dictionary"
                )
            
            # Validate required experience fields
            required_fields = ['type', 'content']
            for field in required_fields:
                if field not in input_data:
                    return EchoResponse(
                        success=False,
                        message=f"Missing required field: {field}"
                    )
            
            # Set defaults for optional fields
            experience = {
                'type': input_data['type'],
                'content': input_data['content'],
                'success': input_data.get('success', 0.5),
                'importance': input_data.get('importance', 0.5),
                'novelty': input_data.get('novelty', 0.5),
                'difficulty': input_data.get('difficulty', 0.5),
                'traits_used': input_data.get('traits_used', [PersonaTraitType.BRANCHES])
            }
            
            initial_state = self._get_persona_state()
            result = self.echo9ml_system.process_experience(experience)
            final_state = self._get_persona_state()
            
            demo_data = {
                'type': 'custom_experience',
                'experience': experience,
                'initial_state': initial_state,
                'process_result': result,
                'final_state': final_state,
                'trait_changes': {
                    trait.value: final_state['traits'][trait] - initial_state['traits'][trait]
                    for trait in PersonaTraitType
                }
            }
            
            return EchoResponse(
                success=True,
                data=demo_data,
                message="Custom experience processed successfully"
            )
            
        except Exception as e:
            return self.handle_error(e, "_process_custom_experience")
    
    def _get_persona_state(self) -> Dict:
        """Get current persona state"""
        if not self.echo9ml_system:
            return {}
        
        return {
            'name': self.echo9ml_system.persona_kernel.name,
            'traits': dict(self.echo9ml_system.persona_kernel.traits),
            'tensor_shape': self.echo9ml_system.tensor_encoding.tensor_shape,
            'evolution_params': self.echo9ml_system.persona_kernel.evolution
        }
    
    def _apply_echo_to_persona(self, demo_data: Dict, echo_value: float) -> Dict:
        """Apply echo value to amplify persona evolution"""
        if echo_value < 0.3:
            return demo_data  # No amplification for low echo values
        
        # Amplify trait changes based on echo value
        amplified_changes = {}
        trait_changes = demo_data.get('trait_changes', {})
        
        for trait_name, change in trait_changes.items():
            # Amplify positive changes more than negative ones
            if change > 0:
                amplified_change = change * (1 + echo_value)
            else:
                amplified_change = change * (1 + echo_value * 0.5)
            
            amplified_changes[trait_name] = amplified_change
            
            # Apply amplified change to actual persona (if echo value is high enough)
            if echo_value > 0.7:
                try:
                    trait_type = next(t for t in PersonaTraitType if t.value == trait_name)
                    current_value = self.echo9ml_system.persona_kernel.traits[trait_type]
                    new_value = max(0.0, min(1.0, current_value + (amplified_change - change)))
                    self.echo9ml_system.persona_kernel.traits[trait_type] = new_value
                except (StopIteration, KeyError):
                    pass  # Skip if trait not found
        
        return {
            'original_changes': trait_changes,
            'amplified_changes': amplified_changes,
            'echo_value': echo_value,
            'changes_applied_to_persona': echo_value > 0.7
        }
    
    def save_demo_results(self) -> EchoResponse:
        """Save all demo results to file"""
        try:
            if not self.save_results:
                return EchoResponse(
                    success=False,
                    message="Result saving is disabled in configuration"
                )
            
            results_data = {
                'timestamp': datetime.now().isoformat(),
                'persona_name': self.echo9ml_system.persona_kernel.name if self.echo9ml_system else 'Unknown',
                'demo_results': self.demo_results,
                'memory_stats': self.memory_stats
            }
            
            results_path = Path(self.results_file)
            with open(results_path, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            return EchoResponse(
                success=True,
                data={'file_path': str(results_path), 'results_count': len(self.demo_results)},
                message=f"Demo results saved to {results_path}"
            )
            
        except Exception as e:
            return self.handle_error(e, "save_demo_results")


# Factory function for easy creation
def create_echo9ml_demo(custom_config: Dict = None) -> Echo9mlDemoStandardized:
    """
    Factory function to create a standardized Echo9ml demo component.
    
    Args:
        custom_config: Optional custom configuration parameters
        
    Returns:
        Configured Echo9mlDemoStandardized instance
    """
    config = EchoConfig(
        component_name="Echo9mlDemo",
        version="1.0.0", 
        echo_threshold=0.5,
        custom_params=custom_config or {}
    )
    
    return Echo9mlDemoStandardized(config)


# Backward compatibility functions from original demo
def demonstrate_basic_usage():
    """Backward compatibility function for basic usage demonstration"""
    demo = create_echo9ml_demo()
    
    init_result = demo.initialize()
    if not init_result.success:
        print(f"❌ Initialization failed: {init_result.message}")
        return
    
    result = demo.process(None, demo_type='basic')
    if result.success:
        print("=" * 60)
        print("Echo9ml Basic Usage Demonstration") 
        print("=" * 60)
        
        data = result.data
        print(f"✅ Processed experience: {data.get('experience_processed', {}).get('content', 'N/A')}")
        print(f"   Trait changes:")
        for trait, change in data.get('trait_changes', {}).items():
            if abs(change) > 0.001:
                print(f"     {trait}: {change:+.3f}")


def demonstrate_learning_progression():
    """Backward compatibility function for learning progression demonstration"""
    demo = create_echo9ml_demo()
    
    init_result = demo.initialize()
    if not init_result.success:
        print(f"❌ Initialization failed: {init_result.message}")
        return
    
    result = demo.process(None, demo_type='learning')
    if result.success:
        print("\n" + "=" * 60)
        print("Learning Progression Demonstration")
        print("=" * 60)
        
        data = result.data
        summary = data.get('evolution_summary', {})
        print(f"🎓 Learning completed! Total improvements:")
        print(f"   Reasoning: {summary.get('total_reasoning_improvement', 0):+.3f}")
        print(f"   Memory: {summary.get('total_memory_improvement', 0):+.3f}")


def main():
    """Main function for backward compatibility"""
    if not ECHO9ML_AVAILABLE:
        print("❌ Echo9ml system not available - missing dependencies")
        print("Please ensure echo9ml.py is available and dependencies are installed")
        return 1
    
    # Run demonstrations
    demonstrate_basic_usage()
    demonstrate_learning_progression()
    
    print("\n" + "=" * 60)
    print("✅ Echo9ml demonstrations completed!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())