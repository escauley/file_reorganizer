'''
Input:
########
    * -m : Mapping file 
    * -n : Name field from the mapping file to identify individual files
    * -f : Main field from the mapping file to use when mapping
    * -s : Sub field from the mapping file to use when mapping (optional)
    * -d : Source directory with the files to reorganize
    * -x : File extension

Output:
########
    * A set of folders and subfolders with files organized based on the specified mapping fields

Usage:
########
    * python classification.py -h

    *Gives a description of the neccessary commands

    * python organize_files.py -m <path/mapping_file.csv> -n <name_field> -f <field_name> -s <subfield_name> -d <path/> -x <.file_extension>

    *Runs the script with the given mapping file, fields for mapping, and directory containing all files to reorganize
'''

from numpy import source
import csv
import argparse
import os
import shutil
import sys

def main(mapping_file, name_field, main_field, sub_field, source_directory, file_extension):
    '''
    Loads a mapping file and uses specified fields to reorganize files. 
    '''

    print("Reorganizing " + source_directory + " with mapping file " + mapping_file)
    # Check if subfield was specified
    if sub_field != 'no_sub':
        print("File names from the mapping field '" + name_field + "' will be reorganized first based on '" + main_field + "' then based on '" + sub_field + "'")
    else:
        print("File names from the mapping field '" + name_field + "' will be reorganized based on '" + main_field + "' only.")

    # Check if directory path exists
    if os.path.isdir(source_directory) is False:
        sys.exit("Source directory not found, exiting")

    # Check that source directory path is formatted correctly
    if source_directory.endswith('/') is False:
        sys.exit("Source directory must end with a backslash ('/'), exiting...")

    # Make a tmp directory to hold files while they are moved
    if os.path.isdir(source_directory + "tmp") is False:
        os.mkdir(source_directory + "tmp")

    # Gather stats on number of files and folders created
    file_count = 0
    folder_count = 0
    sub_folder_count = 0
    
    # Check that the path to the mapping file exists
    if os.path.isfile(mapping_file) is False:
        sys.exit('No mapping file found, make sure path to mapping file is specified correctly! Exiting...')

    
    # Open the mapping file and create a dictionary from the values
    with open(mapping_file, 'r') as mapping:

        # Load the mapping and skip the header
        reader = csv.reader(mapping)
        
        # Gather the headers and identify the index number of the name, main, and sub fields to map
        for row in reader:
             headers = row
             break
        
        # Index number = field column number 
        name_index = headers.index(name_field)
        main_index = headers.index(main_field)
        # Check if sub field was specified
        if sub_field != 'no_sub':
            sub_index = headers.index(sub_field)

        # Move each file into directories according to the mapping
        for row in reader: 

            # Check if file exists in the source directoy or tmp directory
            if os.path.isfile(source_directory + row[name_index] + file_extension) is False and os.path.isfile(source_directory + "tmp/" + row[name_index] + file_extension) is False:
                
                print("No file found for " + row[name_index])

                # File doesn't exist
                continue
                
                

            else:
                file_count = file_count + 1
                
                # If the file has not been moved to tmp directory, move the file to tmp directory
                if os.path.isfile(source_directory + row[name_index] + file_extension):
                    os.rename(source_directory + row[name_index] + file_extension, source_directory + "tmp/" + row[name_index] + file_extension)

                # If the main folder does not exist, create it
                if os.path.isdir(source_directory + row[main_index]) is False:
                    os.mkdir(source_directory + row[main_index])

                    folder_count = folder_count + 1
                
                # Check if sub_field was specified
                if sub_field != 'no_sub':

                    # If the sub folder does not exist, create it
                    if os.path.isdir(source_directory + row[main_index] + "/" + row[sub_index]) is False:
                        os.mkdir(source_directory + row[main_index] + "/" + row[sub_index])

                        sub_folder_count = sub_folder_count + 1
                

                    # Copy the file into the mapped sub-directory
                    shutil.copy(source_directory + "tmp/" + row[name_index] + file_extension, source_directory + row[main_index] + "/" + row[sub_index] + "/" + row[name_index] + file_extension)
                
                # If no sub field specified, copy the file into the mapped main directory
                else:
                    shutil.copy(source_directory + "tmp/" + row[name_index] + file_extension, source_directory + row[main_index] + "/" + row[name_index] + file_extension)

    # Remove the tmp directory
    shutil.rmtree(source_directory + "tmp/")

    print("File reorganization complete!")
    print("There are now " + str(file_count) + " total files in " + str(folder_count) + " main folders and " + str(sub_folder_count) + " sub folders.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands for file reorganizer script.')
    parser.add_argument('--mapping_file', '-m',
                        help='An absolute path to the mapping file, not located in the source directory')
    parser.add_argument('--name_field', '-n',
                        help='The name mapping field')
    parser.add_argument('--main_field', '-f',
                        help='The main mapping field')
    parser.add_argument('--sub_field', '-s',
                        help='The submapping field (optional)', nargs='?', default='no_sub')
    parser.add_argument('--source_directory', '-d',
                        help='An absolute path to the source directory to reorganize')
    parser.add_argument('--file_extension', '-x',
                        help='The file extension of files to reorganize (eg .csv, .txt, etc)')
    args = parser.parse_args()

    main(args.mapping_file, args.name_field, args.main_field, args.sub_field, args.source_directory, args.file_extension)