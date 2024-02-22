# NEST UBEM processing tools

This repository includes a set of QGIS processing models to create UBEM input dataset for a quick simulation in the [EUReCA](https://github.com/BETALAB-team/EUReCA) environment, starting from national GIS datasets. The project has been carried on in the context of the PNRR project NEST, task 8.4.7 (see below for futher information).

### 1. Download the repository

Download the repository to your local storage either using the zip file

> Code -> Download ZIP

or directly cloning the repository.

> git clone https://github.com/BETALAB-team/PNRR_847_GIS_workflow.git

*Note: If you download the file as a zip file, you should first extract it.
 

### 2. Get the Inputs Ready

The project needs four input files. 

1. Census tract shapefile for the desired region. This data is downloadable from [the ISTAT website.](https://www.istat.it/it/archivio/104317#accordions )

The shapefile can be found under the section "**Basi territoriali - dati definitivi (1991-2011)**"

2. Census tract indicators, which is a csv file that can be found in the [same link](https://www.istat.it/it/archivio/104317#accordions).

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

*If when the project is opened you get a security warning* <span style="background-color: #fcb103; color: black; padding: 3px;">**Security Warning:** Python macros cannot currently be run</span>, *make sure to click on the "enable macros" option*

### 4. Make Sure QuickOSM Plugin Is installed

This project uses the QuickOSM plugin to get the data from OpenStreetMap database.

If you have not yet installed this plugin go to the following section from the menu bar:

> Menu ribbon -> Plugin -> Manage and Install Plugins

Here search for the QuickOSM plugin and install it.

### 5. Run the project

Make sure to have an active internet connection.

In the QGIS project file, from the toolbox, open the process named "WORKFLOW". It is found in:

> Processing Toolbox -> Project models -> WORKFLOW

Add the input files to the respective field. 

Click on the Run

## Reference
