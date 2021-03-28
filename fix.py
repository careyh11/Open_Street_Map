import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "reno.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#UPDATED EXPECTED AS WELL
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Loop", "Way", "View", "Circle", "Row", "CreekTrail", "40",
            "Terrace"]

# UPDATE THIS VARIABLE, UPDATED
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

# DICTIONARY FOR POSTAL CODES MODELED FROM audit_steet_type
def audit_postal_code(postal_code_types, postal_code):  
    if not postal_code.isupper() or ' ' not in postal_code:
        postal_code_types['case_whitespace_problems'].add(postal_code)
    else:
        postal_code_types['other'].add(postal_code)
    return postal_code_types

# REMOVE WHITESPACE OR ANY EXTRA CHARS BEYOND 5
def update_postal_code(postal_code):
    postal_code = postal_code.upper()
    if ' ' not in postal_code:
        if len(postal_code) != 5:
            postal_code = postal_code[0:5]
    return postal_code # changed from - postal_code

# UPDATE STREET NAMES
mapping_keys = []
for k,v in mapping.items():
    mapping_keys.append(k)

def update_names(name, mapping):
    m = street_type_re.search(name)
    if name == 'sparks place':
        return name.title()
    elif name == 'Sparks Square - 3':
        return 'Sparks Square'
    elif m:
        bad_suffix = m.group()
        if m.group() in mapping_keys: #l
            good_suffix = mapping[bad_suffix]
            return re.sub(bad_suffix,good_suffix,name)
        else:
            return name
    else: 
        return name

# ADD RENO AS CITY IF NOT THERE OR MISSPELLED
def add_reno():
    osm_file = open(OSMFILE, "r")  
    city_list = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:city" and tag.attrib['v'] != "Reno":
                    city_list.add(tag.attrib['v'])
    return city_list

if __name__ == "__main__":
    add_reno()
