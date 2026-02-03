#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include "nbody_cuda.h"  // Include kernel declarations

// Forward declarations
void generate_random_bodies(double* positions, double* velocities, double* masses, int num_bodies, int seed);
void print_bodies(const double* positions, const double* velocities, const double* masses, int num_bodies, int max_print);
double get_elapsed_time(clock_t start, clock_t end);
void save_results_to_file(const double* positions, const double* velocities, const double* masses, 
                          int num_bodies, int num_steps, double total_time, double avg_time, 
                          double min_time, double max_time, double throughput);

int main(int argc, char* argv[]) {
    // Default parameters
    int num_bodies = 1000;
    int num_steps = 100;
    double dt = 0.01;
    double G = 1.0;
    double softening = 0.01;
    
    // Parse command line arguments
    if (argc >= 2) {
        num_bodies = atoi(argv[1]);
    }
    if (argc >= 3) {
        num_steps = atoi(argv[2]);
    }
    if (argc >= 4) {
        dt = atof(argv[3]);
    }
    
    printf("\n");
    printf("============================================================\n");
    printf("  CUDA SIMULATION\n");
    printf("============================================================\n");
    printf("\n");
    
    // Check for CUDA device
    int device_count;
    cudaError_t err = cudaGetDeviceCount(&device_count);
    if (err != cudaSuccess || device_count == 0) {
        fprintf(stderr, "Error: No CUDA devices found!\n");
        return 1;
    }
    
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);
    
    // Allocate host memory
    size_t pos_size = num_bodies * 3 * sizeof(double);
    size_t vel_size = num_bodies * 3 * sizeof(double);
    size_t mass_size = num_bodies * sizeof(double);
    size_t force_size = num_bodies * 3 * sizeof(double);
    
    double* h_positions = (double*)malloc(pos_size);
    double* h_velocities = (double*)malloc(vel_size);
    double* h_masses = (double*)malloc(mass_size);
    double* h_forces = (double*)malloc(force_size);
    
    if (!h_positions || !h_velocities || !h_masses || !h_forces) {
        fprintf(stderr, "Error: Failed to allocate host memory!\n");
        return 1;
    }
    
    // Generate initial conditions
    printf("Generating %d bodies...\n", num_bodies);
    generate_random_bodies(h_positions, h_velocities, h_masses, num_bodies, 42);
    
    // Allocate device memory
    double* d_positions;
    double* d_velocities;
    double* d_masses;
    double* d_forces;
    
    err = cudaMalloc((void**)&d_positions, pos_size);
    if (err != cudaSuccess) {
        fprintf(stderr, "Error: Failed to allocate device memory for positions!\n");
        return 1;
    }
    
    err = cudaMalloc((void**)&d_velocities, vel_size);
    if (err != cudaSuccess) {
        fprintf(stderr, "Error: Failed to allocate device memory for velocities!\n");
        return 1;
    }
    
    err = cudaMalloc((void**)&d_masses, mass_size);
    if (err != cudaSuccess) {
        fprintf(stderr, "Error: Failed to allocate device memory for masses!\n");
        return 1;
    }
    
    err = cudaMalloc((void**)&d_forces, force_size);
    if (err != cudaSuccess) {
        fprintf(stderr, "Error: Failed to allocate device memory for forces!\n");
        return 1;
    }
    
    // Copy initial data to device
    cudaMemcpy(d_positions, h_positions, pos_size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_velocities, h_velocities, vel_size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_masses, h_masses, mass_size, cudaMemcpyHostToDevice);
    
    // Configure kernel launch parameters
    int block_size = 256;
    int grid_size = (num_bodies + block_size - 1) / block_size;
    
    printf("\nRunning simulation on GPU for %d steps...\n", num_steps);
    printf("------------------------------------------------------------\n");
    
    // Timing
    clock_t total_start = clock();
    double* step_times = (double*)malloc(num_steps * sizeof(double));
    double total_elapsed = 0.0;
    
    // Simulation loop
    for (int step = 0; step < num_steps; step++) {
        clock_t step_start = clock();
        
        // Reset forces
        cudaMemset(d_forces, 0, force_size);
        
        // Calculate forces
        calculate_forces<<<grid_size, block_size>>>(
            d_positions,
            d_masses,
            d_forces,
            num_bodies,
            G,
            softening
        );
        
        // Check for kernel errors
        err = cudaGetLastError();
        if (err != cudaSuccess) {
            fprintf(stderr, "Error in calculate_forces kernel: %s\n", cudaGetErrorString(err));
            return 1;
        }
        
        // Update positions and velocities
        update_bodies<<<grid_size, block_size>>>(
            d_positions,
            d_velocities,
            d_forces,
            d_masses,
            num_bodies,
            dt
        );
        
        // Check for kernel errors
        err = cudaGetLastError();
        if (err != cudaSuccess) {
            fprintf(stderr, "Error in update_bodies kernel: %s\n", cudaGetErrorString(err));
            return 1;
        }
        
        // Synchronize
        cudaDeviceSynchronize();
        
        clock_t step_end = clock();
        step_times[step] = get_elapsed_time(step_start, step_end);
        total_elapsed += step_times[step];
        
        // Print progress every 5 steps (matching Python format)
        if ((step + 1) % 5 == 0 || step == 0 || step == num_steps - 1) {
            printf("Step %d/%d completed (step time: %.4fs, total: %.2fs)\n", 
                   step + 1, num_steps, step_times[step], total_elapsed);
        }
    }
    
    clock_t total_end = clock();
    double total_time = get_elapsed_time(total_start, total_end);
    
    // Copy results back to host
    cudaMemcpy(h_positions, d_positions, pos_size, cudaMemcpyDeviceToHost);
    cudaMemcpy(h_velocities, d_velocities, vel_size, cudaMemcpyDeviceToHost);
    
    // Calculate statistics
    double avg_step_time = 0.0;
    double min_step_time = step_times[0];
    double max_step_time = step_times[0];
    for (int i = 0; i < num_steps; i++) {
        avg_step_time += step_times[i];
        if (step_times[i] < min_step_time) min_step_time = step_times[i];
        if (step_times[i] > max_step_time) max_step_time = step_times[i];
    }
    avg_step_time /= num_steps;
    
    // Print results (matching Python format)
    printf("\n");
    printf("================================================================================\n");
    printf("PERFORMANCE METRICS\n");
    printf("================================================================================\n");
    printf("Number of bodies: %d\n", num_bodies);
    printf("Number of steps: %d\n", num_steps);
    printf("Total execution time: %.4f seconds\n", total_time);
    printf("Average time per step: %.4f seconds\n", avg_step_time);
    printf("Min time per step: %.4f seconds\n", min_step_time);
    printf("Max time per step: %.4f seconds\n", max_step_time);
    printf("Throughput: %.2f body-steps/second\n", (num_bodies * num_steps) / total_time);
    printf("================================================================================\n");
    printf("\n");
    
    // Print body information
    print_bodies(h_positions, h_velocities, h_masses, num_bodies, 10);
    
    // Save results to file
    save_results_to_file(h_positions, h_velocities, h_masses, num_bodies, num_steps,
                         total_time, avg_step_time, min_step_time, max_step_time,
                         (num_bodies * num_steps) / total_time);
    
    // Cleanup
    free(h_positions);
    free(h_velocities);
    free(h_masses);
    free(h_forces);
    free(step_times);
    
    cudaFree(d_positions);
    cudaFree(d_velocities);
    cudaFree(d_masses);
    cudaFree(d_forces);
    
    return 0;
}

