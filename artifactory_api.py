
import os
import sys
import getpass
import base64
import json
import datetime
import logging
import requests
from dateutil import parser

import utility


log = logging.getLogger(__name__)


class Artifactory_API():

    def __init__(self,
                 url,
                 user=getpass.getuser(),
                 apikey=None,
                 token=None,
                 base=None):

        if not self.__with_http_prefix(url):
            log.error("Invalid url: %s", url)
            sys.exit(1)

        self.baseurl = url

        if base:
            base = self.__remove_leading_slash(base)
            self.baseurl += f'/{base}'

        self.headers = {}

        if user and apikey:
            auth_string = f"{user}:{apikey}".encode('utf-8')
            encoded_auth = base64.b64encode(auth_string).decode('utf-8')
            self.headers['Authorization'] = "Basic " + encoded_auth

        elif apikey:
            self.headers['X-JFrog-Art-Api'] = apikey

        elif token:
            self.headers['Authorization'] = "Bearer " + token


    def get_artifactory_version(self):

        url = f"{self.baseurl}/api/system/version"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        return True, output


    def get_all_repositories(self):

        url = f"{self.baseurl}/api/repositories"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        return True, output


    def get_dir_listing(self, path, recursive=False, include_stat=False):

        path = self.__remove_leading_slash(path)
        url = f"{self.baseurl}/api/storage/{path}"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        children = output.get('children', [])

        listing = []

        for child in children:

            item_name = child['uri'].lstrip('/')  # Remove leading slash from the 'uri'
            is_folder = child['folder']

            subfolder_path = os.path.join(path, item_name)

            entry = {
                'name': item_name,
                'uri': subfolder_path,
                'is_folder': is_folder
            }

            if include_stat:

                status, output = self.get_stat_file(subfolder_path)
                if not status:
                    return False, output

                entry.update(output)

                status, output = self.get_stat_download(subfolder_path)
                if not status:
                    return False, output

                entry.update(output)

            listing.append(entry)

            # If recursive is True and the item is a folder, fetch its contents
            if recursive and is_folder:

                status, subfolder_listing = self.get_dir_listing(subfolder_path, recursive)
                if not status:
                    return False, subfolder_listing

                listing.extend(subfolder_listing)

        return True, listing


    def get_stat_json(self, path, key=None):

        path = self.__remove_leading_slash(path)
        url = f"{self.baseurl}/api/storage/{path}"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("GET", url, params=key)
        if not status:
            return False, output

        return True, output


    def get_stat_file(self, path):

        status, output = self.get_stat_json(path)
        if not status:
            return False, output

        children = None
        if "children" in output:
            children = [
                child["uri"][1:] for child in output["children"]
            ]

        checksums = output.get("checksums", {})

        stat_dict = {
            "repo": output.get("repo", None),
            "size": output.get("size", 0),
            "is_folder": False if output.get("size", None) else True,
            "mime_type": output.get("mimeType", None),
            "children": children,

            "ctime": parser.parse(output["created"]),
            "mtime": parser.parse(output["lastModified"]),
            "last_updated": parser.parse(output["lastUpdated"]),

            "created_by": output.get("createdBy", None),
            "modified_by": output.get("modified", None),

            "sha1": checksums.get("sha1", None),
            "sha256": checksums.get("sha256", None),
            "md5": checksums.get("md5", None),
        }

        return True, stat_dict


    def get_stat_download(self, path):

        status, output = self.get_stat_json(path, key='stats')
        if not status:
            return False, output

        # divide timestamp by 1000 since it is provided in ms
        download_time = datetime.datetime.fromtimestamp(
            output.get("lastDownloaded", 0) / 1000
        )

        stat_dict = {
            "download_count": output.get("downloadCount", None),
            "last_downloaded": download_time,
            "last_downloaded_by": output.get("lastDownloadedBy", None),

            "remote_download_count": output.get("remoteDownloadCount", None),
            "remote_last_downloaded": output.get("remoteLastDownloaded", None)
        }

        return True, stat_dict


    def search_dir(self, path):

        repo_name, search_path = self.__split_repo_name(path)
        url = f"{self.baseurl}/api/search/pattern?pattern={repo_name}:{search_path}"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        files = output.get("files", [])
        files = [os.path.join(repo_name, path) for path in files]

        return True, files


    def download_file(self, path, local_dir, force_download=True):

        path = self.__remove_leading_slash(path)
        url = f"{self.baseurl}/{path}"

        self.headers["Content-Type"] = "application/json"

        filename = os.path.basename(url)
        local_path = os.path.join(local_dir, filename)

        if os.path.exists(local_path) and not force_download:
            return True, local_path

        try:
            os.makedirs(local_dir, exist_ok=True)
        except Exception as E:
            return False, f"cannot create local directory '{local_dir}': {E}"

        status, output = self.__request("GET", url, stream=True)
        if not status:
            return False, output

        response = output

        with open(local_path, 'wb') as file:
            # Reading 10 MB at a time
            for chunk in response.iter_content(chunk_size=10485760):
                file.write(chunk)

        return True, local_path


    def read_text(self, path):

        path = self.__remove_leading_slash(path)
        url = f"{self.baseurl}/{path}"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("GET", url, decode=False)
        if not status:
            return False, output

        content_binary = output
        content_txt = content_binary.decode('utf-8')

        return True, content_txt


    def download_folder(self, path, local_dir):

        status, output = self.get_dir_listing(path, recursive=True, include_stat=False)
        if not status:
            return False, output

        for entry in output:

            uri = entry.get("uri", None)
            if not uri:
                return False, "uri is missing!"

            local_dir_full = os.path.join(local_dir, uri)

            is_folder = entry.get("is_folder", None)

            if is_folder:

                try:
                    os.makedirs(local_dir_full, exist_ok=True)
                except Exception as E:
                    return False, E

            else:

                base_dir = os.path.dirname(local_dir_full)

                try:
                    os.makedirs(base_dir, exist_ok=True)
                except Exception as E:
                    return False, E

                status, output = self.download_file(uri, base_dir)
                if not status:
                    return False, output

        return True, None


    def upload_file(self, path, local_file, upload_with_hash=True):
        """
            NOTE: path should point to a directory. 'local_file' is placed under that path.
            If the remote file already exists, then we override it
        """

        if not os.path.exists(local_file):
            return False, f"local file does not exist: {local_file}"

        with open(local_file, "rb") as fobj:
            file_data = fobj.read()

        status, output = self.mkdir(path)
        if not status:
            return False, output

        path = self.__remove_leading_slash(path)
        url_rel = f"{path}/{os.path.basename(local_file)}"
        url = f"{self.baseurl}/{url_rel}"

        # If the remote artifactory already exists, then 'local_file' is
        # uploaded ONLY if checksum of the remote artifactory is equal to 'sha256'.
        if upload_with_hash and self.is_path_exists(url_rel):

            hash_local = utility.get_file_hash(local_file, algorithm="sha256")

            status, output = self.get_stat_file(url_rel)
            if not status:
                return False, output

            hash_remote = output.get("sha256", None)

            if hash_remote and hash_local == hash_remote:
                return True, None

        self.headers["Content-Type"] = "application/octet-stream"

        status, output = self.__request("PUT", url, data=file_data)
        if not status:
            return False, output

        return True, output


    def is_path_exists(self, path):

        path = self.__remove_leading_slash(path)
        url = f"{self.baseurl}/{path}"

        self.headers["Content-Type"] = "application/json"

        status, _ = self.__request("HEAD", url)

        return status


    def remove_file(self, path):

        path = self.__remove_trailing_slash(path)
        url = f"{self.baseurl}/{path}"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("DELETE", url)
        if not status:
            return False, output

        return True, None


    def mkdir(self, path, exist_ok=True):
        """
            Nested directory creation is also supported.
        """

        if self.is_path_exists(path):
            if exist_ok:
                return True, None
            return False, "path already exists"

        path = self.__remove_trailing_slash(path)
        url = f"{self.baseurl}/{path}/"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("PUT", url)
        if not status:
            return False, output

        return True, output


    def rmdir(self, path):

        path = self.__remove_trailing_slash(path)
        url = f"{self.baseurl}/{path}/"

        self.headers["Content-Type"] = "application/json"

        status, output = self.__request("DELETE", url)
        if not status:
            return False, output

        return True, None


    ##############################
    ####### Helper Methods #######
    ##############################

    def __request(self, method, url, stream=False, decode=True, **kwargs):

        try:
            response = requests.request(method,
                                        url,
                                        headers=self.headers,
                                        timeout=20,
                                        stream=stream,
                                        **kwargs)
        except Exception as E:
            return False, str(E)

        try:
            response.raise_for_status()
        except Exception as E:
            return False, f'Return code={response.status_code}, {E}\n{response.text}'

        if stream:
            return True, response

        if not decode:
            return True, response.content

        try:
            content_decoded = response.content.decode('utf-8')
            if not content_decoded:
                return True, {}

            data_dict = json.loads(content_decoded)
        except Exception as E:
            return False, f'Error while decoding content: {E}'

        return True, data_dict


    def __with_http_prefix(self, host):

        if host.startswith("http://"):
            return True

        if host.startswith("https://"):
            return True

        return False


    def __remove_leading_slash(self, input_string):

        return input_string.lstrip('/')


    def __remove_trailing_slash(self, input_string):

        return input_string.rstrip('/')


    def __split_repo_name(self, glob_pattern):

        repo_name, search_path = glob_pattern.split("/", 1)
        return repo_name, search_path
