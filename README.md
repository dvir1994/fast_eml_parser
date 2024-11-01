# Fast EML Parser

Purpose: Parse EML files and extract attachments
How to run:

1. Go to Gmail and download the emails you want to parse - in mbox format
2. Update the constants in `mail_parse[fuzzy].py` with the path to the mbox file and the client dictionary
3. Run the python script with the command `python mail_parse[fuzzy].py`
- you can run the script with fuzzy matching by using the mail_parse_fuzzy.py script
- this will increase the number of false positives, but will also increase the number of matches

## Features

- Include OCR support for documents (PDF and JPEG)
- Iterate over emails once and check for inclusion in the client dictionary by key
- Include search functionality by ID number
- Create a client list dictionary with names and IDs (as identifiers)
- Include IDs in output folder names

## Server setup

```python
ssh-keygen -t rsa
# upload the key to GitHub deploy keys
git clone git@REPO_URL
apt update
apt install -y python3-pip tesseract-ocr tesseract-ocr-heb poppler-utils

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

conda create -n eml_parse python=3.10.3
conda activate eml_parse

pip3 install pytesseract pdf2image pillow fast-mail-parser fuzzywuzzy futures tqdm

mkdir -p "/tmp/output/"
mkdir -p "/tmp/fast_eml_parst/test/"

```
