import argparse


def _iso8601(value: str) -> str:
    from datetime import datetime
    try:
        datetime.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid ISO 8601 datetime: {value!r}")
    return value
