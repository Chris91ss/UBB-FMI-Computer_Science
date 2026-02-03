import threading
import time
import random
from colorama import Fore, init
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)


# ==================== POLYNOMIAL MULTIPLICATION ====================

def regular_multiply_sequential(poly1: List[int], poly2: List[int]) -> List[int]:
    """
    Regular O(n²) polynomial multiplication - Sequential version.
    Each coefficient of result is computed by summing products.
    """
    n1, n2 = len(poly1), len(poly2)
    result = [0] * (n1 + n2 - 1)
    
    for i in range(n1):
        for j in range(n2):
            result[i + j] += poly1[i] * poly2[j]
    
    return result


def regular_multiply_parallel(poly1: List[int], poly2: List[int], num_threads: int = 4) -> Tuple[List[int], float]:
    """
    Regular O(n²) polynomial multiplication - Parallel version.
    Each thread computes a range of result coefficients.
    Synchronization: Thread-safe list access with locks.
    """
    n1, n2 = len(poly1), len(poly2)
    result = [0] * (n1 + n2 - 1)
    result_lock = threading.Lock()
    
    def compute_coefficient_range(start_idx: int, end_idx: int):
        """Compute coefficients from start_idx to end_idx (exclusive)"""
        for k in range(start_idx, end_idx):
            # For coefficient k, we need poly1[i] * poly2[j] where i + j = k
            for i in range(max(0, k - n2 + 1), min(n1, k + 1)):
                j = k - i
                if 0 <= j < n2:
                    with result_lock:
                        result[k] += poly1[i] * poly2[j]
    
    total_coeffs = len(result)
    coeffs_per_thread = total_coeffs // num_threads
    
    start_time = time.time()
    threads = []
    
    for i in range(num_threads):
        start_idx = i * coeffs_per_thread
        end_idx = (i + 1) * coeffs_per_thread if i < num_threads - 1 else total_coeffs
        
        thread = threading.Thread(target=compute_coefficient_range, args=(start_idx, end_idx))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time


def karatsuba_multiply_sequential(poly1: List[int], poly2: List[int]) -> List[int]:
    """
    Karatsuba algorithm for polynomial multiplication - Sequential version.
    Time complexity: O(n^log2(3)) ≈ O(n^1.585)
    """
    # Base case: if polynomials are small, use regular multiplication
    if len(poly1) < 2 or len(poly2) < 2:
        return regular_multiply_sequential(poly1, poly2)
    
    # Make both polynomials the same length
    max_len = max(len(poly1), len(poly2))
    poly1_padded = poly1 + [0] * (max_len - len(poly1))
    poly2_padded = poly2 + [0] * (max_len - len(poly2))
    
    # Split point
    mid = max_len // 2
    
    # Split polynomials
    low1, high1 = poly1_padded[:mid], poly1_padded[mid:]
    low2, high2 = poly2_padded[:mid], poly2_padded[mid:]
    
    # Recursive calls
    z0 = karatsuba_multiply_sequential(low1, low2)
    z2 = karatsuba_multiply_sequential(high1, high2)
    
    # Compute (low1 + high1) * (low2 + high2)
    # Handle different lengths when adding
    max_sum_len1 = max(len(low1), len(high1))
    sum1 = [0] * max_sum_len1
    for i in range(len(low1)):
        sum1[i] += low1[i]
    for i in range(len(high1)):
        sum1[i] += high1[i]
    
    max_sum_len2 = max(len(low2), len(high2))
    sum2 = [0] * max_sum_len2
    for i in range(len(low2)):
        sum2[i] += low2[i]
    for i in range(len(high2)):
        sum2[i] += high2[i]
    
    z1 = karatsuba_multiply_sequential(sum1, sum2)
    
    # z1 = z1 - z0 - z2
    z1 = subtract_polynomials(z1, z0)
    z1 = subtract_polynomials(z1, z2)
    
    # Combine results: result = z0 + z1 * x^mid + z2 * x^(2*mid)
    # Result size should be len(poly1) + len(poly2) - 1
    result_size = len(poly1) + len(poly2) - 1
    result = [0] * result_size
    
    # Add z0
    for i in range(len(z0)):
        if i < result_size:
            result[i] += z0[i]
    
    # Add z1 * x^mid
    for i in range(len(z1)):
        idx = i + mid
        if idx < result_size:
            result[idx] += z1[i]
    
    # Add z2 * x^(2*mid)
    for i in range(len(z2)):
        idx = i + 2 * mid
        if idx < result_size:
            result[idx] += z2[i]
    
    return result


