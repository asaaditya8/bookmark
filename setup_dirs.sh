#!/bin/bash

printf "Making Directories..."

mkdir html
mkdir notebooks

printf "Done!\n"

printf "Initializing Git Repository..."

git init

printf "Done!\n"

printf "Adding pre-push script..."

cat <<\EOF >> pre-push_python.py
import os
import sys
import yaml

def get_abs_path(path):
    if path[0] == '~':
        return os.path.expanduser(path)
    else:
        # assumes path is relative to CWD
        return os.path.abspath(path)

def get_save_user_input(filename):
    sys.stderr.write("Enter source of .ipynb notebooks > ")
    src = get_abs_path(input())

    while not os.path.isdir(src):

        sys.stderr.write("Sorry couldn't find the path. Try Again:\n")
        sys.stderr.write("Enter source of .ipynb notebooks > ")
        src = get_abs_path(input())

    sys.stderr.write("Enter destination of html files > ")
    dst = get_abs_path(input())

    while not os.path.isdir(dst):

        sys.stderr.write("Sorry couldn't find the path. Try Again:\n")
        sys.stderr.write("Enter destination of html files > ")
        dst = get_abs_path(input())

    data = {'src': src, 'dst': dst}
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, indent=2)

    return data


# Checking if a saved file exists
def file_exists(filename):
    return os.path.isfile(filename)
# Checking if it contains anything
def empty_file(filename):
    with open(filename, 'r') as f:
        return yaml.load(f) is None

if __name__ == '__main__':
    FILENAME = 'config.cfg'

    try:
        assert file_exists(FILENAME)
        assert not empty_file(FILENAME)
        # Reading saved user input
        with open(FILENAME, 'r') as f:
            data = yaml.load(f)

        # Checking all the required keys are there
        assert 'src' in data
        assert 'dst' in data

        # Checking if the values are not empty for any key
        assert data['src'] is not None
        assert data['dst'] is not None

        # Change it to abs path
        data['src'] = get_abs_path(data['src'])
        data['dst'] = get_abs_path(data['dst'])

        # Check if it is correct
        assert os.path.isdir(data['src'])
        assert os.path.isdir(data['dst'])

    except:
        # Need user input again
        data = get_save_user_input(FILENAME)

    print(data['src'] + ' ' + data['dst'])
EOF

printf "Done!\n"

printf "Adding pre-push hook..."

cd .git/hooks

cat <<\EOF >> pre-push
#!/bin/bash

paths="$(python3 pre-push_python.py)"
src=$(printf "$paths" | awk '{ print $1 }')
dst=$(printf "$paths" | awk '{ print $2 }')

conda run -n jupy jupyter nbconvert "${src}/*.ipynb" --to html --output-dir "${dst}"
git add .
git commit -m "built html for jupyter notebooks"
EOF

chmod +x pre-push

cd ../..

printf "Done!\n"

printf "Setting files to ignore..."

cat <<\EOF >> .gitignore
.ipynb_checkpoints/*
notebooks/*
EOF

printf "Done!\n"

printf "\nTo setup jupyter notebooks.\nGo to Notebook Metadata.\nFind jupytext.\nThen find formats key.\n And put this in its value:\n notebooks//ipynb,py:percent\n\n"
