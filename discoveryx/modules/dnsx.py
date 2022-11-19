#!/usr/bin/env python3

import logging

from discoveryx.modules.base import ModuleBase


class Dnsx(ModuleBase):
    """dnsx runner"""

    @classmethod
    def run(cls, stdin: str, out_dir: str, docker: bool = False):
        """Run dnsx

        :param stdin: stdin command to prepend dnsx command
        :param out_dir: output directory name
        :param docker: boolean if running via docker
        :returns: output file name
        """
        executable = (
            f"{cls.TOOL_DIR}/dnsx"
            if not docker
            else "docker run projectdiscovery/dnsx:latest"
        )

        output_file = f"{out_dir.rstrip('/')}/dnsx.txt"
        dnsx_command = f"{executable} -silent"

        command = f"{stdin} | {dnsx_command} > {output_file} 2>&1"

        logging.info("Running 'dnsx'")
        logging.debug(command)

        if cls.exec_shell_command(cls, command):
            return output_file

        return None
