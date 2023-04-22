#!/bin/bash

# Script for batch compiling dot files in directory to png images.
# Usage: ./converter.sh <directory>

for filename in ./$1/*.dot; do
	dot -Tpng $filename -o $filename.png
	dot -Tsvg $filename -o $filename.svg
done
