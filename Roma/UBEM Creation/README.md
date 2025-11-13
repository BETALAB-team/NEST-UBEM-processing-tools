# PNRR NEST T8.4.7 - UNINA Case study 

This repository includes a set of QGIS graphical models allowing an automatic execution of pre-processing operations on open GIS datasets (concerning a selected study area in Roma, Italy) to generate a suitable input file for an EUReCA-based UBEM

### Get QGIS input datasets
From the folder *Roma*, extract *RomaSampleInputs/Data.zip*. This archive holds GIS input layers concerning the selected study area in Roma (Italy). The input included in this precompilated project are open data sources, similar to those used in the Padova project, that can be freely downloaded. In particular the data sources are: 

1. Geo-Topographic Database (GTDB) of cities of Lazio Region (shape files of the city of Roma can be freely downloaded by clicking on the *DBT_Lazio_RM* archive) [Regione Lazio Open Data](http://dati.lazio.it/catalog/it/dataset/2014-carta-tecnica-regionale-numerica-scala-1-5-000-provincia-di-roma)

*Note that only two layers (called CLASSES) of the Roma GTDB, both concerning buildings, are involved in the proposed workflow: the 'Building Unit' class (Layer name: "**EDIFC**"), the 'Building Use' class (Layer name: "**EDIFC_EDIFC_USO**"), the 'Building Name' class (Layer name: "**EEDIFC_EDIFC_NOME_T**"),

### Open QGIS project
Open the QGIS project 'Project_Roma_StudyArea.qgz' with loaded GIS input layers related to Roma study area
> Roma/Project_Roma.qgz

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