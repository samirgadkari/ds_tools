import zlib
import regex

unique_trees = 'unique_trees'
unique_trees_actual = 'unique_trees_actual'
regexes = 'regexes'
html_analysis = {unique_trees: set(), unique_trees_actual: {}, regexes: {}}
unique_html_structures = {}
min_space_between_html_and_regex = 10

def store_unique_tree(s):

    html_analysis[unique_trees].add(s)

def get_adler_crc(s):
    return zlib.adler32(bytes(s.encode('utf-8'))) & 0xffffffff

def add_regex_for_tree(s, list_of_regex):

    # The 0xffffffff is required to make the hash value compatible
    # across multiple python versions.
    adler_crc = get_adler_crc(s)
    html_analysis['regexes'][adler_crc] = list_of_regex

def format_regex(s, adler_crc, num):
    regex = html_analysis['regexes'][adler_crc][num]
    if regex == None:
        return ''
    else:
        return regex

def max_string_length(s):
    max_len = 0
    for line in s.split('\n'):
        max_len = max(len(line), max_len)
    return max_len

def spaces_between_html_and_regex(line, max_len):

    return max_len - len(line) + min_space_between_html_and_regex

def print_html_analysis():
    for unique_tree in html_analysis[unique_trees]:
        adler_crc = get_adler_crc(unique_tree)
        actual_tree = html_analysis[unique_trees_actual][adler_crc]
        max_len = max_string_length(actual_tree)
        i = 0
        for line in actual_tree.split('\n'):
            stripped_line = line.strip().strip('"')

            if not (stripped_line.startswith('<') and \
                    stripped_line.endswith('>')):

                print(line, \
                      ' ' * spaces_between_html_and_regex(line, max_len), \
                      format_regex(actual_tree, adler_crc, i))
            else:
                print(line)

            i += 1

def build_regexes_for_all_unique_trees():
    print('len(html_analysis[unique_trees]):', len(html_analysis[unique_trees]))
    for unique_tree in html_analysis[unique_trees]:
        adler_crc = get_adler_crc(unique_tree)
        tree = html_analysis[unique_trees_actual][adler_crc]
        regexes = []
        for line in tree.split('\n'):
            if len(line.strip()) == 0:
                regexes.append(None)
                continue

            if not (line.strip().startswith('<') and \
                    line.strip().endswith('>')):
                regexes.append(regex.build_regex(line.strip().strip('"')))
            else:
                regexes.append(None)
        add_regex_for_tree(unique_tree, regexes)
