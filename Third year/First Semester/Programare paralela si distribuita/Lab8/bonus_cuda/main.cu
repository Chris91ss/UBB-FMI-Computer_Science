#include <iostream>
#include <iomanip>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <cuda_runtime.h>
#include "polynomial_cuda.h"

void print_separator() {
    std::cout << "============================================================" << std::endl;
}

void print_section_header(const std::string& title) {
    std::cout << std::endl;
    print_separator();
    std::cout << title << std::endl;
    print_separator();
}

void run_basic_test() {
    print_section_header("BASIC FUNCTIONALITY TEST");
    
    // Test with small polynomials
    std::vector<int> poly1 = {1, 2, 3};  // 1 + 2x + 3x^2
    std::vector<int> poly2 = {4, 5};      // 4 + 5x
    
    std::cout << "Polynomial 1: ";
    print_polynomial(poly1);
    std::cout << "Polynomial 2: ";
    print_polynomial(poly2);
    std::cout << std::endl;
    
    // CPU regular
    auto start = std::chrono::high_resolution_clock::now();
    std::vector<int> cpu_result = cpu_regular_multiply(poly1, poly2);
    auto end = std::chrono::high_resolution_clock::now();
    double cpu_time = std::chrono::duration<double>(end - start).count();
    
    // CUDA regular
    std::vector<int> cuda_result;
    float cuda_time = cuda_regular_multiply(poly1, poly2, cuda_result);
    
    std::cout << "CPU Regular Result: ";
    print_polynomial(cpu_result);
    std::cout << "CUDA Regular Result: ";
    print_polynomial(cuda_result);
    
    if (polynomials_equal(cpu_result, cuda_result)) {
        std::cout << "[OK] Results match!" << std::endl;
    } else {
        std::cout << "[ERROR] Results differ!" << std::endl;
    }
    
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "CPU Time: " << cpu_time << " seconds" << std::endl;
    std::cout << "CUDA Time: " << cuda_time << " seconds" << std::endl;
    std::cout << "Speedup: " << cpu_time / cuda_time << "x" << std::endl;
}

void run_performance_comparison() {
    print_section_header("PERFORMANCE COMPARISON");
    
    struct TestConfig {
        int deg1, deg2;
        std::string name;
    };
    
    std::vector<TestConfig> configs = {
        {10, 10, "Small (10x10)"},
        {50, 50, "Medium (50x50)"},
        {100, 100, "Large (100x100)"},
        {200, 200, "Very Large (200x200)"},
        {500, 500, "Huge (500x500)"}
    };
    
    std::cout << std::fixed << std::setprecision(6);
    std::cout << std::left << std::setw(20) << "Size" 
              << std::right << std::setw(15) << "CPU Reg (s)"
              << std::setw(15) << "CUDA Reg (s)"
              << std::setw(12) << "Speedup"
              << std::setw(15) << "CPU Kar (s)"
              << std::setw(15) << "CUDA Kar (s)"
              << std::setw(12) << "Speedup"
              << std::setw(10) << "Status" << std::endl;
    std::cout << std::string(114, '-') << std::endl;
    
    for (const auto& config : configs) {
        std::vector<int> poly1 = generate_random_polynomial(config.deg1);
        std::vector<int> poly2 = generate_random_polynomial(config.deg2);
        
        // CPU Regular
        auto start = std::chrono::high_resolution_clock::now();
        std::vector<int> cpu_reg_result = cpu_regular_multiply(poly1, poly2);
        auto end = std::chrono::high_resolution_clock::now();
        double cpu_reg_time = std::chrono::duration<double>(end - start).count();
        
        // CUDA Regular
        std::vector<int> cuda_reg_result;
        float cuda_reg_time = cuda_regular_multiply(poly1, poly2, cuda_reg_result);
        
        // CPU Karatsuba
        start = std::chrono::high_resolution_clock::now();
        std::vector<int> cpu_kar_result = cpu_karatsuba_multiply(poly1, poly2);
        end = std::chrono::high_resolution_clock::now();
        double cpu_kar_time = std::chrono::duration<double>(end - start).count();
        
        // CUDA Karatsuba
        std::vector<int> cuda_kar_result;
        float cuda_kar_time = cuda_karatsuba_multiply(poly1, poly2, cuda_kar_result, 32);
        
        // Verify correctness
        bool reg_correct = polynomials_equal(cpu_reg_result, cuda_reg_result);
        bool kar_correct = polynomials_equal(cpu_kar_result, cuda_kar_result);
        
        double reg_speedup = (cuda_reg_time > 0) ? (cpu_reg_time / cuda_reg_time) : 0.0;
        double kar_speedup = (cuda_kar_time > 0) ? (cpu_kar_time / cuda_kar_time) : 0.0;
        
        std::cout << std::left << std::setw(20) << config.name
                  << std::right << std::setprecision(6) << std::setw(15) << cpu_reg_time
                  << std::setw(15) << cuda_reg_time
                  << std::setprecision(2) << std::setw(12) << reg_speedup << "x"
                  << std::setprecision(6) << std::setw(15) << cpu_kar_time
                  << std::setw(15) << cuda_kar_time
                  << std::setprecision(2) << std::setw(12) << kar_speedup << "x";
        
        if (reg_correct && kar_correct) {
            std::cout << std::setw(10) << "[OK]";
        } else {
            std::cout << std::setw(10) << "[ERROR]";
        }
        std::cout << std::endl;
    }
}

