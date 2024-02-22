# PNRR NEST T8.4.7 - UNICA Repository (README)

This repository includes a set of QGIS graphical models allowing an automatic execution of pre-processing operations on open GIS datasets (concerning a selected study area in Cagliari, Italy) to generate a suitable input file for an EUReCA-based UBEM

### Get QGIS input datasets
From the folder *Cagliari*, extract *CagliariSampleInputs.rar*. This archive holds GIS input layers concerning the selected study area in Cagliari (Italy). The input included in this precompilated project are open data sources, similar to those used in the Padova project, that can be freely downloaded. In particular the data sources are: 

1. ISTAT census sections (shapefile can be found under the section **Basi territoriali - dati definitivi (1991-2011)**) [ISTAT website](https://www.istat.it/it/archivio/104317#accordions)
2. ISTAT census indicators (csv file can be found under the section **Variabili censuarie (1991-2011)**) [ISTAT website](https://www.istat.it/it/archivio/104317#accordions)
3. Geo-Topographic Database (GTDB) of Sardinian cities (shape files of the city of Cagliari can be freely downloaded by clicking on the *CAGLIARI* archive) [Sardinia Geoportal](https://www.sardegnageoportale.it/index.php?xsl=2420&s=40&v=9&c=95648&na=1&n=10&esp=1&tb=14401)

*Note that only two layers (called CLASSES) of the Cagliari GTDB, both concerning buildings, are involved in the proposed workflow: the 'Volume Unit' class (Layer name: "**ST02TE01CL01**"), the 'Building Unit' class (Layer name: "**ST02TE01CL02**").

### Open QGIS project
Open the QGIS project 'Project_Cagliari_StudyArea.qgz' with loaded GIS input layers related to Cagliari study area
> Cagliari/Project_Cagliari.qgz

### Add custom functions to the QGIS profile

The QGIS model uses some custom functions that need to be added to your QGIS Profile. 

Follow the steps below:
1. go to the repository folder 'QGIS_PythonFunctions'
    > Repository_UNICA/QGIS_PythonFunctions/
2. Copy each python file (*files ending with '.py'*)
3. Open the folder 'expressions' through the following path from QGIS
   > Menu bar -> Setting -> User Profiles -> Open active profile folder -> python -> expressions
5. Paste the items from step 2 in this folder.

### Open the QGIS Graphical Model inside QGIS
Follow the path below
> Menu bar -> Processing -> Model Designer -> Open Model

and select the file 'WORKFLOW_UNICA.model3' included in the repository

> Repository_UNICA/QGIS_GraphicalModels/WORKFLOW_UNICA.model3

### Run the QGIS Graphical Model
1. Get sure you have an active internet connection
2. Assign the input layers properly to te respective input nodes of the graphical model 'WORKFLOW_UNICA.model3'
3. Click on 'Run Model'.


