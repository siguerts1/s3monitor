import boto3
import logging
from helpers.creds import AWSHelper

# First, ensure that AWS connectivity to account is possible
AWSHelper.check_aws_credentials()

# Set up logging
logger = logging.getLogger(__name__)


class S3ClientInterface:
    def __init__(self, region_name='us-east-1'):
        """
        Initialize the S3 client.
        :param region_name: AWS region to connect to (default is 'us-east-1')
        """
        self.region_name = region_name
        self.s3_client = None
        self._create_s3_client()

    def _create_s3_client(self):
        """
        Creates an authenticated boto3 S3 client using the region and environment variables (AWS credentials).
        """
        try:
            self.s3_client = boto3.client('s3', region_name=self.region_name)
            logger.info(f"Successfully connected to S3 in region {self.region_name}")
        except Exception as e:
            logger.error(f"Failed to connect to S3: {e}")
            raise

    def get_client(self):
        """
        Return the boto3 S3 client object.
        :return: boto3 client object for interacting with S3.
        """
        if not self.s3_client:
            raise Exception("S3 client is not initialized")
        return self.s3_client
