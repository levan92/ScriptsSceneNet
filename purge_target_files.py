import os
import argparse

def main(dir,target):
    for root, folders, files in os.walk(dir):
        for file in files:
            if file.startswith(target):
                filepath = os.path.join(root, file)
                os.remove(filepath)
                print('Removed',filepath)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, help='directory to be purged of certain file')
    parser.add_argument('target', type=str, help='target file to be purged')
    args = parser.parse_args()
    main(args.dir, args.target)
