# ODA Parken

A project exploring the datasets of parking fines that are provided by the city of Aachen through its open data portal: https://offenedaten.aachen.de.

### The Data
Currently there are two datasets of parking fines available in  the open data portal:

- 2019 [.xls](https://offenedaten.aachen.de/dataset/verwarn-und-bussgelder-ruhender-verkehr-2019)
- 2020 [.csv](https://offenedaten.aachen.de/dataset/verwarn-und-bussgelder-ruhender-verkehr-parkverstoesse-2020)

## How-To: Locations

In order to convert the textual descriptions of the fine locations into standardized addresses and coordinates, follow the steps below.

1. Download the datasets that you are interested in from the portal (e.g. using the links above) and copy them to the `data` folder.
2. Download the OSM data for Aachen (for example using [bbbike.org](https://extract.bbbike.org/)) and put the OSM XML file, named `aachen.osm`, into the `data` folder.
2. Rename the files using the format: `fines_YYYY.csv` where `YYYY` corresponds to the year.
3. Convert _.xls_ files to _.csv_ with the following columns: | Tattag | Zeit | Tatort 2 | Tatbestand |Geldbuße |
4. Insert the wanted years to the _years_ list in the beginning of the `preprocessing/infer_locations.py` script.
5. Run the `infer_locations.py` script in the `preprocessing` folder.

## Notes

- Two  datasets from 2019 and 2020
- No exact location information, only free form text entry
- Dates in 2019 dataset are in an unclear format (maybe days since reference date)
- You can find a translation of the _Tatbestand_ column at the [KBA](https://www.kba.de/DE/Themen/ZentraleRegister/FAER/BT_KAT_OWI/bkat_owi_09_11_2021_gezippt.html).

## Licenses

The fines data is licensed under the [Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0), but is not included in this repository, download the data yourself from the open data portal.

The geocoding is based on an updated and modified version of the [osmgeocode.py](https://github.com/brianw/osmgeocode) script by _brianw_. The original script is itself based on the [osm.py](https://github.com/bmander/graphserver/tree/master) script by Brandon Martin-Anderson which is available under the BSD license.