def karatsuba_multiply_parallel(poly1: List[int], poly2: List[int], num_threads: int = 4, 
                                threshold: int = 32) -> Tuple[List[int], float]:
    """
    Karatsuba algorithm for polynomial multiplication - Parallel version.
    Uses parallel execution for recursive calls when polynomials are large enough.
    Synchronization: ThreadPoolExecutor for managing parallel recursive calls.
    """
    def karatsuba_parallel_internal(p1: List[int], p2: List[int]) -> List[int]:
        # Base case: use regular multiplication for small polynomials
        if len(p1) < threshold or len(p2) < threshold:
            return regular_multiply_sequential(p1, p2)

        # Make both polynomials the same length
        max_len = max(len(p1), len(p2))
        p1_padded = p1 + [0] * (max_len - len(p1))
        p2_padded = p2 + [0] * (max_len - len(p2))
        
        mid = max_len // 2
        
        low1, high1 = p1_padded[:mid], p1_padded[mid:]
        low2, high2 = p2_padded[:mid], p2_padded[mid:]
        
        # Parallel execution of independent recursive calls
        with ThreadPoolExecutor(max_workers=min(num_threads, 3)) as executor:
            future_z0 = executor.submit(karatsuba_parallel_internal, low1, low2)
            future_z2 = executor.submit(karatsuba_parallel_internal, high1, high2)
            
            # Compute sums - handle different lengths
            max_sum_len1 = max(len(low1), len(high1))
            sum1 = [0] * max_sum_len1
            for i in range(len(low1)):
                sum1[i] += low1[i]
            for i in range(len(high1)):
                sum1[i] += high1[i]
            
            max_sum_len2 = max(len(low2), len(high2))
            sum2 = [0] * max_sum_len2
            for i in range(len(low2)):
                sum2[i] += low2[i]
            for i in range(len(high2)):
                sum2[i] += high2[i]
            
            future_z1 = executor.submit(karatsuba_parallel_internal, sum1, sum2)
            
            z0 = future_z0.result()
            z2 = future_z2.result()
            z1 = future_z1.result()
        
        # z1 = z1 - z0 - z2
        z1 = subtract_polynomials(z1, z0)
        z1 = subtract_polynomials(z1, z2)
        
        # Combine results - result size should be len(p1) + len(p2) - 1
        result_size = len(p1) + len(p2) - 1
        result = [0] * result_size
        
        for i in range(len(z0)):
            if i < result_size:
                result[i] += z0[i]
        
        for i in range(len(z1)):
            idx = i + mid
            if idx < result_size:
                result[idx] += z1[i]
        
        for i in range(len(z2)):
            idx = i + 2 * mid
            if idx < result_size:
                result[idx] += z2[i]
        
        return result
    
    start_time = time.time()
    result = karatsuba_parallel_internal(poly1, poly2)
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time


def subtract_polynomials(poly1: List[int], poly2: List[int]) -> List[int]:
    """Subtract two polynomials"""
    max_len = max(len(poly1), len(poly2))
    result = [0] * max_len
    
    for i in range(len(poly1)):
        result[i] += poly1[i]
    
    for i in range(len(poly2)):
        result[i] -= poly2[i]
    
    return result


def generate_random_polynomial(degree: int, min_coeff: int = 1, max_coeff: int = 10) -> List[int]:
    """Generate a random polynomial of given degree"""
    return [random.randint(min_coeff, max_coeff) for _ in range(degree + 1)]


