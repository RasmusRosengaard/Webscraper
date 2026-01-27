import os
from urllib.parse import urlparse
from datetime import datetime
from logger import get_logger

class StorageHandler:
    def __init__(self, base_dir: str = "storage"):
        self.logger = get_logger("StorageHandler")
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

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

    def save_result(self, result) -> None:
        filepath = os.path.join(self.base_dir, self._make_filename(result.url))

        final_text = "\n\n".join(
            txt for _, txt in sorted(result.content.items()) if txt
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_text)

        self.logger.success(f"Saved file: {filepath}")
