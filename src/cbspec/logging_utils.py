"""
Text + JSON logging for a single pipeline run.
"""

import json
from datetime import datetime
from pathlib import Path

class RunLogger:
    """
    Handles both text and JSON output and logging for a single pipeline run.

    logs_dir: directory where output files are stored.
    """

    def __init__(self, logs_dir: Path):
        self.logs_dir = logs_dir
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.text_path = self.logs_dir / "run.log"
        self.json_path = self.logs_dir / "run.jsonl"

        self.text_file = open(self.text_path, "a")
        self.json_file = open(self.json_path, "a")

    @staticmethod
    def _ts():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_text(self, message: str):
        line = f"{self._ts()}\t{message}\n"
        self.text_file.write(line)
        self.text_file.flush()

    def log_json(self, **kwargs):
        entry = {"time": self._ts(), **kwargs}
        self.json_file.write(json.dumps(entry) + "\n")
        self.json_file.flush()

    def close(self):
        self.text_file.close()
        self.json_file.close()