#!/usr/bin/env python3
"""
Echo Evolution System - A comprehensive self-evolving framework for EchoSurface

This module integrates concepts from multiple self-evolution implementations:
- ESMWorker pattern from echopilot.py (collaborative evolution)
- Self-adaptation approach from pixie.rs (performance-based evolution)
- Resource monitoring from cronbot.py (system awareness)
- GitHub workflow modification from self_evo.py (environment adaptation)

The system features:
1. Multiple evolving agents that communicate and constrain each other
2. Performance-based adaptation of parameters
3. Resource monitoring and adaptation
4. Environment modification capabilities
5. Memory of past evolutions and their outcomes
"""

import asyncio
import random
import logging
import json
import os
import time
import psutil
import threading
from datetime import datetime
from queue import Queue
from typing import Dict, List, Any, Optional, Union, Tuple
import yaml

# Import unified architecture components
try:
    from echo_component_base import ProcessingEchoComponent, EchoConfig, EchoResponse
except ImportError:
    # Fallback if component base is not available
    ProcessingEchoComponent = object
    EchoConfig = type('EchoConfig', (), {})
    EchoResponse = type('EchoResponse', (), {})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("echo_evolution")

# Constants
EVOLUTION_MEMORY_FILE = "evolution_memory.json"
DEFAULT_POLL_INTERVAL = 1.0  # seconds
DEFAULT_ERROR_THRESHOLD = 0.1  # 10% error rate
DEFAULT_EVOLUTION_CYCLES = 5
DEFAULT_IMPROVEMENT_RANGE = (-0.1, 0.5)  # Random improvement range

class EvolutionMemory:
    """Manages the persistent memory of evolution cycles and outcomes"""
    
    def __init__(self, file_path: str = EVOLUTION_MEMORY_FILE):
        self.file_path = file_path
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load evolution memory from file or create new if doesn't exist"""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create new memory structure
            memory = {
                "cycles": [],
                "agents": {},
                "system_metrics": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            self._save_memory(memory)
            return memory
    
    def _save_memory(self, memory: Dict = None) -> None:
        """Save the memory to file"""
        if memory is None:
            memory = self.memory
        
        memory["last_updated"] = datetime.utcnow().isoformat()
        
        with open(self.file_path, 'w') as file:
            json.dump(memory, file, indent=2)
    
    def record_cycle(self, cycle_data: Dict) -> None:
        """Record data from an evolution cycle"""
        self.memory["cycles"].append(cycle_data)
        self._save_memory()
    
    def update_agent(self, agent_name: str, agent_data: Dict) -> None:
        """Update information about an evolution agent"""
        if agent_name not in self.memory["agents"]:
            self.memory["agents"][agent_name] = {
                "history": [],
                "created_at": datetime.utcnow().isoformat()
            }
        
        # Add current state to history
        self.memory["agents"][agent_name]["history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            **agent_data
        })
        
        # Update current state
        self.memory["agents"][agent_name].update(agent_data)
        
        self._save_memory()
    
    def record_system_metrics(self, metrics: Dict) -> None:
        """Record system performance metrics"""
        metrics["timestamp"] = datetime.utcnow().isoformat()
        self.memory["system_metrics"].append(metrics)
        self._save_memory()
    
    def get_agent_history(self, agent_name: str) -> List[Dict]:
        """Get the full history of an agent's evolution"""
        if agent_name in self.memory["agents"]:
            return self.memory["agents"][agent_name]["history"]
        return []
    
    def get_recent_cycles(self, count: int = 5) -> List[Dict]:
        """Get the most recent evolution cycles"""
        return self.memory["cycles"][-count:] if self.memory["cycles"] else []

