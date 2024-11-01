import os
import tqdm
import random
import string
import concurrent.futures
from ocr_test import image_ocr, pdf_ocr
from fast_mail_parser import parse_email

OUTPUT_FOLDER = "/tmp/output/"
INPUT_FOLDER = "/tmp/fast_eml/test/"
WORKER_THREADS = 5  # Adjust the number of worker threads as needed
RANDOM_STRING_K = 3
SERVER_NUMBER = 1
# total files - 63,641
SERVER_INDEX = {
    "1": (0, 6363),
    "2": (6364, 12727),
    "3": (12728, 19091),
    "4": (19092, 25455),
    "5": (25456, 31819),
    "6": (31820, 38183),
    "7": (38184, 44547),
    "8": (44548, 50911),
    "9": (50912, 57275),
    "10": (57276, 63641),  # The last server gets the remainder
}


def process_attachment(attachment, client_folder_name):
    # Determine the type of attachment and perform OCR
    if (
        attachment.mimetype.startswith(("image/jpeg", "image/png", "image/jpg"))
        and "ppm" not in attachment.mimetype.lower()
    ):
        text = image_ocr(attachment.content)
    elif attachment.mimetype == "application/pdf":
        text = pdf_ocr(attachment.content)
    else:
        return False

    # Check for the presence of rent agreement text
    if "rent agreement" in text:
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=RANDOM_STRING_K)
        ).lower()

        output_path = os.path.join(
            OUTPUT_FOLDER, client_folder_name, f"rent_agreement_{random_string}.pdf"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(attachment.content)
        return True
    return False


def process_eml_file(eml_file_path, client_folder_name):
    with open(eml_file_path, "r") as f:
        message_payload = f.read()

    try:
        # Parse the email content
        email = parse_email(message_payload)
    except Exception as e:
        print(f"Failed to parse email {eml_file_path}: {e}")
        return

    # Process each attachment in the email
    for index, attachment in enumerate(email.attachments):
        try:
            process_attachment(attachment, client_folder_name)
        except Exception as e:
            print(f"Error processing attachment in {eml_file_path}: {e}")


def process_client_folder(client_folder):
    client_folder_name = os.path.basename(client_folder)
    eml_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(client_folder)
        for file in files
        if file.endswith(".eml")
    ]
    return [(eml_file, client_folder_name) for eml_file in eml_files]


if __name__ == "__main__":
    # Get a list of all client folders
    client_folders = [
        os.path.join(INPUT_FOLDER, name)
        for name in os.listdir(INPUT_FOLDER)
        if os.path.isdir(os.path.join(INPUT_FOLDER, name))
    ]

    # Collect all .eml files with their client folder names
    eml_files_with_folders = []
    for client_folder in client_folders:
        eml_files_with_folders.extend(process_client_folder(client_folder))

    # get the share of this server to work on
    start, end = SERVER_INDEX[str(SERVER_NUMBER)]
    server_share = eml_files_with_folders[start : end + 1]

    # Process .eml files with multi-threading and a progress bar
    with tqdm.tqdm(total=len(server_share)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=WORKER_THREADS
        ) as executor:
            futures = [
                executor.submit(process_eml_file, eml_file, client_folder_name)
                for eml_file, client_folder_name in server_share
            ]
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)
