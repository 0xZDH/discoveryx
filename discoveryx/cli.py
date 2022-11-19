#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from discoveryx import __title__
from discoveryx import __version__


def parse_args() -> argparse.Namespace:
    """Parse command line arguments

    :returns: argparse namespace
    """
    parser = argparse.ArgumentParser(description=f"{__title__} -- v{__version__}")

    parser.add_argument(
        "-i",
        "--ip",
        type=str,
        help="ip address to scan (comma-separated)",
    )
    parser.add_argument(
        "-il",
        "--iplist",
        type=str,
        help="list of ip addresses to scan (file)",
    )
    parser.add_argument(
        "-d",
        "--domain",
        type=str,
        help="domain to scan (comma-separated)",
    )
    parser.add_argument(
        "-dl",
        "--domainlist",
        type=str,
        help="list of domains to scan (file)",
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="run tools via Docker containers",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="install tools and setup environment",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="update existing tool installs",
    )
    parser.add_argument("--debug", action="store_true", help="enable debugging")
    args = parser.parse_args()

    # If setup or update, skip arg validation
    if args.setup or args.update:
        return args

    # Validate arguments
    if (not args.domain and not args.domainlist) and (not args.ip and not args.iplist):
        parser.error(
            "missing required argument(s): -i/--ip, -il/--iplist, -d/--domain, or -dl/--domainlist"
        )

    if (args.domain or args.domainlist) and (args.ip or args.iplist):
        parser.error(
            "invalid argument(s): only one type of target can be provided, ip or domain"
        )

    if args.domain and args.domainlist:
        parser.error(
            "invalid argument(s): only -d/--domain or -dl/--domainlist allowed"
        )

    if args.ip and args.iplist:
        parser.error("invalid argument(s): only -i/--ip or -il/--iplist allowed")

    # Parse arguments
    if args.iplist:
        if not Path(args.iplist).is_file():
            parser.error("invalid ip file")

    if args.domainlist:
        if not Path(args.domainlist).is_file():
            parser.error("invalid domain file")

    return args
