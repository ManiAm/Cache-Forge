
import json
import csv
import zipfile
import tarfile
import os

os.makedirs("sample_files", exist_ok=True)

with open("sample_files/sample.txt", "w") as f:
    f.write("This is a sample text file.")

with open("sample_files/sample.json", "w") as f:
    json.dump({"project": "Cache-Forge", "version": 1.0}, f)

with open("sample_files/sample.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "email"])
    writer.writerow(["Alice", "alice@example.com"])
    writer.writerow(["Bob", "bob@example.com"])

with open("sample_files/sample.log", "w") as f:
    f.write("INFO 2025-07-28 Starting Cache-Forge\nERROR 2025-07-28 Something failed")

with open("sample_files/sample.conf", "w") as f:
    f.write("[settings]\ncache_dir=/var/cache/forge\nlog_level=INFO")

with zipfile.ZipFile("sample_files/sample.zip", "w") as zipf:
    zipf.write("sample_files/sample.txt", arcname="sample.txt")

with tarfile.open("sample_files/sample.tar.gz", "w:gz") as tar:
    tar.add("sample_files/sample.txt", arcname="sample.txt")
