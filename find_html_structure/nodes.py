from bs4 import BeautifulSoup
from bs4 import NavigableString

def strip_key_val(k, v):
    return k.strip(), v.strip()

def split_instructions(instructions):

    keys = []
    values = []
    for ins in instructions.split(','):
        k, v = ins.split('=')
        k, v = strip_key_val(k, v)

        if (k == 'parent_of_key_element') and v.startswith('up'):
            k1, v1 = v.split('-')
            k1, v1 = strip_key_val(k1, v1)
            v = [k1, int(v1)]

        keys.append(k)
        values.append(v)
    return keys, values

def get_html_element_key_value(current, instructions, selectors):
    k = instructions[0]
    v = selectors[0]
    parent, child = current, current
    key_value, child_value = '', ''

    for i in range(len(instructions)):
        k = instructions[i]
        v = selectors[i]

        if k == 'find_key_value':
            key_value = current = current.string

        elif k == 'parent_of_key_element':
            for i in range(v[1]):
                parent = current = current.parent

        elif k == 'find_child':
            children = current.select(v)
            if len(children) > 1:
                raise(ValueError, \
                      'Should only have one child in a selected element')
            child = current = children[0]

        elif k == 'find_child_value':
            child_value = current = current.string

    if isinstance(key_value, str):
        key_value = key_value.strip()
    if isinstance(child_value, str):
        child_value = child_value.strip()

    return key_value, child_value, parent

def process_instructions(soup, instructions, selectors):

    if instructions[0] == 'find_key_element':
        keys = soup.select(selectors[0])

        res = {}
        for key in keys:
            k, v, parent = get_html_element_key_value( \
                                                       key, \
                                                       instructions[1:], \
                                                       selectors[1:])
            res[k] = [v, parent]
    else:
        raise(ValueError, 'First instruction must be for find_key_element')

    return res

def find_all_tags(filename, html, instructions, selectors):
    soup = BeautifulSoup(html, 'html.parser')
    res = {}
    res[filename] = process_instructions(soup, instructions, selectors)
    return res

def process_all_html(file_data, instructions_and_selectors):

    instructions, selectors = split_instructions(instructions_and_selectors)
    all_file_results = [find_all_tags(filename, html, instructions, selectors) \
                          for filename, html in file_data.items()]

    return all_file_results
