#!/bin/bash

# This file is part of the Software Factory Blueprint project
# Copyright (C) Pelagicore AB 2017
# SPDX-License_identifier: LGPL-2.1
# This file is subject to the terms of the LGPL-2.1 license.
# Please see the LICENSE file for details.


# This script does spell checks and can add words to a dictionary.
# It can be used as a git hook to perform checks, it should be named
# "pre-push","pre-commit" based on the use case and kept into the ".git/hooks/"
# and be executable. It can be bypassed by --no-verify option with git command.

set -e

# Language of the doc, install appropriate aspell libs when using
# a non-English language
lang=en

# Extension for files to be spell checked
file_extension="rst, rsti, md"

# Default execution mode for the script, check usage for more options
# One of onebyone, all or quiet.
mode="onebyone"

# List of additional dictionaries to be used for spell check
custom_dicts=""

# List of misspeled words used for addition to dictionary
misspelled_wordlist=""

# List to files to be spell checked matching the extension criteria
files=""

# Find the files from the source dir based on extensions
function fetch_files() {
    # Create an array of extensions
    IFS=', ' read -r -a extension_list <<< "$file_extension"

    # Find files
    for extension in "${extension_list[@]}"; do
        files+=$(find $source_dir/ -type f -name "*.$extension")
        files+=" "
    done
}

# Find and add the dictionaries with a particular name
function add_additional_dicts() {

    for dict in $(find $source_dir -name "aspell.en.pws"); do
        # Add dictionaries other than the project dictionary
        if [ "$dict" != "$project_dict" ]; then
            custom_dicts="$custom_dicts --add-extra-dicts=$dict"
        fi
    done
}

# Spell check the files using the dictionaries
function spell_check() {
    for file in $files; do
        if [ "$mode" == "onebyone" ]; then
            # Run aspell in interactive interface for each file
            $aspell_cmd $custom_dicts check $file
        else
            # Run aspell in non interactive mode, and list typos
            words=$($aspell_cmd $custom_dicts list < $file)
            # Convert to array and remove duplicates
            words=$(echo "$words" | tr ' ' '\n' | sort -u)
            if [ ! -z "$words" ]; then
                # Show this message once in case there are typos
                if [ -z "$misspelled_wordlist" ]; then
                    printf "%s\n" "Spell check failed on the following words :
------------------------------------------------"
                fi
                # Print the file, line and typo information
                for word in $words; do
                    grep --exclude-dir={.git} --color=always -HIrone "\<$word\>" "$file" \
                    | awk -F ":" '{print "File: " $1 "\tline number: " $2 "\tTypo: " $3}'
                done
                printf "%s\n" "-----------------------------------------"
                # Add typos to auto add list
                misspelled_wordlist+="$words"" "
            fi
        fi
    done
    if [ "$mode" == "onebyone" ]; then
        sort_project_dict
        cleanup 0
    fi
    if [ -z "$misspelled_wordlist" ]; then
        if [ "$mode" == "quiet" ]; then
            exit 0
        else
            printf "%s\n" "No typos found."
            cleanup 0
        fi
    else
        if [ "$mode" == "all" ]; then
            add_words_dict
            sort_project_dict
        fi
        cleanup 1
    fi
}

# Add misspelled words to the custom dictionary
function add_words_dict() {
    misspelled_wordlist=$(echo $misspelled_wordlist | tr ' ' '\n' | sort -u)
    if [ ! -z "$misspelled_wordlist" ]; then
        printf "%s\n" "
Add misspelled words into your custom dictionary or ignore the findings ?
    * a[ll]      (add all words to the dictionary)
    * o[ne]      (add words one by one to the dictionary)
    * n[one]     (add none, and quit)"

        while true; do
            exec < /dev/tty
            read answer
            shopt -s nocasematch
            case "$answer" in
                a|all)
                    add_words_all
                    break ;;
                o|nebyone)
                    add_words_manual
                    break ;;
                n|none)
                    break ;;
                *)
                    printf "%s\n" "Incorrect answer. Try again."
                    continue
            esac
            shopt -u nocasematch
        done
    fi
}

