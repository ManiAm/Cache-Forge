
import os
import sys
import logging
from dotenv import load_dotenv

from artifactory_api import Artifactory_API

logging.basicConfig(level=logging.INFO, format='%(message)s')

log = logging.getLogger(__name__)

load_dotenv()

script_file = os.path.realpath(__file__)
script_file = os.path.abspath(script_file)
script_dir = os.path.dirname(script_file)
sample_files_dir = os.path.join(script_dir, "sample_files")


if __name__ == "__main__":

    apikey = os.getenv("ARTIFACTORY_TOKEN", None)
    if not apikey:
        log.error("ARTIFACTORY_TOKEN is not set")
        sys.exit(1)

    rest_api = Artifactory_API(
        url="http://localhost:8081",
        apikey=apikey,
        base="artifactory")

    #######

    status, version = rest_api.get_artifactory_version()
    if status:
        log.info("Artifactory version: %s", version["version"])
    else:
        log.info("Error fetching version: %s", version)

    status, repos = rest_api.get_all_repositories()
    if status:
        log.info("Repositories:")
        for repo in repos:
            log.info("- %s (type: %s)", repo["key"], repo["type"])
    else:
        log.info("Failed to list repos: %s", repos)

    #######

    for root, dirs, files in os.walk(sample_files_dir):

        for file in files:

            file_path = os.path.join(root, file)
            log.info("Uploading: %s", file_path)

            status, result = rest_api.upload_file(
                path="example-repo-local/",
                local_file=file_path,
                upload_with_hash=True   # Only uploads if changed
            )

            if status:
                log.info("Uploaded %s", file)
            else:
                log.error("Failed to upload %s:%s", file, result)

    #######

    status, listing = rest_api.get_dir_listing("example-repo-local/", recursive=True)
    if not status:
        log.error("get_dir_listing failed: %s", listing)
        sys.exit(1)

    log.info("Folder contents:")
    for item in listing:
        log.info("- %s %s", item["uri"], "(folder)" if item["is_folder"] else "")
