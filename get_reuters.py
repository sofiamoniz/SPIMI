import tarfile
import wget
import os
from definitions import ROOT_DIR


reuters_url = "http://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz"
list_of_files = os.listdir(ROOT_DIR)

reuters_directory = ROOT_DIR + "/reuters21578/"
reuters_extension = ".sgm"
reuters_files = []


def get_reuters():
    """
    Download tar file and store in root directory of project.
    Extract contents into 'reuters21578' directory.
    Delete tar file.
    """
    if "reuters21578" not in list_of_files:
        print("Downloading Reuters files...")
        file = wget.download(reuters_url, ROOT_DIR)
        tar = tarfile.open(file)
        tar.extractall(path=reuters_directory)
        tar.close()
        os.remove(file)


def get_reuters_files():
    """
    First, get the reuters files from online.
    Then, grab the files in the reuters directory that end in with the .sgm file extension.
    :return: sorted list of files ending with .sgm.
    """
    get_reuters()

    for file in os.listdir(reuters_directory):
        if file.endswith(reuters_extension):
            reuters_files.append(os.path.join(reuters_directory, file))

    return sorted(reuters_files)
