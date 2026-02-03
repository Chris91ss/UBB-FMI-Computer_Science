# Complete Guide: Building and Running CUDA Programs

This guide explains the entire process of building and running CUDA programs, specifically for Windows with Visual Studio.

## Prerequisites Check

### 1. Verify CUDA Installation
```powershell
nvcc --version
```
Should show CUDA compiler version (e.g., "Cuda compilation tools, release 12.x")

### 2. Verify GPU and Drivers
```powershell
nvidia-smi
```
Should show your NVIDIA GPU information and driver version.

### 3. Find GPU Compute Capability
```powershell
nvidia-smi --query-gpu=compute_cap --format=csv
```
This returns a number like `7.5`, `8.0`, `8.6`, etc. You'll need this for compilation.

## Project Structure

A CUDA project typically has:
```
project_folder/
├── source_file.cu          # CUDA source files (.cu extension)
├── header_file.h           # Header files
├── main.cu                 # Main program entry point
└── Makefile               # Build configuration (optional)
```

## Building CUDA Programs

### Method 1: Direct nvcc Command (Simplest)

**Step 1: Open PowerShell in project directory**

**Step 2: Set up Visual Studio environment**
CUDA's `nvcc` compiler requires Visual Studio's C++ compiler (`cl.exe`) to be in PATH. You have two options:

**Option A: Use Visual Studio Developer Command Prompt**
- Open Start Menu
- Search for "Developer Command Prompt for VS 2022" (or your VS version)
- Navigate to project folder:
  ```powershell
  cd "C:\path\to\project"
  ```

**Option B: Set up environment in regular PowerShell**
```powershell
# Run VS environment setup (adjust path to your VS installation)
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && powershell'
```

**Step 3: Compile with nvcc**
```powershell
nvcc -O3 -arch=sm_XX -std=c++11 -o program_name.exe source1.cu source2.cu main.cu
```

**Parameters explained:**
- `-O3`: Maximum optimization level
- `-arch=sm_XX`: GPU architecture (replace XX with your compute capability)
  - `sm_75` = Compute Capability 7.5 (RTX 20xx, GTX 16xx)
  - `sm_80` = Compute Capability 8.0 (RTX 30xx, A100)
  - `sm_86` = Compute Capability 8.6 (RTX 30xx)
  - `sm_89` = Compute Capability 8.9 (RTX 40xx)
- `-std=c++11`: C++ standard (may show warning, but works)
- `-o program_name.exe`: Output executable name
- Last arguments: All `.cu` source files to compile

**Example:**
```powershell
nvcc -O3 -arch=sm_75 -std=c++11 -o polynomial_cuda.exe main.cu polynomial_cuda.cu
```

### Method 2: Using Makefile

**Step 1: Create/Edit Makefile**
The Makefile contains build rules. Example:
```makefile
NVCC = nvcc
NVCC_FLAGS = -O3 -arch=sm_75 -std=c++11
TARGET = program_name
SOURCES = main.cu source.cu

$(TARGET): $(SOURCES)
	$(NVCC) $(NVCC_FLAGS) -o $(TARGET) $(SOURCES)

clean:
	rm -f $(TARGET) *.o
```

**Step 2: Build**
```powershell
# In VS Developer Command Prompt
make

# Or in PowerShell (if you have make installed)
make
```

**Note:** Make may not be available on Windows by default. Use Method 1 or Method 3 instead.

### Method 3: Visual Studio Project

**Step 1: Create CUDA Project**
- File → New → Project
- Select "CUDA Runtime" project template
- Or create Empty Project and add `.cu` files

**Step 2: Configure Project Properties**
- Right-click project → Properties
- **CUDA C/C++ → Device → Code Generation:**
  - Set to: `compute_75,sm_75` (adjust for your GPU)
- **C/C++ → Language → C++ Language Standard:** C++11 or later

**Step 3: Build**
- Build → Build Solution (or F7)

## Common Build Issues and Solutions

### Issue 1: "Cannot find compiler 'cl.exe' in PATH"
**Solution:** You need Visual Studio environment. Use one of:
- Open VS Developer Command Prompt
- Or run: `cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && your_command'`

