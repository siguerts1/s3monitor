from dataclasses import dataclass
from datetime import datetime

@dataclass
class BucketFile:
    key: str               # The file's key (path/name in S3)
    size: int              # Size in bytes
    last_modified: datetime  # Last modification date
    storage_class: str = "STANDARD"  # Default to standard storage

    def size_in_mb(self) -> float:
        """Return file size in MB."""
        return round(self.size / (1024 * 1024), 2)
