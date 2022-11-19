#!/usr/bin/env python3

import logging
import os
import subprocess
from pathlib import Path

from discoveryx.modules import *


class Discover:
    """Discovery path runner"""

    def __stat_file(self, f: str):
        """Output the line count of a given file

        :param f: file name to stat
        """
        toolname = f.split("/")[-1]  # /home/output/httpx.txt -> httpx.txt
        toolname = toolname.split(".")[0]  # httpx.txt -> httpx

        try:
            p = subprocess.Popen(
                f"wc -l {f} | awk '{{print $1}}'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            count = p.communicate()[0]
            rc = p.returncode

            # Handle non-zero exit codes
            if rc != 0:
                return

            count = int(count)
            if count > 0:
                logging.debug(f"{toolname} results: {count}")
            else:
                logging.debug(f"{toolname} returned no results")

        except Exception as e:
            logging.error(f"File stat exception: {e}")

    def __check_file(self, f: str) -> bool:
        """Check if a file exists and has data

        :param f: file name to check
        :returns: boolean if file exists and contains data
        """
        if not f:
            return False

        if not Path(f).is_file():
            return False

        self.__stat_file(self, f)

        if os.stat(f).st_size == 0:
            return False

        return True

    @classmethod
    def run(cls, stdin: str, out_dir: str, path: str, docker: bool = False):
        """Run discovery path

        Bash Examples:

            echo example.com | subfinder -silent | dnsx -silent
            echo example.com | dnsx -resp-only -a -aaaa -silent | naabu -silent
            echo example.com | naabu -silent | httpx -silent
            echo example.com | httpx -silent | katana -silent

        :param stdin: stdin command to start
        :param out_dir: output directory
        :param path: discovery path (ip, domain)
        :param docker: boolean if running via docker
        """
        # Perform initial domain discovery path
        # Only perform dnsx with domains to avoid cases where some addresses
        # don't resolve, but are running web services
        if path == "domain":

            subfinder_outfile = Subfinder.run(stdin, out_dir, docker)
            if not cls.__check_file(cls, subfinder_outfile):
                return

            stdin = f"cat {subfinder_outfile}"
            dnsx_outfile = Dnsx.run(stdin, out_dir, docker)
            if not cls.__check_file(cls, dnsx_outfile):
                return

            stdin = f"cat {dnsx_outfile}"

        naabu_outfile = Naabu.run(stdin, out_dir, docker)
        if not cls.__check_file(cls, naabu_outfile):
            return

        stdin = f"cat {naabu_outfile}"
        httpx_outfile = Httpx.run(stdin, out_dir, docker)
        if not cls.__check_file(cls, httpx_outfile):
            return

        # Since httpx returns multiple values, grab only the url
        stdin = f"cat {httpx_outfile} | awk '{{print $1}}'"

        katana_outfile = Katana.run(stdin, out_dir, docker)
        cls.__stat_file(cls, katana_outfile)

        nuclei_outfile = Nuclei.run(stdin, out_dir, docker)
        cls.__stat_file(cls, nuclei_outfile)
