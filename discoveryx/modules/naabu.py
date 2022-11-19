#!/usr/bin/env python3

import logging

from discoveryx.modules.base import ModuleBase


class Naabu(ModuleBase):
    """naabu runner"""

    @classmethod
    def run(cls, stdin: str, out_dir: str, docker: bool = False):
        """Run naabu

        :param stdin: stdin command to prepend naabu command
        :param out_dir: output directory name
        :param docker: boolean if running via docker
        :returns: output file name
        """
        executable = (
            f"{cls.TOOL_DIR}/naabu"
            if not docker
            else "docker run projectdiscovery/naabu:latest"
        )

        output_file = f"{out_dir.rstrip('/')}/naabu.txt"

        # Only scan for HTTP potential ports
        # https://github.com/danielmiessler/SecLists/blob/master/Discovery/Infrastructure/common-http-ports.txt
        naabu_command = f"{executable} -silent -ports-file resc/common-http-ports.txt"

        command = f"{stdin} | {naabu_command} > {output_file} 2>&1"

        logging.info("Running 'naabu'")
        logging.debug(command)

        if cls.exec_shell_command(cls, command):
            return output_file

        return None
