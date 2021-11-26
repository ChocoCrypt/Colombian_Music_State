import seaborn as sns
from sklearn import preprocessing
from sklearn import utils
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#se leen los datos
datos = pd.read_csv("completoSinRep.csv")
#pendiente a hacer inputting
for i in datos.columns:
    datos = datos.dropna(subset=[i])

artistas = [i for i in datos["artist"]]
vx = datos["x1_graphics"]
vy = datos["x2_graphics"]
vxl = [i for i in datos["x1_graphics"]]
vyl = [i for i in datos["x2_graphics"]]

#estos son los vectores descriptivos de la canción
vectores_descriptivos = [
    datos.iloc[i,5:133].to_numpy() for i in range(len(datos["artist"]))
]


popularidades = datos["popularity_mean"]
media_popularidades = np.mean(popularidades)
max_popularidades = np.max(popularidades)
min_popularidades = np.min(popularidades)
print(f"popularidades:\nmedia={media_popularidades} , max={max_popularidades} , min={min_popularidades}")

#voy a definir a los artistas populares como los artistas que están sobre la
#media de la popularidad, sin embargo esto es una desición polémica pues para
#decir que alguien es popular se podría usar alguna otra métrica
artistas_populares = datos.loc[datos["popularity_mean"]>media_popularidades]
artistas_impopulares = datos.loc[datos["popularity_mean"]<media_popularidades]

#ahora calculo las matrices de los sonidos de los artistas populares según su sonido
vectores = [
    datos.iloc[i,5:133].to_numpy() for i in range(len(datos["artist"]))
]

vectores_artistas_populares = [
    datos.iloc[i,5:133].to_numpy() for i in range(len(artistas_populares["artist"]))
]

vectores_artistas_impopulares = [
    datos.iloc[i,5:133].to_numpy() for i in range(len(artistas_impopulares["artist"]))
]

vectores = np.array(vectores)
vectores_artistas_populares = np.array(vectores_artistas_populares)
vectores_artistas_impopulares = np.array(vectores_artistas_impopulares[0:len(vectores_artistas_populares)])


#print(vectores_artistas_populares.shape)
#print(vectores_artistas_impopulares.shape)
popularidades = []
for i in datos["popularity_mean"]:
    popularidades.append(i)
popularidades = np.array(popularidades)
#toca preprocesar las popularidades para debuguear esto
lab_enc = preprocessing.LabelEncoder()
popularidades = lab_enc.fit_transform(popularidades)
#popularidades = np.array([i for i in range(len(vectores))])
#hacemos una regresión logistica para predecir si un artista es popular o no

print("running LogisticRegression regression")
lgreg = LogisticRegression()
lgreg.fit(vectores ,popularidades )

print("running rdforest")
rdforest = RandomForestClassifier()
rdforest.fit(vectores , popularidades)



