import argparse

def read_cli_args():
    """Handle CLI arguments and options"""
    parser = argparse.ArgumentParser(
        prog="netchecker", description="check the availability of Internet uplinks"
    )

    parser.add_argument(
        "-m",
        "--mark",
        metavar="SO_MARK",
        type=int,
        help="Enter the SO_MARK"
    )
    return parser.parse_args()