# PNRR T8.4.7 - UNICA Repository (README)

This repository includes a set of QGIS graphical models allowing an automatic execution of pre-processing operations on open GIS datasets (concerning a selected study area in Cagliari) to generate a suitable input file for an EUReCA-based UBEM

### 1. Download the folder ‘Repository_UNICA’ and extract the data
Download the repository to your local storage and extract the related data if included in a compressed folder

> Code -> Download ZIP

### 2. Get QGIS input datasets
Extract QGIS input layers from the folder ‘QGISProject_CagliariInputData.rar’ holding GIS input layers concerning the selected Cagliari study area
> Repository_UNICA/QGIS_Project/QGISProject_CagliariInputData.rar

*Note that all input datasets are freely available on the following data sources:
1. ISTAT census sections (shapefile can be found under the section "**Basi territoriali - dati definitivi (1991-2011)**") [ISTAT website] (https://www.istat.it/it/archivio/104317#accordions)
2. ISTAT census indicators (csv file can be found under the section "**Variabili censuarie (1991-2011)**") [ISTAT website] (https://www.istat.it/it/archivio/104317#accordions)
3. Geo-Topographic Database (GTDB) of Sardinian cities (shape files of the city of Cagliari can be freely downloaded by clicking on 'CAGLIARI.zip'*) https://www.sardegnageoportale.it/index.php?xsl=2420&s=40&v=9&c=95648&na=1&n=10&esp=1&tb=14401

*Note that only two layers of the Cagliari GTDB are involved in the proposed workflows: the 'Volume Unit' class (Layer name: "")

### 3. Open QGIS project
Open the QGIS project 'Project_Cagliari_StudyArea.qgz' with loaded GIS input layers related to Cagliari study area
> Repository_UNICA/QGIS_Project/Project_Cagliari_StudyArea.qgz

### 4. Install QuickOSM
Get sure to have properly installed the open-source plugin for QGIS 'QuickOSM' to access OpenStreetMap open datasets