class ResourceMonitor:
    """Monitors system resources and provides data for evolution decisions"""
    
    def __init__(self):
        self.stop_event = threading.Event()
        self.resource_queue = Queue()
        self.monitor_thread = None
        self.evolution_memory = EvolutionMemory()
    
    def start(self) -> None:
        """Start monitoring system resources"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            logger.warning("Resource monitor is already running")
            return
        
        self.stop_event.clear()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Resource monitoring started")
    
    def stop(self) -> None:
        """Stop monitoring system resources"""
        if not self.monitor_thread or not self.monitor_thread.is_alive():
            logger.warning("Resource monitor is not running")
            return
        
        self.stop_event.set()
        self.monitor_thread.join()
        logger.info("Resource monitoring stopped")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while not self.stop_event.is_set():
            try:
                # Collect system metrics
                cpu_usage = psutil.cpu_percent(interval=0.5)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                metrics = {
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory.percent,
                    "disk_usage": disk.percent
                }
                
                # Add to queue for immediate access
                self.resource_queue.put(metrics)
                
                # Record to memory periodically (every 5 seconds)
                if int(time.time()) % 5 == 0:
                    self.evolution_memory.record_system_metrics(metrics)
                
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error in resource monitoring: {str(e)}")
                time.sleep(1)
    
    def get_current_metrics(self) -> Dict:
        """Get the most recent resource metrics"""
        if self.resource_queue.empty():
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "disk_usage": 0.0
            }
        
        metrics = None
        # Empty the queue and keep only the latest metrics
        while not self.resource_queue.empty():
            metrics = self.resource_queue.get()
        
        return metrics

class EchoAgent:
    """
    A self-evolving agent within the Echo Evolution system.
    
    Each agent has a specific domain/pattern it evolves, and communicates with other
    agents to form a network of mutual evolution constraints.
    """
    
    def __init__(
        self, 
        name: str, 
        domain: str,
        initial_state: float = 0.0,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        error_threshold: float = DEFAULT_ERROR_THRESHOLD
    ):
        self.name = name
        self.domain = domain
        self.state = initial_state
        self.poll_interval = poll_interval
        self.error_threshold = error_threshold
        self.iteration = 0
        self.error_count = 0
        self.job_count = 0
        self.memory = EvolutionMemory()
        
        # Register agent in memory
        self.memory.update_agent(self.name, {
            "domain": self.domain,
            "state": self.state,
            "poll_interval": self.poll_interval,
            "error_threshold": self.error_threshold
        })
    
    async def evolve(self, constraints: List[float], resource_metrics: Dict = None) -> float:
        """
        Evolve the agent based on constraints from other agents and system resources.
        
        This implements a multi-factor evolution that considers:
        1. Random improvement (innovation)
        2. Constraints from other agents (collaboration)
        3. System resource utilization (environment adaptation)
        4. Past performance (self-correction)
        """
        # Calculate random improvement factor (innovation)
        improvement = random.uniform(*DEFAULT_IMPROVEMENT_RANGE)
        
        # Calculate constraint factor from other agents (collaboration)
        constraint_factor = sum(constraints) / (len(constraints) or 1)
        
        # Calculate resource adaptation factor (environment adaptation)
        resource_factor = 0.0
        if resource_metrics:
            # If system is under heavy load, reduce changes
            if resource_metrics["cpu_usage"] > 80 or resource_metrics["memory_usage"] > 80:
                resource_factor = -0.2
            # If system has plenty of resources, be more aggressive with changes
            elif resource_metrics["cpu_usage"] < 30 and resource_metrics["memory_usage"] < 50:
                resource_factor = 0.2
        
        # Calculate error correction factor (self-correction)
        error_rate = self.error_count / (self.job_count + 1)
        correction_factor = -0.2 if error_rate > self.error_threshold else 0.1
        
        # Apply all factors to evolve state
        previous_state = self.state
        self.state += improvement + (constraint_factor * 0.1) + resource_factor + correction_factor
        
        # Ensure state doesn't go negative
        self.state = max(0.0, self.state)
        
        # Update iteration counters
        self.iteration += 1
        self.job_count += 1
        
        # Log evolution
        logger.info(
            f"[{self.name}] Cycle {self.iteration}: state updated to {self.state:.2f} "
            f"(previous: {previous_state:.2f}, change: {self.state - previous_state:.2f})"
        )
        logger.debug(
            f"[{self.name}] Factors: improvement={improvement:.2f}, constraint={constraint_factor:.2f}, "
            f"resource={resource_factor:.2f}, correction={correction_factor:.2f}"
        )
        
        # Record evolution in memory
        self.memory.update_agent(self.name, {
            "state": self.state,
            "iteration": self.iteration,
            "factors": {
                "improvement": improvement,
                "constraint": constraint_factor,
                "resource": resource_factor,
                "correction": correction_factor
            },
            "error_rate": error_rate
        })
        
        # Adjust poll interval based on performance
        self._adjust_poll_interval(error_rate)
        
        await asyncio.sleep(self.poll_interval)
        return self.state
    
    def _adjust_poll_interval(self, error_rate: float) -> None:
        """Adjust the poll interval based on error rate"""
        if error_rate > self.error_threshold:
            # Increase poll interval for high error rates
            self.poll_interval += 0.1
        else:
            # Decrease poll interval for low error rates, with a minimum
            self.poll_interval = max(0.1, self.poll_interval - 0.05)
        
        # Update memory with new poll interval
        self.memory.update_agent(self.name, {
            "poll_interval": self.poll_interval
        })
    
    def echo(self, data: Any, echo_value: float = None) -> Dict[str, Any]:
        """
        Echo function for Deep Tree Echo integration.
        
        This method provides the agent's perspective on input data,
        incorporating the agent's current state, domain expertise,
        and evolutionary history.
        
        Args:
            data: Input data to process with echo
            echo_value: Optional echo value to apply (uses agent state if None)
            
        Returns:
            Dict containing echoed data with agent metadata
        """
        if echo_value is None:
            echo_value = self.state
        
        # Calculate resonance based on data relevance to agent's domain
        resonance = self._calculate_resonance(data)
        
        # Apply echo transformation
        echoed_data = {
            'original_data': data,
            'agent_name': self.name,
            'agent_domain': self.domain,
            'echo_value': echo_value,
            'resonance': resonance,
            'agent_state': self.state,
            'iteration': self.iteration,
            'error_rate': self.error_count / (self.job_count + 1),
            'poll_interval': self.poll_interval,
            'timestamp': datetime.utcnow().isoformat(),
            'echo_metadata': {
                'processing_quality': min(1.0, max(0.0, self.state)),
                'agent_maturity': self.iteration / 100.0,  # Normalize iteration count
                'domain_expertise': resonance * echo_value
            }
        }
        
        # Record echo operation in memory
        self.memory.record_system_metrics({
            'agent_echo': self.name,
            'resonance': resonance,
            'echo_value': echo_value,
            'data_type': str(type(data).__name__)
        })
        
        return echoed_data
    
    def _calculate_resonance(self, data: Any) -> float:
        """
        Calculate how well the data resonates with this agent's domain.
        
        This is a simplified implementation that could be enhanced based
        on specific domain requirements.
        """
        if not data:
            return 0.0
        
        data_str = str(data).lower()
        domain_str = self.domain.lower()
        
        # Simple keyword matching for resonance calculation
        domain_keywords = domain_str.split()
        matches = sum(1 for keyword in domain_keywords if keyword in data_str)
        
        # Calculate resonance as percentage of domain keywords found
        if domain_keywords:
            base_resonance = matches / len(domain_keywords)
        else:
            base_resonance = 0.5  # Default moderate resonance
        
        # Modify resonance based on agent state (better agents resonate better)
        state_bonus = self.state * 0.2  # Up to 20% bonus for high-state agents
        
        return min(1.0, base_resonance + state_bonus)
    
    async def process_job(self) -> bool:
        """Simulate processing a job with potential failures based on state quality"""
        try:
            # More evolved states (higher values) have lower failure rates
            failure_threshold = max(0.05, 0.5 - (self.state * 0.1))
            
            # Simulate job processing
            await asyncio.sleep(self.poll_interval)
            
            # Simulate potential failure
            if random.random() < failure_threshold:
                self.error_count += 1
                logger.warning(f"[{self.name}] Job failed (error rate: {self.error_count}/{self.job_count+1})")
                return False
            
            logger.debug(f"[{self.name}] Job completed successfully")
            return True
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[{self.name}] Error processing job: {str(e)}")
            return False

class EvolutionNetwork(ProcessingEchoComponent):
    """
    Manages a network of evolving agents that mutually influence each other,
    forming a self-improving ecosystem.
    
    Integrates with the unified Deep Tree Echo architecture while maintaining
    backward compatibility with existing evolution functionality.
    """
    
    def __init__(self, config: EchoConfig = None):
        # Initialize unified interface if config is provided
        if config is not None:
            super().__init__(config)
        else:
            # Backward compatibility - create default config
            self.config = None
            self.logger = logging.getLogger("echo_evolution")
        
        self.agents = {}
        self.emitter = {}
        self.resource_monitor = ResourceMonitor()
        self.memory = EvolutionMemory()
        self.logger.info("Evolution Network initialized")
    
    def initialize(self) -> Any:
        """Initialize the evolution network (unified interface)"""
        try:
            if hasattr(super(), 'initialize'):
                result = super().initialize()
                if hasattr(result, 'success') and not result.success:
                    return result
            
            # Start resource monitoring
            self.resource_monitor.start()
            
            # Initialize processing pipeline for evolution data
            if hasattr(self, 'add_processing_step'):
                self.add_processing_step(self._preprocess_evolution_data, "evolution_preprocessor")
                self.add_processing_step(self._analyze_agent_states, "agent_analyzer")
                self.add_processing_step(self._generate_evolution_summary, "summary_generator")
            
            message = "Evolution Network initialized successfully"
            self.logger.info(message)
            
            # Return EchoResponse if available, otherwise return simple dict
            if hasattr(self, 'config') and self.config is not None:
                return EchoResponse(success=True, message=message)
            else:
                return {"success": True, "message": message}
                
        except Exception as e:
            error_msg = f"Failed to initialize Evolution Network: {str(e)}"
            self.logger.error(error_msg)
            if hasattr(self, 'handle_error'):
                return self.handle_error(e, "initialize")
            else:
                return {"success": False, "message": error_msg}
    
    def process(self, input_data: Any, **kwargs) -> Any:
        """Process evolution data (unified interface)"""
        try:
            if hasattr(self, 'validate_input'):
                validation = self.validate_input(input_data)
                if hasattr(validation, 'success') and not validation.success:
                    return validation
            
            # Process through parent pipeline if available
            if hasattr(super(), 'process'):
                return super().process(input_data, **kwargs)
            
            # Default processing for evolution data
            processed_data = {
                'input_data': input_data,
                'network_state': self.get_summary(),
                'processing_timestamp': datetime.utcnow().isoformat(),
                'agent_count': len(self.agents)
            }
            
            # Return EchoResponse if available
            if hasattr(self, 'config') and self.config is not None:
                return EchoResponse(
                    success=True,
                    data=processed_data,
                    message="Evolution data processed successfully"
                )
            else:
                return {"success": True, "data": processed_data}
                
        except Exception as e:
            if hasattr(self, 'handle_error'):
                return self.handle_error(e, "process")
            else:
                return {"success": False, "message": str(e)}
    
    def echo(self, data: Any, echo_value: float = 0.0) -> Any:
        """Perform echo operation across the evolution network (unified interface)"""
        try:
            # Collect echoes from all agents
            agent_echoes = []
            for agent_name, agent in self.agents.items():
                try:
                    agent_echo = agent.echo(data, echo_value)
                    agent_echoes.append(agent_echo)
                except Exception as e:
                    self.logger.warning(f"Agent {agent_name} echo failed: {str(e)}")
            
            # Calculate network-level echo metrics
            network_echo = {
                'network_echo_value': echo_value,
                'agent_echoes': agent_echoes,
                'network_resonance': self._calculate_network_resonance(agent_echoes),
                'evolution_state': self.get_summary(),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Return EchoResponse if available
            if hasattr(self, 'config') and self.config is not None:
                return EchoResponse(
                    success=True,
                    data=network_echo,
                    message=f"Network echo completed with {len(agent_echoes)} agent responses",
                    metadata={'agent_count': len(agent_echoes), 'echo_value': echo_value}
                )
            else:
                return {"success": True, "data": network_echo}
                
        except Exception as e:
            if hasattr(self, 'handle_error'):
                return self.handle_error(e, "echo")
            else:
                return {"success": False, "message": str(e)}
    
    def _calculate_network_resonance(self, agent_echoes: List[Dict]) -> float:
        """Calculate overall network resonance from agent echoes"""
        if not agent_echoes:
            return 0.0
        
        total_resonance = sum(echo.get('resonance', 0.0) for echo in agent_echoes)
        return total_resonance / len(agent_echoes)
    
    def _preprocess_evolution_data(self, data: Any) -> Any:
        """Preprocessing step for evolution pipeline"""
        if isinstance(data, dict):
            data['preprocessed'] = True
            data['preprocessing_timestamp'] = datetime.utcnow().isoformat()
        return data
    
    def _analyze_agent_states(self, data: Any) -> Any:
        """Analysis step for agent states"""
        if isinstance(data, dict):
            data['agent_analysis'] = {
                'total_agents': len(self.agents),
                'average_state': sum(self.emitter.values()) / len(self.emitter) if self.emitter else 0,
                'state_distribution': list(self.emitter.values())
            }
        return data
    
    def _generate_evolution_summary(self, data: Any) -> Any:
        """Generate summary step for evolution pipeline"""
        if isinstance(data, dict):
            data['evolution_summary'] = self.get_summary()
        return data
    
    def add_agent(self, agent: EchoAgent) -> None:
        """Add an agent to the evolution network"""
        if agent.name in self.agents:
            logger.warning(f"Agent '{agent.name}' already exists in the network")
            return
        
        self.agents[agent.name] = agent
        self.emitter[agent.name] = agent.state
        logger.info(f"Added agent '{agent.name}' to the evolution network")
    
    def get_constraints(self, agent_name: str) -> List[float]:
        """Get constraints from all other agents for the specified agent"""
        return [state for name, state in self.emitter.items() if name != agent_name]
    
    async def run_cycle(self) -> Dict:
        """Run a single evolution cycle for all agents"""
        cycle_start_time = time.time()
        tasks = []
        
        # Start resource monitoring if not already running
        if not self.resource_monitor.monitor_thread or not self.resource_monitor.monitor_thread.is_alive():
            self.resource_monitor.start()
        
        # Get current system metrics
        resource_metrics = self.resource_monitor.get_current_metrics()
        
        # Create evolution tasks for all agents
        for agent in self.agents.values():
            constraints = self.get_constraints(agent.name)
            tasks.append(asyncio.create_task(agent.evolve(constraints, resource_metrics)))
        
        # Wait for all agents to evolve
        results = await asyncio.gather(*tasks)
        
        # Update emitter values with new states
        for agent_name, result in zip(self.agents.keys(), results):
            self.emitter[agent_name] = result
        
        # Record cycle data in memory
        cycle_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "duration": time.time() - cycle_start_time,
            "agents": {name: agent.state for name, agent in self.agents.items()},
            "resource_metrics": resource_metrics
        }
        self.memory.record_cycle(cycle_data)
        
        return cycle_data
    
    async def run_job_cycle(self) -> Dict:
        """Run a job processing cycle for all agents"""
        cycle_start_time = time.time()
        tasks = []
        
        # Create job processing tasks for all agents
        for agent in self.agents.values():
            tasks.append(asyncio.create_task(agent.process_job()))
        
        # Wait for all jobs to complete
        results = await asyncio.gather(*tasks)
        
        # Calculate success rate
        success_count = sum(1 for result in results if result)
        success_rate = success_count / len(results) if results else 0
        
        # Record job cycle data
        cycle_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "duration": time.time() - cycle_start_time,
            "success_rate": success_rate,
            "job_results": {name: result for name, result in zip(self.agents.keys(), results)}
        }
        
        return cycle_data
    
    async def run_evolution_and_jobs(self, cycles: int = DEFAULT_EVOLUTION_CYCLES) -> Dict:
        """Run multiple evolution cycles alternating with job processing"""
        results = {
            "evolution_cycles": [],
            "job_cycles": [],
            "start_time": datetime.utcnow().isoformat(),
            "agent_progression": {name: [] for name in self.agents.keys()}
        }
        
        for cycle in range(cycles):
            logger.info(f"\n=== Global Evolution Cycle {cycle+1}/{cycles} ===")
            
            # Run evolution cycle
            evo_result = await self.run_cycle()
            results["evolution_cycles"].append(evo_result)
            
            # Track agent progression
            for name, state in evo_result["agents"].items():
                results["agent_progression"][name].append(state)
            
            # Run job processing cycle
            logger.info(f"=== Global Job Cycle {cycle+1}/{cycles} ===")
            job_result = await self.run_job_cycle()
            results["job_cycles"].append(job_result)
            
            # Brief pause between cycles
            await asyncio.sleep(0.2)
        
        results["end_time"] = datetime.utcnow().isoformat()
        results["total_duration"] = (
            datetime.fromisoformat(results["end_time"]) - 
            datetime.fromisoformat(results["start_time"])
        ).total_seconds()
        
        # Clean up resource monitor
        self.resource_monitor.stop()
        
        return results
    
    def modify_environment(self, workflow_file: str = None) -> bool:
        """Modify the environment based on collective agent states"""
        if not workflow_file:
            logger.info("No workflow file specified for environment modification")
            return False
        
        try:
            # Read workflow file
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)
            
            # Determine modification based on agent states
            avg_state = sum(self.emitter.values()) / len(self.emitter)
            
            # Only modify if average state is substantial
            if avg_state > 0.5:
                # Modify schedule based on average state
                # Higher states mean more frequent schedules
                minute = int(60 / (avg_state + 1))
                new_cron = f"{minute} * * * *"  # Run every 'minute' minutes
                
                if 'on' in workflow and 'schedule' in workflow['on']:
                    workflow['on']['schedule'][0]['cron'] = new_cron
                    logger.info(f"Modified workflow schedule to '{new_cron}'")
                
                # Save the modified workflow
                with open(workflow_file, 'w') as f:
                    yaml.dump(workflow, f)
                
                return True
            else:
                logger.info(f"Average agent state ({avg_state:.2f}) too low for environment modification")
                return False
                
        except Exception as e:
            logger.error(f"Error modifying environment: {str(e)}")
            return False
    
    def get_summary(self) -> Dict:
        """Get a summary of the evolution network's current state"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_count": len(self.agents),
            "agents": {
                name: {
                    "state": agent.state,
                    "iteration": agent.iteration,
                    "error_rate": agent.error_count / (agent.job_count + 1),
                    "poll_interval": agent.poll_interval
                }
                for name, agent in self.agents.items()
            },
            "average_state": sum(agent.state for agent in self.agents.values()) / len(self.agents) if self.agents else 0
        }

