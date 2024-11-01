import mailbox
import concurrent.futures
from itertools import islice

mbox_file = "/root/work/eml_scrape/your_export.mbox"
output_dir = "/root/work/eml_scrape/eml_output/"

def write_eml(message_tuple):
    index, message = message_tuple
    with open(f'{output_dir}/message{index}.eml', 'w') as eml_file:
        eml_file.write(message.as_string())

def mbox2eml(mbox_file_name):
    mbox = mailbox.mbox(mbox_file_name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(write_eml, enumerate(mbox))

mbox2eml(mbox_file)