void generate_random_bodies(double* positions, double* velocities, double* masses, int num_bodies, int seed) {
    srand(seed);
    
    for (int i = 0; i < num_bodies; i++) {
        // Random position in cube [-10, 10]^3
        positions[i * 3 + 0] = (double)rand() / RAND_MAX * 20.0 - 10.0;
        positions[i * 3 + 1] = (double)rand() / RAND_MAX * 20.0 - 10.0;
        positions[i * 3 + 2] = (double)rand() / RAND_MAX * 20.0 - 10.0;
        
        // Random velocity in [-0.1, 0.1]^3
        velocities[i * 3 + 0] = (double)rand() / RAND_MAX * 0.2 - 0.1;
        velocities[i * 3 + 1] = (double)rand() / RAND_MAX * 0.2 - 0.1;
        velocities[i * 3 + 2] = (double)rand() / RAND_MAX * 0.2 - 0.1;
        
        // Random mass in [0.1, 1.0]
        masses[i] = (double)rand() / RAND_MAX * 0.9 + 0.1;
    }
}

void print_bodies(const double* positions, const double* velocities, const double* masses, int num_bodies, int max_print) {
    printf("================================================================================\n");
    printf("BODY INFORMATION\n");
    printf("================================================================================\n");
    printf("%-8s %-12s %-12s %-12s %-12s %-12s %-12s %-10s\n", 
           "Index", "X", "Y", "Z", "VX", "VY", "VZ", "Mass");
    printf("--------------------------------------------------------------------------------\n");
    
    int print_count = (num_bodies < max_print) ? num_bodies : max_print;
    for (int i = 0; i < print_count; i++) {
        printf("%-8d %-12.4f %-12.4f %-12.4f %-12.4f %-12.4f %-12.4f %-10.4f\n",
               i,
               positions[i * 3 + 0], positions[i * 3 + 1], positions[i * 3 + 2],
               velocities[i * 3 + 0], velocities[i * 3 + 1], velocities[i * 3 + 2],
               masses[i]);
    }
    
    if (num_bodies > max_print) {
        printf("... (%d more bodies)\n", num_bodies - max_print);
    }
    
    printf("================================================================================\n");
    printf("\n");
}

