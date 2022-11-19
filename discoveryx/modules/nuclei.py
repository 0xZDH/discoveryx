#!/usr/bin/env python3

import logging

from discoveryx.modules.base import ModuleBase


class Nuclei(ModuleBase):
    """nuclei runner"""

    @classmethod
    def run(cls, stdin: str, out_dir: str, docker: bool = False):
        """Run nuclei

        :param stdin: stdin command to prepend nuclei command
        :param out_dir: output directory name
        :param docker: boolean if running via docker
        :returns: output file name
        """
        executable = (
            f"{cls.TOOL_DIR}/nuclei"
            if not docker
            else "docker run projectdiscovery/nuclei:latest"
        )

        output_file = f"{out_dir.rstrip('/')}/nuclei.txt"
        json_file = f"{out_dir.rstrip('/')}/nuclei.json"

        nuclei_command = f"{executable} -silent -json -o {json_file}"

        command = f"{stdin} | {nuclei_command} > {output_file} 2>&1"

        logging.info("Running 'nuclei'")
        logging.debug(command)

        if cls.exec_shell_command(cls, command):
            return output_file

        return None
