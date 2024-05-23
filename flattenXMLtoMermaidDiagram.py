import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml_recursively(element, parent_tag, relationships):
    # Get the current tag name
    current_tag = element.tag

    # Record the relationship
    if parent_tag:
        relationships.append((parent_tag, current_tag))

    # Process children
    for child in element:
        parse_xml_recursively(child, current_tag, relationships)

def xml_to_dataframe(xml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Initialize list for relationships
    relationships = []

    # Parse recursively
    parse_xml_recursively(root, "", relationships)

    # Convert to DataFrame
    df = pd.DataFrame(relationships, columns=['Parent', 'Child'])
    #df.drop_duplicates(inplace=True)
    
    return df


xml_file_path = 'analytics.index.20240102.xml'
df = xml_to_dataframe(xml_file_path)

df.drop_duplicates(inplace=True)

df.reset_index(drop=True, inplace=True)
df['value']= 1
output_file = 'structure_' + xml_file_path + '.csv'
df.to_csv(output_file, sep=',', index=False)
df.to_clipboard()
