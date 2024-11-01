from random import randint
import concurrent.futures
import tqdm
import os
import re
from fast_mail_parser import parse_email

ROOT_DIR = "/Users/dvir/projects/fast_eml_parse/output/carmen"
WORKER_THREADS = 2
files_counter = 0

# calculate file num
for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".eml"):
            files_counter += 1
pbar = tqdm.tqdm(total=files_counter)


def rename_eml_file(eml_file_path):
    pbar.update(1)
    with open(eml_file_path, "r") as f:
        message_payload = f.read()

    mail = parse_email(message_payload)
    new_file_name = re.sub(r"[^\w\s]", "", mail.subject) + ".eml"

    new_file_path = os.path.abspath(
        os.path.join(os.path.dirname(eml_file_path), new_file_name)
    )

    # If the file already exists, append a number to the end of the file name.
    if os.path.exists(new_file_path):
        new_file_name = new_file_name + f"{randint(0,100)}.eml"

    new_file_path = os.path.abspath(
        os.path.join(os.path.dirname(eml_file_path), new_file_name)
    )

    os.rename(eml_file_path, new_file_path)


# create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=WORKER_THREADS)

for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".eml"):
            eml_file_path = os.path.join(root, file)

            executor.submit(rename_eml_file, eml_file_path)

# wait for all tasks to finish
executor.shutdown(wait=True)

# close the progress bar
pbar.close()
