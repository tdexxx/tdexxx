from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 给定的值
p = 14668080038311483271
F = GF(p)

# 加密的消息
msg = b"\xcc]B:\xe8\xbc\x91\xe2\x93\xaa\x88\x17\xc4\xe5\x97\x87@\x0fd\xb5p\x81\x1e\x98,Z\xe1n`\xaf\xe0%:\xb7\x8aD\x03\xd2Wu5\xcd\xc4#m'\xa7\xa4\x80\x0b\xf7\xda8\x1b\x82k#\xc1gP\xbd/\xb5j"

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

# 快速求解
print("Starting quick solve method...")

# 使用最后一行的特殊性质
last_row_C = vector(F, C.row(-1))
last_row_D = vector(F, D.row(-1))

# 关键优化：使用矩阵的迹（trace）
# 迹在相似变换下保持不变，而且可以更快地进行运算
trace_C = C.trace()
trace_D = D.trace()

print(f"Trace of C: {trace_C}")
print(f"Trace of D: {trace_D}")

# 使用离散对数求解，这里我们知道key在2^62到p之间
key = discrete_log(trace_D, trace_C, bounds=(2^62, p))
print(f"\nFound key: {key}")

# 验证
if C^key == D:
    print("Verified: C^key = D")
    
    # 准备AES解密
    key_bytes = pad(int(key).to_bytes((int(key).bit_length() + 7) // 8, byteorder='big'), 16)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    try:
        decrypted = unpad(cipher.decrypt(msg), 64)
        print(f"\nDecrypted flag: {decrypted}")
    except Exception as e:
        print(f"Decryption error: {e}")
else:
    print("Error: Key verification failed")