void run_detailed_test(int degree1, int degree2) {
    print_section_header("DETAILED TEST");
    
    std::vector<int> poly1 = generate_random_polynomial(degree1);
    std::vector<int> poly2 = generate_random_polynomial(degree2);
    
    std::cout << "Polynomial 1 (degree " << degree1 << "): ";
    if (degree1 <= 10) {
        print_polynomial(poly1);
    } else {
        std::cout << "[too large to display]" << std::endl;
    }
    
    std::cout << "Polynomial 2 (degree " << degree2 << "): ";
    if (degree2 <= 10) {
        print_polynomial(poly2);
    } else {
        std::cout << "[too large to display]" << std::endl;
    }
    std::cout << std::endl;
    
    // CPU Regular
    auto start = std::chrono::high_resolution_clock::now();
    std::vector<int> cpu_reg_result = cpu_regular_multiply(poly1, poly2);
    auto end = std::chrono::high_resolution_clock::now();
    double cpu_reg_time = std::chrono::duration<double>(end - start).count();
    
    // CUDA Regular
    std::vector<int> cuda_reg_result;
    float cuda_reg_time = cuda_regular_multiply(poly1, poly2, cuda_reg_result);
    
    // CPU Karatsuba
    start = std::chrono::high_resolution_clock::now();
    std::vector<int> cpu_kar_result = cpu_karatsuba_multiply(poly1, poly2);
    end = std::chrono::high_resolution_clock::now();
    double cpu_kar_time = std::chrono::duration<double>(end - start).count();
    
    // CUDA Karatsuba
    std::vector<int> cuda_kar_result;
    float cuda_kar_time = cuda_karatsuba_multiply(poly1, poly2, cuda_kar_result, 32);
    
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "CPU Regular:    " << cpu_reg_time << " seconds" << std::endl;
    std::cout << "CUDA Regular:   " << cuda_reg_time << " seconds (speedup: " 
              << (cpu_reg_time / cuda_reg_time) << "x)" << std::endl;
    std::cout << "CPU Karatsuba:  " << cpu_kar_time << " seconds" << std::endl;
    std::cout << "CUDA Karatsuba: " << cuda_kar_time << " seconds (speedup: " 
              << (cpu_kar_time / cuda_kar_time) << "x)" << std::endl;
    
    bool reg_match = polynomials_equal(cpu_reg_result, cuda_reg_result);
    bool kar_match = polynomials_equal(cpu_kar_result, cuda_kar_result);
    
    std::cout << std::endl;
    if (reg_match && kar_match) {
        std::cout << "[OK] All results match!" << std::endl;
    } else {
        std::cout << "[ERROR] Results differ!" << std::endl;
        if (!reg_match) std::cout << "  - Regular multiplication results differ" << std::endl;
        if (!kar_match) std::cout << "  - Karatsuba multiplication results differ" << std::endl;
    }
}

int main(int argc, char* argv[]) {
    std::cout << "============================================================" << std::endl;
    std::cout << "CUDA Polynomial Multiplication - Performance Comparison" << std::endl;
    std::cout << "============================================================" << std::endl;
    
    // Check for CUDA device
    int deviceCount;
    cudaError_t err = cudaGetDeviceCount(&deviceCount);
    if (err != cudaSuccess) {
        std::cerr << "Error getting CUDA device count: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }
    if (deviceCount == 0) {
        std::cerr << "Error: No CUDA devices found!" << std::endl;
        return 1;
    }
    
    // Set device
    err = cudaSetDevice(0);
    if (err != cudaSuccess) {
        std::cerr << "Error setting CUDA device: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }
    
    cudaDeviceProp prop;
    err = cudaGetDeviceProperties(&prop, 0);
    if (err != cudaSuccess) {
        std::cerr << "Error getting device properties: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }
    
    // Fix encoding issue with device name on Windows
    std::cout << "CUDA Device: ";
    for (int i = 0; i < 256 && prop.name[i] != '\0'; i++) {
        if (prop.name[i] >= 32 && prop.name[i] < 127) {
            std::cout << prop.name[i];
        }
    }
    std::cout << std::endl;
    std::cout << "Compute Capability: " << prop.major << "." << prop.minor << std::endl;
    std::cout << "Total Global Memory: " << (prop.totalGlobalMem / (1024 * 1024)) << " MB" << std::endl;
    std::cout << "Multiprocessors: " << prop.multiProcessorCount << std::endl;
    std::cout << std::endl;
    
    if (argc == 1) {
        // Run all tests
        run_basic_test();
        run_performance_comparison();
    } else if (argc == 3) {
        // Run detailed test with specified degrees
        int deg1 = std::atoi(argv[1]);
        int deg2 = std::atoi(argv[2]);
        run_detailed_test(deg1, deg2);
    } else {
        std::cout << "Usage: " << argv[0] << " [degree1 degree2]" << std::endl;
        std::cout << "  If no arguments provided, runs all tests" << std::endl;
        std::cout << "  If two arguments provided, runs detailed test with specified degrees" << std::endl;
        return 1;
    }
    
    return 0;
}