def format_polynomial(poly: List[int]) -> str:
    """Format polynomial as a string"""
    terms = []
    for i, coeff in enumerate(poly):
        if coeff != 0:
            if i == 0:
                terms.append(str(coeff))
            elif i == 1:
                terms.append(f"{coeff}x" if coeff != 1 else "x")
            else:
                terms.append(f"{coeff}x^{i}" if coeff != 1 else f"x^{i}")
    
    if not terms:
        return "0"
    
    return " + ".join(reversed(terms))


# ==================== BIG NUMBER MULTIPLICATION ====================

def big_number_regular_sequential(num1: str, num2: str) -> str:
    """
    Regular O(n²) big number multiplication - Sequential version.
    """
    n1, n2 = len(num1), len(num2)
    result = [0] * (n1 + n2)
    
    # Reverse for easier indexing
    num1 = num1[::-1]
    num2 = num2[::-1]
    
    for i in range(n1):
        for j in range(n2):
            result[i + j] += int(num1[i]) * int(num2[j])
    
    # Handle carries
    carry = 0
    for i in range(len(result)):
        result[i] += carry
        carry = result[i] // 10
        result[i] %= 10
    
    # Convert to string and remove leading zeros
    result_str = ''.join(str(d) for d in reversed(result))
    return result_str.lstrip('0') or '0'


def big_number_regular_parallel(num1: str, num2: str, num_threads: int = 4) -> Tuple[str, float]:
    """
    Regular O(n²) big number multiplication - Parallel version.
    Synchronization: Thread-safe list access with locks.
    """
    n1, n2 = len(num1), len(num2)
    result = [0] * (n1 + n2)
    result_lock = threading.Lock()
    
    num1_rev = num1[::-1]
    num2_rev = num2[::-1]
    
    def compute_digit_range(start_idx: int, end_idx: int):
        """Compute result digits from start_idx to end_idx"""
        for k in range(start_idx, end_idx):
            for i in range(max(0, k - n2 + 1), min(n1, k + 1)):
                j = k - i
                if 0 <= j < n2:
                    product = int(num1_rev[i]) * int(num2_rev[j])
                    with result_lock:
                        result[k] += product
    
    total_digits = len(result)
    digits_per_thread = total_digits // num_threads
    
    start_time = time.time()
    threads = []
    
    for i in range(num_threads):
        start_idx = i * digits_per_thread
        end_idx = (i + 1) * digits_per_thread if i < num_threads - 1 else total_digits
        
        thread = threading.Thread(target=compute_digit_range, args=(start_idx, end_idx))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Handle carries sequentially (can be parallelized but adds complexity)
    carry = 0
    for i in range(len(result)):
        result[i] += carry
        carry = result[i] // 10
        result[i] %= 10
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    result_str = ''.join(str(d) for d in reversed(result))
    return result_str.lstrip('0') or '0', execution_time


def big_number_add(num1: str, num2: str) -> str:
    """Add two big numbers represented as strings"""
    num1 = num1.lstrip('0') or '0'
    num2 = num2.lstrip('0') or '0'
    
    # Reverse for easier processing
    n1 = num1[::-1]
    n2 = num2[::-1]
    max_len = max(len(n1), len(n2))
    
    result = []
    carry = 0
    
    for i in range(max_len):
        d1 = int(n1[i]) if i < len(n1) else 0
        d2 = int(n2[i]) if i < len(n2) else 0
        total = d1 + d2 + carry
        result.append(str(total % 10))
        carry = total // 10
    
    if carry:
        result.append(str(carry))
    
    return ''.join(reversed(result))