def create_echo_evolution_system(config: EchoConfig = None, agent_domains: List[Tuple[str, str]] = None) -> EvolutionNetwork:
    """
    Factory function to create an Echo Evolution system with unified interface support.
    
    Args:
        config: Optional EchoConfig for unified interface integration
        agent_domains: List of (agent_name, domain) tuples for agent creation
        
    Returns:
        Configured EvolutionNetwork instance
    """
    if config is None:
        # Create default config for unified interface
        config = EchoConfig(
            component_name="echo_evolution",
            version="1.0.0",
            echo_threshold=0.75,
            max_depth=10,
            custom_params={
                "poll_interval": DEFAULT_POLL_INTERVAL,
                "error_threshold": DEFAULT_ERROR_THRESHOLD,
                "evolution_cycles": DEFAULT_EVOLUTION_CYCLES
            }
        )
    
    # Create evolution network with unified interface
    network = EvolutionNetwork(config)
    
    # Initialize the network
    init_result = network.initialize()
    if hasattr(init_result, 'success') and not init_result.success:
        logger.error(f"Failed to initialize evolution network: {init_result.message}")
        return network
    
    # Add default agents if none specified
    if agent_domains is None:
        agent_domains = [
            ("CognitiveAgent", "Cognitive Architecture"),
            ("MemoryAgent", "Memory Management"),
            ("SensoryAgent", "Sensory Processing"),
            ("IntegrationAgent", "System Integration")
        ]
    
    # Create and add agents
    for name, domain in agent_domains:
        agent = EchoAgent(name, domain, initial_state=random.uniform(0, 1))
        network.add_agent(agent)
    
    logger.info(f"Created echo evolution system with {len(agent_domains)} agents")
    return network

