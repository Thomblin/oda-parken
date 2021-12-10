import pandas as pd
import numpy as np

#import the datasets corresponding to these years
years = ["2019", "2020"]

fines = current_fines = pd.read_csv("../data/fines_"+years[0]+".csv", sep=";", dtype={"Tattag": str, "Zeit": str, "Tatort 2": str, "Tatbestand": str, "Geldbuße": int})

for year in years[1:]:
    current_fines = pd.read_csv("../data/fines_"+year+".csv", sep=";",dtype={"Tattag": str, "Zeit": str, "Tatort 2": str, "Tatbestand": str, "Geldbuße": int})
    fines.append(current_fines)
    
fines = fines.rename(columns={"Tatort 2": "location_text"})
fines.location_text = fines.location_text.astype(str)

def parse_street_no(number):
    
    #handle street nos with letters in them by removing them (future potential for improvement!)
    number = "".join([char for char in number if char.isdigit()])
    
    if len(number) == 0:
        return
    
    if "-" in number:
        try:
            return [int(no) for no in number.split("-")]
        except ValueError:
            return None
    elif "/" in number:
        try:
            return [int(no) for no in number.split("/")]
        except ValueError:
            return None
    else:
        try:
            return [int(number)]
        except ValueError:
            return None
    

locations = list(fines["location_text"])

identified = 0
for location in locations:
    was_identified = False
    #bring input into a uniform format and split into components
    components = location.lower().split()
    
    major_part = []
    relation = ""
    minor_part = []

    for i in range(0, len(components)):
        component = components[i]
        if component in ["ggü.", "vor", "neben", "ecke", "gegenüber", "haltestelle", "laterne", "hinter"]:
            if component == "ggü." or component == "gegenüber":
                relation = "ggü."
            elif component == "neben" or component == "hinter":
                relation = "vor"
            else:
                relation = component
                
            minor_part = components[i+1:]
            break
        elif parse_street_no(component) != None:
            relation = "number"
            minor_part = component
            break
        else:
            major_part.append(component)
            
    street_name = ""
    street_no = 0
            
    if relation == "number":
        street_name = " ".join(major_part)
        street_no = parse_street_no(minor_part)
        was_identified = True
    
    elif relation == "vor":
        if "haus-nr." in minor_part and parse_street_no(minor_part[-1]):
            street_name = " ".join(major_part)
            street_no = parse_street_no(minor_part[-1])
            was_identified = True
            
    elif relation == "ggü.":
        if "haus-nr." in minor_part and parse_street_no(minor_part[-1]):
            street_name = " ".join(major_part)
            street_no = parse_street_no(minor_part[-1])
            was_identified = True
    
    # street crossings are disabled for now, but are an opportnunity for improvement in the future
    #elif relation == "ecke":
    #    if len(minor_part) == 1:
    #        street_name = " ".join(major_part)
    #        minor_street_name = minor_part[0]
    #        was_identified = True
            
    
    if was_identified:
        identified += 1
        #print(street_name + " " + str(street_no))
    else:
        print(str(major_part) + "/" + relation + "/" + str(minor_part))
      
        
#performance: 0.8083
print(identified / len(locations))