def big_number_subtract(num1: str, num2: str) -> str:
    """Subtract two big numbers (num1 - num2), assumes num1 >= num2"""
    num1 = num1.lstrip('0') or '0'
    num2 = num2.lstrip('0') or '0'
    
    # Reverse for easier processing
    n1 = num1[::-1]
    n2 = num2[::-1]
    
    result = []
    borrow = 0
    
    for i in range(len(n1)):
        d1 = int(n1[i])
        d2 = int(n2[i]) if i < len(n2) else 0
        diff = d1 - d2 - borrow
        
        if diff < 0:
            diff += 10
            borrow = 1
        else:
            borrow = 0
        
        result.append(str(diff))
    
    # Remove leading zeros
    result_str = ''.join(reversed(result)).lstrip('0')
    return result_str or '0'


def big_number_multiply_by_power_of_10(num: str, power: int) -> str:
    """Multiply a big number by 10^power"""
    if power == 0:
        return num
    return num + '0' * power


def big_number_karatsuba_sequential(num1: str, num2: str) -> str:
    """
    Karatsuba algorithm for big number multiplication - Sequential version.
    """
    # Remove leading zeros
    num1 = num1.lstrip('0') or '0'
    num2 = num2.lstrip('0') or '0'
    
    # Base case: use regular multiplication for small numbers
    if len(num1) < 2 or len(num2) < 2:
        return big_number_regular_sequential(num1, num2)
    
    # Make both numbers the same length
    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)
    
    # Split point - split so that high part has m digits, low part has the rest
    # We want m to be roughly half, but we split from the left
    m = (max_len + 1) // 2  # Use ceiling division for m
    
    # Split numbers: num = high * 10^(max_len - m) + low
    high1, low1 = num1[:m], num1[m:]
    high2, low2 = num2[:m], num2[m:]
    
    # Remove leading zeros from splits
    high1 = high1.lstrip('0') or '0'
    low1 = low1.lstrip('0') or '0'
    high2 = high2.lstrip('0') or '0'
    low2 = low2.lstrip('0') or '0'
    
    # Recursive calls
    z0 = big_number_karatsuba_sequential(low1, low2)
    z2 = big_number_karatsuba_sequential(high1, high2)
    
    # Compute (low1 + high1) * (low2 + high2)
    sum1 = big_number_add(low1, high1)
    sum2 = big_number_add(low2, high2)
    z1 = big_number_karatsuba_sequential(sum1, sum2)
    
    # z1 = z1 - z0 - z2
    z1 = big_number_subtract(z1, z0)
    z1 = big_number_subtract(z1, z2)
    
    # Combine: result = z0 + z1 * 10^(max_len - m) + z2 * 10^(2*(max_len - m))
    shift = max_len - m
    term1 = big_number_multiply_by_power_of_10(z1, shift)
    term2 = big_number_multiply_by_power_of_10(z2, 2 * shift)
    
    result = big_number_add(z0, term1)
    result = big_number_add(result, term2)
    
    return result


