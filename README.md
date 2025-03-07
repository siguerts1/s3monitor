# s3monitor
Coveo take home assessment
--------------------------

A Python-based tool to monitor AWS S3 buckets, retrieve metadata, and estimate storage costs.

Features - VERSION 0.1.0:
- Fetch bucket metadata (name, creation date, file count, total size, last modified file, cost estimation)
- Filter by region and storage class
- Display size results in bytes, kB, MB, GB, TB
- Versioning system with --version flag
- Automated unit tests with unittest | Currently just a base tests for handlers functions
- CI/CD integration with GitHub Actions | Currently only POC of automated unittesting

INSTALLATION:
- git clone this repo
- pip3 install -r requirements.txt
- check help : python3 main.py --help
- check version you're running on: python3 main.py --version
- Run your first test: python3 main.py
- Run you unit tests: coverage run -m unittest discover -s tests


------------------------------------------------------------------------------------------------------------------------------------------
FUTURE VERSIONS & EXAMPLES OF FORESEEABLE CHALLENGES

1. IAM Handling Issues

- Some S3 buckets may have restricted IAM permissions, preventing access.
- Buckets may require specific roles or policies, making authentication complex.
- Handling temporary credentials and rotating access keys may introduce operational overhead.


2. Performance Challenges with Large-Scale Operations

- As the number of files and buckets grows, listing objects may become slow and inefficient.
- AWS API rate limits could restrict how fast we can query multiple S3 buckets.
- Large-scale operations could lead to increased compute and memory usage.
- Network latency and API response times could degrade performance, requiring optimization in future releases.
- Need to assess how to efficiently fetch metadata without scanning every object in real-time.


3. Scalability and System Limitations

- Handling hundreds of buckets with millions of files will introduce bottlenecks.
- Real-time updates may become infeasible due to large dataset sizes.
- Storage and metadata tracking could require external systems in future versions.


