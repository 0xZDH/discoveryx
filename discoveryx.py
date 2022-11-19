#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path

from discoveryx import __banner__
from discoveryx.check import ToolCheck
from discoveryx.cli import parse_args
from discoveryx.discover import Discover
from discoveryx.logger import init_logger
from discoveryx.setup import Setup
from discoveryx.update import Update


if __name__ == "__main__":
    args = parse_args()
    print(__banner__)

    init_logger(args.debug)

    # Run setup
    if args.setup:
        Setup.run()
        sys.exit(0)

    # Run update
    if args.update:
        Update.run()
        sys.exit(0)

    # Validate all tools are present
    if not ToolCheck.run(args.docker):
        sys.exit(1)

    # Build initial stdin command based on provided input
    if args.ip or args.domain:
        stdin_ = args.ip or args.domain
        stdin = f"echo {stdin_}"

    else:
        stdin_ = args.iplist or args.domainlist
        stdin = f"cat {stdin_}"

    # Create output directory
    now = datetime.now().strftime("%Y%m%dT%H%M%S")
    out_dir = f"output/{now}/"
    if not Path(out_dir).is_dir():
        Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Identify discovery path
    discovery_path = "ip" if args.ip or args.iplist else "domain"
    Discover.run(stdin, out_dir, discovery_path, args.docker)
