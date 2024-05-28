#!/bin/bash
# Description:
#   * Download big size file from Google Drive. To use, specify FILE_ID and OUTPUT.
#   * This script is based on the following link. [https://qiita.com/namakemono/items/c963e75e0af3f7eed732]

FILE_ID="1nEEDlm5upN4OxvsZS_kGCyfyHq5SBNrp"
OUTPUT="db.sqlite3"
curl -sc /tmp/cookie "https://drive.usercontent.google.com/u/0/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o ${OUTPUT}

