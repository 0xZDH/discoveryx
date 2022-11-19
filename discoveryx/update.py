#!/usr/bin/env python3

import logging
import shutil
from pathlib import Path

from discoveryx.setup import Setup


class Update:
    """Update helper class

    NOTE: This could probably be optimized by creating a 'versions' text file
          that contains the current installed versions of each tool and then
          pulling and comparing each tool version and only deleting/downloading
          tools that have newer releases.
    """

    HOME = str(Path.home())

    @classmethod
    def run(cls):
        """Update all tools by removing directory and reinstalling"""
        directory = f"{cls.HOME}/.discoveryx/tools/"

        # Remove the tools directory if it exists so we can reinstall
        # the latest versions
        if Path(directory).is_dir():
            logging.info("Removing previous tool installs")
            shutil.rmtree(directory)

        # Run setup
        Setup.run()