def big_number_karatsuba_parallel(num1: str, num2: str, num_threads: int = 4, 
                                  threshold: int = 10) -> Tuple[str, float]:
    """
    Karatsuba algorithm for big number multiplication - Parallel version.
    Synchronization: ThreadPoolExecutor for managing parallel recursive calls.
    """
    def karatsuba_parallel_internal(n1: str, n2: str) -> str:
        # Remove leading zeros
        n1 = n1.lstrip('0') or '0'
        n2 = n2.lstrip('0') or '0'
        
        # Base case
        if len(n1) < threshold or len(n2) < threshold:
            return big_number_regular_sequential(n1, n2)
        
        max_len = max(len(n1), len(n2))
        n1 = n1.zfill(max_len)
        n2 = n2.zfill(max_len)
        
        # Split point - split so that high part has m digits, low part has the rest
        m = (max_len + 1) // 2  # Use ceiling division for m
        
        # Split numbers: num = high * 10^(max_len - m) + low
        high1, low1 = n1[:m], n1[m:]
        high2, low2 = n2[:m], n2[m:]
        
        # Remove leading zeros from splits
        high1 = high1.lstrip('0') or '0'
        low1 = low1.lstrip('0') or '0'
        high2 = high2.lstrip('0') or '0'
        low2 = low2.lstrip('0') or '0'
        
        # Parallel execution
        with ThreadPoolExecutor(max_workers=min(num_threads, 3)) as executor:
            future_z0 = executor.submit(karatsuba_parallel_internal, low1, low2)
            future_z2 = executor.submit(karatsuba_parallel_internal, high1, high2)
            
            sum1 = big_number_add(low1, high1)
            sum2 = big_number_add(low2, high2)
            future_z1 = executor.submit(karatsuba_parallel_internal, sum1, sum2)
            
            z0 = future_z0.result()
            z2 = future_z2.result()
            z1 = future_z1.result()
        
        z1 = big_number_subtract(z1, z0)
        z1 = big_number_subtract(z1, z2)
        
        # Combine: result = z0 + z1 * 10^(max_len - m) + z2 * 10^(2*(max_len - m))
        shift = max_len - m
        term1 = big_number_multiply_by_power_of_10(z1, shift)
        term2 = big_number_multiply_by_power_of_10(z2, 2 * shift)
        
        result = big_number_add(z0, term1)
        result = big_number_add(result, term2)
        
        return result
    
    start_time = time.time()
    result = karatsuba_parallel_internal(num1, num2)
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time


def generate_random_big_number(digits: int) -> str:
    """Generate a random big number with given number of digits"""
    first_digit = str(random.randint(1, 9))  # First digit can't be 0
    rest_digits = ''.join(str(random.randint(0, 9)) for _ in range(digits - 1))
    return first_digit + rest_digits


# ==================== DEMO AND TEST FUNCTIONS ====================

def run_polynomial_demo():
    """Run a demo of polynomial multiplication"""
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "POLYNOMIAL MULTIPLICATION DEMO")
    print(Fore.GREEN + "=" * 60)
    
    degree1 = 5
    degree2 = 4
    num_threads = 4
    
    print(Fore.CYAN + f"\nPolynomial 1 degree: {degree1}")
    print(Fore.CYAN + f"Polynomial 2 degree: {degree2}")
    print(Fore.CYAN + f"Number of threads: {num_threads}\n")
    
    poly1 = generate_random_polynomial(degree1)
    poly2 = generate_random_polynomial(degree2)
    
    print(Fore.YELLOW + f"Polynomial 1: {format_polynomial(poly1)}")
    print(Fore.YELLOW + f"Polynomial 2: {format_polynomial(poly2)}\n")
    
    # Test all 4 variants
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "1. Regular O(n²) - Sequential")
    print(Fore.MAGENTA + "=" * 60)
    start = time.time()
    result1 = regular_multiply_sequential(poly1, poly2)
    time1 = time.time() - start
    print(Fore.CYAN + f"Result: {format_polynomial(result1)}")
    print(Fore.YELLOW + f"Time: {time1:.6f} seconds\n")
    
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "2. Regular O(n²) - Parallel")
    print(Fore.MAGENTA + "=" * 60)
    result2, time2 = regular_multiply_parallel(poly1, poly2, num_threads)
    print(Fore.CYAN + f"Result: {format_polynomial(result2)}")
    print(Fore.YELLOW + f"Time: {time2:.6f} seconds\n")
    
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "3. Karatsuba - Sequential")
    print(Fore.MAGENTA + "=" * 60)
    start = time.time()
    result3 = karatsuba_multiply_sequential(poly1, poly2)
    time3 = time.time() - start
    print(Fore.CYAN + f"Result: {format_polynomial(result3)}")
    print(Fore.YELLOW + f"Time: {time3:.6f} seconds\n")
    
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "4. Karatsuba - Parallel")
    print(Fore.MAGENTA + "=" * 60)
    result4, time4 = karatsuba_multiply_parallel(poly1, poly2, num_threads)
    print(Fore.CYAN + f"Result: {format_polynomial(result4)}")
    print(Fore.YELLOW + f"Time: {time4:.6f} seconds\n")
    
    # Verify results match
    if result1 == result2 == result3 == result4:
        print(Fore.GREEN + "✓ All results match!")
    else:
        print(Fore.RED + "✗ Results differ!")


