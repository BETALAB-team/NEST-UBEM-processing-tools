# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:06:25 2024

@author: khaje
"""
# Libraries
import pandas as pd
import geopandas as gpd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")
# from hopkins import hopkins
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score,pairwise_distances

#functions
def width(geometry):
    minx=geometry.bounds[0]
    miny=geometry.bounds[1]
    maxx=geometry.bounds[2]
    maxy=geometry.bounds[3]
    wid=np.sqrt((maxx-minx)**2+(maxy-miny)**2)
    return wid

#function to find optimal cluster numbers
def find_elbow_point(data, max_clusters=10):
    inertias = []

    for i in range(1, max_clusters+1):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    # Calculate the differences in consecutive inertias
    diff = np.diff(inertias)

    # Calculate the second derivative of the differences
    diff2 = np.diff(diff)

    # Find the index of the maximum value of the second derivative
    elbow_index = np.where(diff2 == max(diff2))[0][0]

    return elbow_index + 1  # Add 2 because indexing starts from 0
def representative_distances(X, labels, centroids):
    # Calculate pairwise distances between data points and centroids
    distances = pairwise_distances(X, centroids[labels])
    
    return distances

# Directories
current_dir = os.path.dirname(os.path.realpath(__file__))
main_dir=os.path.abspath(os.path.join(current_dir, ".."))
geojson_path = os.path.join(main_dir, "eureca_ubem", "Input","geojson","Buildings_summary.geojson")

# Load the file
Geojson=gpd.read_file(geojson_path)
Data=Geojson.copy()
Data=Data[["SEZIONE","End Use","Height","Envelope","id","Zone volume [m3]","Zone net floor area [m2]","geometry"]]
Data["perimeter"]=Data["geometry"].length
Data['width'] = Data['geometry'].apply(lambda geom: width(geom))
Data["area"]=Data["geometry"].area
Data["non_scaled_volume"]=Data["area"]*Data["Height"]
Data["scale"]=np.sqrt(Data["Zone volume [m3]"]/Data["non_scaled_volume"])
Data["width"]=Data["width"]/Data["scale"]
Data["footprint"]=Data["area"]/(Data["scale"]**2)
Data["perimeter"]=Data["perimeter"]/Data["scale"]
Data["x"]=Data["geometry"].centroid.x
Data["y"]=Data["geometry"].centroid.y
# Preprocess data
Data["x"] = 10*(Data["x"] - Data["x"].min()) / (Data["x"].max() - Data["x"].min())
Data["y"] = 10*(Data["y"] - Data["y"].min()) / (Data["y"].max() - Data["y"].min())
Data.drop(["geometry","area","non_scaled_volume","scale"],axis=1,inplace=True)
Data["End Use"], labels_enduse=pd.factorize(Data["End Use"])
Envelope_map={"1991-2000":1995,
              "After 2010":2015,
              "2000-2005":2003,
              "1981-1990":1985,
              "1971-1980":1975,
              "1930-1945":1938,
              "Before 1930":1915,
              "1945-1960":1953,
              "1961-1970":1965}

Data["year"]=Data["Envelope"].map(Envelope_map)
Data["year"] = 10*(Data["year"] - Data["year"].min()) / (Data["year"].max() - Data["year"].min())
Data.drop("Envelope",axis=1,inplace=True)
Data.rename(columns={'Zone volume [m3]': 'volume'}, inplace=True)
Data.rename(columns={'Zone net floor area [m2]': 'area'}, inplace=True)
Data.rename(columns={'Height': 'height'}, inplace=True)
Data.rename(columns={'End Use': 'enduse'}, inplace=True)
# # sns.heatmap(Data.corr(),cmap="Spectral",annot=True)
# # There is high correlation between shape values
Data["shape"]=(2*Data["footprint"]+Data["height"]*Data["perimeter"])/Data["volume"]
Data["aspect"]=Data["height"]/Data["width"]
Data["footprint"] = 10*(Data["footprint"] - Data["footprint"].min()) / (Data["footprint"].max() - Data["footprint"].min())
Data.drop(["height","volume","area","perimeter","width"],inplace=True,axis=1)

# Define the number of clusters based on the desired group size
number_inert=list()
silhouettes=list()
num_clusters=[220]
for n in num_clusters:
    print(n)
    desired_group_size = n
    n_clusters = n

    # # Perform kmeans clustering
    # kmm_geometery=KMeans(n_clusters=n_clusters,random_state=42)
    # kmm_geometery.fit(Data[["x","y"]])
    # Data["labels_geom"]=kmm_geometery.labels_
    # num_geom_labels=len(set(kmm_geometery.labels_))

    # # plt.scatter(Data["x"],Data["y"],c=Data["labels_geom"],cmap="Spectral")
    # Datas=pd.DataFrame()
    # Inertias_mean=list()
    # print(1)
    # for i in range(1,num_geom_labels+1):
    #     Check=Data[Data["labels_geom"]==i-1]
    #     length=len(Check)
    #     k=min(desired_group_size,find_elbow_point(Check[["enduse","year","aspect","shape","footprint"]], max_clusters=min(11,length)))
    #     kmm_attributes=KMeans(n_clusters=k,random_state=40)
    #     kmm_attributes.fit(Check[["enduse","year","aspect","shape","footprint"]])
    #     cluster_labels = kmm_attributes.fit_predict(Check[["enduse","year","aspect","shape","footprint"]])
    #     # silhouette_avg = silhouette_score(Check[["enduse","year","aspect","shape","footprint"]], cluster_labels)
    #     Check["categories"]=kmm_attributes.labels_
    #     Datas=pd.concat([Datas,Check])
    #     Inertias_mean.append(kmm_attributes.inertia_)
    #     # sil.append(silhouette_avg)
    
    # # Perform kmeans clustering
    # kmm_geometery=KMedoids(n_clusters=n_clusters,random_state=42)
    # kmm_geometery.fit(Data[["x","y"]])
    # Data["labels_geom"]=kmm_geometery.labels_
    # num_geom_labels=len(set(kmm_geometery.labels_))
    # print(2)
    # # plt.scatter(Data["x"],Data["y"],c=Data["labels_geom"],cmap="Spectral")
    # Datas=pd.DataFrame()
    # Inertias_medoid=list()
    # for i in range(1,num_geom_labels+1):
    #     Check=Data[Data["labels_geom"]==i-1]
    #     length=len(Check)
    #     if(length<3):
    #         k=1
    #     else:
                
    #         k=min(desired_group_size,find_elbow_point(Check[["enduse","year","aspect","shape","footprint"]], max_clusters=min(11,length)))
    #     kmm_attributes=KMeans(n_clusters=k,random_state=40)
    #     kmm_attributes.fit(Check[["enduse","year","aspect","shape","footprint"]])
    #     cluster_labels = kmm_attributes.fit_predict(Check[["enduse","year","aspect","shape","footprint"]])
    #     # silhouette_avg = silhouette_score(Check[["enduse","year","aspect","shape","footprint"]], cluster_labels)
    #     Check["categories"]=kmm_attributes.labels_
    #     Datas=pd.concat([Datas,Check])
    #     Inertias_medoid.append(kmm_attributes.inertia_)
    #     # sil.append(silhouette_avg)
    # print(3)
    Datas=pd.DataFrame()
    Inertias_sezioni=list()
    sezioni=list(set(Data["SEZIONE"]))
    representation={}
    size={}
    clusters={}
    prediction_variables=["year","aspect","shape","footprint"]
    j=0
    for i in sezioni:
        j=j+1
        print(j+1)
        Check=Data[Data["SEZIONE"]==i]
        Predict=Data[prediction_variables]
        length=len(Check)
        if(length<3):
            k=1
        else:
                
            k=min(length,1+find_elbow_point(Check[prediction_variables], max_clusters=min(11,length)))
       
        kmm_attributes=KMeans(n_clusters=k,random_state=40)
        kmm_attributes.fit(Check[prediction_variables])
        labels = np.unique(kmm_attributes.labels_)
        centroids = kmm_attributes.cluster_centers_
        cluster_labels = kmm_attributes.fit_predict(Check[prediction_variables])
        # silhouette_avg = silhouette_score(Check[["enduse","year","aspect","shape","footprint"]], cluster_labels)
        Check["categories"]=kmm_attributes.labels_
        Check["divs"]=sCheck["categories"].astype(str)+Check["enduse"].astype(str)+Check["SEZIONE"].astype(str)
        Check["rep_distance"] = np.min(representative_distances(Check[prediction_variables], labels, centroids),axis=1)
        Datas=pd.concat([Datas,Check])
        distance = np.mean(np.min(representative_distances(Predict, labels, centroids),axis=1))
        # Inertias_sezioni.append(kmm_attributes.inertia_)
        # sil.append(silhouette_avg)
        representation[i]=distance
        size[i]=length
        clusters[i]=k
        # Inertias_sezioni.append(kmm_attributes.inertia_)
        # sil.append(silhouette_avg)

df = pd.DataFrame([representation, size,clusters], index=['representation', 'size','clusters'])
df=df.transpose()

sections=gpd.read_file("sections.geojson")
sorted_df = df.sort_values(by='representation')

best_tracts_geo = sections[sections['SEZ2011'].isin(sorted_df.index)]
merged_df = pd.merge(best_tracts_geo, sorted_df, left_on='SEZ2011', right_index=True, how='left')

merged_df.to_file("represent_wo_enduse.geojson", driver='GeoJSON')


    