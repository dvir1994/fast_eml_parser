import hashlib
import os


root_dir = "/Users/dvir/projects/fast_eml_parse/output/carmen"
counter = 0


def calculate_file_hash(file_path):

    with open(file_path, "rb") as file:
        hasher = hashlib.sha256()
        hasher.update(file.read())
        return hasher.hexdigest()


def remove_duplicate_files_in_subfolder(subfolder_path):

    # Create a dictionary to store the hashes of the files in the subfolder.
    file_hashes = {}

    # Walk through the subfolder.
    for root, _, files in os.walk(subfolder_path):
        for file in files:
            # If the file is not a directory, calculate its hash.
            if not os.path.isdir(os.path.join(root, file)):
                file_path = os.path.join(root, file)
                file_hash = calculate_file_hash(file_path)

                # If the hash is already in the dictionary, then the file is a duplicate.
                if file_hash in file_hashes:
                    # Remove the duplicate file.
                    os.remove(file_path)
                    print(f"removed file - {file_path}")
                else:
                    # Add the hash to the dictionary.
                    file_hashes[file_hash] = file_path


for subfolder in os.listdir(root_dir):
    subfolder_path = os.path.join(root_dir, subfolder)

    remove_duplicate_files_in_subfolder(subfolder_path)
    counter += 1
    print(f"Done subfolder {counter}")
