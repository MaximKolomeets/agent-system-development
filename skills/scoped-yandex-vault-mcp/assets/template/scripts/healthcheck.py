from urllib.error import URLError
from urllib.request import urlopen


try:
    with urlopen("http://127.0.0.1:8200/healthz", timeout=3) as response:
        raise SystemExit(0 if response.status == 200 else 1)
except (OSError, URLError):
    raise SystemExit(1)
