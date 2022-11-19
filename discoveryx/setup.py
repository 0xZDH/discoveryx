#!/usr/bin/env python3

import logging
import os
import platform
import requests  # type: ignore
import stat
import zipfile
from pathlib import Path
from tqdm import tqdm  # type: ignore


class Setup:
    """Setup helper class"""

    HOME = str(Path.home())

    def __get_operating_system(self) -> str:
        """Get the current operating system

        :returns: operating system string name
        """
        # platform.system() map
        platform_system_map = {
            "Linux": "linux",
            "Darwin": "macOS",
            "Windows": "windows",
        }

        try:
            return platform_system_map[platform.system()]

        except (KeyError, Exception):
            logging.error(f"Invalid operating system: {platform.system()}")
            return None

    def __get_architecture(self):
        """Get the current architecture

        :returns: architecture string name
        """
        # platform.machine() map
        platform_machine_map = {
            # x86
            "x86": "386",  # windows
            "i386": "386",
            "i686": "386",  # linux
            # x64
            "AMD64": "amd64",  # windows
            "x86_64": "amd64",  # linux / macOS
            # ARM64
            "arm64": "arm64",  # macOS
            "ARM64": "arm64",  # windows
            "aarch64": "arm64",  # linux
        }

        try:
            return platform_machine_map[platform.machine()]

        except (KeyError, Exception):
            logging.error(f"Invalid system architecture: {platform.machine()}")
            return None

    def __get_latest_release(self, tool: str, user: str) -> str:
        """Get the latest release version for a given tool

        :param tool: tool name
        :param user: tool github account
        :returns: latest tool version string
        """
        url = f"https://api.github.com/repos/{user}/{tool}/releases/latest"

        try:
            response = requests.get(url)
            version = response.json()["tag_name"]

            # Remove 'v' from 'v1.1.1'
            if version.startswith("v"):
                version = version[1:]

            return version

        except Exception as e:
            logging.error(f"Failed to retrieve latest version for: {tool}")
            return None

    def __download(self, tool: str, user: str = "projectdiscovery") -> bool:
        """Download a given ProjectDiscovery tool from Github

        :param tool: tool name
        :param user: tool github account
        :returns: boolean if downloaded
        """
        # Determine the operating system and architecture to download
        system = self.__get_operating_system(self)
        arch = self.__get_architecture(self)

        # Retrieve the latest version for the given tool
        version = self.__get_latest_release(self, tool, user)

        if not system or not arch or not version:
            return False

        # e.g. https://github.com/projectdiscovery/naabu/releases/download/v2.1.1/naabu_2.1.1_linux_amd64.zip
        url = (
            f"https://github.com/{user}"
            + f"/{tool}/releases/download"
            + f"/v{version}/{tool}_{version}_{system}_{arch}.zip"
        )

        tool_directory = f"{self.HOME}/.discoveryx/tools"
        exe_file = f"{tool_directory}/{tool}"
        zip_file = f"{tool_directory}/{tool}.zip"

        try:
            logging.info(f"Downloading: '{tool}'")
            response = requests.get(url, stream=True)

            # Handle invalid tool specification
            if response.status_code == 404:
                raise Exception(f"invalid tool specification: {tool}_{version}_{system}_{arch}")  # fmt: skip

            # Get the total bytes returned so we can build a progress bar
            response_size_bytes = int(response.headers.get("content-length", 0))
            block_size = 1024  # 1 Kibibyte

            # tqdm progress bar based on returned bytes
            progress_bar = tqdm(total=response_size_bytes, unit="iB", unit_scale=True)

            # Write the ZIP file in chunks
            with open(zip_file, "wb") as h:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    h.write(data)

            progress_bar.close()

            # Unzip directory
            with zipfile.ZipFile(zip_file, "r") as z:
                z.extractall(tool_directory)

            # Clean up the LICENSE and README files if included
            for f in [f"{tool}.zip", "README.md", "LICENSE.md"]:
                try:
                    os.remove(f"{tool_directory}/{f}")
                except FileNotFoundError:
                    pass

            # Set the file permissions to execute
            st = os.stat(exe_file)
            os.chmod(exe_file, st.st_mode | stat.S_IEXEC)

            return True

        except Exception as e:
            logging.error(f"{tool} download exception: {e}")
            return False

    def __download_naabu(self) -> bool:
        """Download ProjectDiscovery: naabu

        :returns: boolean if tool exists and/or downloaded
        """
        tool = "naabu"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            logging.warning("To use 'naabu', ensure 'libpcap' is installed: https://github.com/projectdiscovery/naabu#prerequisite")  # fmt: skip
            return self.__download(self, tool)

        return True

    def __download_subfinder(self) -> bool:
        """Download ProjectDiscovery: subfinder

        :returns: boolean if tool exists and/or downloaded
        """
        tool = "subfinder"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            return self.__download(self, tool)

        return True

    def __download_httpx(self) -> bool:
        """Download ProjectDiscovery: httpx

        :returns: boolean if tool exists and/or downloaded
        """
        tool = "httpx"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            return self.__download(self, tool)

        return True

    def __download_nuclei(self) -> bool:
        """Download ProjectDiscovery: nuclei

        :returns: boolean if tool exists and/or downloaded
        """
        tool = "nuclei"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            return self.__download(self, tool)

        return True

    def __download_dnsx(self) -> bool:
        """Download ProjectDiscovery: dnsx

        :returns: boolean if tool exists and/or downloaded
        """
        tool = "dnsx"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            return self.__download(self, tool)

        return True

    def __download_katana(self) -> bool:
        """Download ProjectDiscovery: katana

        :returns: boolean if tool exists and/or downloaded
        """
        tool = "katana"

        if not Path(f"{self.HOME}/.discoveryx/tools/{tool}").is_file():
            return self.__download(self, tool)

        return True

    @classmethod
    def run(cls):
        """Run all download support methods"""
        directory = f"{cls.HOME}/.discoveryx/tools/"
        if not Path(directory).is_dir():
            Path(directory).mkdir(parents=True, exist_ok=True)

        class_method_list = [m for m in dir(cls) if callable(getattr(cls, m))]
        for method in class_method_list:
            if method.startswith("_Setup__download_"):
                download = getattr(cls, method)
                if not download(cls):
                    logging.error("Setup failed")
                    return