async def main():
    """Main function demonstrating the Echo Evolution System"""
    # Define domains for evolution
    domains = [
        ("CognitiveAgent", "Cognitive Architecture"),
        ("MemoryAgent", "Memory Management"),
        ("SensoryAgent", "Sensory Processing"),
        ("IntegrationAgent", "System Integration")
    ]
    
    # Create evolution network
    network = EvolutionNetwork()
    
    # Add agents to network
    for name, domain in domains:
        agent = EchoAgent(name, domain, initial_state=random.uniform(0, 1))
        network.add_agent(agent)
    
    logger.info("Starting Echo Evolution System")
    results = await network.run_evolution_and_jobs(cycles=3)
    
    # Optionally modify environment (e.g., GitHub workflow)
    workflow_file = ".github/workflows/echo_evolution.yml"
    if os.path.exists(workflow_file):
        network.modify_environment(workflow_file)
    
    # Print summary
    summary = network.get_summary()
    logger.info("\n=== Echo Evolution Summary ===")
    logger.info(f"Total Agents: {summary['agent_count']}")
    logger.info(f"Average State: {summary['average_state']:.2f}")
    logger.info("Agent States:")
    for name, info in summary['agents'].items():
        logger.info(f"  {name}: {info['state']:.2f} (error rate: {info['error_rate']:.2%})")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())