import xml.etree.ElementTree as ET
import pandas as pd

def flatten_xml(elem, path='', row_data=None, all_data=None):
    """
    Recursive function to flatten the XML, handling nested structures.
    """
    if row_data is None:
        row_data = {}
    if all_data is None:
        all_data = []

    has_children = False
    for child in elem:
        has_children = True
        child_path = f'{path}{elem.tag}.'
        flatten_xml(child, child_path, row_data.copy(), all_data)

    if not has_children:
        tag = path + elem.tag
        row_data[tag] = elem.text
        all_data.append(row_data)

    return all_data

def xml_to_dataframe(xml_file):
    """
    Converts XML file to pandas DataFrame, handling nested structures.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Flatten the XML and get data
    data = []
    for child in root:
        flattened_data = flatten_xml(child)
        data.extend(flattened_data)

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

# Use the function with your XML file
xml_file = 'your_xml_file.xml'  # Replace with your XML file path
df = xml_to_dataframe(xml_file)
print(df)
