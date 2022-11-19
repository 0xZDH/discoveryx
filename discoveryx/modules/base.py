#!/usr/bin/env python3

import logging
import subprocess
from pathlib import Path


class ModuleBase:
    """Module base class"""

    TOOL_DIR = f"{str(Path.home())}/.discoveryx/tools"

    def exec_shell_command(self, c: str) -> bool:
        """Execute shell command

        :param c: command to execute
        :returns: if command executed properly
        """
        try:
            p = subprocess.Popen(
                c,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            _ = p.communicate()[0]
            rc = p.returncode

            # Handle non-zero exit codes
            if rc != 0:
                return False

            return True

        except Exception as e:
            logging.error(f"Command Exception: {e}")
            return False
