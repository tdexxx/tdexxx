from sage.all import *

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

print("Analyzing matrix properties...")

# 计算特征值
char_poly_C = C.characteristic_polynomial()
eigenvalues_C = C.eigenvalues()
print(f"Eigenvalues of C: {eigenvalues_C}")

# 计算Jordan形式
J, P = C.jordan_form(transformation=True)
print("\nJordan form J:")
print(J)
print("\nTransformation matrix P:")
print(P)

# 计算最后一行的特性
last_row_C = vector(F, C.row(-1))
last_row_D = vector(F, D.row(-1))

print("\nAnalyzing last row properties...")
print(f"Last row of C: {last_row_C}")
print(f"Last row of D: {last_row_D}")

# 找到最大特征值
max_eig = max(abs(x) for x in eigenvalues_C)
print(f"\nLargest eigenvalue: {max_eig}")

# 尝试从特征向量得到key
print("\nTrying to find key from eigenvalue ratios...")
for i in range(len(eigenvalues_C)):
    if eigenvalues_C[i] != 0:
        for j in range(i+1, len(eigenvalues_C)):
            if eigenvalues_C[j] != 0:
                try:
                    ratio = eigenvalues_C[i] / eigenvalues_C[j]
                    print(f"Ratio of eigenvalues {i} and {j}: {ratio}")
                except:
                    continue

print("\nTrying discrete log with maximum eigenvalue...")
# 对每个非零特征值尝试离散对数
for i, eig in enumerate(eigenvalues_C):
    if eig != 0:
        try:
            key = discrete_log(D.eigenvalues()[i], eig, bounds=(2^62, p))
            print(f"Potential key from eigenvalue {i}: {key}")
            # 验证
            if C**key == D:
                print("Found valid key!")
                print(f"Final key: {key}")
                break
        except Exception as e:
            print(f"Failed for eigenvalue {i}: {e}")

print("Analysis complete")
