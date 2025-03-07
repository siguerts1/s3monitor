import logging
from botocore.exceptions import BotoCoreError, ClientError
from models.bucket import Bucket
from models.bucketfile import BucketFile
from client import S3ClientInterface

# Set up logging
logger = logging.getLogger(__name__)

class S3Collector:
    def __init__(self, bucket_name):
        """
        Initialize the S3Collector to fetch metadata from an S3 bucket.
        :param bucket_name: Name of the S3 bucket.
        """
        self.bucket_name = bucket_name
        self.s3_client = S3ClientInterface().get_client()

    def get_bucket_info(self, storage_class_filter=None):
        """
        Retrieve S3 bucket metadata using the Bucket and BucketFile models.
        :param storage_class_filter: Optional filter for a specific storage class.
        """
        try:
            # Fetch bucket creation date
            creation_date = self._get_bucket_creation_date()
            
            # Fetch files in the bucket with optional storage class filter
            files = self._get_bucket_files(storage_class_filter)

            # Create Bucket instance
            bucket = Bucket(name=self.bucket_name, creation_date=creation_date, files=files)

            # Count files per storage class
            storage_class_counts = {}
            for file in files:
                storage_class_counts[file.storage_class] = storage_class_counts.get(file.storage_class, 0) + 1

            return {
                "Bucket Name": bucket.name,
                "Creation Date": creation_date,
                "Number of Files": bucket.file_count(),
                "Total Size (MB)": bucket.total_size_in_mb(),
                "Last Modified Date": bucket.last_modified(),
                "Estimated Cost (USD)": bucket.estimated_cost(),
                "Storage Class Breakdown": storage_class_counts
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error retrieving bucket info: {e}")
            return None

    def _get_bucket_creation_date(self):
        """
        Fetches the actual creation date of the bucket.
        """
        try:
            response = self.s3_client.list_buckets()
            for bucket in response.get('Buckets', []):
                if bucket['Name'] == self.bucket_name:
                    return bucket['CreationDate'].strftime('%B %d, %Y, %H:%M:%S (UTC)')
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error retrieving bucket creation date: {e}")
        return "Unknown"

    def _get_bucket_files(self, storage_class_filter=None):
        """
        Fetches and returns a list of BucketFile objects representing files in the bucket.
        Applies storage class filtering if specified.
        """
        paginator = self.s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name)

        files = []
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    storage_class = obj.get("StorageClass", "STANDARD")
                    
                    if storage_class_filter and storage_class != storage_class_filter:
                        continue
                    
                    file = BucketFile(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"],
                        storage_class=storage_class
                    )
                    files.append(file)
        return files
