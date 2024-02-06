# PNRR T8.4.7 - UNICA Repository (README)

This repository includes a set of QGIS graphical models allowing an automatic execution of pre-processing operations on open GIS datasets (concerning a selected study area in Cagliari, Italy) to generate a suitable input file for an EUReCA-based UBEM

### 1. Download the folder ‘Repository_UNICA’ and extract the data
Download the repository to your local storage and extract the related data if included in a compressed folder

> Code -> Download ZIP

### 2. Get QGIS input datasets
Extract QGIS input layers from the folder ‘QGISProject_CagliariInputData.rar’ holding GIS input layers concerning the selected study area in Cagliari (Italy)
> Repository_UNICA/QGIS_Project/QGISProject_CagliariInputData.rar

*Note that all input datasets are freely available on the following data sources:
1. ISTAT census sections (shapefile can be found under the section "**Basi territoriali - dati definitivi (1991-2011)**") [ISTAT website](https://www.istat.it/it/archivio/104317#accordions)
2. ISTAT census indicators (csv file can be found under the section "**Variabili censuarie (1991-2011)**") [ISTAT website](https://www.istat.it/it/archivio/104317#accordions)
3. Geo-Topographic Database (GTDB) of Sardinian cities (shape files of the city of Cagliari can be freely downloaded by clicking on 'CAGLIARI.zip'*) [Sardinia Geoportal](https://www.sardegnageoportale.it/index.php?xsl=2420&s=40&v=9&c=95648&na=1&n=10&esp=1&tb=14401)

*Note that only two layers (called CLASSES) of the Cagliari GTDB, both concerning buildings, are involved in the proposed workflow: the 'Volume Unit' class (Layer name: "**ST02TE01CL01**"), the 'Building Unit' class (Layer name: "**ST02TE01CL02**").

### 3. Open QGIS project
Open the QGIS project 'Project_Cagliari_StudyArea.qgz' with loaded GIS input layers related to Cagliari study area
> Repository_UNICA/QGIS_Project/Project_Cagliari_StudyArea.qgz

### 4. Install QuickOSM
Get sure to have properly installed the open-source plugin for QGIS 'QuickOSM' to access OpenStreetMap open datasets

### 5. Add custom functions to the QGIS profile

The QGIS model uses some custom functions that need to be added to your QGIS Profile. 

Follow the steps below:
1. go to the repository folder 'QGIS_PythonFunctions'
    > Repository_UNICA/QGIS_PythonFunctions/
2. Copy each python file (*files ending with '.py'*)
3. Open the folder 'expressions' through the following path from QGIS
   > Menu bar -> Setting -> User Profiles -> Open active profile folder -> python -> expressions
5. Paste the items from step 2 in this folder.

### 6. Open the QGIS Graphical Model inside QGIS
Follow the path below
> Menu bar -> Processing -> Model Designer -> Open Model

and select the file 'WORKFLOW_UNICA.model3' included in the repository

> Repository_UNICA/QGIS_GraphicalModels/WORKFLOW_UNICA.model3

### 7. Run the QGIS Graphical Model
1. Get sure you have an active internet connection
2. Assign the input layers properly to te respective input nodes of the graphical model 'WORKFLOW_UNICA.model3'
3. Click on 'Run Model'.


