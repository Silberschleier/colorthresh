#!/bin/bash
FILES=*.png
for f in $FILES
do
    echo "Processing $f..."
    python ../colorthresh.py $@ --output "threshed_$f" "$f"
done
echo "Generation merged.pdf..."
convert -page A4 threshed_* merged.pdf
rm threshed_*