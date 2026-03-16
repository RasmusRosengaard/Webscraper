import os
from urllib.parse import urlparse
from datetime import datetime
from logger import get_logger

class StorageHandler:
    def __init__(self):
        self.output_dir = os.getenv("OUTPUT_DIR", "output")
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger = get_logger("StorageHandler")

    def _make_filename(self, url: str) -> str:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        path = parsed.path.strip("/") or "index"
        safe_path = path.replace("/", "_")

        if parsed.query:
            q = parsed.query.replace("&", "_").replace("=", "-")
            safe_path = f"{safe_path}__{q}"

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{domain}_{safe_path}__{ts}.txt"

    def save_result(self, result):
        filename = f"{result.url.replace('https://','').replace('http://','').replace('/','_')}.txt"
        path = os.path.join(self.output_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            for line in result.content.values():
                f.write(line + "\n")

        self.logger.success(f"Saved file: {path}")
