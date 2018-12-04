from enum import Flag, auto
class CharGroup(Flag):
    BEGIN = auto()
    LETTERS = auto()
    WHITESPACE = auto()
    COMMAS = auto()
    LETTERS_WHITESPACE_COMMAS = LETTERS | WHITESPACE | COMMAS
    PERIOD = auto()
    NUMBERS = auto()
    NUMBERS_PERIOD_COMMAS = NUMBERS | PERIOD | COMMAS
    MULTIPLIER = auto()     # BILLION, MILLION, THOUSAND
    SEPARATOR = auto()
    END = auto()

multiplier_names = ['billion', 'million', 'thousand', 'billions', 'millions', 'thousands']
separators = '()[]%/;:-,'
whitespace = ' \n\t'
groupings = {}

def identify_character_group_by_itself(c, pos, mult_pos):

    for positions in mult_pos:
        start, stop = positions[0], positions[1]
        if (pos >= start) and (pos <= stop):
            return CharGroup.MULTIPLIER

    if ((c >= 'A') and (c <= 'Z')) or ((c >= 'a') and (c <= 'z')) or \
       (c == '\t') or (c == '\n') or (c == ' '):
        return CharGroup.LETTERS_WHITESPACE_COMMAS
    elif ((c >= '0') and (c <= '9')) or (c == '.') or (c == ','):
        return CharGroup.NUMBERS_PERIOD_COMMAS
    elif (c in separators):
        return CharGroup.SEPARATOR
    else:
        # This is just a default.  If we find we need some other
        # characters to pull out information, we can add them above.
        return CharGroup.SEPARATOR

def identify_character_group_in_sequence(pos, mult_pos, c, current_group):

    char_group = identify_character_group_by_itself(c, pos, mult_pos)

    if (current_group != char_group):

        if (current_group == CharGroup.NUMBERS_PERIOD_COMMAS) and \
           (c in whitespace):
            groupings[pos] = CharGroup.SEPARATOR
            return current_group
        elif c.isalpha() and \
             (current_group == CharGroup.LETTERS_WHITESPACE_COMMAS):
            groupings[pos] = current_group
        elif (char_group in current_group):
            groupings[pos] = current_group
        else:
            groupings[pos] = char_group

    return char_group

def find_all_multipliers(s):
    res = []
    for m in multiplier_names:
        idx = s.find(m)
        if idx != -1:
            res.append([idx, idx + len(m) - 1])

    return res

def parse_string(s):
    groupings.clear()
    current_group = CharGroup.BEGIN

    multiplier_start_stop_pos = find_all_multipliers(s)
    i = 0
    for letter in s:
        current_group = \
            identify_character_group_in_sequence(i, \
                                                 multiplier_start_stop_pos, \
                                                 letter, current_group)
        i += 1

def build_regex(s):
    if len(s) == 0:
        return None

    parse_string(s)
    res = []
    for pos, char_group in groupings.items():
        if (char_group == CharGroup.SEPARATOR):
            if (s[pos] == ' '):
                res.append('\s')
            else:
                res.append('\\' + s[pos])
        elif (char_group == CharGroup.NUMBERS_PERIOD_COMMAS):
            res.append('([\d.,]+)')
        elif (char_group == CharGroup.LETTERS_WHITESPACE_COMMAS):
            res.append('([a-zA-Z\s]+)')
        elif (char_group == CharGroup.MULTIPLIER):
            res.append('([a-zA-Z]+)')
        else:
            raise(ValueError, 'Cannot get regex for char group:', char_group)
    return ''.join(res)
