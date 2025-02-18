#!/bin/bash

# Script to generate AI prompt files
set -e  # Exit immediately if any command fails

echo "Starting prompt generation process..."

# Generate files_log.txt
echo "Running files_log_gen.py..."
python tools/files_log_gen.py code

# Generate the final prompts using prompts_gen.py
echo "Running prompts_gen.py..."
python tools/prompts_gen.py

echo "Success: All prompt files generated!"