double get_elapsed_time(clock_t start, clock_t end) {
    return ((double)(end - start)) / CLOCKS_PER_SEC;
}

void save_results_to_file(const double* positions, const double* velocities, const double* masses, 
                          int num_bodies, int num_steps, double total_time, double avg_time, 
                          double min_time, double max_time, double throughput) {
    // Generate filename with timestamp
    time_t rawtime;
    struct tm* timeinfo;
    char filename[256];
    char timestamp[32];
    
    time(&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(timestamp, sizeof(timestamp), "%Y%m%d_%H%M%S", timeinfo);
    sprintf(filename, "results_CUDA_%s.txt", timestamp);
    
    FILE* f = fopen(filename, "w");
    if (f == NULL) {
        printf("Warning: Could not open file for writing: %s\n", filename);
        return;
    }
    
    // Get current date/time string
    char datetime_str[64];
    strftime(datetime_str, sizeof(datetime_str), "%Y-%m-%d %H:%M:%S", timeinfo);
    
    // Write header
    fprintf(f, "================================================================================\n");
    fprintf(f, "N-BODY SIMULATION RESULTS\n");
    fprintf(f, "Simulation Type: CUDA\n");
    fprintf(f, "Date: %s\n", datetime_str);
    fprintf(f, "================================================================================\n");
    fprintf(f, "\n");
    
    // Write performance metrics
    fprintf(f, "PERFORMANCE METRICS\n");
    fprintf(f, "--------------------------------------------------------------------------------\n");
    fprintf(f, "Number of bodies: %d\n", num_bodies);
    fprintf(f, "Number of steps: %d\n", num_steps);
    fprintf(f, "Total execution time: %.4f seconds\n", total_time);
    fprintf(f, "Average time per step: %.4f seconds\n", avg_time);
    fprintf(f, "Min time per step: %.4f seconds\n", min_time);
    fprintf(f, "Max time per step: %.4f seconds\n", max_time);
    fprintf(f, "Throughput: %.2f body-steps/second\n", throughput);
    fprintf(f, "\n");
    fprintf(f, "================================================================================\n");
    fprintf(f, "\n");
    
    // Write body information
    fprintf(f, "BODY INFORMATION\n");
    fprintf(f, "--------------------------------------------------------------------------------\n");
    fprintf(f, "%-8s %-12s %-12s %-12s %-12s %-12s %-12s %-10s\n", 
           "Index", "X", "Y", "Z", "VX", "VY", "VZ", "Mass");
    fprintf(f, "--------------------------------------------------------------------------------\n");
    
    for (int i = 0; i < num_bodies; i++) {
        fprintf(f, "%-8d %-12.4f %-12.4f %-12.4f %-12.4f %-12.4f %-12.4f %-10.4f\n",
               i,
               positions[i * 3 + 0], positions[i * 3 + 1], positions[i * 3 + 2],
               velocities[i * 3 + 0], velocities[i * 3 + 1], velocities[i * 3 + 2],
               masses[i]);
    }
    
    fprintf(f, "================================================================================\n");
    
    fclose(f);
    
    printf("Results saved to: %s\n", filename);
}

