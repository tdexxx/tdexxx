from sage.all import *

# 给定的值
p = 14668080038311483271
P = GF(p)

C = matrix(P, [
    [11315841881544731102, 2283439871732792326, 6800685968958241983, 6426158106328779372, 9681186993951502212],
    [4729583429936371197, 9934441408437898498, 12454838789798706101, 1137624354220162514, 8961427323294527914],
    [12212265161975165517, 8264257544674837561, 10531819068765930248, 4088354401871232602, 14653951889442072670],
    [6045978019175462652, 11202714988272207073, 13562937263226951112, 6648446245634067896, 13902820281072641413],
    [1046075193917103481, 3617988773170202613, 3590111338369894405, 2646640112163975771, 5966864698750134707]
])

D = matrix(P, [
    [1785348659555163021, 3612773974290420260, 8587341808081935796, 4393730037042586815, 10490463205723658044],
    [10457678631610076741, 1645527195687648140, 13013316081830726847, 12925223531522879912, 5478687620744215372],
    [9878636900393157276, 13274969755872629366, 3231582918568068174, 7045188483430589163, 5126509884591016427],
    [4914941908205759200, 7480989013464904670, 5860406622199128154, 8016615177615097542, 13266674393818320551],
    [3005316032591310201, 6624508725257625760, 7972954954270186094, 5331046349070112118, 6127026494304272395]
])

print("分析矩阵特征...")
# 分析最后一行（v5 * 0的结果）
last_row_C = vector(P, C.row(-1))
last_row_D = vector(P, D.row(-1))
print(f"C的最后一行: {last_row_C}")
print(f"D的最后一行: {last_row_D}")

# 计算最小多项式
min_poly_C = C.minimal_polynomial()
print(f"\nC的最小多项式: {min_poly_C}")

# 计算特征多项式和特征值
char_poly_C = C.characteristic_polynomial()
eig_C = C.eigenvalues()
eig_D = D.eigenvalues()
print(f"\nC的特征值: {eig_C}")
print(f"D的特征值: {eig_D}")

# 尝试寻找模式
print("\n寻找数学关系...")
for i in range(5):
    ratio = D[4][i] / C[4][i] if C[4][i] != 0 else "undefined"
    print(f"D[4][{i}] / C[4][{i}] = {ratio}")

# Baby-step Giant-step方法搜索key
def bsgs_matrix(base, target, p, lower_bound):
    m = isqrt(p - lower_bound) + 1
    # Baby steps
    baby_steps = {}
    current = matrix.identity(P, 5)
    for j in range(m):
        if j % 10000 == 0:
            print(f"Baby step: {j}")
        baby_steps[tuple(current[4])] = j
        current *= base

    # Giant steps
    giant = base^(-m)
    current = target
    for i in range((p - lower_bound) // m + 1):
        if i % 10000 == 0:
            print(f"Giant step: {i}")
        curr_tuple = tuple(current[4])
        if curr_tuple in baby_steps:
            result = i * m + baby_steps[curr_tuple]
            if result >= lower_bound:
                return result
        current *= giant
    return None

print("\n开始BSGS搜索...")
key = bsgs_matrix(C, D, p, 2**62)
if key:
    print(f"找到可能的key: {key}")
    # 验证
    if C^key == D:
        print("验证成功！")
    else:
        print("验证失败。")
