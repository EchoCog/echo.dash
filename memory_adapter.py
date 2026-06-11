"""
Streamlined Memory Adapter - Backward Compatibility Layer

This module implements a unified memory adapter that bridges the fragmented
memory system across memory_management.py, deep_tree_echo.py, and
cognitive_architecture.py while maintaining backward compatibility.
This module provides a streamlined adapter for backward compatibility with
fragmented memory systems. It focuses on the essential adapter pattern without
duplicating the comprehensive functionality already in unified_echo_memory.py.

This addresses the "Fragmented Memory System" architecture gap by providing
clean adapter interfaces while delegating all complex operations to the
unified system.
"""

import logging
from typing import Dict, List, Optional, Any, Union

# Import unified memory system - all core functionality comes from here
from unified_echo_memory import (
    MemoryType,
    MemoryNode, 
    MemoryEdge,
    HypergraphMemory,
    UnifiedEchoMemory,
    create_unified_memory_system
)


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
    Streamlined memory adapter for backward compatibility
    
    This adapter provides simple, consistent interfaces while delegating
    all operations to the unified memory system. It focuses on compatibility
    rather than reimplementing functionality.
    """
    
    def __init__(self, component_name: str = "memory_adapter"):
        """Initialize the memory adapter"""
        self.logger = logging.getLogger(__name__)
        self.component_name = component_name
        
        # Use the unified memory system as the backend
        self.unified_memory = create_unified_memory_system(
            component_name=component_name,
            storage_path="memory_storage"
        )

        # Initialize the unified memory system
        self.unified_memory.initialize()

        # Legacy memory storage for backward compatibility
        self._legacy_memories: Dict[str, Any] = {}

        self.logger.info("Memory adapter initialized for %s", component_name)

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
                self.logger.debug("Memory stored successfully: %s", memory_id)
                return memory_id
            else:
                self.logger.error("Failed to store memory: %s", response.message)
                return self._fallback_store(content, memory_type, metadata, echo_value)

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error storing memory: %s", e)
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

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error retrieving memory %s: %s", memory_id, e)
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

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error searching memories: %s", e)
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
                self.logger.debug("Memory updated successfully: %s", memory_id)
                return True
            else:
                self.logger.error("Failed to update memory: %s", response.message)
                return False

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error updating memory %s: %s", memory_id, e)
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
                self.logger.debug("Memory deleted successfully: %s", memory_id)
                return True
            else:
                self.logger.error("Failed to delete memory: %s", response.message)
                return False

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error deleting memory %s: %s", memory_id, e)
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

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error getting memory overview: %s", e)
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
                self.logger.error("Failed to clear memories: %s", response.message)
                return False

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            self.logger.error("Error clearing memories: %s", e)
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
        
        self.logger.info(f"Memory adapter '{component_name}' initialized")
    
    # =========================================================================
    # PRIMARY ADAPTER METHODS - Simple wrappers around unified system
    # =========================================================================
    
    def store_memory(self, content: str, memory_type: Union[str, MemoryType], 
                    metadata: Optional[Dict[str, Any]] = None, 
                    echo_value: float = 0.0) -> str:
        """Store a memory via the unified system"""
        # Convert string memory type if needed
        if isinstance(memory_type, str):
            memory_type = MemoryType(memory_type.lower())
        
        result = self.unified_memory.store_memory(
            content=content,
            memory_type=memory_type,
            echo_value=echo_value,
            metadata=metadata or {}
        )
        
        if result.success:
            return result.data['memory_id']
        else:
            self.logger.error(f"Failed to store memory: {result.message}")
            raise RuntimeError(f"Memory storage failed: {result.message}")
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryNode]:
        """Retrieve a memory by ID"""
        result = self.unified_memory.retrieve_memory(memory_id)
        
        if result.success and result.data:
            # Convert dict back to MemoryNode
            data = result.data
            return MemoryNode(
                id=data['id'],
                content=data['content'],
                memory_type=MemoryType(data['memory_type']),
                creation_time=data.get('creation_time', 0),
                last_access_time=data.get('last_access_time', 0),
                access_count=data.get('access_count', 0),
                salience=data.get('salience', 0.5),
                echo_value=data.get('echo_value', 0.0),
                source=data.get('source', 'unknown'),
                metadata=data.get('metadata', {}),
                embeddings=data.get('embeddings')
            )
        return None
    
    def search_memories(self, query: str, memory_type: Optional[Union[str, MemoryType]] = None,
                       limit: int = 10) -> List[MemoryNode]:
        """Search memories by content"""
        # Convert string memory type if needed
        search_type = None
        if memory_type:
            if isinstance(memory_type, str):
                search_type = MemoryType(memory_type.lower())
            else:
                search_type = memory_type
        
        result = self.unified_memory.search_memories(
            query=query,
            memory_type=search_type,
            echo_threshold=0.0,  # Use low threshold for adapter compatibility
            max_results=limit
        )
        
        if result.success and result.data:
            # Convert dict results back to MemoryNode objects
            memory_nodes = []
            for mem_data in result.data.get('results', []):
                node = MemoryNode(
                    id=mem_data['id'],
                    content=mem_data['content'],
                    memory_type=MemoryType(mem_data['memory_type']),
                    creation_time=mem_data.get('creation_time', 0),
                    last_access_time=mem_data.get('last_access_time', 0),
                    access_count=mem_data.get('access_count', 0),
                    salience=mem_data.get('salience', 0.5),
                    echo_value=mem_data.get('echo_value', 0.0),
                    source=mem_data.get('source', 'unknown'),
                    metadata=mem_data.get('metadata', {}),
                    embeddings=mem_data.get('embeddings')
                )
                memory_nodes.append(node)
            return memory_nodes
        return []
    
    def update_memory(self, memory_id: str, content: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None,
                     echo_value: Optional[float] = None) -> bool:
        """Update an existing memory"""
        update_data = {
            'operation': 'update',
            'memory_id': memory_id
        }
        
        if content is not None:
            update_data['content'] = content
        if metadata is not None:
            update_data['metadata'] = metadata
        if echo_value is not None:
            update_data['echo_value'] = echo_value
        
        result = self.unified_memory.process(update_data)
        return result.success
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory"""
        result = self.unified_memory.process({
            'operation': 'delete',
            'memory_id': memory_id
        })
        return result.success
    
    # =========================================================================
    # LEGACY COMPATIBILITY METHODS
    # =========================================================================
    
    def create_legacy_memory(self, content: str, memory_type: str, **kwargs) -> str:
        """Create memory using legacy format (cognitive_architecture compatibility)"""
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
        """Get memory in legacy format"""
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
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def get_memory_overview(self) -> Dict[str, Any]:
        """Get overview of memory system status"""
        result = self.unified_memory.get_memory_overview()
        
        if result.success:
            overview = result.data
            overview['adapter_component'] = self.component_name
            return overview
        else:
            return {
                'error': result.message,
                'adapter_component': self.component_name
            }
    
    def clear_all_memories(self) -> bool:
        """Clear all memories (use with caution)"""
        result = self.unified_memory.process({'operation': 'clear'})
        return result.success


# =========================================================================
# GLOBAL ADAPTER MANAGEMENT
# =========================================================================

_global_memory_adapter: Optional[MemoryAdapter] = None

def get_memory_adapter(component_name: str = "global_memory_adapter") -> MemoryAdapter:
    """
    Get or create the global memory adapter instance.

    Get or create the global memory adapter instance
    
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


# =========================================================================
# BACKWARD COMPATIBILITY EXPORTS
# =========================================================================

# Export all necessary symbols for backward compatibility
__all__ = [
    'MemoryAdapter',
    'get_memory_adapter', 
    'reset_memory_adapter',
    'MemoryType',
    'MemoryNode',
    'MemoryEdge', 
    'HypergraphMemory'
]
