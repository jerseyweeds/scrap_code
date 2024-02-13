import xml.etree.ElementTree as ET
import pandas as pd

def flatten_xml(elem, path='', tag_dict={}, index=0):
    """
    Recursively flatten the XML and handle conflicts by prepending parent tag names.
    Also, handle elements with 'Size' attribute.
    """
    if 'Size' in elem.attrib:
        size = int(elem.attrib['Size'])
        child_tag = elem.tag
        for i in range(size):
            sub_path = f"{path}{child_tag}_{i+1}_"
            for child in elem[i]:
                flatten_xml(child, sub_path, tag_dict, i)
    elif len(elem):
        path += elem.tag + '_'
        for child in elem:
            flatten_xml(child, path, tag_dict, index)
    else:
        tag_name = f"{path.rstrip('_')}_{index+1}" if index > 0 else path.rstrip('_')
        tag_dict[tag_name] = elem.text

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
