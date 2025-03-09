SIZE_UNITS = {
    "bytes": 1,
    "kb": 1024,
    "mb": 1024 ** 2,
    "gb": 1024 ** 3,
    "tb": 1024 ** 4
}


def process_bucket_info(info, size_unit):
    """
    Processes and prints bucket information with the appropriate size unit.
    :param info: Dictionary containing bucket details.
    :param size_unit: Desired size unit for output.
    """
    conversion_factor = SIZE_UNITS[size_unit]
    info["Total Size"] = round(info["Total Size (MB)"] * (1024 ** 2) / conversion_factor, 2)
    del info["Total Size (MB)"]
    info["Size Unit"] = size_unit.upper()

    print("\nS3 Bucket Information:")
    for key, value in info.items():
        print(f"{key}: {value}")
    print("\n" + "-" * 50)
