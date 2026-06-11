"""
Memory Adapter Pattern Implementation

This module implements a unified memory adapter that bridges the fragmented 
memory system across memory_management.py, deep_tree_echo.py, and 
cognitive_architecture.py while maintaining backward compatibility.

This addresses the "Fragmented Memory System" architecture gap.
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

# Import unified memory system
from unified_echo_memory import (
    MemoryType as UnifiedMemoryType,
    MemoryNode as UnifiedMemoryNode,
    MemoryEdge as UnifiedMemoryEdge,
    HypergraphMemory as UnifiedHypergraphMemory,
    UnifiedEchoMemory,
    create_unified_memory_system
)

# Backward compatibility aliases
MemoryType = UnifiedMemoryType
MemoryNode = UnifiedMemoryNode
MemoryEdge = UnifiedMemoryEdge
HypergraphMemory = UnifiedHypergraphMemory

class MemoryAdapter:
    """
    Unified memory adapter that provides a consistent interface across all components.
    
    This adapter acts as a bridge between the fragmented memory implementations,
    providing a single point of access for all memory operations while maintaining
    backward compatibility with existing code.
    """
    
    def __init__(self, component_name: str = "unified_memory_adapter"):
        self.logger = logging.getLogger(__name__)
        self.component_name = component_name
        
        # Initialize the unified memory system
        self.unified_memory = create_unified_memory_system(
            component_name=component_name,
            storage_path="memory_storage"
        )
        
        # Initialize the unified memory system
        self.unified_memory.initialize()
        
        # Legacy memory storage for backward compatibility
        self._legacy_memories: Dict[str, Any] = {}
        
        self.logger.info(f"Memory adapter initialized for {component_name}")
    
    def store_memory(self, content: str, memory_type: Union[str, MemoryType], 
                    metadata: Optional[Dict[str, Any]] = None, 
                    echo_value: float = 0.0) -> str:
        """
        Store a memory in the unified system.
        
        Args:
            content: Memory content
            memory_type: Type of memory (str or MemoryType enum)
            metadata: Optional metadata dictionary
            echo_value: Echo value for the memory
            
        Returns:
            Memory ID
        """
        try:
            # Convert string memory type to enum if needed
            if isinstance(memory_type, str):
                memory_type = MemoryType(memory_type.lower())
            
            # Use unified memory system
            response = self.unified_memory.process({
                'operation': 'store',
                'content': content,
                'memory_type': memory_type.value,
                'echo_value': echo_value,
                'metadata': metadata or {}
            })
            
            if response.success:
                memory_id = response.data.get('memory_id', str(hash(content)))
                self.logger.debug(f"Memory stored successfully: {memory_id}")
                return memory_id
            else:
                self.logger.error(f"Failed to store memory: {response.message}")
                return self._fallback_store(content, memory_type, metadata, echo_value)
                
        except Exception as e:
            self.logger.error(f"Error storing memory: {e}")
            return self._fallback_store(content, memory_type, metadata, echo_value)
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryNode]:
        """
        Retrieve a memory by ID.
        
        Args:
            memory_id: Memory identifier
            
        Returns:
            MemoryNode if found, None otherwise
        """
        try:
            response = self.unified_memory.process({
                'operation': 'retrieve',
                'memory_id': memory_id
            })
            
            if response.success and response.data:
                return self._dict_to_memory_node(response.data)
            else:
                # Check legacy storage
                if memory_id in self._legacy_memories:
                    return self._legacy_memories[memory_id]
                return None
                
        except Exception as e:
            self.logger.error(f"Error retrieving memory {memory_id}: {e}")
            return self._legacy_memories.get(memory_id)
    
    def search_memories(self, query: str, memory_type: Optional[Union[str, MemoryType]] = None,
                       limit: int = 10) -> List[MemoryNode]:
        """
        Search memories by content.
        
        Args:
            query: Search query
            memory_type: Optional memory type filter
            limit: Maximum number of results
            
        Returns:
            List of matching MemoryNode objects
        """
        try:
            # Convert string memory type to enum if needed
            type_filter = None
            if memory_type:
                if isinstance(memory_type, str):
                    type_filter = MemoryType(memory_type.lower()).value
                else:
                    type_filter = memory_type.value
            
            response = self.unified_memory.process({
                'operation': 'search',
                'query': query,
                'memory_type': type_filter,
                'max_results': limit
            })
            
            if response.success and response.data:
                # Extract results from the response data
                results = response.data.get('results', [])
                return [self._dict_to_memory_node(mem) for mem in results]
            else:
                return self._fallback_search(query, memory_type, limit)
                
        except Exception as e:
            self.logger.error(f"Error searching memories: {e}")
            return self._fallback_search(query, memory_type, limit)
    
    def update_memory(self, memory_id: str, content: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None,
                     echo_value: Optional[float] = None) -> bool:
        """
        Update an existing memory.
        
        Args:
            memory_id: Memory identifier
            content: New content (optional)
            metadata: New metadata (optional) 
            echo_value: New echo value (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            update_data = {'operation': 'update', 'memory_id': memory_id}
            
            if content is not None:
                update_data['content'] = content
            if metadata is not None:
                update_data['metadata'] = metadata
            if echo_value is not None:
                update_data['echo_value'] = echo_value
            
            response = self.unified_memory.process(update_data)
            
            if response.success:
                self.logger.debug(f"Memory updated successfully: {memory_id}")
                return True
            else:
                self.logger.error(f"Failed to update memory: {response.message}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating memory {memory_id}: {e}")
            return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: Memory identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.unified_memory.process({
                'operation': 'delete',
                'memory_id': memory_id
            })
            
            if response.success:
                # Also remove from legacy storage
                self._legacy_memories.pop(memory_id, None)
                self.logger.debug(f"Memory deleted successfully: {memory_id}")
                return True
            else:
                self.logger.error(f"Failed to delete memory: {response.message}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting memory {memory_id}: {e}")
            return False
    
    def get_memory_overview(self) -> Dict[str, Any]:
        """
        Get overview of memory system status.
        
        Returns:
            Dictionary with memory statistics and status
        """
        try:
            response = self.unified_memory.process({
                'operation': 'analyze', 
                'analysis_type': 'overview'
            })
            
            if response.success:
                overview = response.data or {}
                overview['legacy_memories'] = len(self._legacy_memories)
                overview['component_name'] = self.component_name
                return overview
            else:
                return {
                    'error': response.message,
                    'legacy_memories': len(self._legacy_memories),
                    'component_name': self.component_name
                }
                
        except Exception as e:
            self.logger.error(f"Error getting memory overview: {e}")
            return {
                'error': str(e),
                'legacy_memories': len(self._legacy_memories),
                'component_name': self.component_name
            }
    
    def clear_all_memories(self) -> bool:
        """
        Clear all memories (use with caution).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.unified_memory.process({'operation': 'clear'})
            
            if response.success:
                self._legacy_memories.clear()
                self.logger.info("All memories cleared successfully")
                return True
            else:
                self.logger.error(f"Failed to clear memories: {response.message}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error clearing memories: {e}")
            return False
    
    # === Backward Compatibility Methods ===
    
    def create_legacy_memory(self, content: str, memory_type: str, **kwargs) -> str:
        """
        Create memory using legacy cognitive_architecture.Memory format.
        
        Args:
            content: Memory content
            memory_type: Memory type string
            **kwargs: Additional legacy memory fields
            
        Returns:
            Memory ID
        """
        metadata = {
            'legacy_format': True,
            'emotional_valence': kwargs.get('emotional_valence', 0.0),
            'importance': kwargs.get('importance', 0.5),
            'context': kwargs.get('context', {}),
            'associations': list(kwargs.get('associations', []))
        }
        
        echo_value = kwargs.get('importance', 0.5)  # Map importance to echo_value
        
        return self.store_memory(content, memory_type, metadata, echo_value)
    
    def get_legacy_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Get memory in legacy cognitive_architecture.Memory format.
        
        Args:
            memory_id: Memory identifier
            
        Returns:
            Dictionary in legacy format or None
        """
        memory_node = self.retrieve_memory(memory_id)
        if not memory_node:
            return None
        
        metadata = memory_node.metadata or {}
        
        return {
            'content': memory_node.content,
            'memory_type': memory_node.memory_type.value,
            'timestamp': memory_node.creation_time,
            'emotional_valence': metadata.get('emotional_valence', 0.0),
            'importance': memory_node.salience,
            'context': metadata.get('context', {}),
            'associations': set(metadata.get('associations', []))
        }
    
    # === Private Helper Methods ===
    
    def _fallback_store(self, content: str, memory_type: MemoryType, 
                       metadata: Optional[Dict[str, Any]], echo_value: float) -> str:
        """Fallback storage in case unified system fails"""
        memory_id = f"legacy_{hash(content)}_{int(time.time())}"
        
        self._legacy_memories[memory_id] = MemoryNode(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            salience=echo_value,
            metadata=metadata or {}
        )
        
        return memory_id
    
    def _fallback_search(self, query: str, memory_type: Optional[MemoryType], 
                        limit: int) -> List[MemoryNode]:
        """Fallback search in legacy storage"""
        results = []
        query_lower = query.lower()
        
        for memory in self._legacy_memories.values():
            if isinstance(memory, MemoryNode):
                # Check content match
                if query_lower in memory.content.lower():
                    # Check type filter
                    if memory_type is None or memory.memory_type == memory_type:
                        results.append(memory)
                        if len(results) >= limit:
                            break
        
        return results
    
    def _dict_to_memory_node(self, data: Dict[str, Any]) -> MemoryNode:
        """Convert dictionary to MemoryNode"""
        memory_type = data.get('memory_type', 'declarative')
        if isinstance(memory_type, str):
            memory_type = MemoryType(memory_type)
        
        return MemoryNode(
            id=data.get('id', ''),
            content=data.get('content', ''),
            memory_type=memory_type,
            creation_time=data.get('creation_time', time.time()),
            last_access_time=data.get('last_access_time', time.time()),
            access_count=data.get('access_count', 0),
            salience=data.get('salience', 0.5),
            echo_value=data.get('echo_value', 0.0),
            source=data.get('source', 'unknown'),
            metadata=data.get('metadata', {}),
            embeddings=data.get('embeddings')
        )

# Global memory adapter instance
_global_memory_adapter: Optional[MemoryAdapter] = None

def get_memory_adapter(component_name: str = "global_memory_adapter") -> MemoryAdapter:
    """
    Get or create the global memory adapter instance.
    
    Args:
        component_name: Name for the component
        
    Returns:
        MemoryAdapter instance
    """
    global _global_memory_adapter
    
    if _global_memory_adapter is None:
        _global_memory_adapter = MemoryAdapter(component_name)
    
    return _global_memory_adapter

def reset_memory_adapter():
    """Reset the global memory adapter (primarily for testing)"""
    global _global_memory_adapter
    _global_memory_adapter = None