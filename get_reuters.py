import tarfile
import wget
import os


reuters_url = "http://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz"


def get_reuters():
    this_directory = os.path.dirname(os.path.realpath(__file__))
    list_of_files = os.listdir(this_directory)
    print(list_of_files)

    if "reuters21578" not in list_of_files:
        file = wget.download(reuters_url, this_directory)
        tar = tarfile.open(file)
        tar.extractall(path="reuters21578")
        tar.close()
        os.remove(file)
    else:
        print("You already have the necessary reuters21578 directory.")


if __name__ == '__main__':
    get_reuters()
