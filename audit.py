"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "reno.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#UPDATED EXPECTED AS WELL *************************************************************************************************************
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Loop", "Way", "View", "Circle", "Row", "CreekTrail", "40",
            "Terrace"]

# UPDATE THIS VARIABLE, UPDATED *****************************************************************************************************
mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "Ave": "Avenue",
            "Blvd": "Boulevard",
            "blvd:": "Boulevard",
            "Pkwy": "Parkway",
            "pkwy": "Parkway",
            "Ln": "Lane",
            "pl": "Place",
            "Ct": "Court",
            "Pl": "Place",
            "Dr": "Drive",
            "Pl.": "Place",
            "Dr": "Drive"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    return street_types #FIXED


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(OSMFILE):
    osm_file = open(OSMFILE, "r")
    street_types = defaultdict(set)
    postal_code_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postal_code(tag):
                    audit_postal_code(postal_code_types, tag.attrib['v'])

    osm_file.close()
    return street_types, postal_code_types


# YOUR CODE STARTS **********************************************************************************************************************************************************************************************************


# CHARS FOR POSTAL CODE
def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


# DICTIONARY FOR POSTAL CODES MODELED FROM audit_steet_type
def audit_postal_code(postal_code_types, postal_code):  
    if not postal_code.isupper() or ' ' not in postal_code:
        postal_code_types['case_whitespace_problems'].add(postal_code)
    else:
        postal_code_types['other'].add(postal_code)
    return postal_code_types


# POSTAL CODE TEST MODELED FROM test
def postal_code_test(): 
    postcode_types = audit(OSMFILE)[1]
    pprint.pprint(dict(postcode_types))

    for postcode_type, postcodes in postcode_types.items():
        for postcode in postcodes:
            better_postcode = update_postal_code(postcode)
            print(postcode, "=>", better_postcode)
            

# YOUR CODE ENDS **********************************************************************************************************************************************************************************************************
  

def test():
    st_types = audit(OSMFILE)[0]#ADDED FOR DICT, FIXED
    len(st_types) == 5
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print(name, "=>", better_name)
            if name == "West Lexington St.":
                better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                better_name == "Baldwin Road"
                

#if __name__ == '__main__':
#    test()
#    postal_code_test()
