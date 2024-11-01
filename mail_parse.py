import tqdm
import os
import shutil
import glob
import concurrent.futures
from fuzzywuzzy import process
from fast_mail_parser import parse_email
from client_list import unique_client_list
from ocr_test import image_ocr, pdf_ocr

EML_FILES_PATH = "/root/work/eml_scrape/eml_input/"
OUTPUT_FOLDER_PATH = "/root/work/eml_scrape/eml_output/"
FUZZY_SEARCH_SENSITIVITY = 90
WORKER_THREADS = 5


def fuzzy_search(target_name, text):
    # split the text into individual words
    words = text.split()
    # join the words into a string with spaces
    text = " ".join(words)
    # perform fuzzy search
    result = process.extractOne(target_name, [text])
    return result[1]


def copy_eml_to_client_folder(int_client_name, eml_file_path, client_id_num):
    destination_path = OUTPUT_FOLDER_PATH + f"{int_client_name} - {client_id_num}" + "/"
    # create destination if it does not exist and copy the file
    os.makedirs(destination_path, exist_ok=True)
    shutil.copy(eml_file_path, destination_path)


def find_client_name_in_emls(eml_file_path):
    pbar.update(1)

    with open(eml_file_path, "r") as f:
        message_payload = f.read()

    # try to parse this mail
    try:
        email = parse_email(message_payload)
    except Exception as e:
        print(e)

    # search for client name in email content/subject
    try:
        email_subject = email.subject
    except Exception:
        email_subject = ""
    try:
        email_text_html = email.text_html[0]
    except Exception:
        email_text_html = ""
    try:
        email_text_plain = email.text_plain
    except Exception:
        email_text_plain = ""

    # perform OCR for relevant attachements - image / PDF
    total_text_from_attachments = ""
    try:
        for attachment in email.attachments:
            if (
                attachment.mimetype.startswith("image/jpeg")
                and "ppm" not in attachment.mimetype.lower()
            ):
                total_text_from_attachments += image_ocr(attachment.content)

            if attachment.mimetype == "application/pdf":
                total_text_from_attachments += pdf_ocr(attachment.content)
    except Exception as e:
        print(f"Error with OCR: {print (e)}")

    # iterate over client list
    for client_id, client_name in unique_client_list:
        try:
            if (
                (client_id in email_subject)
                or (client_id in email_text_html)
                or (client_id in email_text_plain)
                or (client_id in total_text_from_attachments)
                or (client_name in email_subject)
                or (client_name in email_text_html)
                or (client_name in email_text_plain)
                or (client_name in total_text_from_attachments)
                # or (fuzzy_search(email.subject, client_name) > FUZZY_SEARCH_SENSITIVITY)
                # or (fuzzy_search(email.text_html[0], client_name) > FUZZY_SEARCH_SENSITIVITY)
            ):
                # copy mail file to folder
                copy_eml_to_client_folder(client_name, eml_file_path, client_id)
        except Exception as e:
            print(e)


# insert all eml files to a list
eml_files = glob.glob(EML_FILES_PATH + "*.eml")
# create a progress bar
pbar = tqdm.tqdm(total=len(eml_files))
# create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=WORKER_THREADS)

for eml_file_path in eml_files:
    # submit a task to the ThreadPoolExecutor
    executor.submit(find_client_name_in_emls, eml_file_path)

# wait for all tasks to finish
executor.shutdown(wait=True)

# close the progress bar
pbar.close()