def custom_polynomial_test():
    """Custom polynomial multiplication test"""
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "CUSTOM POLYNOMIAL MULTIPLICATION TEST")
    print(Fore.GREEN + "=" * 60)
    
    try:
        degree1 = int(input(Fore.CYAN + "Enter degree of polynomial 1 (default 5): " + Fore.RESET) or "5")
        degree2 = int(input(Fore.CYAN + "Enter degree of polynomial 2 (default 4): " + Fore.RESET) or "4")
        num_threads = int(input(Fore.CYAN + "Enter number of threads (default 4): " + Fore.RESET) or "4")
        
        poly1 = generate_random_polynomial(degree1)
        poly2 = generate_random_polynomial(degree2)
        
        print(Fore.YELLOW + f"\nPolynomial 1: {format_polynomial(poly1)}")
        print(Fore.YELLOW + f"Polynomial 2: {format_polynomial(poly2)}\n")
        
        print(Fore.MAGENTA + "Running all 4 variants...\n")
        
        start = time.time()
        result1 = regular_multiply_sequential(poly1, poly2)
        time1 = time.time() - start
        
        result2, time2 = regular_multiply_parallel(poly1, poly2, num_threads)
        
        start = time.time()
        result3 = karatsuba_multiply_sequential(poly1, poly2)
        time3 = time.time() - start
        
        result4, time4 = karatsuba_multiply_parallel(poly1, poly2, num_threads)
        
        print(Fore.CYAN + f"Regular Sequential: {time1:.6f} seconds")
        print(Fore.CYAN + f"Regular Parallel:   {time2:.6f} seconds")
        print(Fore.CYAN + f"Karatsuba Sequential: {time3:.6f} seconds")
        print(Fore.CYAN + f"Karatsuba Parallel:   {time4:.6f} seconds")
        
        if result1 == result2 == result3 == result4:
            print(Fore.GREEN + "\n✓ All results match!")
        else:
            print(Fore.RED + "\n✗ Results differ!")
            
    except ValueError as e:
        print(Fore.RED + f"Invalid input: {e}")


def polynomial_performance_comparison():
    """Performance comparison table for polynomial multiplication"""
    print(Fore.GREEN + "=" * 80)
    print(Fore.GREEN + "POLYNOMIAL MULTIPLICATION - PERFORMANCE COMPARISON")
    print(Fore.GREEN + "=" * 80)
    
    test_configs = [
        (10, 10, 2),
        (20, 20, 4),
        (50, 50, 4),
        (100, 100, 4),
        (200, 200, 8),
        (500, 500, 8),
    ]
    
    print(Fore.CYAN + "\nRunning performance tests...\n")
    
    results = []
    
    for deg1, deg2, threads in test_configs:
        print(Fore.YELLOW + f"Testing: degree {deg1} × degree {deg2} with {threads} threads")
        
        poly1 = generate_random_polynomial(deg1)
        poly2 = generate_random_polynomial(deg2)
        
        # Regular Sequential
        start = time.time()
        regular_multiply_sequential(poly1, poly2)
        time_reg_seq = time.time() - start
        
        # Regular Parallel
        _, time_reg_par = regular_multiply_parallel(poly1, poly2, threads)
        
        # Karatsuba Sequential
        start = time.time()
        karatsuba_multiply_sequential(poly1, poly2)
        time_kar_seq = time.time() - start
        
        # Karatsuba Parallel
        _, time_kar_par = karatsuba_multiply_parallel(poly1, poly2, threads)
        
        results.append({
            'deg1': deg1,
            'deg2': deg2,
            'threads': threads,
            'reg_seq': time_reg_seq,
            'reg_par': time_reg_par,
            'kar_seq': time_kar_seq,
            'kar_par': time_kar_par
        })
    
    # Print table
    print(Fore.GREEN + "\n" + "=" * 90)
    print(Fore.GREEN + "PERFORMANCE SUMMARY TABLE")
    print(Fore.GREEN + "=" * 90)
    print(Fore.CYAN + f"{'Degrees':<12} {'Threads':<10} {'Reg Seq (s)':<15} {'Reg Par (s)':<15} "
          f"{'Kar Seq (s)':<15} {'Kar Par (s)':<15}")
    print(Fore.CYAN + "-" * 90)
    
    for res in results:
        print(Fore.YELLOW + f"{res['deg1']}×{res['deg2']:<10} {res['threads']:<10} "
              f"{res['reg_seq']:<15.6f} {res['reg_par']:<15.6f} "
              f"{res['kar_seq']:<15.6f} {res['kar_par']:<15.6f}")
    
    print()


