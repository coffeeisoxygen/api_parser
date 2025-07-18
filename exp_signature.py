import base64
import hashlib


# Contoh input, silakan ganti sesuai kebutuhan
def generate_signature(memberid, product, dest, refid, pin, password):
    raw = f"OtomaX|{memberid}|{product}|{dest}|{refid}|{pin}|{password}"
    print(f"Raw string: {raw}")
    sha1_digest = hashlib.sha1(raw.encode()).digest()
    print(f"SHA1 digest (hex): {sha1_digest.hex()}")
    b64 = base64.b64encode(sha1_digest).decode()
    print(f"Base64: {b64}")
    signature = b64.rstrip("=").replace("+", "-").replace("/", "_")
    print(f"Final signature: {signature}")
    return signature


if __name__ == "__main__":
    # Contoh data, silakan sesuaikan
    memberid = "vps"
    product = "CLPDATA"
    dest = "08123456789"
    refid = "3038936"
    pin = "123456"
    password = "test123"
    generate_signature(memberid, product, dest, refid, pin, password)
