from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 已知的key和加密消息
key = 5876204818862281779
msg = b"\xcc]B:\xe8\xbc\x91\xe2\x93\xaa\x88\x17\xc4\xe5\x97\x87@\x0fd\xb5p\x81\x1e\x98,Z\xe1n`\xaf\xe0%:\xb7\x8aD\x03\xd2Wu5\xcd\xc4#m'\xa7\xa4\x80\x0b\xf7\xda8\x1b\x82k#\xc1gP\xbd/\xb5j"

# 将key转换为bytes，然后pad到16字节
key_bytes = key.to_bytes((key.bit_length() + 7) // 8, byteorder='big')
key_bytes = key_bytes.ljust(16, b'\x00')  # 使用0填充到16字节
print(f"Key bytes (hex): {key_bytes.hex()}")

# 创建AES解密器
cipher = AES.new(key_bytes, AES.MODE_ECB)

# 解密数据
decrypted = cipher.decrypt(msg)
print(f"Raw decrypted data (hex): {decrypted.hex()}")
print(f"Raw decrypted data (trying to decode): {decrypted}")

# 尝试不同的padding大小
for pad_size in [16, 32, 48, 64]:
    try:
        unpadded = unpad(decrypted, pad_size)
        print(f"\nSuccessfully unpadded with size {pad_size}:")
        print(f"Flag: LILCTF{{{unpadded.decode()}}}")
        break
    except Exception as e:
        print(f"\nFailed with padding size {pad_size}: {e}")
