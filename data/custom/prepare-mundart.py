from pathlib import Path

import requests
import zipfile
import os
import xml.etree.ElementTree as ET

# The URL of the zip file
url = "https://idiotikon.ch/Texte/chmk/XML-CHMK_v2.0_free_subcorpus.zip"

# The local path to save the downloaded zip file
zip_path = "./XML-CHMK_v2.0_free_subcorpus.zip"

# The directory to extract the contents of the zip file
extract_to = "./mundart"


def download_and_unzip(url, zip_path, extract_to):
    # Ensure the extract_to directory exists
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Download the file
    print(f"Downloading file from {url}")
    response = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(response.content)
    print("Download complete.")

    # Unzip the file
    print(f"Extracting contents to {extract_to}")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")

    # Optionally, remove the downloaded zip file after extraction
    os.remove(zip_path)
    print(f"Removed the zip file {zip_path}.")


# download and unzip
mundart_path = Path(extract_to)

if not mundart_path.exists():
    download_and_unzip(url, zip_path, extract_to)

contents = []
print("processing xml files...")
for xml_file in mundart_path.rglob("*.xml"):
    tree = ET.parse(xml_file)
    s_elements = tree.findall(".//{http://www.tei-c.org/ns/1.0}s")

    sentences = []
    for s_element in s_elements:
        words = s_element.findall(".//{http://www.tei-c.org/ns/1.0}w")
        sentence = " ".join([w.text for w in words])
        sentences.append(sentence)

    text = "\n".join([s for s in sentences])
    contents.append(text)

context_text = "\n\n".join(contents)
Path("mundart.txt").write_text(context_text, encoding="utf-8")
print("done")
