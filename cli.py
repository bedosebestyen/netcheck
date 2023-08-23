import argparse

def read_cli_args():
    parser = argparse.ArgumentParser(description="Check internet uplink connection for different protocols.")
    parser.add_argument(
        '--icmp-weight',
        type=int,
        default=1,
        help="Weight for ICMP test")
    parser.add_argument(
        '--tcp-weight',
        type=int,
        default=1,
        help="Weight for TCP test")
    parser.add_argument(
        '--dns-weight',
        type=int,
        default=1,
        help="Weight for DNS test")
    parser.add_argument(
        '--ntp-weight',
        type=int,
        default=1,
        help="Weight for NTP test")
    parser.add_argument(
        '--mark',
        type=int,
        default=None,
        help="SO_MARK value")

    return parser.parse_args()