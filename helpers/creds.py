import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class AWSHelper:
    def check_aws_credentials():
        """Check if AWS credentials are properly set up."""
        try:
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"✅ AWS Credentials OK - Account: {identity['Account']}")
            return True
        except NoCredentialsError:
            print("❌ ERROR: No AWS credentials found. Please configure them using `aws configure` or environment variables.")
        except PartialCredentialsError:
            print("❌ ERROR: Incomplete AWS credentials found. Check your configuration.")
        except ClientError as e:
            print(f"❌ ERROR: AWS authentication failed - {e}")
        
        return False
