#include <cuda_runtime.h>
#include <math.h>
#include <stdio.h>

/**
 * CUDA kernel to calculate gravitational forces between all bodies.
 * Uses direct O(n²) force calculation.
 * 
 * @param positions - Array of positions [x0, y0, z0, x1, y1, z1, ...]
 * @param masses - Array of masses
 * @param forces - Output array for forces [fx0, fy0, fz0, fx1, fy1, fz1, ...]
 * @param num_bodies - Number of bodies
 * @param G - Gravitational constant
 * @param softening - Softening parameter to avoid division by zero
 */
__global__ void calculate_forces(
    const double* positions,
    const double* masses,
    double* forces,
    int num_bodies,
    double G,
    double softening
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (i >= num_bodies) return;
    
    double fx = 0.0, fy = 0.0, fz = 0.0;
    double xi = positions[i * 3 + 0];
    double yi = positions[i * 3 + 1];
    double zi = positions[i * 3 + 2];
    double mi = masses[i];
    
    // Calculate force from all other bodies
    for (int j = 0; j < num_bodies; j++) {
        if (i == j) continue;
        
        double xj = positions[j * 3 + 0];
        double yj = positions[j * 3 + 1];
        double zj = positions[j * 3 + 2];
        double mj = masses[j];
        
        // Calculate distance vector
        double dx = xj - xi;
        double dy = yj - yi;
        double dz = zj - zi;
        
        // Calculate distance squared with softening
        double dist_sq = dx * dx + dy * dy + dz * dz + softening * softening;
        double dist = sqrt(dist_sq);
        double dist_cubed = dist_sq * dist;
        
        // Calculate force magnitude
        double force_mag = G * mi * mj / dist_cubed;
        
        // Accumulate force components
        fx += force_mag * dx;
        fy += force_mag * dy;
        fz += force_mag * dz;
    }
    
    // Store force
    forces[i * 3 + 0] = fx;
    forces[i * 3 + 1] = fy;
    forces[i * 3 + 2] = fz;
}

/**
 * CUDA kernel to update positions and velocities based on forces.
 * 
 * @param positions - Array of positions [x0, y0, z0, x1, y1, z1, ...]
 * @param velocities - Array of velocities [vx0, vy0, vz0, vx1, vy1, vz1, ...]
 * @param forces - Array of forces [fx0, fy0, fz0, fx1, fy1, fz1, ...]
 * @param masses - Array of masses
 * @param num_bodies - Number of bodies
 * @param dt - Time step
 */
__global__ void update_bodies(
    double* positions,
    double* velocities,
    const double* forces,
    const double* masses,
    int num_bodies,
    double dt
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (i >= num_bodies) return;
    
    double inv_mass = 1.0 / masses[i];
    
    // Update velocity: v = v + (F/m) * dt
    velocities[i * 3 + 0] += forces[i * 3 + 0] * inv_mass * dt;
    velocities[i * 3 + 1] += forces[i * 3 + 1] * inv_mass * dt;
    velocities[i * 3 + 2] += forces[i * 3 + 2] * inv_mass * dt;
    
    // Update position: x = x + v * dt
    positions[i * 3 + 0] += velocities[i * 3 + 0] * dt;
    positions[i * 3 + 1] += velocities[i * 3 + 1] * dt;
    positions[i * 3 + 2] += velocities[i * 3 + 2] * dt;
}

