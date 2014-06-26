#!/bin/bash
# 2013.9.24 CKS
# Converts all *.scss files to *.css using sass.
for f in *.scss; do
    if [[ $f != _* ]]; then
        echo "Processing $f..."
        filename=$(basename "$f")
        new_filename="${filename%.*}.css"
        sass $f "../css/$new_filename"
    fi
done