### Issue 2: "nvcc is not recognized"
**Solution:** Add CUDA to PATH:
- Usually: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vXX.X\bin`
- Or use VS Developer Command Prompt (usually has CUDA in PATH)

### Issue 3: "compute capability mismatch"
**Solution:** Update `-arch=sm_XX` flag to match your GPU's compute capability

### Issue 4: Warning about `-std=c++11`
**Solution:** This is harmless. The flag is ignored but compilation still works.

## Running CUDA Programs

### Basic Execution
```powershell
.\program_name.exe
```

### With Arguments
```powershell
.\program_name.exe arg1 arg2
```

### Expected Behavior
- Program should detect GPU automatically
- May show GPU information (name, compute capability, memory)
- Runs computation and displays results
- If GPU not found, program will exit with error

## Complete Workflow Example

Here's the exact workflow I used for the polynomial multiplication project:

### 1. Check GPU
```powershell
nvidia-smi --query-gpu=compute_cap --format=csv
# Output: 7.5
```

### 2. Navigate to Project
```powershell
cd "C:\Users\Chris\Desktop\Third year\Programare paralela si distribuita\Lab8\bonus_cuda"
```

### 3. Build (in VS Developer Command Prompt or with environment setup)
```powershell
# Option A: Direct command (if in VS Dev Prompt)
nvcc -O3 -arch=sm_75 -std=c++11 -o polynomial_cuda.exe main.cu polynomial_cuda.cu

# Option B: From regular PowerShell with environment setup
cmd /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" && nvcc -O3 -arch=sm_75 -std=c++11 -o polynomial_cuda.exe main.cu polynomial_cuda.cu'
```

### 4. Run
```powershell
.\polynomial_cuda.exe
```

### 5. Rebuild After Changes
Simply repeat step 3. No need to clean first (nvcc handles it).

## File Organization

### Source Files (.cu)
- Contains both host code (CPU) and device code (GPU kernels)
- Device code marked with `__global__`, `__device__`, or `__host__` keywords
- Can mix C++ and CUDA code in same file

### Header Files (.h)
- Standard C++ headers
- Function declarations
- Can be included in both `.cu` and `.cpp` files

### Compilation Process
1. `nvcc` separates host and device code
2. Device code compiled to PTX (parallel thread execution)
3. Host code compiled with Visual Studio's C++ compiler
4. Linked together into executable

## Quick Reference Commands

```powershell
# Check CUDA
nvcc --version

# Check GPU
nvidia-smi
nvidia-smi --query-gpu=compute_cap --format=csv

# Build (replace sm_75 with your GPU's compute capability)
nvcc -O3 -arch=sm_75 -std=c++11 -o program.exe file1.cu file2.cu

# Run
.\program.exe

# Clean (delete executable)
Remove-Item program.exe
```

## Troubleshooting Checklist

1. ✅ CUDA toolkit installed? → `nvcc --version`
2. ✅ NVIDIA drivers installed? → `nvidia-smi`
3. ✅ Visual Studio installed? → Needed for `cl.exe`
4. ✅ GPU compute capability known? → `nvidia-smi --query-gpu=compute_cap`
5. ✅ Correct architecture flag? → Match `-arch=sm_XX` to your GPU
6. ✅ In correct directory? → `cd` to project folder
7. ✅ VS environment set up? → Use Developer Command Prompt or vcvars64.bat

## Key Takeaways for AI Assistants

When helping users build CUDA programs:

1. **Always check GPU compute capability first** - Required for `-arch` flag
2. **VS environment is critical** - `nvcc` needs `cl.exe` from Visual Studio
3. **Use Developer Command Prompt** - Simplest way to get correct environment
4. **Architecture flag must match GPU** - Wrong flag = compilation error or runtime failure
5. **Multiple .cu files** - List all source files in nvcc command
6. **Error messages are usually clear** - "Cannot find cl.exe" = need VS environment
7. **Rebuild is simple** - Just run nvcc command again

## Windows-Specific Notes

- Use `.exe` extension for executables
- Use backslash `\` or forward slash `/` for paths (PowerShell handles both)
- Use `.\program.exe` to run (not `./program.exe` like Linux)
- PowerShell doesn't support `&&` - use `;` or separate commands
- Make may not be available - use direct nvcc commands instead


