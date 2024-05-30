# NEST UBEM - Simulation Example

In this folder the required input to run the simulation in the EUReCA environment can be found. In order to proceed with the UBEM simulation, the following steps are needed. 

## Setting Up the EUReCA tool

EUReCA is an open source urban building energy modeling tool developed at the University of Padova. In order to set up and use this tool, first you should download its repository to your local storage from [this link](https://github.com/BETALAB-team/EUReCA). You can do it by downloading the repository as a ZIP file

> Code -> Download ZIP

or you can directly clone the repository using the following git command:

> git clone https://github.com/BETALAB-team/NEST-UBEM-processing-tools.git

*Note: If you download the file as a zip file, you should first extract it.*

### Installing EUReCA into Python
EUReCA is a tool written in the python environment. In order to use this tool, you should have python installed on your system. 
It is recommended to create a new environment particularly for the purpose of working with EUReCA. 
In order to install the EUReCA in the python enviroment you can use the following code in your terminal:
> pip install -e *<path-to-the-repository-folder-in-your-local-storage/eureca-ubem>* 

## Preparing the Inputs
To run a simulation with EUReCA, following files are needed:
 - A `weather_data.epw` weather file. 
 - A `EnvelopeTypes.xlsx` spreadsheet. It includes the thermo-physic properties of building envelopes. 
 - A `Schedules.xlsx` spreadsheet. It includes the operational schedules of occupancy, appliances, temperature, humidity setpoints, HVAC usage for different end-uses. 
 - The `config.json` file, which defines the simulation parameters.
 - The `city.goejson` model. 

 *You can refer to the [EUReCA repository](https://github.com/BETALAB-team/EUReCA) to get more info about these files. 

 The samples for the first four input files can be found in the `InputAux` folder. The geojson of the city is obtainable using the QGIS processing model. A sample of such geojson for the city center of Padova can be found in the `Input Geojson` folder. 

## Running a Simulation

To run a simulation with the EUReCA tool, you should open the `eureca_ubem/input/Main.py` file from the repository. Then, you need to modify the paths to each input file based on your simulation. At this point, you can run the simulation. 

*A sample output of the EUReCA tool using the geojson obtained by the QGIS process models can be found in the `Sample Output` folder.*