import math
import json
import os
from itertools import permutations, combinations

def factorial(n):
    if not isinstance(n, int): return None
    if n < 0 or n > 12: return None
    try: return math.factorial(n)
    except: return None

def sqrt(n):
    if not isinstance(n, int) or n < 0: return None
    res = math.isqrt(n)
    if res * res == n: return res
    return None

def get_all_expressions(numbers):
    if not numbers: return {}
    if len(numbers) == 1:
        n = numbers[0]
        results = {n: str(n)}
        f = factorial(n)
        if f is not None: results[f] = f"{n}!"
        s = sqrt(n)
        if s is not None: results[s] = f"√{n}"
        return results

    results = {}
    for i in range(1, len(numbers)):
        for left_subset in combinations(range(len(numbers)), i):
            right_subset = [idx for idx in range(len(numbers)) if idx not in left_subset]
            left_exprs = get_all_expressions([numbers[idx] for idx in left_subset])
            right_exprs = get_all_expressions([numbers[idx] for idx in right_subset])
            
            for lv, le in left_exprs.items():
                for rv, re in right_exprs.items():
                    ops = [(lv + rv, f"({le}+{re})"), (lv - rv, f"({le}-{re})"), (rv - lv, f"({re}-{le})"), (lv * rv, f"({le}*{re})")]
                    if rv != 0 and lv % rv == 0: ops.append((lv // rv, f"({le}/{re})"))
                    if lv != 0 and rv % lv == 0: ops.append((rv // lv, f"({re}/{le})"))
                    if 0 < rv < 10 and 0 <= lv < 20:
                        try:
                            val = lv ** rv
                            if val < 10**8: ops.append((val, f"({le}^{re})"))
                        except: pass
                    
                    for val, expr in ops:
                        if not isinstance(val, int): continue
                        if abs(val) > 10**9: continue
                        if val not in results or len(expr) < len(results[val]):
                            results[val] = expr
                            f = factorial(val)
                            if f is not None and f not in results: results[f] = f"({expr})!"
                            s = sqrt(val)
                            if s is not None and s not in results: results[s] = f"√({expr})"
    return results

def solve_with_library(numbers, target):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lib_path = os.path.join(script_dir, "sum_library.json")
    if not os.path.exists(lib_path):
        return solve_basic(numbers, target)
    
    with open(lib_path, "r", encoding="utf-8") as f:
        library = json.load(f)
    
    n_count = len(numbers)

    for base_count in range(1, n_count + 1):
        for base_indices in combinations(range(n_count), base_count):
            remaining_indices = [idx for idx in range(n_count) if idx not in base_indices]
            base_nums = [numbers[idx] for idx in base_indices]
            
            for entry in library:
                lib_nums_needed = entry["nums"]
                if len(lib_nums_needed) != base_count: continue
                
                # Try all permutations of base_nums to match lib_nums_needed
                for p_base in permutations(base_nums):
                    can_match = True
                    matched_display_nums = []
                    temp_p_base = list(p_base)
                    
                    for target_num in lib_nums_needed:
                        found = False
                        for b_idx, b_val in enumerate(temp_p_base):
                            if b_val == target_num:
                                matched_display_nums.append(str(b_val))
                                temp_p_base.pop(b_idx)
                                found = True
                                break
                            if b_val == 0 and target_num == 1:
                                matched_display_nums.append("(0!)")
                                temp_p_base.pop(b_idx)
                                found = True
                                break
                        if not found:
                            can_match = False
                            break
                    
                    if can_match:
                        lib_val = entry["val"]
                        lib_expr_template = entry["expr"]
                        display_expr = lib_expr_template
                        
                        # Replace numbers in template with matched display strings
                        # We need to be careful with 2^0 case where 2 and 0 are separate
                        for target_num, display_str in zip(lib_nums_needed, matched_display_nums):
                            # Replace placeholders like {0}, {1} etc. if we had them, 
                            # but here we use a simpler string replacement.
                            # For 2^{0}, we replace '2' and '0'
                            if display_str != str(target_num):
                                # Replace specific patterns to avoid over-replacing
                                display_expr = display_expr.replace(f"={target_num}", f"={display_str}", 1)
                                display_expr = display_expr.replace(f"^{{{target_num}}}", f"^{{{display_str}}}", 1)
                        
                        if "i=0" in display_expr: continue
                        
                        r_nums = [numbers[idx] for idx in remaining_indices]
                        r_exprs = get_all_expressions(r_nums)
                        
                        res = check_offset(lib_val, r_exprs, target, display_expr)
                        if res: return res

    return solve_basic(numbers, target)

def solve_basic(numbers, target):
    exprs = get_all_expressions(numbers)
    if target in exprs:
        return f"{exprs[target]} = {target}"
    return f"ไม่พบคำตอบที่ใช้ตัวเลขครบ {len(numbers)} ตัว"

def check_offset(base_val, r_exprs, target, base_expr):
    if not r_exprs:
        if base_val == target: return f"{base_expr} = {target}"
        return None
    
    for rv, re in r_exprs.items():
        if base_val + rv == target: return f"{base_expr} + {re} = {target}"
        if base_val - rv == target: return f"{base_expr} - {re} = {target}"
        if rv - base_val == target: return f"{re} - {base_expr} = {target}"
        if base_val * rv == target: return f"{base_expr} * {re} = {target}"
        if rv != 0 and base_val % rv == 0 and base_val // rv == target: return f"{base_expr} / {re} = {target}"
        
    return None

def parse_and_solve(input_str):
    try:
        if "=" not in input_str: return "รูปแบบไม่ถูกต้อง"
        parts = input_str.split("=")
        num_part = parts[0].strip()
        target_part = parts[1].strip()
        nums = [int(d) for d in num_part if d.isdigit()]
        target = int(target_part)
        return solve_with_library(nums, target)
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(parse_and_solve(sys.argv[1]))
    else:
        while True:
            user_input = input("\nกรอกโจทย์: ").strip()
            if user_input.lower() == 'exit': break
            if user_input: print(parse_and_solve(user_input))
