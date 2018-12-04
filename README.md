# ds_tools
## Overview
This program will:
  1. Read all files specified as the second parameter on the command line.
  2. Find unique tree structures of the specified parent.
     The parent is specified by providing a way to move around the tree.
     More information on this below.
  3. For each string value, calculate a regular expression that will
     match the whole string.  Group numbers and text/spaces,
     so we can retrieve those later.
  4. Print those unique tree structures with actual tree data.
     Next to each line print the regular expression we found for it.
  5. Extract the numbers in the values, and print them along with the key:
     ex. Afghanisthan,27755775,2002

 
## To run this script:
python html_numbers.py ../../test_data/cia/factbook_2002/fields/\*.html 'find_key_element=.CountryLink, find_key_value=string, parent_of_key_element=up-3, find_child=.Normal, find_child_value=string'

 This information is interpreted as follows:
1. find_key_element=.CountryLink
   
   This will find all tags with the CountryLink class in each file.
2. find_key_value=string
   
   Tells this program to get the string within the CountryLink tag
   and that it is a key value.
   ex. 'Afghanisthan'
3. parent_of_key_element=up-3
   
   Tells this program to go up 3 levels and get the tag.
   This tag will contain the key, and the values.
   ex. In my case, the key tag was country name,
   value tags were all the information associated within this tag.
4. find_child_value=string
   
   Tells this program to find all strings other than the key value,
   and consider them as the values for the key.
   ex. '27,755,775 (July 2002 est.)'
   Note: The commas in the numbers are removed when printing
   the key/value pairs.

