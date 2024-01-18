# NEST PNRR task 8 4 7 repository

This repository is a set of QGIS functions to process national GIS dataset to create the input file for a UBEM

Steps to run the processor:

### 1.Download the repository

Download the repository to your local storage either using the zip file

> Code -> Download ZIP

or directly cloning the repository.

> git clone https://github.com/BETALAB-team/PNRR_847_GIS_workflow.git

*Note: If you download the file as a zip file, you should first extract it.
 

### 2. Get the Inputs Ready

The project needs four input files. 

1. Census tract shapefile for the desired region. This data is downloadable from [link](https://www.istat.it/it/archivio/104317#accordions "the ISTAT website.")

The shapefile can be found under the section "**Basi territoriali - dati definitivi (1991-2011)**"

2. Census tract indicators, which is a csv file that can be found in the [link](https://www.istat.it/it/archivio/104317#accordions "same link").

This file can be found under the section "**Variabili censuarie (1991-2011)**"

3. Height data from national geoportal. This data is a wfs data that can be queried with the following link:

> http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/wfs/Edifici.map&

4. Shapefile defining the borders of the desired area. This shapefile can be made using basic polygons in the QGIS. 

*Note: You can see a sample input in the zip file located at the "Example_Padova" folder*

**If you are using the case of Padova, you just need to extract the zip file that is located in**

> Example_Padova\Data.zip


### 3. Open QGIS project

Open the project file 

> Project\Project.qgz

Or if you want to use the Padova case, open the respective file from:

> Example_Padova\Padova_Project.qgz


### 4. Add required functions to the QGIS profile

The required functions for this project are located in 
 
> .\Functions\

Copy all of the python files (*files ending with '.py'*)

In the QGIS software, in the menu bar open the active profile folder

> Menu ribbon -> Setting -> User Profiles -> Open active profile folder

In the opened folder, go to the following path:

> .\python\expressions\

Paste the items you had copied in this folder.

### 5. Run the project

Make sure to have an active internet connection.

In the QGIS project file, from the toolbox, open the process named "WORKFLOW". It is found in:

> Processing Toolbox -> Project models -> WORKFLOW

Add the input files to the respective field. 

Click on the Run
