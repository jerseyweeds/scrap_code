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

    return df

# Replace 'your_file.xml' with your actual XML file path
xml_file_path = 'your_file.xml'
df = xml_to_dataframe(xml_file_path)
print(df)