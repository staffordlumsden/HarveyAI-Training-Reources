from pathlib import Path
import zlib, base64
parts=[]
for i in range(5):
    parts.append(Path(f"scripts/vault_chunk_{i}.txt").read_text().strip())
data=zlib.decompress(base64.b64decode("".join(parts)))
Path("Harvey_Vault_Set_Up_Walkthrough.html").write_bytes(data)
