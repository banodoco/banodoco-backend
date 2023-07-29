#!/bin/bash

# Define the database file name
DB_FILE="db.sqlite3"

# Check if the SQLite3 command-line tool is installed
if ! command -v sqlite3 &> /dev/null; then
    echo "SQLite3 is not installed. Please install SQLite3 before running this script."
    exit 1
fi

# Create the database file
sqlite3 "$DB_FILE" ""

# Check if the database file was created successfully
if [ $? -eq 0 ]; then
    echo "SQLite database '$DB_FILE' created successfully."
else
    echo "Error creating the database file."

# Run django migration
python manage.py migrate
fi
