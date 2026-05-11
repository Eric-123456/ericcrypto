from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

# 生成 ECC 密鑰對
key = ECC.generate(curve='P-256')  # 使用 P-256 曲線

# 取得私鑰和公鑰
private_key = key
public_key = key.public_key()

# 模擬訊息
message = b"Hello, this is a message to sign."

# 計算訊息的 SHA-256 哈希值
h = SHA256.new(message)

# 使用私鑰生成簽名
signer = DSS.new(private_key, 'fips-186-3')
signature = signer.sign(h)

print("Signature:", signature.hex())

# 使用公鑰驗證簽名
verifier = DSS.new(public_key, 'fips-186-3')
try:
    verifier.verify(h, signature)
    print("Signature is valid.")
except ValueError:
    print("Signature is invalid.")