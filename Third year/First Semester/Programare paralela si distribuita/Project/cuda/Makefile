# Makefile for CUDA N-Body Simulation

# Compiler
NVCC = nvcc

# Compiler flags
NVCC_FLAGS = -O3 -std=c++11 -arch=sm_75

# Adjust -arch=sm_XX based on your GPU:
# sm_75 = Compute Capability 7.5 (RTX 20xx, GTX 16xx)
# sm_80 = Compute Capability 8.0 (RTX 30xx, A100)
# sm_86 = Compute Capability 8.6 (RTX 30xx)
# sm_89 = Compute Capability 8.9 (RTX 40xx)

# Target executable
TARGET = nbody_cuda.exe

# Source files
SOURCES = main.cu nbody_cuda.cu

# Default target
all: $(TARGET)

# Build target (Windows with Visual Studio)
$(TARGET): $(SOURCES)
	@echo Building CUDA n-body simulation...
	cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && nvcc $(NVCC_FLAGS) -o $(TARGET) $(SOURCES)'

# Clean build artifacts
clean:
	rm -f $(TARGET) *.o

# Run the program
run: $(TARGET)
	./$(TARGET)

# Help
help:
	@echo "Available targets:"
	@echo "  make          - Build the program"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make run      - Build and run the program"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "To check your GPU compute capability:"
	@echo "  nvidia-smi --query-gpu=compute_cap --format=csv"
	@echo ""
	@echo "Update -arch=sm_XX in Makefile to match your GPU"
	@echo ""
	@echo "On Windows, you can also use build.bat:"
	@echo "  build.bat"

.PHONY: all clean run help

