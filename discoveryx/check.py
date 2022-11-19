#!/usr/bin/env python3

import logging
from pathlib import Path
from shutil import which


class ToolCheck:
    """Tool check helper class"""

    HOME = str(Path.home())

    def __check_naabu(self):
        """Check for tool: naabu"""
        tool = "naabu"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.error(f"{self.HOME}/.discoveryx/tools/{tool} does not exist")
            return False

        return True

    def __check_subfinder(self):
        """Check for tool: subfinder"""
        tool = "subfinder"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.error(f"{self.HOME}/.discoveryx/tools/{tool} does not exist")
            return False

        return True

    def __check_httpx(self):
        """Check for tool: httpx"""
        tool = "httpx"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.error(f"{self.HOME}/.discoveryx/tools/{tool} does not exist")
            return False

        return True

    def __check_nuclei(self):
        """Check for tool: nuclei"""
        tool = "nuclei"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.error(f"{self.HOME}/.discoveryx/tools/{tool} does not exist")
            return False

        return True

    def __check_dnsx(self):
        """Check for tool: dnsx"""
        tool = "dnsx"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.error(f"{self.HOME}/.discoveryx/tools/{tool} does not exist")
            return False

        return True

    def __check_katana(self):
        """Check for tool: katana"""
        tool = "katana"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.error(f"{self.HOME}/.discoveryx/tools/{tool} does not exist")
            return False

        return True

    @classmethod
    def run(cls, docker: bool = False) -> bool:
        """Run all check support methods

        :param docker: boolean if running via docker
        :returns: boolean if all tools exist
        """
        valid = True

        if not docker:
            directory = f"{cls.HOME}/.discoveryx/tools/"
            if not Path(directory).is_dir():
                logging.error("discoveryx tools directory does not exist")
                logging.warning("Rerun discoveryx with the '--setup' flag")
                return False

            class_method_list = [m for m in dir(cls) if callable(getattr(cls, m))]
            for method in class_method_list:
                if method.startswith("_ToolCheck__check_"):
                    check = getattr(cls, method)
                    if not check(cls):
                        valid = False

            if not valid:
                logging.error("discoveryx tools are missing")
                logging.warning("Rerun discoveryx with the '--setup' flag")

        else:
            if not which("docker"):
                logging.error("docker is not installed")
                logging.warning("Install docker before rerunning discoveryx")
                valid = False

        return valid
