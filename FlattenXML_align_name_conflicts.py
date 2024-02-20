import xml.etree.ElementTree as ET
import pandas as pd

def flatten_xml(elem, path='', tag_dict={}):
    """
    Recursive function to flatten the XML and collect data in a dictionary
    """
    if list(elem):
        path += elem.tag + '.'
        for child in elem:
            flatten_xml(child, path, tag_dict)
    else:
        tag = path + elem.tag
        if tag in tag_dict:
            if type(tag_dict[tag]) is list:
                tag_dict[tag].append(elem.text)
            else:
                tag_dict[tag] = [tag_dict[tag], elem.text]
        else:
            tag_dict[tag] = elem.text
    return tag_dict

def xml_to_dataframe(xml_file):
    """
    Converts XML file to pandas DataFrame
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Flatten the XML and get data
    data = [flatten_xml(child) for child in root]

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

# Use the function with your XML file
xml_file = 'your_xml_file.xml'  # Replace with your XML file path
df = xml_to_dataframe(xml_file)
print(df)
