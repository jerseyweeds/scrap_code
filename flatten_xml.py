import xml.etree.ElementTree as ET
import pandas as pd

def flatten_xml(elem, path='', tag_dict={}, parent_index=1, split_char='|'):
    """
    Recursively flatten the XML and handle conflicts by prepending parent tag names with a custom delimiter.
    Handle elements with 'Size' attribute by processing each child individually.
    """
    if 'Size' in elem.attrib:
        size = int(elem.attrib['Size'])
        for i, child in enumerate(elem, start=1):
            new_path = f"{path}{elem.tag}{split_char}{i}{split_char}"
            flatten_xml(child, new_path, tag_dict, split_char=split_char)
    elif len(elem):
        new_path = f"{path}{elem.tag}{split_char}"
        for child in elem:
            flatten_xml(child, new_path, tag_dict, split_char=split_char)
    else:
        tag_name = f"{path.rstrip(split_char)}{split_char}{parent_index}" if parent_index > 1 else path.rstrip(split_char)
        tag_dict[tag_name] = elem.text

def xml_to_dataframe(file_path, split_char='|'):
    """
    Convert XML data from a file to pandas DataFrame using a custom delimiter for tag names.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    all_records = []
    for elem in root:
        record = {}
        flatten_xml(elem, '', record, split_char=split_char)
        all_records.append(record)

    return pd.DataFrame(all_records)

# Example usage
file_path = 'sm.xml'
df = xml_to_dataframe(file_path)
print(df)
