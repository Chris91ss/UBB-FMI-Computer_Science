"""
Barnes-Hut tree structure for efficient n-body force calculations.
"""
import numpy as np


class OctNode:
    """Octree node for 3D space partitioning."""
    
    def __init__(self, center, size):
        """
        Initialize an octree node.
        
        Args:
            center: numpy array [x, y, z] - center of the node
            size: float - size of the node (edge length)
        """
        self.center = np.array(center, dtype=np.float64)
        self.size = float(size)
        self.total_mass = 0.0
        self.center_of_mass = np.zeros(3, dtype=np.float64)
        self.body = None  # If leaf node, contains a body
        self.children = [None] * 8  # 8 octants
    
    def is_leaf(self):
        """Check if this is a leaf node."""
        return self.body is not None or all(child is None for child in self.children)
    
    def get_octant(self, position):
        """
        Determine which octant a position belongs to.
        
        Returns:
            int: octant index (0-7)
        """
        octant = 0
        if position[0] > self.center[0]:
            octant |= 1
        if position[1] > self.center[1]:
            octant |= 2
        if position[2] > self.center[2]:
            octant |= 4
        return octant
    
    def get_octant_center(self, octant):
        """Get the center of a specific octant."""
        offset = self.size / 4.0
        center = self.center.copy()
        if octant & 1:
            center[0] += offset
        else:
            center[0] -= offset
        if octant & 2:
            center[1] += offset
        else:
            center[1] -= offset
        if octant & 4:
            center[2] += offset
        else:
            center[2] -= offset
        return center


class BarnesHutTree:
    """Barnes-Hut tree for n-body simulation."""
    
    def __init__(self, bodies, theta=0.5):
        """
        Initialize and build the Barnes-Hut tree.
        
        Args:
            bodies: list of Body objects
            theta: float, threshold for approximation (default 0.5)
        """
        self.bodies = bodies
        self.theta = theta
        self.root = None
        self.build_tree()
    
    def build_tree(self):
        """Build the Barnes-Hut tree from bodies."""
        if not self.bodies:
            return
        
        # Find bounding box
        positions = np.array([body.position for body in self.bodies])
        min_pos = positions.min(axis=0)
        max_pos = positions.max(axis=0)
        
        # Calculate center and size
        center = (min_pos + max_pos) / 2.0
        size = max(max_pos - min_pos) * 1.1  # Add 10% padding
        
        # Create root node
        self.root = OctNode(center, size)
        
        # Insert all bodies
        for body in self.bodies:
            self._insert(self.root, body)
        
        # Calculate center of mass for all nodes
        self._calculate_com(self.root)
    
    def _insert(self, node, body):
        """Insert a body into the tree."""
        if node.is_leaf():
            if node.body is None:
                # Empty leaf, insert here
                node.body = body
                node.total_mass = body.mass
                node.center_of_mass = body.position.copy()
                return
            else:
                # Leaf with body, need to subdivide
                old_body = node.body
                node.body = None
                
                # Subdivide and reinsert old body
                self._subdivide(node)
                self._insert(node, old_body)
        
        # Insert into appropriate child
        octant = node.get_octant(body.position)
        if node.children[octant] is None:
            child_center = node.get_octant_center(octant)
            node.children[octant] = OctNode(child_center, node.size / 2.0)
        
        self._insert(node.children[octant], body)
    
    def _subdivide(self, node):
        """Subdivide a node into 8 children."""
        for i in range(8):
            if node.children[i] is None:
                child_center = node.get_octant_center(i)
                node.children[i] = OctNode(child_center, node.size / 2.0)
    
    def _calculate_com(self, node):
        """Calculate center of mass for a node and its children."""
        if node.body is not None:
            node.total_mass = node.body.mass
            node.center_of_mass = node.body.position.copy()
            return
        
        total_mass = 0.0
        com = np.zeros(3, dtype=np.float64)
        
        for child in node.children:
            if child is not None:
                self._calculate_com(child)
                total_mass += child.total_mass
                com += child.center_of_mass * child.total_mass
        
        if total_mass > 0:
            node.total_mass = total_mass
            node.center_of_mass = com / total_mass
    
    def calculate_force(self, body, G=1.0):
        """
        Calculate gravitational force on a body using the tree.
        
        Args:
            body: Body object
            G: gravitational constant (default 1.0)
        
        Returns:
            numpy array: force vector [fx, fy, fz]
        """
        force = np.zeros(3, dtype=np.float64)
        self._calculate_force_recursive(self.root, body, force, G)
        return force
    
    def _calculate_force_recursive(self, node, body, force, G):
        """Recursively calculate force from tree node."""
        if node is None or node.total_mass == 0:
            return
        
        # Vector from body to node center of mass
        r = node.center_of_mass - body.position
        distance = np.linalg.norm(r)
        
        # Avoid self-interaction and division by zero
        if distance < 1e-10:
            return
        
        # Check if node is far enough (s/d < theta)
        s = node.size
        if s / distance < self.theta or node.is_leaf():
            # Use approximation or direct calculation
            if node.body is not None and node.body is not body:
                # Direct calculation for leaf
                force_magnitude = G * body.mass * node.body.mass / (distance ** 3)
                force += force_magnitude * r
            elif node.body is None:
                # Approximation for internal node
                force_magnitude = G * body.mass * node.total_mass / (distance ** 3)
                force += force_magnitude * r
        else:
            # Need to recurse into children
            for child in node.children:
                if child is not None:
                    self._calculate_force_recursive(child, body, force, G)

