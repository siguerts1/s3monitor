from dataclasses import dataclass
from typing import List
from models.bucketfile import BucketFile

@dataclass
class Bucket:
    name: str
    creation_date: str
    files: List[BucketFile]  # List of files in the bucket

    def file_count(self) -> int:
        """Return the number of files in the bucket."""
        return len(self.files)

    def total_size(self) -> int:
        """Return the total size of all files in bytes."""
        return sum(file.size for file in self.files)

    def total_size_in_mb(self) -> float:
        """Return the total size in MB."""
        return round(self.total_size() / (1024 * 1024), 2)

    def last_modified(self) -> str:
        """Return the last modified date of the most recent file."""
        return max((file.last_modified for file in self.files), default=None)

    def estimated_cost(self) -> float:
        """Estimate cost based on AWS S3 standard pricing ($0.023 per GB)."""
        storage_gb = self.total_size() / (1024 ** 3)  # Convert bytes to GB
        return round(storage_gb * 0.023, 4)
