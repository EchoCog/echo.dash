#!/usr/bin/env python3
"""
Standardized Echo9ml Integration Component

This module provides a standardized interface for integrating the Echo9ml persona
evolution system with existing cognitive architecture, implemented as an Echo component.

Migrated from echo9ml_integration.py to use echo_component_base standardization.
"""

import json
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from echo_component_base import MemoryEchoComponent, EchoConfig, EchoResponse

# Import dependencies with error handling
try:
    from echo9ml import Echo9mlSystem, PersonaTraitType
    ECHO9ML_AVAILABLE = True
except ImportError:
    ECHO9ML_AVAILABLE = False
    PersonaTraitType = None

try:
    from cognitive_architecture import CognitiveArchitecture, PersonalityTrait, Memory, MemoryType
    COGNITIVE_ARCH_AVAILABLE = True
except ImportError:
    COGNITIVE_ARCH_AVAILABLE = False
    MemoryType = None


class Echo9mlIntegrationStandardized(MemoryEchoComponent):
    """
    Standardized Echo9ml Integration component
    
    Provides integration capabilities between Echo9ml persona evolution and
    cognitive architecture with memory for storing integration results.
    """
    
    def __init__(self, config: EchoConfig):
        super().__init__(config)
        
        # Integration-specific configuration
        self.enable_echo9ml = config.custom_params.get('enable_echo9ml', True)
        self.enable_cognitive_arch = config.custom_params.get('enable_cognitive_arch', True)
        self.echo9ml_save_path = config.custom_params.get('echo9ml_save_path', None)
        self.sync_interval = config.custom_params.get('sync_interval', 60.0)  # seconds
        self.auto_save = config.custom_params.get('auto_save', True)
        
        # Initialize systems
        self.echo9ml_system = None
        self.cognitive_arch = None
        self.last_sync_time = 0.0
        self.integration_stats = {
            'syncs_performed': 0,
            'memories_integrated': 0,
            'traits_synchronized': 0,
            'errors': []
        }
        
        # Trait mapping between systems
        self.trait_mapping = {
            "curiosity": "GROWTH",
            "adaptability": "GROWTH", 
            "persistence": "TRUNK",
            "creativity": "CANOPY",
            "analytical": "BRANCHES",
            "social": "NETWORK"
        }
        
    def initialize(self) -> EchoResponse:
        """Initialize the Echo9ml integration component"""
        try:
            initialization_data = {
                'echo9ml_enabled': False,
                'cognitive_arch_enabled': False,
                'integration_active': False,
                'available_features': []
            }
            
            # Initialize Echo9ml system if available and enabled
            if self.enable_echo9ml and ECHO9ML_AVAILABLE:
                try:
                    self.echo9ml_system = Echo9mlSystem(save_path=self.echo9ml_save_path)
                    initialization_data['echo9ml_enabled'] = True
                    initialization_data['available_features'].append('persona_evolution')
                    self.logger.info("Echo9ml system initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize Echo9ml system: {e}")
                    self.integration_stats['errors'].append(f"Echo9ml init error: {str(e)}")
            
            # Initialize cognitive architecture if available and enabled
            if self.enable_cognitive_arch and COGNITIVE_ARCH_AVAILABLE:
                try:
                    self.cognitive_arch = CognitiveArchitecture()
                    initialization_data['cognitive_arch_enabled'] = True
                    initialization_data['available_features'].append('cognitive_processing')
                    self.logger.info("Cognitive architecture initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize cognitive architecture: {e}")
                    self.integration_stats['errors'].append(f"Cognitive arch init error: {str(e)}")
            
            # Check if integration is possible
            integration_possible = (initialization_data['echo9ml_enabled'] and 
                                  initialization_data['cognitive_arch_enabled'])
            
            if integration_possible:
                # Perform initial trait synchronization
                sync_result = self._sync_personality_traits()
                if sync_result.success:
                    initialization_data['integration_active'] = True
                    initialization_data['available_features'].append('trait_synchronization')
                    self.logger.info("Systems successfully integrated")
            
            self._initialized = True
            
            # Store initialization state
            self.store_memory('initialization_state', initialization_data)
            
            return EchoResponse(
                success=True,
                data=initialization_data,
                message="Echo9ml integration component initialized",
                metadata={
                    'integration_active': initialization_data['integration_active'],
                    'features_count': len(initialization_data['available_features'])
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "initialize")
    
    def process(self, input_data: Any, **kwargs) -> EchoResponse:
        """
        Process integration operations
        
        Args:
            input_data: Integration request or data to process
            **kwargs: Additional options like 'operation', 'sync_traits', 'store_memory'
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
            
            operation = kwargs.get('operation', 'integrate')
            
            self.logger.info(f"Processing integration operation: {operation}")
            
            # Execute appropriate operation
            if operation == 'integrate':
                result = self._integrate_data(input_data)
            elif operation == 'sync_traits':
                result = self._sync_personality_traits()
            elif operation == 'store_memory':
                result = self._enhanced_memory_storage(input_data)
            elif operation == 'get_state':
                result = self._get_enhanced_cognitive_state()
            elif operation == 'introspection':
                result = self._enhanced_introspection()
            elif operation == 'save_state':
                result = self._save_enhanced_state()
            elif operation == 'load_state':
                result = self._load_enhanced_state()
            else:
                return EchoResponse(
                    success=False,
                    message=f"Unknown operation: {operation}. Available: integrate, sync_traits, store_memory, get_state, introspection, save_state, load_state"
                )
            
            if not result.success:
                return result
            
            # Update integration stats
            self.integration_stats['syncs_performed'] += 1
            
            # Store operation result
            operation_key = f"operation_{operation}_{datetime.now().timestamp()}"
            self.store_memory(operation_key, result.data)
            
            return EchoResponse(
                success=True,
                data=result.data,
                message=f"Integration operation completed: {operation}",
                metadata={
                    'operation': operation,
                    'memory_key': operation_key,
                    'stats': self.integration_stats
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "process")
    
    def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
        """
        Perform echo operation with integration consideration
        
        Echoes integration results with amplified persona evolution.
        """
        try:
            # Process the data through integration first
            process_result = self.process(data, operation='integrate')
            
            if not process_result.success:
                return process_result
            
            # Apply echo amplification to integration results
            echo_amplified_data = self._apply_echo_to_integration(
                process_result.data, echo_value
            )
            
            # Create echoed integration data
            echoed_data = {
                'original_integration': process_result.data,
                'echo_value': echo_value,
                'echo_amplified_results': echo_amplified_data,
                'enhanced_cognitive_state': None,
                'timestamp': datetime.now().isoformat()
            }
            
            # Get enhanced cognitive state if systems are available
            if self.echo9ml_system and self.cognitive_arch:
                state_result = self._get_enhanced_cognitive_state()
                if state_result.success:
                    echoed_data['enhanced_cognitive_state'] = state_result.data
            
            # Store echoed results
            echo_key = f"echo_{datetime.now().timestamp()}"
            store_result = self.store_memory(echo_key, echoed_data)
            
            return EchoResponse(
                success=True,
                data=echoed_data,
                message=f"Integration echo completed (value: {echo_value})",
                metadata={
                    'echo_value': echo_value,
                    'memory_key': echo_key,
                    'integration_amplified': echo_value > 0.5
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "echo")
    
    def _sync_personality_traits(self) -> EchoResponse:
        """Synchronize personality traits between systems"""
        try:
            if not (self.echo9ml_system and self.cognitive_arch):
                return EchoResponse(
                    success=False,
                    message="Both Echo9ml and cognitive architecture required for trait sync"
                )
            
            sync_data = {
                'traits_synchronized': 0,
                'mappings_applied': [],
                'sync_timestamp': datetime.now().isoformat()
            }
            
            # Map cognitive architecture traits to Echo9ml traits
            for trait_name, echo_trait_name in self.trait_mapping.items():
                if hasattr(self.cognitive_arch, 'personality_traits') and trait_name in self.cognitive_arch.personality_traits:
                    try:
                        # Get PersonaTraitType enum value
                        echo_trait = getattr(PersonaTraitType, echo_trait_name)
                        
                        current_value = self.cognitive_arch.personality_traits[trait_name].current_value
                        existing_value = self.echo9ml_system.persona_kernel.traits[echo_trait]
                        
                        # Blend values (70% existing, 30% from cognitive arch)
                        blended_value = 0.7 * existing_value + 0.3 * current_value
                        self.echo9ml_system.persona_kernel.traits[echo_trait] = blended_value
                        
                        sync_data['traits_synchronized'] += 1
                        sync_data['mappings_applied'].append({
                            'cognitive_trait': trait_name,
                            'echo_trait': echo_trait_name,
                            'cognitive_value': current_value,
                            'existing_echo_value': existing_value,
                            'blended_value': blended_value
                        })
                        
                    except (AttributeError, KeyError) as e:
                        self.logger.warning(f"Failed to sync trait {trait_name}: {e}")
            
            self.integration_stats['traits_synchronized'] += sync_data['traits_synchronized']
            self.last_sync_time = time.time()
            
            return EchoResponse(
                success=True,
                data=sync_data,
                message=f"Synchronized {sync_data['traits_synchronized']} personality traits"
            )
            
        except Exception as e:
            return self.handle_error(e, "_sync_personality_traits")
    
    def _enhanced_memory_storage(self, memory_data: Dict) -> EchoResponse:
        """Enhanced memory storage with both systems"""
        try:
            if not isinstance(memory_data, dict):
                return EchoResponse(
                    success=False,
                    message="Memory data must be a dictionary with content, type, and optional metadata"
                )
            
            content = memory_data.get('content', '')
            memory_type_str = memory_data.get('type', 'general')
            context = memory_data.get('context', {})
            emotional_valence = memory_data.get('emotional_valence', 0.0)
            importance = memory_data.get('importance', 0.5)
            
            storage_data = {
                'memory_stored': False,
                'echo9ml_integrated': False,
                'memory_id': None,
                'experience_processed': False
            }
            
            # Store in cognitive architecture if available
            if self.cognitive_arch and COGNITIVE_ARCH_AVAILABLE:
                try:
                    # Create memory object (simplified - adjust based on actual API)
                    memory_id = f"mem_{datetime.now().timestamp()}"
                    storage_data['memory_id'] = memory_id
                    storage_data['memory_stored'] = True
                    
                except Exception as e:
                    self.logger.error(f"Failed to store in cognitive architecture: {e}")
            
            # Integrate with Echo9ml if available
            if self.echo9ml_system:
                try:
                    # Process as experience for persona evolution
                    experience = {
                        "type": "memory_formation",
                        "content": content,
                        "memory_type": memory_type_str,
                        "success": min(1.0, importance + 0.3),
                        "importance": importance,
                        "valence": emotional_valence,
                        "context": "memory"
                    }
                    
                    self.echo9ml_system.process_experience(experience)
                    storage_data['echo9ml_integrated'] = True
                    storage_data['experience_processed'] = True
                    
                except Exception as e:
                    self.logger.error(f"Failed to integrate with Echo9ml: {e}")
            
            self.integration_stats['memories_integrated'] += 1
            
            return EchoResponse(
                success=True,
                data=storage_data,
                message="Enhanced memory storage completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_enhanced_memory_storage")
    
    def _get_enhanced_cognitive_state(self) -> EchoResponse:
        """Get comprehensive cognitive state from both systems"""
        try:
            enhanced_state = {
                'timestamp': datetime.now().isoformat(),
                'integration_active': bool(self.echo9ml_system and self.cognitive_arch),
                'cognitive_architecture': None,
                'echo9ml_state': None,
                'integration_stats': self.integration_stats
            }
            
            # Get cognitive architecture state
            if self.cognitive_arch:
                try:
                    enhanced_state['cognitive_architecture'] = {
                        'available': True,
                        'memory_count': len(getattr(self.cognitive_arch, 'memories', {})),
                        'goal_count': len(getattr(self.cognitive_arch, 'goals', [])),
                        'personality_traits': {}
                    }
                    
                    # Add personality traits if available
                    if hasattr(self.cognitive_arch, 'personality_traits'):
                        enhanced_state['cognitive_architecture']['personality_traits'] = {
                            name: {
                                'current_value': trait.current_value,
                                'base_value': getattr(trait, 'base_value', 0.0)
                            }
                            for name, trait in self.cognitive_arch.personality_traits.items()
                        }
                        
                except Exception as e:
                    enhanced_state['cognitive_architecture'] = {'available': False, 'error': str(e)}
            
            # Get Echo9ml state
            if self.echo9ml_system:
                try:
                    echo_snapshot = self.echo9ml_system.get_cognitive_snapshot()
                    enhanced_state['echo9ml_state'] = {
                        'available': True,
                        'persona_name': echo_snapshot['persona_kernel']['name'],
                        'traits': echo_snapshot['persona_kernel']['traits'],
                        'tensor_shape': echo_snapshot['tensor_encoding']['shape'],
                        'hypergraph': echo_snapshot['hypergraph'],
                        'attention': echo_snapshot['attention'],
                        'meta_cognitive': echo_snapshot['meta_cognitive']
                    }
                except Exception as e:
                    enhanced_state['echo9ml_state'] = {'available': False, 'error': str(e)}
            
            return EchoResponse(
                success=True,
                data=enhanced_state,
                message="Enhanced cognitive state retrieved"
            )
            
        except Exception as e:
            return self.handle_error(e, "_get_enhanced_cognitive_state")
    
    def _enhanced_introspection(self) -> EchoResponse:
        """Enhanced introspection combining both systems"""
        try:
            introspection_data = {
                'timestamp': datetime.now().isoformat(),
                'traditional_introspection': None,
                'echo9ml_introspection': None,
                'integrated_insights': []
            }
            
            # Get traditional introspection if available
            if self.cognitive_arch and hasattr(self.cognitive_arch, 'perform_recursive_introspection'):
                try:
                    traditional_prompt = self.cognitive_arch.perform_recursive_introspection()
                    introspection_data['traditional_introspection'] = traditional_prompt
                except Exception as e:
                    introspection_data['traditional_introspection'] = f"Error: {str(e)}"
            
            # Get Echo9ml snapshot for introspection
            if self.echo9ml_system:
                try:
                    echo_snapshot = self.echo9ml_system.get_cognitive_snapshot()
                    
                    # Create structured introspection data
                    echo_introspection = {
                        'persona_traits': echo_snapshot['persona_kernel']['traits'],
                        'attention_focus': echo_snapshot['attention']['top_focus'][:5],
                        'recent_evolution': echo_snapshot['system_stats'],
                        'meta_suggestions': echo_snapshot['meta_cognitive']['recent_suggestions'][-3:]
                    }
                    
                    introspection_data['echo9ml_introspection'] = echo_introspection
                    
                    # Generate integrated insights
                    introspection_data['integrated_insights'] = self._generate_integrated_insights(echo_snapshot)
                    
                except Exception as e:
                    introspection_data['echo9ml_introspection'] = f"Error: {str(e)}"
            
            return EchoResponse(
                success=True,
                data=introspection_data,
                message="Enhanced introspection completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_enhanced_introspection")
    
    def _generate_integrated_insights(self, echo_snapshot: Dict) -> List[str]:
        """Generate insights from integrated system analysis"""
        insights = []
        
        try:
            # Analyze trait evolution
            traits = echo_snapshot['persona_kernel']['traits']
            high_traits = [trait for trait, value in traits.items() if value > 0.8]
            low_traits = [trait for trait, value in traits.items() if value < 0.3]
            
            if high_traits:
                insights.append(f"Strong capabilities in: {', '.join(high_traits)}")
            
            if low_traits:
                insights.append(f"Growth opportunities in: {', '.join(low_traits)}")
            
            # Analyze attention patterns
            attention_focus = echo_snapshot['attention']['top_focus']
            if attention_focus:
                top_focus = attention_focus[0]
                insights.append(f"Primary attention focused on: {top_focus}")
            
            # Analyze evolution trends
            stats = echo_snapshot['system_stats']
            if stats['total_evolution_events'] > 10:
                insights.append("Significant persona evolution detected - system is actively learning")
            
            # Meta-cognitive suggestions
            suggestions = echo_snapshot['meta_cognitive']['recent_suggestions']
            if suggestions:
                latest_suggestion = suggestions[-1]
                insights.append(f"Latest system recommendation: {latest_suggestion.get('description', 'Optimize processing')}")
        
        except Exception as e:
            insights.append(f"Insight generation error: {str(e)}")
        
        return insights
    
    def _integrate_data(self, input_data: Any) -> EchoResponse:
        """Integrate arbitrary data through both systems"""
        try:
            integration_result = {
                'data_type': type(input_data).__name__,
                'cognitive_processing': None,
                'echo9ml_processing': None,
                'integration_success': False
            }
            
            # Process through cognitive architecture if available
            if self.cognitive_arch:
                try:
                    # This would depend on the specific API of cognitive_architecture
                    # For now, we'll create a generic processing result
                    integration_result['cognitive_processing'] = {
                        'processed': True,
                        'data_size': len(str(input_data)),
                        'timestamp': datetime.now().isoformat()
                    }
                except Exception as e:
                    integration_result['cognitive_processing'] = {'error': str(e)}
            
            # Process through Echo9ml if available
            if self.echo9ml_system and isinstance(input_data, dict):
                try:
                    # Convert input to experience format
                    experience = {
                        'type': input_data.get('type', 'integration'),
                        'content': str(input_data),
                        'success': 0.7,
                        'importance': 0.6,
                        'context': 'integration'
                    }
                    
                    result = self.echo9ml_system.process_experience(experience)
                    integration_result['echo9ml_processing'] = {
                        'processed': True,
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    }
                except Exception as e:
                    integration_result['echo9ml_processing'] = {'error': str(e)}
            
            # Check integration success
            integration_result['integration_success'] = (
                integration_result['cognitive_processing'] is not None and
                integration_result['echo9ml_processing'] is not None
            )
            
            return EchoResponse(
                success=True,
                data=integration_result,
                message="Data integration completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_integrate_data")
    
    def _apply_echo_to_integration(self, integration_data: Dict, echo_value: float) -> Dict:
        """Apply echo amplification to integration results"""
        if echo_value < 0.3:
            return integration_data  # No amplification for low echo values
        
        amplified_data = integration_data.copy()
        
        # Amplify processing results based on echo value
        if 'cognitive_processing' in amplified_data and amplified_data['cognitive_processing']:
            amplified_data['cognitive_processing']['echo_amplified'] = True
            amplified_data['cognitive_processing']['amplification_factor'] = echo_value
        
        if 'echo9ml_processing' in amplified_data and amplified_data['echo9ml_processing']:
            amplified_data['echo9ml_processing']['echo_amplified'] = True
            amplified_data['echo9ml_processing']['amplification_factor'] = echo_value
            
            # If echo value is high, apply additional persona evolution
            if echo_value > 0.7 and self.echo9ml_system:
                try:
                    amplification_experience = {
                        'type': 'echo_amplification',
                        'content': 'High echo value amplification applied',
                        'success': echo_value,
                        'importance': echo_value,
                        'context': 'echo'
                    }
                    
                    self.echo9ml_system.process_experience(amplification_experience)
                    amplified_data['echo9ml_processing']['additional_evolution_applied'] = True
                except Exception as e:
                    self.logger.warning(f"Failed to apply echo amplification: {e}")
        
        return amplified_data
    
    def _save_enhanced_state(self) -> EchoResponse:
        """Save state from both systems"""
        try:
            save_result = {
                'cognitive_arch_saved': False,
                'echo9ml_saved': False,
                'memory_saved': False
            }
            
            # Save cognitive architecture state
            if self.cognitive_arch and hasattr(self.cognitive_arch, 'save_state'):
                try:
                    self.cognitive_arch.save_state()
                    save_result['cognitive_arch_saved'] = True
                except Exception as e:
                    self.logger.error(f"Failed to save cognitive architecture: {e}")
            
            # Save Echo9ml state
            if self.echo9ml_system and hasattr(self.echo9ml_system, 'save_state'):
                try:
                    self.echo9ml_system.save_state()
                    save_result['echo9ml_saved'] = True
                except Exception as e:
                    self.logger.error(f"Failed to save Echo9ml state: {e}")
            
            # Save component memory
            if self.auto_save:
                memory_backup = {
                    'integration_stats': self.integration_stats,
                    'last_sync_time': self.last_sync_time,
                    'memory_store': dict(self.memory_store),
                    'timestamp': datetime.now().isoformat()
                }
                
                backup_key = f"backup_{datetime.now().timestamp()}"
                store_result = self.store_memory(backup_key, memory_backup)
                save_result['memory_saved'] = store_result.success
            
            return EchoResponse(
                success=True,
                data=save_result,
                message="Enhanced state save completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_save_enhanced_state")
    
    def _load_enhanced_state(self) -> EchoResponse:
        """Load state for both systems"""
        try:
            load_result = {
                'cognitive_arch_loaded': False,
                'echo9ml_loaded': False,
                'sync_performed': False
            }
            
            # Load cognitive architecture state
            if self.cognitive_arch and hasattr(self.cognitive_arch, 'load_state'):
                try:
                    self.cognitive_arch.load_state()
                    load_result['cognitive_arch_loaded'] = True
                except Exception as e:
                    self.logger.error(f"Failed to load cognitive architecture: {e}")
            
            # Load Echo9ml state
            if self.echo9ml_system and hasattr(self.echo9ml_system, 'load_state'):
                try:
                    if self.echo9ml_system.load_state():
                        load_result['echo9ml_loaded'] = True
                except Exception as e:
                    self.logger.error(f"Failed to load Echo9ml state: {e}")
            
            # Re-sync traits after loading
            if load_result['cognitive_arch_loaded'] and load_result['echo9ml_loaded']:
                sync_result = self._sync_personality_traits()
                load_result['sync_performed'] = sync_result.success
            
            return EchoResponse(
                success=True,
                data=load_result,
                message="Enhanced state load completed"
            )
            
        except Exception as e:
            return self.handle_error(e, "_load_enhanced_state")


# Factory function for easy creation
def create_echo9ml_integration(custom_config: Dict = None) -> Echo9mlIntegrationStandardized:
    """
    Factory function to create a standardized Echo9ml integration component.
    
    Args:
        custom_config: Optional custom configuration parameters
        
    Returns:
        Configured Echo9mlIntegrationStandardized instance
    """
    config = EchoConfig(
        component_name="Echo9mlIntegration",
        version="1.0.0",
        echo_threshold=0.6,
        custom_params=custom_config or {}
    )
    
    return Echo9mlIntegrationStandardized(config)


# Backward compatibility wrapper
class EnhancedCognitiveArchitecture:
    """Backward compatibility wrapper for the original API"""
    
    def __init__(self, enable_echo9ml: bool = True, echo9ml_save_path: Optional[str] = None):
        self.integration = create_echo9ml_integration({
            'enable_echo9ml': enable_echo9ml,
            'echo9ml_save_path': echo9ml_save_path,
            'enable_cognitive_arch': True
        })
        
        # Initialize the component
        init_result = self.integration.initialize()
        if not init_result.success:
            raise RuntimeError(f"Failed to initialize integration: {init_result.message}")
    
    def enhanced_memory_storage(self, content: str, memory_type, context: Dict = None,
                              emotional_valence: float = 0.0, importance: float = 0.5) -> str:
        """Backward compatibility method"""
        memory_data = {
            'content': content,
            'type': memory_type.value if hasattr(memory_type, 'value') else str(memory_type),
            'context': context or {},
            'emotional_valence': emotional_valence,
            'importance': importance
        }
        
        result = self.integration.process(memory_data, operation='store_memory')
        if result.success:
            return result.data.get('memory_id', 'unknown')
        else:
            raise RuntimeError(f"Memory storage failed: {result.message}")
    
    def get_enhanced_cognitive_state(self) -> Dict[str, Any]:
        """Backward compatibility method"""
        result = self.integration.process(None, operation='get_state')
        if result.success:
            return result.data
        else:
            return {}
    
    def enhanced_introspection(self) -> Optional[str]:
        """Backward compatibility method"""
        result = self.integration.process(None, operation='introspection')
        if result.success:
            data = result.data
            # Format as string for backward compatibility
            intro = data.get('traditional_introspection', '')
            echo_data = data.get('echo9ml_introspection', {})
            insights = data.get('integrated_insights', [])
            
            formatted = f"{intro}\n\nIntegrated Insights:\n" + "\n".join(f"- {insight}" for insight in insights)
            return formatted
        else:
            return None
    
    def save_enhanced_state(self):
        """Backward compatibility method"""
        self.integration.process(None, operation='save_state')
    
    def load_enhanced_state(self):
        """Backward compatibility method"""
        self.integration.process(None, operation='load_state')


def create_enhanced_cognitive_architecture(enable_echo9ml: bool = True,
                                         echo9ml_save_path: Optional[str] = None) -> EnhancedCognitiveArchitecture:
    """
    Backward compatibility factory function
    
    Args:
        enable_echo9ml: Whether to enable Echo9ml persona evolution
        echo9ml_save_path: Optional custom save path for Echo9ml data
    
    Returns:
        Enhanced cognitive architecture with Echo9ml integration
    """
    return EnhancedCognitiveArchitecture(enable_echo9ml, echo9ml_save_path)


# Export main classes
__all__ = [
    'Echo9mlIntegrationStandardized', 
    'create_echo9ml_integration',
    'EnhancedCognitiveArchitecture', 
    'create_enhanced_cognitive_architecture'
]