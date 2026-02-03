# Building and Running the CUDA N-Body Simulation Program

## Prerequisites

1. **NVIDIA GPU** with CUDA support

2. **CUDA Toolkit** installed (download from https://developer.nvidia.com/cuda-downloads)

3. **C++ Compiler** (Visual Studio or MinGW on Windows)

4. **Make** (optional, see alternative methods below)

## Method 1: Using Make (Recommended if you have Make installed)

### Step 1: Check your GPU architecture

```powershell
nvidia-smi --query-gpu=compute_cap --format=csv
```

This will show your GPU's compute capability (e.g., 7.5, 8.0, etc.)

### Step 2: Update Makefile (if needed)

Open `Makefile` and check the `-arch=sm_XX` flag. Update it to match your GPU:

- sm_75 = Compute Capability 7.5 (RTX 20xx, GTX 16xx)
- sm_80 = Compute Capability 8.0 (RTX 30xx, A100)
- sm_86 = Compute Capability 8.6 (RTX 30xx)
- sm_89 = Compute Capability 8.9 (RTX 40xx)

### Step 3: Build

**Option A: Using build.bat (Windows, recommended)**
```powershell
cd cuda
.\build.bat
```

**Option B: Using make**
```powershell
cd cuda
make
```

**Option C: Direct command**
```powershell
cd cuda
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && nvcc -O3 -arch=sm_75 -std=c++11 -o nbody_cuda.exe main.cu nbody_cuda.cu'
```

### Step 4: Run

```powershell
# Run with default parameters (1000 bodies, 100 steps)
.\nbody_cuda.exe

# Run with specific number of bodies and steps
.\nbody_cuda.exe 2000 200

# Run with custom bodies, steps, and time step
.\nbody_cuda.exe 2000 200 0.01
```

## Method 2: Direct nvcc Command (If Make is not available)

### Step 1: Find your GPU compute capability

```powershell
nvidia-smi --query-gpu=compute_cap --format=csv
```

### Step 2: Build directly with nvcc

```powershell
cd cuda

# Replace sm_75 with your GPU's compute capability
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && nvcc -O3 -arch=sm_75 -std=c++11 -o nbody_cuda.exe main.cu nbody_cuda.cu'
```

### Step 3: Run

```powershell
.\nbody_cuda.exe
```

## Method 3: Using Visual Studio (Windows)

1. Create a new CUDA project in Visual Studio

2. Add the source files: `main.cu`, `nbody_cuda.cu`, `nbody_cuda.h`

3. Set the project properties:

   - CUDA C/C++ → Device → Code Generation: `compute_75,sm_75` (adjust for your GPU)

   - C/C++ → Language → C++ Language Standard: C++11 or later

4. Build and run

## Program Usage

The program accepts command-line arguments:

```powershell
.\nbody_cuda.exe [num_bodies] [num_steps] [dt]
```

- `num_bodies`: Number of bodies to simulate (default: 1000)
- `num_steps`: Number of simulation steps (default: 100)
- `dt`: Time step size (default: 0.01)

Examples:

```powershell
# Default: 1000 bodies, 100 steps, dt=0.01
.\nbody_cuda.exe

# 2000 bodies, 200 steps
.\nbody_cuda.exe 2000 200

# 5000 bodies, 500 steps, dt=0.005
.\nbody_cuda.exe 5000 500 0.005
```

## Troubleshooting

### "nvcc is not recognized"

- Add CUDA bin directory to PATH:

  - Usually: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vXX.X\bin`

  - Or run from Visual Studio Developer Command Prompt

### "No CUDA devices found"

- Check that NVIDIA drivers are installed: `nvidia-smi`

- Verify CUDA toolkit is properly installed

- Make sure you have an NVIDIA GPU (not just integrated graphics)

### "compute capability mismatch"

- Update the `-arch=sm_XX` flag to match your GPU

- Check your GPU's compute capability with `nvidia-smi --query-gpu=compute_cap --format=csv`

### Build errors

- Ensure CUDA toolkit is in your PATH

- Check that you're using a compatible C++ compiler

- On Windows, you may need Visual Studio Build Tools or MinGW

## Quick Test

To verify CUDA is working:

```powershell
nvcc --version
nvidia-smi
```

Both commands should work without errors.

## Algorithm

The CUDA implementation uses **direct force calculation** (O(n²)) rather than Barnes-Hut for simplicity on GPU:

- Each CUDA thread calculates forces for one body
- Forces are calculated from all other bodies
- Positions and velocities are updated based on calculated forces
- Massive GPU parallelism compensates for O(n²) complexity

## Performance

The program displays:
- Total execution time
- Average time per step
- Min/Max time per step
- Throughput (body-steps per second)

Results are printed to the console after the simulation completes.
