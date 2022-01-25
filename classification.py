'''

Input:
########
    * -m : The mapping file 
    * -f : The main field from the mapping file to use when mapping
    * -s : The sub field from the mapping file to use when mapping
    * -d : The source directory with the files to reorganize

Output:
########
    * A set of folders and subfolders with files organized based on the specified mapping fields

Usage:
########
    * python classification.py -h

    *Gives a description of the neccessary commands

    * python classification.py -m <path/mapping_file.csv> -f <field_name> -s <subfield_name> -d <path/>

    *Runs the script with the given mapping file, fields for mapping, and directory containing all files to reorganize
'''

import pandas as pd
import csv
import argparse
import os
import shutil

def main(mapping_file, main_field, sub_field, source_directory):
    '''
    Loads a mapping file and uses specified fields to reorganize files. 
    '''

    # Change the working directory
    os.chdir(source_directory)

    # Open the mapping file and create a dictionary from the values
    with open(mapping_file, 'r') as mapping:

        # Load the mapping and skip the header
        reader = csv.reader(mapping)
        next(reader, None)
        
        # Set up the mapping dictionary
        mapping_dict = {}

        # Create list of values for each key
        for row in reader: 

            # Does the key exist?
            if row[0] in mapping_dict:

                # Does the existing key not have this value?
                if row[1] not in mapping_dict.get(row[0]):

                    # Add the value
                    mapping_dict[row[0]].append(row[1])
           
            # The key doesn't exits, create it with first value
            else:
                mapping_dict[row[0]] = [row[1]]

    print(mapping_dict)
    print("Main field: " + main_field)
    print("Sub-field: " + sub_field)

    # Check the number of duplicates in the mapping file
    #df_modified.duplicated(subset='glytoucan_ac').sum()
    # total of 13803 duplicates 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands for file reorganizer script.')
    parser.add_argument('--mapping_file', '-m',
                        help='The mapping file')
    parser.add_argument('--main_field', '-f',
                        help='The main mapping field')
    parser.add_argument('--sub_field', '-s',
                        help='The submapping field')
    parser.add_argument('--source_directory', '-d',
                        help='An absolute path to the source directory to reorganize')
    args = parser.parse_args()

    main(args.mapping_file, args.main_field, args.sub_field, args.source_directory)