def run_big_number_demo():
    """Run a demo of big number multiplication"""
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "BIG NUMBER MULTIPLICATION DEMO")
    print(Fore.GREEN + "=" * 60)
    
    digits1 = 20
    digits2 = 20
    num_threads = 4
    
    print(Fore.CYAN + f"\nNumber 1 digits: {digits1}")
    print(Fore.CYAN + f"Number 2 digits: {digits2}")
    print(Fore.CYAN + f"Number of threads: {num_threads}\n")
    
    num1 = generate_random_big_number(digits1)
    num2 = generate_random_big_number(digits2)
    
    print(Fore.YELLOW + f"Number 1: {num1}")
    print(Fore.YELLOW + f"Number 2: {num2}\n")
    
    # Test all 4 variants
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "1. Regular O(n²) - Sequential")
    print(Fore.MAGENTA + "=" * 60)
    start = time.time()
    result1 = big_number_regular_sequential(num1, num2)
    time1 = time.time() - start
    print(Fore.CYAN + f"Result: {result1[:50]}..." if len(result1) > 50 else f"Result: {result1}")
    print(Fore.YELLOW + f"Time: {time1:.6f} seconds\n")
    
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "2. Regular O(n²) - Parallel")
    print(Fore.MAGENTA + "=" * 60)
    result2, time2 = big_number_regular_parallel(num1, num2, num_threads)
    print(Fore.CYAN + f"Result: {result2[:50]}..." if len(result2) > 50 else f"Result: {result2}")
    print(Fore.YELLOW + f"Time: {time2:.6f} seconds\n")
    
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "3. Karatsuba - Sequential")
    print(Fore.MAGENTA + "=" * 60)
    start = time.time()
    result3 = big_number_karatsuba_sequential(num1, num2)
    time3 = time.time() - start
    print(Fore.CYAN + f"Result: {result3[:50]}..." if len(result3) > 50 else f"Result: {result3}")
    print(Fore.YELLOW + f"Time: {time3:.6f} seconds\n")
    
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "4. Karatsuba - Parallel")
    print(Fore.MAGENTA + "=" * 60)
    result4, time4 = big_number_karatsuba_parallel(num1, num2, num_threads)
    print(Fore.CYAN + f"Result: {result4[:50]}..." if len(result4) > 50 else f"Result: {result4}")
    print(Fore.YELLOW + f"Time: {time4:.6f} seconds\n")
    
    # Verify results match
    if result1 == result2 == result3 == result4:
        print(Fore.GREEN + "✓ All results match!")
    else:
        print(Fore.RED + "✗ Results differ!")


