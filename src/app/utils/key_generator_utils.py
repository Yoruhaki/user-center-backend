from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# 生成基于 secp256r1 曲线的私钥（ES256 专用）
private_key = ec.generate_private_key(ec.SECP256R1())

# 提取公钥
public_key = private_key.public_key()

# 保存私钥到 PEM 文件（需保密！）
with open("es256_private_key.pem", "wb") as f:
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  # 不加密私钥（根据需要可添加密码）
    )
    f.write(private_pem)

# 保存公钥到 PEM 文件（可公开）
with open("es256_public_key.pem", "wb") as f:
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    f.write(public_pem)

print("ES256 密钥对生成成功！")
print("私钥已保存到 es256_private_key.pem（严格保密！）")
print("公钥已保存到 es256_public_key.pem（可公开）")
