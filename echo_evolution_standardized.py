#!/usr/bin/env python3
"""
Standardized Echo Evolution Component

This module provides a standardized interface for the Echo evolution system,
implemented as an Echo component with consistent APIs and response handling.

Migrated from echo_evolution.py to use echo_component_base standardization.
"""

import asyncio
import random
import json
import os
import time
import threading
from datetime import datetime
from queue import Queue
from typing import Dict, List, Any, Optional, Union, Tuple

# Optional import for system metrics
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from echo_component_base import MemoryEchoComponent, EchoConfig, EchoResponse

# Constants
DEFAULT_POLL_INTERVAL = 1.0  # seconds
DEFAULT_ERROR_THRESHOLD = 0.1  # 10% error rate  
DEFAULT_EVOLUTION_CYCLES = 5
DEFAULT_IMPROVEMENT_RANGE = (-0.1, 0.5)  # Random improvement range


class EchoEvolutionStandardized(MemoryEchoComponent):
    """
    Standardized Echo Evolution component
    
    Provides self-evolution capabilities with memory for storing evolution history
    and agent states. Inherits from MemoryEchoComponent for persistent storage.
    """
    
    def __init__(self, config: EchoConfig):
        super().__init__(config)
        
        # Evolution-specific configuration
        self.max_agents = config.custom_params.get('max_agents', 10)
        self.evolution_cycles = config.custom_params.get('evolution_cycles', DEFAULT_EVOLUTION_CYCLES)
        self.poll_interval = config.custom_params.get('poll_interval', DEFAULT_POLL_INTERVAL)
        self.error_threshold = config.custom_params.get('error_threshold', DEFAULT_ERROR_THRESHOLD)
        self.improvement_range = config.custom_params.get('improvement_range', DEFAULT_IMPROVEMENT_RANGE)
        
        # Evolution state
        self.agents = {}
        self.evolution_cycles_completed = 0
        self.system_metrics_history = []
        self.emitter_values = {}
        self.running = False
        self.evolution_task = None
        
    def initialize(self) -> EchoResponse:
        """Initialize the Echo evolution component"""
        try:
            self._initialized = True
            
            # Initialize evolution memory
            initial_memory = {
                'agents': {},
                'cycles': [],
                'system_metrics': [],
                'evolution_stats': {
                    'total_cycles': 0,
                    'total_agents_created': 0,
                    'average_improvement': 0.0,
                    'last_evolution': None
                }
            }
            
            self.store_memory('evolution_memory', initial_memory)
            
            self.logger.info(f"Echo evolution system initialized")
            
            return EchoResponse(
                success=True,
                data={
                    'max_agents': self.max_agents,
                    'evolution_cycles': self.evolution_cycles,
                    'poll_interval': self.poll_interval,
                    'error_threshold': self.error_threshold
                },
                message="Echo evolution component initialized"
            )
        except Exception as e:
            return self.handle_error(e, "initialize")
    
    def process(self, input_data: Any, **kwargs) -> EchoResponse:
        """
        Process evolution operations
        
        Args:
            input_data: Evolution request or agent data
            **kwargs: Additional options like 'operation', 'agent_name', 'cycles'
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
            
            operation = kwargs.get('operation', 'evolve')
            
            self.logger.info(f"Processing evolution operation: {operation}")
            
            # Execute appropriate operation
            if operation == 'evolve':
                result = self._run_evolution(input_data, kwargs)
            elif operation == 'create_agent':
                result = self._create_agent(input_data)
            elif operation == 'get_agent_status':
                result = self._get_agent_status(kwargs.get('agent_name'))
            elif operation == 'get_evolution_history':
                result = self._get_evolution_history()
            elif operation == 'start_continuous':
                result = self._start_continuous_evolution()
            elif operation == 'stop_continuous':
                result = self._stop_continuous_evolution()
            elif operation == 'get_system_metrics':
                result = self._get_system_metrics()
            else:
                return EchoResponse(
                    success=False,
                    message=f"Unknown operation: {operation}. Available: evolve, create_agent, get_agent_status, get_evolution_history, start_continuous, stop_continuous, get_system_metrics"
                )
            
            if not result.success:
                return result
            
            # Store operation result
            operation_key = f"operation_{operation}_{datetime.now().timestamp()}"
            self.store_memory(operation_key, result.data)
            
            return EchoResponse(
                success=True,
                data=result.data,
                message=f"Evolution operation completed: {operation}",
                metadata={
                    'operation': operation,
                    'memory_key': operation_key,
                    'agents_count': len(self.agents)
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "process")
    
    def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
        """
        Perform echo operation with evolution consideration
        
        Echoes evolution results with amplified improvement based on echo value.
        """
        try:
            # Process evolution with echo amplification
            amplified_cycles = max(1, int(self.evolution_cycles * (1 + echo_value)))
            
            process_result = self.process(data, operation='evolve', cycles=amplified_cycles)
            
            if not process_result.success:
                return process_result
            
            # Apply echo amplification to agents
            echo_amplified_data = self._apply_echo_to_evolution(
                process_result.data, echo_value
            )
            
            # Create echoed evolution data
            echoed_data = {
                'original_evolution': process_result.data,
                'echo_value': echo_value,
                'amplified_cycles': amplified_cycles,
                'echo_amplified_agents': echo_amplified_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store echoed results
            echo_key = f"echo_{datetime.now().timestamp()}"
            store_result = self.store_memory(echo_key, echoed_data)
            
            return EchoResponse(
                success=True,
                data=echoed_data,
                message=f"Evolution echo completed (value: {echo_value})",
                metadata={
                    'echo_value': echo_value,
                    'amplified_cycles': amplified_cycles,
                    'memory_key': echo_key,
                    'evolution_amplified': echo_value > 0.3
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "echo")
    
    def _run_evolution(self, input_data: Any, kwargs: Dict) -> EchoResponse:
        """Run evolution cycles"""
        try:
            cycles = kwargs.get('cycles', self.evolution_cycles)
            
            # Create default agents if none exist
            if not self.agents:
                default_agents = [
                    {"name": "Differential Gear", "domain": "coordination"},
                    {"name": "Proximity Sensor", "domain": "awareness"}, 
                    {"name": "Adaptive Filter", "domain": "optimization"}
                ]
                
                for agent_data in default_agents:
                    self._create_agent(agent_data)
            
            evolution_data = {
                'cycles_requested': cycles,
                'cycles_completed': 0,
                'agent_results': [],
                'system_metrics': [],
                'start_time': datetime.now().isoformat(),
                'end_time': None
            }
            
            # Run evolution cycles
            for cycle in range(cycles):
                cycle_start = time.time()
                
                # Get current system metrics
                system_metrics = self._collect_system_metrics()
                evolution_data['system_metrics'].append(system_metrics)
                
                # Get constraints from all agents for cross-influence
                constraints = [agent['state'] for agent in self.agents.values()]
                
                # Evolve each agent
                cycle_results = []
                for agent_name, agent in self.agents.items():
                    # Get constraints from other agents
                    other_constraints = [
                        other_agent['state'] for other_name, other_agent in self.agents.items()
                        if other_name != agent_name
                    ]
                    
                    # Evolve agent
                    new_state = self._evolve_agent(agent, other_constraints, system_metrics)
                    
                    cycle_results.append({
                        'agent_name': agent_name,
                        'previous_state': agent['state'],
                        'new_state': new_state,
                        'improvement': new_state - agent['state'],
                        'iteration': agent['iteration']
                    })
                    
                    # Update emitter values
                    self.emitter_values[agent_name] = new_state
                
                evolution_data['agent_results'].append({
                    'cycle': cycle,
                    'results': cycle_results,
                    'duration': time.time() - cycle_start
                })
                
                evolution_data['cycles_completed'] += 1
                
                # Small delay between cycles
                time.sleep(0.1)
            
            evolution_data['end_time'] = datetime.now().isoformat()
            
            # Update global stats
            self.evolution_cycles_completed += cycles
            
            # Update evolution memory
            memory_result = self.retrieve_memory('evolution_memory')
            if memory_result.success:
                evolution_memory = memory_result.data
                evolution_memory['cycles'].append(evolution_data)
                evolution_memory['evolution_stats']['total_cycles'] += cycles
                evolution_memory['evolution_stats']['last_evolution'] = datetime.now().isoformat()
                
                # Calculate average improvement
                all_improvements = [
                    result['improvement'] 
                    for cycle_data in evolution_data['agent_results']
                    for result in cycle_data['results']
                ]
                if all_improvements:
                    avg_improvement = sum(all_improvements) / len(all_improvements)
                    evolution_memory['evolution_stats']['average_improvement'] = avg_improvement
                
                self.store_memory('evolution_memory', evolution_memory)
            
            return EchoResponse(
                success=True,
                data=evolution_data,
                message=f"Evolution completed: {cycles} cycles"
            )
            
        except Exception as e:
            return self.handle_error(e, "_run_evolution")
    
    def _create_agent(self, agent_data: Any) -> EchoResponse:
        """Create a new evolution agent"""
        try:
            if not isinstance(agent_data, dict):
                return EchoResponse(
                    success=False,
                    message="Agent data must be a dictionary with 'name' and 'domain'"
                )
            
            name = agent_data.get('name')
            domain = agent_data.get('domain', 'general')
            
            if not name:
                return EchoResponse(
                    success=False,
                    message="Agent name is required"
                )
            
            if name in self.agents:
                return EchoResponse(
                    success=False,
                    message=f"Agent {name} already exists"
                )
            
            if len(self.agents) >= self.max_agents:
                return EchoResponse(
                    success=False,
                    message=f"Maximum number of agents ({self.max_agents}) reached"
                )
            
            # Create agent
            agent = {
                'name': name,
                'domain': domain,
                'state': agent_data.get('initial_state', 0.0),
                'iteration': 0,
                'error_count': 0,
                'job_count': 0,
                'poll_interval': agent_data.get('poll_interval', self.poll_interval),
                'error_threshold': agent_data.get('error_threshold', self.error_threshold),
                'created_at': datetime.now().isoformat(),
                'history': []
            }
            
            self.agents[name] = agent
            
            # Update evolution memory
            memory_result = self.retrieve_memory('evolution_memory')
            if memory_result.success:
                evolution_memory = memory_result.data
                evolution_memory['agents'][name] = agent.copy()
                evolution_memory['evolution_stats']['total_agents_created'] += 1
                self.store_memory('evolution_memory', evolution_memory)
            
            return EchoResponse(
                success=True,
                data=agent,
                message=f"Agent {name} created successfully"
            )
            
        except Exception as e:
            return self.handle_error(e, "_create_agent")
    
    def _evolve_agent(self, agent: Dict, constraints: List[float], system_metrics: Dict) -> float:
        """Evolve a single agent based on constraints and system state"""
        try:
            # Calculate random improvement factor (innovation)
            improvement = random.uniform(*self.improvement_range)
            
            # Calculate constraint factor from other agents (collaboration)
            constraint_factor = sum(constraints) / (len(constraints) or 1)
            
            # Calculate resource adaptation factor (environment adaptation)
            resource_factor = 0.0
            if system_metrics:
                cpu_usage = system_metrics.get('cpu_usage', 0)
                memory_usage = system_metrics.get('memory_usage', 0)
                
                # If system is under heavy load, reduce changes
                if cpu_usage > 80 or memory_usage > 80:
                    resource_factor = -0.2
                # If system has plenty of resources, be more aggressive
                elif cpu_usage < 30 and memory_usage < 50:
                    resource_factor = 0.2
            
            # Calculate error correction factor (self-correction)
            error_rate = agent['error_count'] / (agent['job_count'] + 1)
            correction_factor = -0.2 if error_rate > agent['error_threshold'] else 0.1
            
            # Apply all factors to evolve state
            previous_state = agent['state']
            new_state = previous_state + improvement + (constraint_factor * 0.1) + resource_factor + correction_factor
            
            # Ensure state doesn't go negative
            new_state = max(0.0, new_state)
            
            # Update agent
            agent['state'] = new_state
            agent['iteration'] += 1
            agent['job_count'] += 1
            
            # Record evolution factors in history
            evolution_record = {
                'timestamp': datetime.now().isoformat(),
                'iteration': agent['iteration'],
                'previous_state': previous_state,
                'new_state': new_state,
                'factors': {
                    'improvement': improvement,
                    'constraint': constraint_factor,
                    'resource': resource_factor,
                    'correction': correction_factor
                },
                'error_rate': error_rate
            }
            
            agent['history'].append(evolution_record)
            
            # Adjust poll interval based on performance
            if error_rate > agent['error_threshold']:
                agent['poll_interval'] = min(5.0, agent['poll_interval'] * 1.5)
            else:
                agent['poll_interval'] = max(0.1, agent['poll_interval'] * 0.9)
            
            return new_state
            
        except Exception as e:
            self.logger.error(f"Error evolving agent {agent.get('name', 'unknown')}: {e}")
            return agent.get('state', 0.0)
    
    def _collect_system_metrics(self) -> Dict:
        """Collect current system metrics"""
        try:
            if PSUTIL_AVAILABLE:
                return {
                    'cpu_usage': psutil.cpu_percent(),
                    'memory_usage': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Fallback to basic metrics without psutil
                import os
                load_avg = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
                return {
                    'cpu_usage': min(100, load_avg * 20),  # Rough approximation
                    'memory_usage': 50,  # Default moderate usage
                    'disk_usage': 25,  # Default low usage
                    'timestamp': datetime.now().isoformat(),
                    'fallback_metrics': True
                }
        except Exception as e:
            self.logger.warning(f"Failed to collect system metrics: {e}")
            return {
                'cpu_usage': 0,
                'memory_usage': 0, 
                'disk_usage': 0,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _get_agent_status(self, agent_name: Optional[str] = None) -> EchoResponse:
        """Get status of one or all agents"""
        try:
            if agent_name:
                if agent_name not in self.agents:
                    return EchoResponse(
                        success=False,
                        message=f"Agent {agent_name} not found"
                    )
                return EchoResponse(
                    success=True,
                    data=self.agents[agent_name],
                    message=f"Agent {agent_name} status retrieved"
                )
            else:
                return EchoResponse(
                    success=True,
                    data=dict(self.agents),
                    message=f"All agents status retrieved ({len(self.agents)} agents)"
                )
        except Exception as e:
            return self.handle_error(e, "_get_agent_status")
    
    def _get_evolution_history(self) -> EchoResponse:
        """Get evolution history from memory"""
        try:
            memory_result = self.retrieve_memory('evolution_memory')
            if not memory_result.success:
                return EchoResponse(
                    success=False,
                    message="No evolution history found"
                )
            
            evolution_memory = memory_result.data
            
            return EchoResponse(
                success=True,
                data=evolution_memory,
                message="Evolution history retrieved"
            )
        except Exception as e:
            return self.handle_error(e, "_get_evolution_history")
    
    def _get_system_metrics(self) -> EchoResponse:
        """Get current system metrics"""
        try:
            metrics = self._collect_system_metrics()
            return EchoResponse(
                success=True,
                data=metrics,
                message="System metrics retrieved"
            )
        except Exception as e:
            return self.handle_error(e, "_get_system_metrics")
    
    def _start_continuous_evolution(self) -> EchoResponse:
        """Start continuous evolution in background"""
        try:
            if self.running:
                return EchoResponse(
                    success=False,
                    message="Continuous evolution already running"
                )
            
            self.running = True
            
            async def continuous_evolution():
                while self.running:
                    try:
                        # Run one evolution cycle
                        evolution_result = self._run_evolution(None, {'cycles': 1})
                        if evolution_result.success:
                            self.logger.debug("Continuous evolution cycle completed")
                        else:
                            self.logger.warning(f"Evolution cycle failed: {evolution_result.message}")
                        
                        # Wait before next cycle
                        await asyncio.sleep(self.poll_interval * 10)  # Longer interval for continuous
                    except Exception as e:
                        self.logger.error(f"Error in continuous evolution: {e}")
                        await asyncio.sleep(5)  # Wait before retrying
            
            # Start the task
            self.evolution_task = asyncio.create_task(continuous_evolution())
            
            return EchoResponse(
                success=True,
                data={'running': True, 'poll_interval': self.poll_interval * 10},
                message="Continuous evolution started"
            )
        except Exception as e:
            return self.handle_error(e, "_start_continuous_evolution")
    
    def _stop_continuous_evolution(self) -> EchoResponse:
        """Stop continuous evolution"""
        try:
            if not self.running:
                return EchoResponse(
                    success=False,
                    message="Continuous evolution not running"
                )
            
            self.running = False
            
            if self.evolution_task:
                self.evolution_task.cancel()
                self.evolution_task = None
            
            return EchoResponse(
                success=True,
                data={'running': False},
                message="Continuous evolution stopped"
            )
        except Exception as e:
            return self.handle_error(e, "_stop_continuous_evolution")
    
    def _apply_echo_to_evolution(self, evolution_data: Dict, echo_value: float) -> Dict:
        """Apply echo amplification to evolution results"""
        if echo_value < 0.3:
            return evolution_data  # No amplification for low echo values
        
        amplified_data = {}
        
        # Amplify agent improvements based on echo value
        for agent_name, agent in self.agents.items():
            if echo_value > 0.5:
                # Boost agent state for high echo values
                original_state = agent['state']
                amplified_state = original_state * (1 + echo_value * 0.5)
                agent['state'] = amplified_state
                
                amplified_data[agent_name] = {
                    'original_state': original_state,
                    'amplified_state': amplified_state,
                    'amplification_factor': echo_value * 0.5,
                    'echo_applied': True
                }
            else:
                # Moderate amplification
                amplified_data[agent_name] = {
                    'original_state': agent['state'],
                    'amplified_state': agent['state'],
                    'amplification_factor': 0.0,
                    'echo_applied': False
                }
        
        return amplified_data


# Factory function for easy creation
def create_echo_evolution(custom_config: Dict = None) -> EchoEvolutionStandardized:
    """
    Factory function to create a standardized Echo evolution component.
    
    Args:
        custom_config: Optional custom configuration parameters
        
    Returns:
        Configured EchoEvolutionStandardized instance
    """
    config = EchoConfig(
        component_name="EchoEvolution",
        version="1.0.0",
        echo_threshold=0.6,
        custom_params=custom_config or {}
    )
    
    return EchoEvolutionStandardized(config)


# Backward compatibility classes and functions
class EvolutionAgent:
    """Backward compatibility agent class"""
    
    def __init__(self, name: str, domain: str, initial_state: float = 0.0):
        self.name = name
        self.domain = domain
        self.state = initial_state
        self.iteration = 0
        
    async def evolve(self, constraints: List[float]) -> float:
        """Simplified evolution for backward compatibility"""
        improvement = random.uniform(*DEFAULT_IMPROVEMENT_RANGE)
        constraint_factor = sum(constraints) / (len(constraints) or 1)
        
        self.state += improvement + (constraint_factor * 0.1)
        self.state = max(0.0, self.state)
        self.iteration += 1
        
        return self.state


class ConstraintEmitter:
    """Backward compatibility emitter class"""
    
    def __init__(self):
        self.emitter_values = {}
    
    def update(self, pattern_name: str, value: float):
        self.emitter_values[pattern_name] = value
    
    def get_constraints(self, excluding: str = None) -> List[float]:
        return [value for name, value in self.emitter_values.items() if name != excluding]


async def run_evolution_demo():
    """Backward compatibility demo function"""
    print("🧬 Echo Evolution System Demo")
    print("=" * 50)
    
    # Create evolution system
    evolution = create_echo_evolution({
        'evolution_cycles': 3,
        'max_agents': 3
    })
    
    # Initialize
    init_result = evolution.initialize()
    if not init_result.success:
        print(f"❌ Failed to initialize: {init_result.message}")
        return
    
    print("✅ Evolution system initialized")
    
    # Create agents
    agents_data = [
        {"name": "Differential Gear", "domain": "coordination", "initial_state": 0.1},
        {"name": "Proximity Sensor", "domain": "awareness", "initial_state": 0.2},
        {"name": "Adaptive Filter", "domain": "optimization", "initial_state": 0.15}
    ]
    
    for agent_data in agents_data:
        result = evolution.process(agent_data, operation='create_agent')
        if result.success:
            print(f"✅ Created agent: {agent_data['name']}")
    
    # Run evolution
    print("\n🔄 Running evolution...")
    evolution_result = evolution.process(None, operation='evolve', cycles=3)
    
    if evolution_result.success:
        print("✅ Evolution completed!")
        data = evolution_result.data
        print(f"   Cycles completed: {data['cycles_completed']}")
        
        # Show final states
        status_result = evolution.process(None, operation='get_agent_status')
        if status_result.success:
            print("\n📊 Final agent states:")
            for name, agent in status_result.data.items():
                print(f"   {name}: {agent['state']:.3f} (iteration {agent['iteration']})")


def main():
    """Main function for backward compatibility"""
    import sys
    
    if sys.version_info >= (3, 7):
        asyncio.run(run_evolution_demo())
    else:
        # For older Python versions
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_evolution_demo())


if __name__ == "__main__":
    main()