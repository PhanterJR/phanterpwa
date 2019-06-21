# -*- coding: utf-8 -*-
# author: PhanterJR<junior.conex@gmail.com>
# license: MIT
import os
import sys
import argparse
from zipfile import ZipFile

parser = argparse.ArgumentParser()
parser.add_argument('project_name', type=str, default=False,
                    help='Name of the project required')

parser.add_argument('-b', nargs='?', const=True,
                    help='Basic project')

parser.add_argument('-d', nargs='?', const=False,
                    help='Folder os the project')


def main():
    args = parser.parse_args()
    project_name = None
    if args.b is True:
        print("Instaling basic project scaffold")
        file = os.path.join(os.path.dirname(__file__), "scaffolds", "Scaffold_PhanterPWA_MP.zip")
    else:
        print("Instaling full project scaffold")
        file = os.path.join(os.path.dirname(__file__), "scaffolds", "Scaffold_PhanterPWA_MPI.zip")
    folder = ""
    if args.d:
        folder = args.d
    if args.project_name:
        project_name = args.project_name
        with ZipFile(file, "r") as zipf:
            if folder:
                desti = os.path.join(folder, project_name)
            else:
                desti = project_name
            print("Unziping on %s" % desti)
            zipf.extractall(path=desti)
    print("Done!")
    return True


if __name__ == "__main__":
    sys.exit(main())
