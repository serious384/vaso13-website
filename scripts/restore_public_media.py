"""Restore the public Vaso13 media, verifying every file before saving."""
import hashlib
from pathlib import Path
import urllib.request

FILES = {
"assets/audio/belim-belo-snippet.mp3": "7c744ef47e127fd2752381d62e8fca9877272fd421bc44860ae9e18cb5d4e3a9",
"assets/audio/chernovik.mp3": "d33c3d476b4d4b04526d5ca0b5ec0b268e47b2f463d6485f09a588d9fcc3c0cd",
"assets/audio/na-krayu-nochi-snippet.mp3": "003c0855e47ee7102d814ff5a7c357211dd9cdddab434c7d98e58dd5b1ad8761",
"assets/audio/skandalnaya-para.mp3": "a8a6b5bda82c0896314252e73ee15defc2cd6979196affcb892afb638c9364b0",
"assets/audio/zrya-remastered-snippet.mp3": "bcafe9d35baab2b85862e4a168c17bde0b671f5cf41f88cff44c2eb78faa1aba",
"assets/images/hero-stage.png": "43d4fde0d9fe961e7b5d638c2e10cff96fb9b4b909e5273cd8b8a11185c7af16",
}
for name, expected in FILES.items():
    path = Path(name)
    if path.exists():
        data = path.read_bytes()
    else:
        request = urllib.request.Request("https://www.vaso13.ru/" + name, headers={"User-Agent": "Vaso13-Site-Migration/1.0"})
        with urllib.request.urlopen(request, timeout=90) as response:
            data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError("Media checksum mismatch: " + name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print("Verified", name, len(data))
