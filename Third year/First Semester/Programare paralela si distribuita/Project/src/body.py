"""
Body class representing a particle in the n-body simulation.
"""
import numpy as np


class Body:
    """Represents a single body with position, velocity, and mass."""
    
    def __init__(self, position, velocity, mass):
        """
        Initialize a body.
        
        Args:
            position: numpy array [x, y, z]
            velocity: numpy array [vx, vy, vz]
            mass: float, mass of the body
        """
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.mass = float(mass)
        self.force = np.zeros(3, dtype=np.float64)
    
    def update_position(self, dt):
        """Update position based on velocity."""
        self.position += self.velocity * dt
    
    def update_velocity(self, dt):
        """Update velocity based on force."""
        self.velocity += self.force * dt / self.mass
    
    def reset_force(self):
        """Reset force to zero."""
        self.force.fill(0.0)
    
    def __repr__(self):
        return f"Body(pos={self.position}, vel={self.velocity}, mass={self.mass})"

