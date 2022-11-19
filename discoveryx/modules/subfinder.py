#!/usr/bin/env python3

import logging

from discoveryx.modules.base import ModuleBase


class Subfinder(ModuleBase):
    """subfinder runner"""

    @classmethod
    def run(cls, stdin: str, out_dir: str, docker: bool = False):
        """Run subfinder

        :param stdin: stdin command to prepend subfinder command
        :param out_dir: output directory name
        :param docker: boolean if running via docker
        :returns: output file name
        """
        executable = (
            f"{cls.TOOL_DIR}/subfinder"
            if not docker
            else "docker run projectdiscovery/subfinder:latest"
        )

        output_file = f"{out_dir.rstrip('/')}/subfinder.txt"
        subfinder_command = f"{executable} -silent"

        command = f"{stdin} | {subfinder_command} > {output_file} 2>&1"

        logging.info("Running 'subfinder'")
        logging.debug(command)

        if cls.exec_shell_command(cls, command):
            return output_file

        return None
