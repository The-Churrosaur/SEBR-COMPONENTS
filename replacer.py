# searches and replaces desired components
# concats contiguous replacements
# replaces critical component as well

# also changes weld times


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

# build time replacement rule
# WARNING - does not preserve original amount (current level 1/4)
buildmult = 1

# replacement logic

# iterate all files
files = os.listdir(FOLDER)
for file in files:

    filepath = FOLDER + "/" + file
    tree = ET.parse(filepath)
    root = tree.getroot()

    # find and replace build times
    for buildtime in root.iter('BuildTimeSeconds'):
        buildtime.text = str(int(float(buildtime.text) * buildmult))

    # iterate all blocks
    for block in root.iter("Definition"):
        print(block.attrib)
        
        # replace critical component by rule (same as below)
        critical = block.find('CriticalComponent')
        critsubtype = critical.attrib['Subtype']
        print("CRITICALCOMP")
        print(critical)
        print(critsubtype)
        for rule in rules:
            if critsubtype == rule:
                print("REPLACING CRITICAL: ")
                print(rule)
                critical.set('Subtype', rules[rule])

        # iterate all components in that block
        prevcomponent = 0
        components = block.find('Components')
        for component in components.findall('Component'):
            print(component.attrib)

            # check if that component matches a rule and replace
            subtype = component.attrib['Subtype']
            for rule in rules:
                if subtype == rule: 

                    # replacement by rule
                    component.set('Subtype', rules[rule])
                    print("CHANGED TO: ")
                    print(component.attrib)

                    # contiguity -
                    # if identical:
                    # concat count with previus component count
                    # delete previous component

                    if (prevcomponent != 0) and (prevcomponent.attrib['Subtype'] == component.attrib['Subtype']):
                        prevcount = prevcomponent.attrib['Count']
                        count = component.attrib['Count']
                        sum = int(prevcount) + int(count)
                        print(prevcount, "+", count, "=", sum)
                        component.set('Count', str(sum))
                        components.remove(prevcomponent)

                    # set current component as previous component
                    prevcomponent = component

                    print()

        print()
    
    # save changes to tree
    tree.write(filepath)
