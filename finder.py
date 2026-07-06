import os
import re

def extract_lines(file_path, regex, n):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.readlines()
        for line_number, line in enumerate(text):
            match = re.search(regex, line)
            if match:
                start = max(0, line_number - n)
                end = min(len(text), line_number + n + 1)
                yield "".join(text[start:end])

def write_to_file(lines, file_name):
    try:
        with open(file_name, "a") as f:
            for line in lines:
                f.write(line)
    except FileNotFoundError:
        with open(file_name, "w") as f:
            for line in lines:
                f.write(line)

if not os.path.exists("smtp"):
    os.makedirs("smtp")

rez_folder = "Leaked"

akia_regex = r"AKIA[A-Z0-9]{16}"
rds_regex = r"((af-south-1|ap-east-1|ap-south-1|ap-northeast-1|ap-northeast-2|ap-northeast-3|ap-southeast-1|ap-southeast-2|ca-central-1|eu-central-1|eu-west-1|eu-west-2|eu-west-3|eu-north-1|eu-south-1|me-south-1|sa-east-1|us-east-1|us-east-2|us-west-1|us-west-2)\.rds\.amazonaws\.com)"
smtp_regex = r"smtp.sendgrid.net|smtp-relay.sendinblue.com|mail.smtp2go.com|smtp.socketlabs.com|secure.emailsrvr.com|mail.infomaniak.com|smtp25.elasticemail.com|in-v3.mailjet.com|smtp.zoho.com"
nopanel_regex = r"email-smtp\.(af-south-1|ap-east-1|ap-south-1|ap-northeast-1|ap-northeast-2|ap-northeast-3|ap-southeast-1|ap-southeast-2|ca-central-1|eu-central-1|eu-west-1|eu-west-2|eu-west-3|eu-north-1|eu-south-1|me-south-1|sa-east-1|us-east-1|us-east-2|us-west-1|us-west-2)\.amazonaws\.com"

n = 25

regex_to_file = {
    akia_regex: "smtp/akia.txt",
    rds_regex: "smtp/rds.txt",
    smtp_regex: "smtp/smtp.txt",
    nopanel_regex: "smtp/nopanel.txt",
}

def search_regex_in_directory(directory_path):
    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)
        print(f"Searching in: {entry_path}")
        if os.path.isfile(entry_path):
            for regex, file in regex_to_file.items():
                lines = extract_lines(entry_path, regex, n)
                write_to_file(lines, file)
        elif os.path.isdir(entry_path):
            search_regex_in_directory(entry_path)

for site_folder in os.listdir(rez_folder):
    site_path = os.path.join(rez_folder, site_folder)
    search_regex_in_directory(site_path)