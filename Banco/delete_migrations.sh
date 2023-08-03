#!/bin/bash

function remove_migrations {
    cd "$1"
    files=$(find . ! -name "." ! -name ".." ! -name "__init__.py" -type f)
    if [ -n "$files" ]; then
        echo "Files to be deleted in '$1':"
        echo "$files"
        rm -f $files
    fi

    dirs=$(find . -mindepth 1 -type d -empty)
    if [ -n "$dirs" ]; then
        echo "Directories to be deleted in '$1':"
        echo "$dirs"
        rm -rf $dirs
    fi
    cd -
}

echo "Searching for directories named 'migrations'..."
migrations_dirs=$(find . -type d -name "migrations")

for dir in $migrations_dirs; do
    remove_migrations "$dir"
done

echo "All specified files and directories have been removed."