def custom_big_number_test():
    """Custom big number multiplication test"""
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "CUSTOM BIG NUMBER MULTIPLICATION TEST")
    print(Fore.GREEN + "=" * 60)
    
    try:
        digits1 = int(input(Fore.CYAN + "Enter digits for number 1 (default 20): " + Fore.RESET) or "20")
        digits2 = int(input(Fore.CYAN + "Enter digits for number 2 (default 20): " + Fore.RESET) or "20")
        num_threads = int(input(Fore.CYAN + "Enter number of threads (default 4): " + Fore.RESET) or "4")
        
        num1 = generate_random_big_number(digits1)
        num2 = generate_random_big_number(digits2)
        
        print(Fore.YELLOW + f"\nNumber 1: {num1}")
        print(Fore.YELLOW + f"Number 2: {num2}\n")
        
        print(Fore.MAGENTA + "Running all 4 variants...\n")
        
        start = time.time()
        result1 = big_number_regular_sequential(num1, num2)
        time1 = time.time() - start
        
        result2, time2 = big_number_regular_parallel(num1, num2, num_threads)
        
        start = time.time()
        result3 = big_number_karatsuba_sequential(num1, num2)
        time3 = time.time() - start
        
        result4, time4 = big_number_karatsuba_parallel(num1, num2, num_threads)
        
        print(Fore.CYAN + f"Regular Sequential: {time1:.6f} seconds")
        print(Fore.CYAN + f"Regular Parallel:   {time2:.6f} seconds")
        print(Fore.CYAN + f"Karatsuba Sequential: {time3:.6f} seconds")
        print(Fore.CYAN + f"Karatsuba Parallel:   {time4:.6f} seconds")
        
        if result1 == result2 == result3 == result4:
            print(Fore.GREEN + "\n✓ All results match!")
        else:
            print(Fore.RED + "\n✗ Results differ!")
            
    except ValueError as e:
        print(Fore.RED + f"Invalid input: {e}")


def big_number_performance_comparison():
    """Performance comparison table for big number multiplication"""
    print(Fore.GREEN + "=" * 80)
    print(Fore.GREEN + "BIG NUMBER MULTIPLICATION - PERFORMANCE COMPARISON")
    print(Fore.GREEN + "=" * 80)
    
    test_configs = [
        (10, 10, 2),
        (20, 20, 4),
        (50, 50, 4),
        (100, 100, 4),
        (200, 200, 8),
        (500, 500, 8),
    ]
    
    print(Fore.CYAN + "\nRunning performance tests...\n")
    
    results = []
    
    for dig1, dig2, threads in test_configs:
        print(Fore.YELLOW + f"Testing: {dig1} digits × {dig2} digits with {threads} threads")
        
        num1 = generate_random_big_number(dig1)
        num2 = generate_random_big_number(dig2)
        
        # Regular Sequential
        start = time.time()
        big_number_regular_sequential(num1, num2)
        time_reg_seq = time.time() - start
        
        # Regular Parallel
        _, time_reg_par = big_number_regular_parallel(num1, num2, threads)
        
        # Karatsuba Sequential
        start = time.time()
        big_number_karatsuba_sequential(num1, num2)
        time_kar_seq = time.time() - start
        
        # Karatsuba Parallel
        _, time_kar_par = big_number_karatsuba_parallel(num1, num2, threads)
        
        results.append({
            'dig1': dig1,
            'dig2': dig2,
            'threads': threads,
            'reg_seq': time_reg_seq,
            'reg_par': time_reg_par,
            'kar_seq': time_kar_seq,
            'kar_par': time_kar_par
        })
    
    # Print table
    print(Fore.GREEN + "\n" + "=" * 90)
    print(Fore.GREEN + "PERFORMANCE SUMMARY TABLE")
    print(Fore.GREEN + "=" * 90)
    print(Fore.CYAN + f"{'Digits':<12} {'Threads':<10} {'Reg Seq (s)':<15} {'Reg Par (s)':<15} "
          f"{'Kar Seq (s)':<15} {'Kar Par (s)':<15}")
    print(Fore.CYAN + "-" * 90)
    
    for res in results:
        print(Fore.YELLOW + f"{res['dig1']}×{res['dig2']:<10} {res['threads']:<10} "
              f"{res['reg_seq']:<15.6f} {res['reg_par']:<15.6f} "
              f"{res['kar_seq']:<15.6f} {res['kar_par']:<15.6f}")
    
    print()

