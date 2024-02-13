import xml.etree.ElementTree as ET
import pandas as pd

def flatten_xml(elem, path='', tag_dict={}):
    """
    Recursively flatten the XML and handle conflicts by prepending parent tag names.
    """
    if len(elem):
        path += elem.tag + '_'
        for child in elem:
            flatten_xml(child, path, tag_dict)
    else:
        tag_dict[path.rstrip('_')] = elem.text

def xml_to_dataframe(file_path):
    """
    Convert XML data from a file to pandas DataFrame.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_records = []
    for elem in root:
        record = {}
        flatten_xml(elem, '', record)
        all_records.append(record)

    return pd.DataFrame(all_records)

# Example usage
file_path = 'sm.xml'
df = xml_to_dataframe(file_path)
print(df)