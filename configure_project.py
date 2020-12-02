# -*- coding: utf-8 -*-
import os
import json

pdf_dir = os.path.abspath(input("Location/Directory of pdf files:"))
pdfs = list(map(lambda x : os.path.abspath(x), os.listdir(pdf_dir))
index_dir = os.path.abspath(input("Location/Directory to save indices:"))
desc_len = int(input("DESC LEN:"))
desc_threshold = float(input("DESC Threshold:"))
font_size = int(input("Font size in pixels"))
font_path = os.path.abspath(input("Font file (location):"))

with open('config.json', 'w') as f:
    json.dump({
    "PDF_DIR" : pdfs,
    "INDEX_DIR" : index_dir,
    "DESC_LEN" : desc_len,
    "DESC_THRESHOLD" : desc_threshold,
    "FONT_SIZE_IN_PIXELS" : font_size,
    "FONT_PATH_PRIMARY" : font_path
              }, f)
