import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from s3collector import S3Collector
from models.bucketfile import BucketFile

class TestS3Collector(unittest.TestCase):
    
    @patch('s3collector.S3ClientInterface')
    def setUp(self, MockS3Client):
        self.mock_s3_client = MockS3Client.return_value.get_client.return_value
        self.collector = S3Collector("test-bucket")
        self.collector.s3_client = self.mock_s3_client
    
    def test_get_bucket_creation_date(self):
        self.mock_s3_client.list_buckets.return_value = {
            "Buckets": [
                {"Name": "test-bucket", "CreationDate": datetime(2025, 3, 6, 18, 7, 46)}
            ]
        }
        creation_date = self.collector._get_bucket_creation_date()
        self.assertEqual(creation_date, "March 06, 2025, 18:07:46 (UTC)")
    
    def test_get_bucket_creation_date_unknown(self):
        self.mock_s3_client.list_buckets.return_value = {"Buckets": []}
        creation_date = self.collector._get_bucket_creation_date()
        self.assertEqual(creation_date, "Unknown")
    
    def test_get_bucket_files(self):
        mock_paginator = MagicMock()
        self.mock_s3_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [
            {"Contents": [
                {"Key": "file1.txt", "Size": 1024, "LastModified": "2025-03-06T18:07:46", "StorageClass": "STANDARD"},
                {"Key": "file2.txt", "Size": 2048, "LastModified": "2025-03-07T12:34:56", "StorageClass": "GLACIER"}
            ]}
        ]
        files = self.collector._get_bucket_files()
        self.assertEqual(len(files), 2)
        self.assertIsInstance(files[0], BucketFile)
        self.assertEqual(files[0].key, "file1.txt")
        self.assertEqual(files[1].storage_class, "GLACIER")
    
    def test_get_bucket_files_with_filter(self):
        mock_paginator = MagicMock()
        self.mock_s3_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [
            {"Contents": [
                {"Key": "file1.txt", "Size": 1024, "LastModified": "2025-03-06T18:07:46", "StorageClass": "STANDARD"},
                {"Key": "file2.txt", "Size": 2048, "LastModified": "2025-03-07T12:34:56", "StorageClass": "GLACIER"}
            ]}
        ]
        files = self.collector._get_bucket_files(storage_class_filter="STANDARD")
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].storage_class, "STANDARD")
    
    @patch('s3collector.S3Collector._get_bucket_creation_date', return_value="March 06, 2025, 18:07:46 (UTC)")
    @patch('s3collector.S3Collector._get_bucket_files', return_value=[
        BucketFile("file1.txt", 1024, "2025-03-06T18:07:46", "STANDARD"),
        BucketFile("file2.txt", 2048, "2025-03-07T12:34:56", "GLACIER")
    ])
    def test_get_bucket_info(self, mock_get_files, mock_get_creation):
        info = self.collector.get_bucket_info()
        self.assertEqual(info["Bucket Name"], "test-bucket")
        self.assertEqual(info["Creation Date"], "March 06, 2025, 18:07:46 (UTC)")
        self.assertEqual(info["Number of Files"], 2)
        self.assertIn("STANDARD", info["Storage Class Breakdown"])  # Ensure storage class count exists

if __name__ == "__main__":
    unittest.main()
