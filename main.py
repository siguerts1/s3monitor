import logging
import click
from s3collector import S3Collector
from helpers.process_bucket_info import process_bucket_info

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SIZE_UNITS = {
    "bytes": 1,
    "kb": 1024,
    "mb": 1024 ** 2,
    "gb": 1024 ** 3,
    "tb": 1024 ** 4
}

STORAGE_CLASSES = ["STANDARD", "STANDARD_IA", "ONEZONE_IA", "GLACIER", "DEEP_ARCHIVE", "REDUCED_REDUNDANCY"]

@click.command()
@click.option('--bucketname', default=None, help='Specify the S3 bucket name. If omitted, retrieves all available buckets.')
@click.option('--region', default=None, help='Filter buckets by AWS region.')
@click.option('--size-unit', default='mb', type=click.Choice(SIZE_UNITS.keys(), case_sensitive=False), help='Choose size unit: bytes, kB, MB, GB, TB (default: MB).')
@click.option('--storage-class', default=None, type=click.Choice(STORAGE_CLASSES, case_sensitive=False), help='Filter objects by storage class (e.g., STANDARD, STANDARD_IA, GLACIER).')
def main(bucketname, region, size_unit, storage_class):
    """Entrypoint for the S3 monitoring tool."""
    s3_client = S3Collector("").s3_client
    
    if not bucketname:
        logger.info("No bucket name provided. Retrieving all available buckets.")
        response = s3_client.list_buckets()
        buckets = response.get("Buckets", [])
        
        if not buckets:
            logger.info("No buckets found.")
            return
        
        print("\nS3 Bucket Information:")
        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_region = s3_client.get_bucket_location(Bucket=bucket_name).get('LocationConstraint')
            bucket_region = 'us-east-1' if bucket_region is None else bucket_region  # Handle AWS inconsistency
            
            if region and bucket_region != region:
                continue
            
            collector = S3Collector(bucket_name)
            info = collector.get_bucket_info(storage_class)
            
            if info:
                process_bucket_info(info, size_unit)
        return
    
    logger.info(f"Starting S3 monitoring for bucket: {bucketname}")
    collector = S3Collector(bucketname)
    info = collector.get_bucket_info(storage_class)
    
    if info:
        process_bucket_info(info, size_unit)
    else:
        logger.error("Failed to retrieve bucket information.")

if __name__ == "__main__":
    main()