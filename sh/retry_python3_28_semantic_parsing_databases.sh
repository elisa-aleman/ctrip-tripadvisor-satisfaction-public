#!/bin/bash

python3 28_semantic_parsing_databases.py
while [ $? -ne 0 ]; do
    python3 28_semantic_parsing_databases.py
done