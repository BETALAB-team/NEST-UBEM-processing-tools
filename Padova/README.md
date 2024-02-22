# Create Padova's UBEM

Inside the *Padova/PadovaSampleInputs.zip* archive, you can find the starting data to run the Padova project. The project needs four input files. 

1. Census tract shapefile for the desired region. This data is downloadable from the [ISTAT](https://www.istat.it/it/archivio/104317#accordions) website. 
The shapefile can be found under the section **Basi territoriali - dati definitivi (1991-2011)**

1. Census tract indicators, which is a csv file that can be found in the same [link](https://www.istat.it/it/archivio/104317#accordions). 
This file can be found under the section **Variabili censuarie (1991-2011)**

1. Height data from national geoportal. This data is a wfs data that can be queried with this [link]( http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/wfs/Edifici.map&).

2. A shapefile defining the borders of the desired area. This shapefile can be made using basic polygons in the QGIS. 

*Note: You can see a sample input in the zip file located at the "Example_Padova" folder*

**If you are using the case of Padova, you just need to extract the zip file that is located in**

> Example_Padova\Data.zip


### 3. Open QGIS project

Open the project file 

> Project\Project.qgz

Or if you want to use the Padova case, open the respective file from:

> Example_Padova\Padova_Project.qgz

*If when the project is opened you get a security warning* <span style="background-color: #fcb103; color: black; padding: 3px;">**Security Warning:** Python macros cannot currently be run</span>, *make sure to click on the "enable macros" option*

### 5. Run the project

Make sure to have an active internet connection.

In the QGIS project file, from the toolbox, open the process named "WORKFLOW". It is found in:

> Processing Toolbox -> Project models -> WORKFLOW

Add the input files to the respective field. 

Click on the Run