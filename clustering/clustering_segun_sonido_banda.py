from sklearn.cluster import KMeans
import seaborn as sns
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
vectores = [
    datos.iloc[i,5:133].to_numpy() for i in range(len(datos["artist"]))
]


#se calculan las inercias para ver cual es el corte que se necesita
"""
inertias = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(vectores)
    inertia = kmeans.inertia_
    print(f"la inercia de {i} cortes en Kmeans es de {inertia}")
    inertias.append(inertia)

x = [i for i in range(1,15)]
y = inertias

sns.set_style("darkgrid")
plt.title("Inercias de distintos valores de Kmeans")
plt.xlabel("Cantidad de clusters")
plt.ylabel("Inercia")
sns.lineplot(x = x , y = y)
plt.savefig("Inercias_kmeans_sonido_banda.png")
"""

'''
se puede apreciar por la ley del codo que el corte de clusters mas adecuado es
3 clusters, esto quiere decir que hay 3 tipos de bandas diferentes
'''


cantidad_clusters = 3
kmeans = KMeans(n_clusters = cantidad_clusters)
kmeans.fit(vectores)
labels = kmeans.predict(vectores)


datos['labels'] = labels

print(datos["popularity_mean"])

#uno de los problemas es que al poner estos labels por alguna razón se daña el darkgrid de seaborn

sns.set_style("darkgrid")
for i in range(0,len(artistas), 20):
    plt.text(vxl[i] +0.2 , vyl[i]+0.2 , artistas[i])
plt.title('Grafica de Custering de artistas según reducción de la dimensionalidad de sus canciones')
plt.xlabel("x1 reducción de PCA")
plt.ylabel("x2 reducción de PCA")
sns.scatterplot(x = vx , y = vy , hue = labels)
plt.show()
plt.savefig("clusters_segun_sonido.png")



#calculo las medias segun categorías en spotify
dfs = [datos.loc[datos['labels']==i] for i in range(cantidad_clusters)]
for i in datos.columns[133:]:
    mean_cluster = [np.mean(j[i]) for j in dfs]
    if(np.var(mean_cluster)>1):
        print(f"{i}:  {mean_cluster} , {np.var(mean_cluster)}")




