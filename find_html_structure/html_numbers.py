import re
import glob
import sys
from bs4 import BeautifulSoup
from bs4 import NavigableString
import nodes
import regex
import trees

# This program will:
#   1. Read all files specified as the second parameter on the command line.
#   2. Find unique tree structures of the specified parent.
#      The parent is specified by providing a way to move around the tree.
#      More information on this below.
#   3. For each string value, calculate a regular expression that will
#      match the whole string.  Group numbers and text/spaces,
#      so we can retrieve those later.
#   4. Print those unique tree structures will actual tree data.
#      Next to each line print the regular expression we found for it.
#   5. Extract the numbers in the values, and print them along with the key:
#      ex. Afghanisthan,27755775,2002
#
# To run this script:
# python html_numbers.py ../../test_data/cia/factbook_2002/fields/\*.html 'find_key_element=.CountryLink, find_key_value=string, parent_of_key_element=up-3, find_child=.Normal, find_child_value=string'
#
# 1. find_key_element=.CountryLink
#    This will find all tags with the CountryLink class in each file.
# 2. find_key_value=string
#    Tells this program to get the string within the CountryLink tag
#    and that it is a key value.
#    ex. 'Afghanisthan'
# 3. parent_of_key_element=up-3
#    Tells this program to go up 3 levels and get the tag.
#    This tag will contain the key, and the values.
#    ex. In my case, the key tag was country name,
#    value tags were all the information associated within this tag.
# 4. find_child_value=string
#    Tells this program to find all strings other than the key value,
#    and consider them as the values for the key.
#    ex. '27,755,775 (July 2002 est.)'
#    Note: The commas in the numbers are removed when printing
#    the key/value pairs.

def get_html_file_data():
    # This is non-recursive search in the given directory,
    # or searches for the given single file.
    # Search must find HTML files only, so make sure the
    # filepath is pointing to only HTML files.
    if (len(sys.argv) < 3):
        print('Usage: html_structure filepath findall_dictionary')
        sys.exit(1)

    filepath = sys.argv[1]
    print('filepath:', filepath)
    files = glob.glob(filepath)
    # print('files:', files)

    instructions = sys.argv[2]

    file_data = {}

    processed_html_res = {}
    for file in files:
        # for file in files:
        try:
            with open(file, 'r') as f:
                file_data[f.name] = f.read()
        except Exception as ex:
            print('Error for file:', file, ex)

    try:
        processed_html_res = nodes.process_all_html(file_data, instructions)
    except Exception as ex:
        print('Error processing file_data:', ex)

    return processed_html_res

def create_html_representation(prefix, e):
    res = ''
    if isinstance(e, NavigableString):
        res = prefix + '"' + e.strip() + '"\n'
    else:
        res = prefix + '<' + e.name + '>\n'
        for child in e.children:
            res = res + create_html_representation('  ', child)
    return res

def get_tree_reprs(tree_repr):

    stripped_tree_repr = ''
    actual_tree_repr = ''
    for line in tree_repr.split('\n'):
        if len(line.strip()) == 0:
            continue

        if not (line.strip().startswith('<') and \
                line.strip().endswith('>')):
            stripped_tree_repr = stripped_tree_repr + '\n'
        else:
            stripped_tree_repr = stripped_tree_repr + line + '\n'
        actual_tree_repr = actual_tree_repr + line + '\n'

    return stripped_tree_repr, actual_tree_repr

compiled_regexes = {}
numbers_regex = '[\d.,]+'
numbers_compiled_regex = re.compile(numbers_regex)
def get_numbers_from_tree(tree):

    res = []
    for line in tree.split('\n'):
        if len(line.strip()) == 0:
            # regexes.append(None)
            continue

        if not (line.strip().startswith('<') and \
                line.strip().endswith('>')):
            text_regex= regex.build_regex(line)
            compiled_regex = None
            if (text_regex not in compiled_regexes.keys()):
                compiled_regex = compiled_regexes[text_regex] = re.compile(text_regex)
            else:
                compiled_regex = compiled_regexes[text_regex]

            match = compiled_regex.match(line)
            if match != None:
                for i in range(len(match.groups())):
                    if i == 0:
                        continue

                    text = match.group(i)
                    if numbers_compiled_regex.match(text) != None:
                        res.append(text)

    return res

if __name__ == '__main__':

    processed_html_res = get_html_file_data()
    for processed in processed_html_res:
        for filename, res in processed.items():
            for country, res_list in res.items():
                parent = res_list[1]
                tree_repr = create_html_representation('', parent)

                stripped_tree_repr, actual_tree_repr = get_tree_reprs(tree_repr)
                adler_crc = trees.get_adler_crc(stripped_tree_repr)
                trees.html_analysis[trees.unique_trees_actual] \
                                   [adler_crc] = actual_tree_repr

                trees.store_unique_tree(stripped_tree_repr)

    trees.build_regexes_for_all_unique_trees()
    trees.print_html_analysis()

    for processed in processed_html_res:
        for filename, res in processed.items():
            print('Filename:', filename)
            for country, res_list in res.items():
                parent = res_list[1]
                # print('parent:', parent)
                tree_repr = create_html_representation('', parent)

                numbers = get_numbers_from_tree(tree_repr)
                print(country.strip(), end = '')
                for number in numbers:
                    print(',' + str(number.replace(',', '').strip()), end = '')
                print()
