from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 给定的值
p = 14668080038311483271
F = GF(p)

# 定义矩阵
C = matrix(F, [
    [11315841881544731102, 2283439871732792326, 6800685968958241983, 6426158106328779372, 9681186993951502212],
    [4729583429936371197, 9934441408437898498, 12454838789798706101, 1137624354220162514, 8961427323294527914],
    [12212265161975165517, 8264257544674837561, 10531819068765930248, 4088354401871232602, 14653951889442072670],
    [6045978019175462652, 11202714988272207073, 13562937263226951112, 6648446245634067896, 13902820281072641413],
    [1046075193917103481, 3617988773170202613, 3590111338369894405, 2646640112163975771, 5966864698750134707]
])

D = matrix(F, [
    [1785348659555163021, 3612773974290420260, 8587341808081935796, 4393730037042586815, 10490463205723658044],
    [10457678631610076741, 1645527195687648140, 13013316081830726847, 12925223531522879912, 5478687620744215372],
    [9878636900393157276, 13274969755872629366, 3231582918568068174, 7045188483430589163, 5126509884591016427],
    [4914941908205759200, 7480989013464904670, 5860406622199128154, 8016615177615097542, 13266674393818320551],
    [3005316032591310201, 6624508725257625760, 7972954954270186094, 5331046349070112118, 6127026494304272395]
])

msg = b"\xcc]B:\xe8\xbc\x91\xe2\x93\xaa\x88\x17\xc4\xe5\x97\x87@\x0fd\xb5p\x81\x1e\x98,Z\xe1n`\xaf\xe0%:\xb7\x8aD\x03\xd2Wu5\xcd\xc4#m'\xa7\xa4\x80\x0b\xf7\xda8\x1b\x82k#\xc1gP\xbd/\xb5j"

def quick_solve():
    # 关键点：e=0 意味着C的最后一行是v5和A逆矩阵的乘积
    # 因为v5对应的系数e=0，所以这一行在B中全是0
    print("Quick solve method:")
    
    # 1. 找到一个非零元素作为基准
    base = C[0,0]  # 使用第一个元素
    target = D[0,0]
    
    # 2. 直接使用内置的离散对数
    try:
        key = discrete_log(target, base, bounds=(2^62, p))
        print(f"Found potential key: {key}")
        return key
    except Exception as e:
        print(f"Discrete log failed: {e}")
        return None

def try_decrypt(key_int):
    try:
        key_bytes = pad(int(key_int).to_bytes((int(key_int).bit_length() + 7) // 8, byteorder='big'), 16)
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted = cipher.decrypt(msg)
        return unpad(decrypted, 64)
    except Exception as e:
        return None

# 方法1：利用最后一行的特殊性质和Sage的离散对数功能
print("Method 1: Using discrete log on matrix elements...")
last_row_C = vector(GF(p), C.row(-1))
last_row_D = vector(GF(p), D.row(-1))

# 方法2：Jordan标准型分析
print("\nMethod 2: Jordan form analysis...")
try:
    J_C, P_C = C.jordan_form(transformation=True)
    J_D, P_D = D.jordan_form(transformation=True)
    print("Jordan blocks of C:")
    print(J_C.jordan_blocks())
except Exception as e:
    print(f"Error in Jordan form calculation: {e}")

# 方法3：特征值分析
print("\nMethod 3: Eigenvalue analysis...")
char_poly_C = C.characteristic_polynomial()
eig_C = C.eigenvalues()
eig_D = D.eigenvalues()
print(f"C eigenvalues: {eig_C}")
print(f"D eigenvalues: {eig_D}")

# 方法4：使用最小多项式
print("\nMethod 4: Using minimal polynomial...")
min_poly_C = C.minimal_polynomial()
min_poly_D = D.minimal_polynomial()
print(f"Minimal polynomial of C: {min_poly_C}")

# 方法5：Baby-step Giant-step算法尝试
print("\nMethod 5: Baby-step Giant-step on traces...")
trace_C = C.trace()
trace_D = D.trace()

# Baby-step Giant-step参数
m = isqrt(p - 2**62) + 1

# 创建baby steps表
print("Creating baby steps table...")
baby_steps = {}
current = GF(p)(1)
for j in range(m):
    if j % 1000000 == 0:
        print(f"Baby step: {j}")
    baby_steps[current] = j
    current *= trace_C

# Giant steps
print("Taking giant steps...")
factor = trace_C^(m)
current = trace_D
for i in range((p - 2**62) // m + 1):
    if i % 1000000 == 0:
        print(f"Giant step: {i}")
    if current in baby_steps:
        possible_key = i * m + baby_steps[current]
        if possible_key >= 2**62:
            print(f"Found potential key: {possible_key}")
            result = try_decrypt(possible_key)
            if result and result.startswith(b'LILCTF{'):
                print(f"Found flag: {result}")
                break
    current /= factor

# 方法6：并行化的密集搜索
print("\nMethod 6: Dense search with optimization...")
search_space = range(2**62, min(2**62 + 10**6, p))
trace_target = trace_D

def check_trace(k):
    if k % 100000 == 0:
        print(f"Checking key: {k}")
    if (trace_C^k) == trace_target:
        result = try_decrypt(k)
        if result and result.startswith(b'LILCTF{'):
            print(f"Found flag with key {k}: {result}")
            return k
    return None

# 并行搜索
from sage.parallel.multiprocessing_sage import parallel_iter
results = []
for k, res in parallel_iter(4, check_trace, search_space):
    if res is not None:
        results.append(res)
        break

if results:
    key = results[0]
    flag = try_decrypt(key)
    print(f"Final flag: {flag}")
