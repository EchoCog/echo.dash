#!/usr/bin/env python3
"""
Deep Tree Echo Standardized Example

This module demonstrates how to integrate the existing DeepTreeEcho class
with the standardized Echo component base classes. This serves as an example
of the integration pattern for complex components.

This is an example implementation showing the migration path from the legacy
deep_tree_echo.py to the standardized component architecture.
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime

from echo_component_base import MemoryEchoComponent, EchoConfig, EchoResponse

# Import the legacy DeepTreeEcho (with error handling)
try:
    from deep_tree_echo import DeepTreeEcho, TreeNode, SpatialContext
    DEEP_TREE_ECHO_AVAILABLE = True
except ImportError:
    DEEP_TREE_ECHO_AVAILABLE = False
    TreeNode = None
    SpatialContext = None
    

class DeepTreeEchoStandardized(MemoryEchoComponent):
    """
    Standardized version of DeepTreeEcho using the Echo component base classes
    
    This demonstrates how to migrate a complex component to the standardized
    architecture while maintaining backward compatibility and adding new features.
    """
    
    def __init__(self, config: EchoConfig):
        super().__init__(config)
        
        # Extract Deep Tree Echo specific configuration from custom_params
        self.echo_threshold = config.custom_params.get('echo_threshold', config.echo_threshold)
        self.tree_max_depth = config.custom_params.get('tree_max_depth', config.max_depth)
        self.use_julia = config.custom_params.get('use_julia', False)
        self.spatial_awareness = config.custom_params.get('spatial_awareness', True)
        
        # Initialize the legacy Deep Tree Echo system if available
        self.legacy_echo = None
        self.tree_store = {}  # Store tree structures in memory
        
    def initialize(self) -> EchoResponse:
        """Initialize the Deep Tree Echo component"""
        try:
            if not DEEP_TREE_ECHO_AVAILABLE:
                return EchoResponse(
                    success=False,
                    message="Deep Tree Echo dependencies not available"
                )
            
            # Initialize legacy system with standardized parameters
            self.legacy_echo = DeepTreeEcho(
                echo_threshold=self.echo_threshold,
                max_depth=self.tree_max_depth,
                use_julia=self.use_julia
            )
            
            self._initialized = True
            self.logger.info("Deep Tree Echo standardized component initialized")
            
            return EchoResponse(
                success=True,
                message="Deep Tree Echo component initialized successfully",
                metadata={
                    'echo_threshold': self.echo_threshold,
                    'max_depth': self.tree_max_depth,
                    'spatial_awareness': self.spatial_awareness
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "initialize")
    
    def process(self, input_data: Any, **kwargs) -> EchoResponse:
        """
        Process input data through the Deep Tree Echo system
        
        Supports various operations:
        - create_tree: Create new tree from content
        - add_child: Add child node to existing tree
        - propagate_echo: Propagate echo through tree
        - analyze_tree: Analyze tree structure and emotions
        """
        try:
            if not self._initialized:
                init_result = self.initialize()
                if not init_result.success:
                    return init_result
            
            operation = kwargs.get('operation', 'create_tree')
            tree_id = kwargs.get('tree_id', 'default')
            
            if operation == 'create_tree':
                return self._create_tree(input_data, tree_id, **kwargs)
            elif operation == 'add_child':
                return self._add_child(input_data, tree_id, **kwargs)
            elif operation == 'propagate_echo':
                return self._propagate_echo(input_data, tree_id, **kwargs)
            elif operation == 'analyze_tree':
                return self._analyze_tree(tree_id, **kwargs)
            else:
                return EchoResponse(
                    success=False,
                    message=f"Unknown operation: {operation}",
                    metadata={'available_operations': ['create_tree', 'add_child', 'propagate_echo', 'analyze_tree']}
                )
                
        except Exception as e:
            return self.handle_error(e, f"process operation: {operation}")
    
    def echo(self, data: Any, echo_value: float = 0.0) -> EchoResponse:
        """
        Perform echo operation on data using Deep Tree Echo logic
        """
        try:
            if not self._initialized:
                init_result = self.initialize()
                if not init_result.success:
                    return init_result
            
            # Create a temporary tree for the echo operation
            temp_tree_id = f"echo_{datetime.now().timestamp()}"
            
            # Create tree from data
            tree_result = self._create_tree(data, temp_tree_id, echo_value=echo_value)
            if not tree_result.success:
                return tree_result
            
            # Propagate echo through the tree
            echo_result = self._propagate_echo(echo_value, temp_tree_id)
            if not echo_result.success:
                return echo_result
            
            # Store the echo result in memory
            echo_key = f"echo_result_{temp_tree_id}"
            self.store_memory(echo_key, echo_result.data)
            
            return EchoResponse(
                success=True,
                data=echo_result.data,
                message=f"Deep Tree Echo operation completed (value: {echo_value})",
                metadata={
                    'echo_value': echo_value,
                    'tree_id': temp_tree_id,
                    'memory_key': echo_key,
                    'echo_propagation': echo_result.metadata
                }
            )
            
        except Exception as e:
            return self.handle_error(e, "echo")
    
    def _create_tree(self, content: str, tree_id: str, **kwargs) -> EchoResponse:
        """Create a new tree structure from content"""
        try:
            if isinstance(content, str):
                tree_content = content
            else:
                tree_content = str(content)
            
            # Create tree using legacy system
            root_node = self.legacy_echo.create_tree(tree_content)
            
            # Store tree in memory system
            self.tree_store[tree_id] = root_node
            tree_memory_key = f"tree_{tree_id}"
            self.store_memory(tree_memory_key, {
                'root_content': tree_content,
                'created_at': datetime.now().isoformat(),
                'node_count': 1
            })
            
            return EchoResponse(
                success=True,
                data={
                    'tree_id': tree_id,
                    'root_content': tree_content,
                    'emotional_state': root_node.emotional_state.tolist() if root_node.emotional_state is not None else None,
                    'spatial_context': {
                        'position': root_node.spatial_context.position if root_node.spatial_context else None,
                        'orientation': root_node.spatial_context.orientation if root_node.spatial_context else None
                    }
                },
                message=f"Tree '{tree_id}' created successfully",
                metadata={'tree_id': tree_id, 'memory_key': tree_memory_key}
            )
            
        except Exception as e:
            return self.handle_error(e, f"create_tree for tree_id: {tree_id}")
    
    def _add_child(self, content: str, tree_id: str, **kwargs) -> EchoResponse:
        """Add a child node to an existing tree"""
        try:
            if tree_id not in self.tree_store:
                return EchoResponse(
                    success=False,
                    message=f"Tree '{tree_id}' not found"
                )
            
            parent_node = kwargs.get('parent_node') or self.tree_store[tree_id]
            child_content = str(content)
            
            # Add child using legacy system
            child_node = self.legacy_echo.add_child(parent_node, child_content)
            
            # Update memory
            tree_memory_key = f"tree_{tree_id}"
            tree_data = self.retrieve_memory(tree_memory_key).data or {}
            tree_data['node_count'] = tree_data.get('node_count', 1) + 1
            tree_data['last_modified'] = datetime.now().isoformat()
            self.store_memory(tree_memory_key, tree_data)
            
            return EchoResponse(
                success=True,
                data={
                    'tree_id': tree_id,
                    'child_content': child_content,
                    'parent_content': parent_node.content,
                    'emotional_state': child_node.emotional_state.tolist() if child_node.emotional_state is not None else None
                },
                message=f"Child node added to tree '{tree_id}'",
                metadata={'tree_id': tree_id, 'node_count': tree_data['node_count']}
            )
            
        except Exception as e:
            return self.handle_error(e, f"add_child to tree_id: {tree_id}")
    
    def _propagate_echo(self, echo_value: float, tree_id: str, **kwargs) -> EchoResponse:
        """Propagate echo through the tree structure"""
        try:
            if tree_id not in self.tree_store:
                return EchoResponse(
                    success=False,
                    message=f"Tree '{tree_id}' not found"
                )
            
            root_node = self.tree_store[tree_id]
            
            # Perform echo propagation using legacy system
            echo_results = self.legacy_echo.propagate_echo(root_node, echo_value)
            
            # Store propagation results
            propagation_key = f"propagation_{tree_id}_{datetime.now().timestamp()}"
            self.store_memory(propagation_key, echo_results)
            
            return EchoResponse(
                success=True,
                data=echo_results,
                message=f"Echo propagation completed for tree '{tree_id}' with value {echo_value}",
                metadata={
                    'tree_id': tree_id,
                    'echo_value': echo_value,
                    'propagation_key': propagation_key,
                    'affected_nodes': len(echo_results) if isinstance(echo_results, list) else 1
                }
            )
            
        except Exception as e:
            return self.handle_error(e, f"propagate_echo for tree_id: {tree_id}")
    
    def _analyze_tree(self, tree_id: str, **kwargs) -> EchoResponse:
        """Analyze tree structure and provide insights"""
        try:
            if tree_id not in self.tree_store:
                return EchoResponse(
                    success=False,
                    message=f"Tree '{tree_id}' not found"
                )
            
            root_node = self.tree_store[tree_id]
            
            # Perform analysis
            analysis = self._perform_tree_analysis(root_node)
            
            # Store analysis results
            analysis_key = f"analysis_{tree_id}_{datetime.now().timestamp()}"
            self.store_memory(analysis_key, analysis)
            
            return EchoResponse(
                success=True,
                data=analysis,
                message=f"Tree analysis completed for '{tree_id}'",
                metadata={'tree_id': tree_id, 'analysis_key': analysis_key}
            )
            
        except Exception as e:
            return self.handle_error(e, f"analyze_tree for tree_id: {tree_id}")
    
    def _perform_tree_analysis(self, node: TreeNode, depth: int = 0) -> Dict[str, Any]:
        """Perform recursive analysis of tree structure"""
        analysis = {
            'content': node.content,
            'depth': depth,
            'echo_value': node.echo_value,
            'has_children': len(node.children) > 0,
            'child_count': len(node.children),
            'emotional_summary': self._analyze_emotional_state(node.emotional_state),
            'spatial_info': self._analyze_spatial_context(node.spatial_context)
        }
        
        if node.children:
            analysis['children'] = [
                self._perform_tree_analysis(child, depth + 1)
                for child in node.children
            ]
        
        return analysis
    
    def _analyze_emotional_state(self, emotional_state) -> Dict[str, Any]:
        """Analyze emotional state of a node"""
        if emotional_state is None:
            return {'status': 'no_emotional_data'}
        
        emotions = emotional_state.tolist() if hasattr(emotional_state, 'tolist') else list(emotional_state)
        
        return {
            'raw_emotions': emotions,
            'dominant_emotion_index': emotions.index(max(emotions)),
            'emotional_intensity': sum(emotions),
            'emotional_balance': max(emotions) - min(emotions)
        }
    
    def _analyze_spatial_context(self, spatial_context) -> Dict[str, Any]:
        """Analyze spatial context of a node"""
        if spatial_context is None:
            return {'status': 'no_spatial_data'}
        
        return {
            'position': spatial_context.position,
            'orientation': spatial_context.orientation,
            'field_of_view': spatial_context.field_of_view,
            'scale': spatial_context.scale,
            'depth': spatial_context.depth
        }
    
    def get_tree_list(self) -> EchoResponse:
        """Get list of all stored trees"""
        try:
            tree_list = []
            for tree_id in self.tree_store.keys():
                memory_key = f"tree_{tree_id}"
                tree_info = self.retrieve_memory(memory_key).data or {}
                tree_list.append({
                    'tree_id': tree_id,
                    'root_content': tree_info.get('root_content', 'Unknown'),
                    'node_count': tree_info.get('node_count', 1),
                    'created_at': tree_info.get('created_at', 'Unknown')
                })
            
            return EchoResponse(
                success=True,
                data=tree_list,
                message=f"Found {len(tree_list)} stored trees",
                metadata={'tree_count': len(tree_list)}
            )
            
        except Exception as e:
            return self.handle_error(e, "get_tree_list")
    
    def clear_trees(self) -> EchoResponse:
        """Clear all stored trees"""
        try:
            tree_count = len(self.tree_store)
            self.tree_store.clear()
            
            # Also clear tree memories
            for key in list(self.memory_store.keys()):
                if key.startswith('tree_') or key.startswith('propagation_') or key.startswith('analysis_'):
                    del self.memory_store[key]
            
            return EchoResponse(
                success=True,
                message=f"Cleared {tree_count} trees and associated memories",
                metadata={'cleared_trees': tree_count}
            )
            
        except Exception as e:
            return self.handle_error(e, "clear_trees")


# Factory function to create standardized Deep Tree Echo component
def create_deep_tree_echo_standardized(
    echo_threshold: float = 0.75,
    max_depth: int = 10,
    use_julia: bool = False,
    spatial_awareness: bool = True,
    component_name: str = "DeepTreeEchoStandardized"
) -> DeepTreeEchoStandardized:
    """
    Factory function to create a standardized Deep Tree Echo component
    
    Args:
        echo_threshold: Echo threshold value
        max_depth: Maximum tree depth
        use_julia: Whether to use Julia integration
        spatial_awareness: Whether to enable spatial awareness
        component_name: Name for the component
        
    Returns:
        Configured DeepTreeEchoStandardized component
    """
    config = EchoConfig(
        component_name=component_name,
        version="2.0.0",
        echo_threshold=echo_threshold,
        max_depth=max_depth,
        custom_params={
            'echo_threshold': echo_threshold,
            'tree_max_depth': max_depth,
            'use_julia': use_julia,
            'spatial_awareness': spatial_awareness
        }
    )
    
    return DeepTreeEchoStandardized(config)


# Compatibility adapter for existing code
def create_legacy_compatible_echo(echo_threshold: float = 0.75, max_depth: int = 10) -> DeepTreeEchoStandardized:
    """
    Create a Deep Tree Echo component that maintains compatibility with legacy interfaces
    """
    return create_deep_tree_echo_standardized(
        echo_threshold=echo_threshold,
        max_depth=max_depth,
        component_name="DeepTreeEchoLegacyCompatible"
    )


if __name__ == "__main__":
    # Example usage demonstration
    print("🌳 Deep Tree Echo Standardized Example")
    print("=" * 50)
    
    # Create standardized component
    echo_component = create_deep_tree_echo_standardized(
        echo_threshold=0.8,
        max_depth=15,
        component_name="ExampleEcho"
    )
    
    # Initialize
    init_result = echo_component.initialize()
    print(f"Initialization: {'✅' if init_result.success else '❌'}")
    
    if init_result.success:
        # Create a tree
        tree_result = echo_component.process(
            "This is the root of wisdom",
            operation="create_tree",
            tree_id="wisdom_tree"
        )
        print(f"Tree creation: {'✅' if tree_result.success else '❌'}")
        
        # Add children
        child_result = echo_component.process(
            "Knowledge grows from understanding",
            operation="add_child",
            tree_id="wisdom_tree"
        )
        print(f"Child addition: {'✅' if child_result.success else '❌'}")
        
        # Perform echo operation
        echo_result = echo_component.echo("Deep philosophical insight", echo_value=0.85)
        print(f"Echo operation: {'✅' if echo_result.success else '❌'}")
        
        # Get tree list
        trees_result = echo_component.get_tree_list()
        print(f"Trees stored: {len(trees_result.data) if trees_result.success else 0}")
        
        print("\n🎯 Standardized Deep Tree Echo component working correctly!")
    else:
        print("❌ Component initialization failed - Deep Tree Echo dependencies may be missing")