#ifndef NBODY_CUDA_H
#define NBODY_CUDA_H

// CUDA kernel declarations
// These kernels are defined in nbody_cuda.cu
// When compiling with nvcc, both files are compiled together so kernels are visible

__global__ void calculate_forces(
    const double* positions,
    const double* masses,
    double* forces,
    int num_bodies,
    double G,
    double softening
);

__global__ void update_bodies(
    double* positions,
    double* velocities,
    const double* forces,
    const double* masses,
    int num_bodies,
    double dt
);

#endif // NBODY_CUDA_H

