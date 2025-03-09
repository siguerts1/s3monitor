import unittest
from unittest.mock import patch, MagicMock
from client import S3ClientInterface


class TestS3ClientInterface(unittest.TestCase):

    @patch('client.boto3.client')
    def test_create_s3_client_success(self, mock_boto_client):
        mock_boto_client.return_value = MagicMock()
        client = S3ClientInterface(region_name='us-east-1')
        self.assertIsNotNone(client.s3_client)
        mock_boto_client.assert_called_once_with('s3', region_name='us-east-1')

    @patch('client.boto3.client', side_effect=Exception("Connection Error"))
    @patch('client.logger')
    def test_create_s3_client_failure(self, mock_logger, mock_boto_client):
        with self.assertRaises(Exception) as context:
            S3ClientInterface(region_name='us-east-1')
        self.assertEqual(str(context.exception), "Connection Error")
        mock_logger.error.assert_called_with("Failed to connect to S3: Connection Error")

    @patch('client.boto3.client')
    def test_get_client_success(self, mock_boto_client):
        mock_boto_client.return_value = MagicMock()
        client = S3ClientInterface(region_name='us-east-1')
        s3_client = client.get_client()
        self.assertIsNotNone(s3_client)

    @patch('client.boto3.client')
    def test_get_client_not_initialized(self, mock_boto_client):
        client = S3ClientInterface(region_name='us-east-1')
        client.s3_client = None
        with self.assertRaises(Exception) as context:
            client.get_client()
        self.assertEqual(str(context.exception), "S3 client is not initialized")


if __name__ == "__main__":
    unittest.main()
