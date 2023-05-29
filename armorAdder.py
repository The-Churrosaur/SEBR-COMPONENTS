# adds armor comps (MetalGrid) to all large blocks in given folder

import xml.etree.ElementTree as ET
import os


FOLDER = "Test"

# replacement rules, replace KEY elements with VALUE
rules = {
    "SteelPlate":       "Structural", 
    "LargeTube":        "Structural",
    "SmallTube":        "Structural",
    "Construction":     "Structural",
    "Girder":           "Structural",
    "InteriorPlate":    "Structural",
    "Display":          "Structural"
    }


# replacement logic

# iterate all files
files = os.listdir(FOLDER)
for file in files:

    filepath = FOLDER + "/" + file
    tree = ET.parse(filepath)
    root = tree.getroot()

    # iterate all blocks
    for block in root.iter("Definition"):
        print(block)

        # check cubesize
        if block.find('CubeSize').text == "Large":
            print("cubesize is large")
            # add componets
            components = block.find('Components')
            ET.SubElement(components, 'Component', {"Subtype":"MetalGrid", "Count":"10"})

    
    # save changes to tree
    tree.write(filepath)