# Add all words to the dictionary
function add_words_all() {
    printf "%s\n" "Add all of these words to to the dictionary ? (y[es] or n[o])"
    echo $misspelled_wordlist
    exec < /dev/tty
    read answer
    shopt -s nocasematch
    case "$answer" in
        y|yes)
             for word in $misspelled_wordlist; do
                echo $word >> "$project_dict"
                printf "%s\n" "\"$word\" added to the dictionary."
            done
            break ;;
        n|no)
            add_words_dict
            break ;;
        *)
            printf "%s\n" "Incorrect answer, try again."
            continue
    esac
    shopt -u nocasematch
    for word in $misspelled_wordlist; do
        echo $word >> "$project_dict"
        printf "%s\n" "\"$word\" added to the dictionary."
    done
}

# Add words to the dictionary based on user interaction
function add_words_manual() {
    for word in $misspelled_wordlist; do
        printf "%s\n" "Add this word to the dictionary: $word  (y[es] or n[o])"
        while true; do
            exec < /dev/tty
            read answer
            shopt -s nocasematch
            case "$answer" in
                y|yes)
                    echo $word >> "$project_dict"
                    printf "%s\n" "\"$word\" added to the dictionary."
                    break ;;
                n|no)
                    break ;;
                *)
                    printf "%s\n" "Incorrect answer, try again."
                    continue
            esac
            shopt -u nocasematch
        done
    done
}

# Sort the project_dict file so it's easier to diff
function sort_project_dict() {
    { head -n1 "$project_dict"; tail -n+2 "$project_dict" | sort -u; } >file.tmp && mv file.tmp "$project_dict"
}


# Print exit message and terminate with appropriate error code
function cleanup() {
    printf "%s\n" "Spell Check completed with exit code $1"
    exit $1
}

# Print usage information of the script
function usage {
    echo "usage: $0 [options]"
    echo -e "[options] is any of the following:"
    echo -e "  -o | --onebyone  \tdefault mode, show typos one by one with suggestions"
    echo -e "                   \twith option to add them in a interactive cursor interface,"
    echo -e "                   \texit code is always 0 in this mode."
    echo -e "  -a | --all       \tlist all typos with possibility to add all"
    echo -e "                   \texit code > 0 means there are spelling mistakes."
    echo -e "  -q | --quiet     \tquiet mode, only check for spelling errors."
    echo -e "                   \texit code > 0 means there are spelling mistakes."
    echo -e "  -w | --workdir   \tcan be used to specify a source directory if the,"
    echo -e "                   \tscript is executed from a different place such as"
    echo -e "                   \ta build directory, defaults to current working directory"
    echo -e "  -h | --help      \tshow this help"
    exit 1
}

# Set default value of source dir
source_dir="."

# Read the options, w and workdir require an argument
OPTS=`getopt -o oaquhw: --long onebyone,all,quiet,help,workdir: -n 'check_spelling.sh' -- "$@"`

# Check if getopt is able to read all options
if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi

# Set the options
eval set -- "$OPTS"

# Parse the options
while true; do
  case "$1" in
    -o | --onebyone   )             mode="onebyone"
                                    shift ;;
    -a | --all        )             mode="all"
                                    shift ;;
    -q | --quiet      )             mode="quiet"
                                    shift ;;
    -w | --workdir    )             case "$2" in
                                        "") source_dir="."
                                            shift 2 ;;
                                        *)  source_dir=$2
                                            shift 2 ;;
                                    esac ;;
    -h | --help       )             usage
                                    shift 2 ;;
    --                )             shift; break ;;
    *                 )             echo "Invalid option !"
                                    exit 1 ;;
  esac
done

# Holds the project specific words that should be ignored
project_dict="$source_dir""/aspell.en.pws"

# Use aspell with no backup mode using the specified language
aspell_cmd="aspell --dont-backup --personal=$project_dict --lang=$lang"

# Fetch the files based on extension,prepare dictionaries and check
fetch_files
add_additional_dicts
spell_check
