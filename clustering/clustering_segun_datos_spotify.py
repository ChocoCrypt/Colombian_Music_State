from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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

#estos son los vectores descriptivos de la canción
vectores = [
    datos.iloc[i,133:].to_numpy() for i in range(len(datos["artist"]))
]
#tengo que hacer PCA para reducir los componentes principales de spotify
vectores_graficas = []
for i in vectores:
    elemento = np.array(i).reshape(-1,2)
    pca = PCA(n_components = 2)
    pca.fit(elemento)
    valores = pca.singular_values_
    vectores_graficas.append(valores)


vx = [i[0] for i in vectores_graficas]
vy = [i[1] for i in vectores_graficas]
vxl = [i[0] for i in vectores_graficas]
vyl = [i[1] for i in vectores_graficas]

#se calculan las inercias para ver cual es el corte que se necesita
inertias = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(vectores)
    inertia = kmeans.inertia_
    print(f"la inercia de {i} cortes en Kmeans es de {inertia}")
    inertias.append(inertia)

x = [i for i in range(1,15)]
y = inertias

"""
sns.set_style("darkgrid")
plt.title("Inercias de distintos valores de Kmeans en spotify")
plt.xlabel("Cantidad de clusters")
plt.ylabel("Inercia")
sns.lineplot(x = x , y = y)
plt.show()
plt.savefig("Inercias_kmeans_spotify.png")
"""

'''
por inercia es evidente que hay 2 clusters, entonces ahora vamos a analizar cada cluster
'''



#si se separa en 2 clusters en todas las variables de spotify se puede ver que
#dan los artistas que o tienen canciones muy largas o solo hacen hits de una cancion
cantidad_clusters = 2
kmeans = KMeans(n_clusters = cantidad_clusters)
kmeans.fit(vectores)
labels = kmeans.predict(vectores)


datos['labels'] = labels

print(datos["popularity_mean"])

#uno de los problemas es que al poner estos labels por alguna razón se daña el darkgrid de seaborn

sns.set_style("darkgrid")
for i in range(0,len(artistas),1):
    plt.text(vxl[i] +0.2 , vyl[i]+0.2 , artistas[i])
plt.title('Grafica de Custering de artistas según reducción de la dimensionalidad de sus canciones')
plt.xlabel("x1 reducción de PCA")
plt.ylabel("x2 reducción de PCA")
sns.scatterplot(x = vx , y = vy , hue = labels)
plt.show()
plt.savefig("clusters_segun_spotify.png")


'''
como ya hay 3 clusters establecidos, voy a ver la bailabilidad de cada cluster para
'''



#calculo las medias segun categorías en spotify
dfs = [datos.loc[datos['labels']==i] for i in range(cantidad_clusters)]
for i in datos.columns[133:]:
    mean_cluster = [np.mean(j[i]) for j in dfs]
    print(f"{i}:  {mean_cluster} , {np.var(mean_cluster)}")



