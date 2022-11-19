#!/usr/bin/env python3

import logging

from discoveryx.modules.base import ModuleBase


class Katana(ModuleBase):
    """katana runner"""

    @classmethod
    def run(cls, stdin: str, out_dir: str, docker: bool = False):
        """Run katana

        :param stdin: stdin command to prepend katana command
        :param out_dir: output directory name
        :param docker: boolean if running via docker
        :returns: output file name
        """
        executable = (
            f"{cls.TOOL_DIR}/katana"
            if not docker
            else "docker run projectdiscovery/katana:latest"
        )

        output_file = f"{out_dir.rstrip('/')}/katana.txt"
        katana_command = f"{executable} -silent"

        command = f"{stdin} | {katana_command} > {output_file} 2>&1"

        logging.info("Running 'katana'")
        logging.debug(command)

        if cls.exec_shell_command(cls, command):
            return output_file

        return None
