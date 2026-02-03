# Algorithms

## N-Body Problem

The n-body problem is a classical problem in physics that involves predicting the motion of n particles under the influence of gravitational forces. Each body exerts a gravitational force on every other body according to Newton's law of universal gravitation:

F = G * (m1 * m2) / r^2

where:
- F is the gravitational force magnitude
- G is the gravitational constant
- m1 and m2 are the masses of the two bodies
- r is the distance between the bodies

The force vector is:

F_vec = G * (m1 * m2) / r^3 * r_vec

where r_vec is the vector from body 1 to body 2.

For each body, we need to:
1. Calculate the total force from all other bodies
2. Update velocity: v_new = v_old + (F/m) * dt
3. Update position: x_new = x_old + v_new * dt

## Direct Force Calculation

The naive approach calculates forces directly between all pairs of bodies:

```
for each body i:
    force[i] = 0
    for each body j (j != i):
        r = position[j] - position[i]
        distance = |r|
        force[i] += G * mass[i] * mass[j] / distance^3 * r
```

**Time Complexity:** O(n²) per time step, where n is the number of bodies.

## Barnes-Hut Algorithm

The Barnes-Hut algorithm is an approximation method that reduces the complexity from O(n²) to O(n log n) by using a hierarchical tree structure (octree in 3D).

### Algorithm Overview

1. **Tree Construction:** Build an octree that partitions 3D space recursively
2. **Force Calculation:** For each body, traverse the tree:
   - If a node is far enough (s/d < θ), use the node's center of mass as an approximation
   - If a node is too close, recurse into its children
   - θ (theta) is a threshold parameter (typically 0.5)

### Pseudocode

```
BuildTree(bodies):
    Find bounding box
    Create root node
    For each body:
        Insert body into tree

Insert(node, body):
    If node is empty:
        Place body in node
    Else if node is leaf:
        Subdivide node
        Reinsert old body
        Insert new body
    Else:
        Insert body into appropriate child octant

CalculateForce(tree, body):
    force = 0
    CalculateForceRecursive(tree.root, body, force)
    return force

CalculateForceRecursive(node, body, force):
    If node is null:
        return
    
    r = node.center_of_mass - body.position
    distance = |r|
    
    If distance is very small:
        return  # Avoid self-interaction
    
    If (node.size / distance < theta) OR node is leaf:
        If node is leaf and node.body != body:
            force += G * body.mass * node.body.mass / distance^3 * r
        Else:
            force += G * body.mass * node.total_mass / distance^3 * r
    Else:
        For each child of node:
            CalculateForceRecursive(child, body, force)
```

### Time Complexity

- **Tree Construction:** O(n log n)
- **Force Calculation:** O(n log n) per body, O(n² log n) total (but with good constant factors)
- **Overall:** O(n log n) per time step (much better than O(n²) for large n)

### Accuracy

The Barnes-Hut algorithm is an approximation. The accuracy depends on the θ parameter:
- Smaller θ: More accurate but slower (more tree traversals)
- Larger θ: Less accurate but faster (fewer tree traversals)
- Typical value: θ = 0.5 provides good balance

