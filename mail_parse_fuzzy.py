import os
import sys
import shutil
import glob
import concurrent.futures
from fuzzywuzzy import process
from fast_mail_parser import parse_email, ParseError
from client_list import unique_client_list

EML_FILES_PATH = "/Users/dvir/projects/fast_eml_parse/eml_input/"
OUTPUT_FOLDER_PATH = "/Users/dvir/projects/fast_eml_parse/eml_output/"
FUZZY_SEARCH_SENSITIVITY = 90
CLINET_COUNTER = 0
EML_ITERATION_COUNTER = 0
WORKER_THREADS = 10
TEST_COUNTER = 0

def fuzzy_search(target_name, text):
    # Split the text into individual words
    words = text.split()
    # Join the words into a string with spaces
    text = " ".join(words)
    # Perform fuzzy search
    result = process.extractOne(target_name, [text])
    return result[1]


def find_client_name_in_emls(eml_file_path, current_client_name):

    with open(eml_file_path, "r") as f:
        message_payload = f.read()

    # try to parse this mail
    try:
        email = parse_email(message_payload)
    except ParseError as e:
        print("Failed to parse email: ", e)
        sys.exit(1)

    # search for client name in email content/subject
    mail_subject_search_result = fuzzy_search(email.subject, current_client_name)
    try:
        mail_content_search_result = fuzzy_search(
            email.text_html[0], current_client_name
        )
    except Exception as e:
        pass

    try:
        if (
            (mail_content_search_result > FUZZY_SEARCH_SENSITIVITY)
            or (mail_subject_search_result > FUZZY_SEARCH_SENSITIVITY)
            or (current_client_name in email.subject)
            or (current_client_name in email.text_html[0])
        ):
            # copy mail file to folder
            copy_eml_to_client_folder(current_client_name, eml_file_path)
    except Exception as e:
        pass


def copy_eml_to_client_folder(int_client_name, eml_file_path):
    # Destination file path (where you want to copy the file)
    destination_path = OUTPUT_FOLDER_PATH + int_client_name + "/"

    # Copy the file
    # if the destination path does not exist yet, create it
    os.makedirs(destination_path, exist_ok=True)
    shutil.copy(eml_file_path, destination_path)


# insert all eml files to a list
eml_files = glob.glob(EML_FILES_PATH + "*.eml")
eml_files_len = len(eml_files)


# Create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=WORKER_THREADS)

# Go over the client list
for client_name in unique_client_list:
    # Iterate over each EML file
    for eml_file_path in eml_files:
        # Submit a task to the ThreadPoolExecutor
        executor.submit(find_client_name_in_emls, eml_file_path, client_name)

# Wait for all tasks to finish
executor.shutdown(wait=True)

# Print the total number of EML files and clients processed
print(f"Done {EML_ITERATION_COUNTER} / {eml_files_len}")
print(f"Done {CLINET_COUNTER} / {len(unique_client_list)}")
