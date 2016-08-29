#!/usr/bin/env python

import os
import json
import sys
import argparse
from getpass import getuser
import traceback


def get_json_blob(file_path, file_name):
    """
    import json blob from file
    :param: file_path:
    """
    with open(file_path + '/' + file_name) as f:
        return json.load(f)

        
def process_json(data, main_key):
    """
    convert json into records (which are lists)
    :param data: a dictionary of values
    :param main_key the main key of the dict that we want to extract data from
    :return (set, list). all keys appeared in the dict, records
    """
    # use input main_key or expect there to just be one key and use that
    if not main_key:
        main_key = data.keys()[0]
    items_list = data[main_key]
    
    # get all unique keys in dict
    key_set = []
    map(lambda record: key_set.extend(record.keys()), items_list)
    key_set = set(key_set)

    records = create_records(key_set, items_list)
    
    header = ['\t'.join(key_set) + '\n']
    records = ['\t'.join(record)+'\n' for record in records]
    
    return header, records


def create_records(key_set, items_list):
    """
    :param items_list: list. a list of rows ready to be written back to a file
    return
    """

    records = []
    for record in items_list:
        row = []
        for key in key_set:
            # the value of the given key
            val = record.get(key)
            print val
            
            # process value depending on types
            if val:
                # format list
                if type(val) == list:
                    print "val is list"
                    # format list of dicts
                    if type(val[0]) == dict:
                        print "val is dict"
                        # keys and values from dictionary/ies
                        tups = [[(k,str(v))for k, v in sub_item.iteritems()] for sub_item in val]
                        # joins tuples keys and values with :
                        results = [[':'.join(tup) for tup in item] for item in tups]
                        # joins tuples in same dict with ; and | between dicts
                        results = ['|'.join([';'.join(item) for item in results])]
                        row += results
                    # format list of strings
                    else:
                        print "val is list but not dict"
                        row += ['|'.join(map(lambda elm: str(elm), val))]
                        print row
                # format everything that is not a list
                else:
                    print "val is something else"
                    row += [str(val)]
            else:
                row += ['']
        records.append(row)
    return records


def get_params(input_path, output_path, input_file, output_file):
    """
    get input/output paths and parameters based on OS/ input arguments
    """
    default_path = os.path.expanduser('~'+getuser()) 
    input_path = input_path or default_path
    output_path = output_path or input_path or default_path
    output_file = output_file or input_file.split('.')[0] + '.tsv'

    print "Chosen variables:"
    print "input_path: ", input_path
    print "output_path:", output_path
    print "output_file:", output_file

    return input_path, output_path, output_file 


def write_to_disk(output_path, file_name, output_header, output_records):
    """
    """
    with open(output_path + '/' + file_name, 'w') as f:
        f.writelines(output_header)
        f.writelines(output_records)


def main():
    """
    ENTRY POINT
    """

    # get parameters - from arguments or default values
    args = parse_args()

    try:
        input_path, output_path, output_file = get_params(args.input_path, args.output_path, args.input_file, args.output_file)
        
        data = get_json_blob(input_path, args.input_file)
        header, records = process_json(data, args.main_key)
        
        write_to_disk(output_path, output_file, header, records)

    except:
        print traceback.format_exc()
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    # compulsory 
    parser.add_argument('-i', '--input-file', type=str, help='Input file name', required=True)

    # optional 
    parser.add_argument('-I', '--input-path', type=str, help='Input file path (using delimiter /)')
    parser.add_argument('-O', '--output-path', type=str, help='Output file path (using delimiter /)')
    parser.add_argument('-o', '--output-file', type=str, help='Output file name')
    parser.add_argument('-k', '--main-key', type=str, help='Main key to access the list of records')
    return parser.parse_args(sys.argv[1:])

        
if __name__ == '__main__':
    main()
