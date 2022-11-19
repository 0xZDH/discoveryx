#!/usr/bin/env python3

import logging

from discoveryx.modules.base import ModuleBase


class Httpx(ModuleBase):
    """httpx runner"""

    @classmethod
    def run(cls, stdin: str, out_dir: str, docker: bool = False):
        """Run httpx

        :param stdin: stdin command to prepend httpx command
        :param out_dir: output directory name
        :param docker: boolean if running via docker
        :returns: output file name
        """
        executable = (
            f"{cls.TOOL_DIR}/httpx"
            if not docker
            else "docker run projectdiscovery/httpx:latest"
        )

        output_file = f"{out_dir.rstrip('/')}/httpx.txt"
        httpx_command = f"{executable} -silent -nc -status-code -title -tech-detect"

        command = f"{stdin} | {httpx_command} > {output_file} 2>&1"

        logging.info("Running 'httpx'")
        logging.debug(command)

        if cls.exec_shell_command(cls, command):
            return output_file

        return None
