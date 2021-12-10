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

#exploration
#print([i for i in list(fines["location_text"].str.contains("bla")) if i != False])

#print(len(fines))
#print(len(fines[fines["location_text"].str.contains("Haus-Nr.")]))
    
#print(fines.head())

def parse_street_no(number):

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
            return [int(components[1])]
        except ValueError:
            return None
    

locations = list(fines["location_text"])

identified = 0
for location in locations:
    #bring input into a uniform format and split into components
    components = location.lower().split()
    
    #sometimes the oprators write the streetname in two words
    #special exception for streets starting with "am" or "im"
    if len(components) > 1 and components[1] in ["straße", "gässchen", "weg", "gasse"] or components[0] == "im" or components[0] == "am":
        components = ["".join([components[0], components[1]])] + components[2:]
    
    #check locations of the form: "streetname streetnumber"
    if len(components) == 1:
        if ("straße" in components[0]) or ("weg" in components[0]) or ("gasse" in components[0]) or ("gässchen" in components[0]):
            streetname = components[0]
            identified += 1
            
    elif len(components) == 2:
        street_no = parse_street_no(components[1])

        if street_no != None:
            streetname = components[0] #CAKE remove ,
            identified += 1
    elif len(components) == 4:
        if ("ggü." in components or "gegenüber" in components) and "haus-nr." in components:
            street_no = parse_street_no(components[3])
            if street_no != None:
                streetname = components[0] #CAKE remove ,
                identified += 1
            continue
        elif "neben" in components and "haus-nr." in components:
            street_no = parse_street_no(components[3])
            if street_no != None:
                streetname = components[0] #CAKE remove ,
                identified += 1
            continue
        elif "vor" in components and "haus-nr." in components:
            street_no = parse_street_no(components[3])
            if street_no != None:
                streetname = components[0] #CAKE remove ,
                identified += 1
            continue
    else:
        print(components)
        
#performance: 0.449
print(identified / len(locations))
