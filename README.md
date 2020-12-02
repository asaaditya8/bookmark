# Bookmark

### Requirements
python >= 3.6
pyimgui
glfw (it is one of the pyimgui's supported backends)
pdfminer
textacy
whoosh
lexrank
tqdm


### How to setup environment?

```
conda create -n myenv -c conda-forge python=3.6
# For packages available in anaconda
conda install <package_name>

# For packages available in pip
pip install <package_name>
```

### How to run?
- Create a configuration file.
- Add all the required parameters.
- Run the project.
```
# This will save all the preferences in config.json.
python configure_project.py

# Then run the application.
python project.py
```

### What I learned?
- Familiarity with PyImgui for gui
- Whoosh for text search
- Pdfminer for handling pdf
- **NLP**:
    - Textacy for keyword extraction
    - Lexrank for automatic summarization
