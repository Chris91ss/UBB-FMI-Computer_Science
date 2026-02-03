# Makefile for CUDA Polynomial Multiplication

# Compiler
NVCC = nvcc

# Compiler flags
NVCC_FLAGS = -O3 -arch=sm_75 -std=c++11 -Xcompiler -fopenmp

# If you have an older GPU, you may need to change the architecture
# Common architectures:
# - sm_35, sm_37 (Kepler)
# - sm_50, sm_52 (Maxwell)
# - sm_60, sm_61, sm_62 (Pascal)
# - sm_70, sm_72 (Volta)
# - sm_75 (Turing)
# - sm_80, sm_86 (Ampere)
# - sm_89 (Ada)
# - sm_90 (Hopper)

# To find your GPU architecture, run: nvidia-smi --query-gpu=compute_cap --format=csv

# Target executable
TARGET = polynomial_cuda

# Source files
SOURCES = main.cu polynomial_cuda.cu

# Object files
OBJECTS = $(SOURCES:.cu=.o)

# Default target
all: $(TARGET)

# Build target
$(TARGET): $(OBJECTS)
	$(NVCC) $(NVCC_FLAGS) -o $(TARGET) $(OBJECTS)

# Compile .cu files to .o files
%.o: %.cu
	$(NVCC) $(NVCC_FLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(TARGET) $(OBJECTS)

# Run the program
run: $(TARGET)
	./$(TARGET)

# Run with custom degrees
run-test: $(TARGET)
	./$(TARGET) 100 100

.PHONY: all clean run run-test






