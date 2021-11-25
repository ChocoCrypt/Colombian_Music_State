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
#pendiente a quitar comentarios
'''
inertias = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(vectores)
    inertia = kmeans.inertia_
    print(f"la inercia de {i} cortes en Kmeans es de {inertia}")
    inertias.append(inertia)

x = [i for i in range(1,15)]
y = inertias
'''


#sns.lineplot(x = x , y = y)
#plt.show()
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
for i in range(0,len(artistas), 15):
    plt.text(vxl[i] +0.2 , vyl[i]+0.2 , artistas[i])
plt.title('Grafica de Custering de artistas según reducción de la dimensionalidad de sus canciones')
plt.xlabel("x1 reducción de PCA")
plt.ylabel("x2 reducción de PCA")
sns.scatterplot(x = vx , y = vy , hue = labels)
plt.show()
plt.savefig("clusters_segun_sonido.png" , dpi= 96*10)


'''
como ya hay 3 clusters establecidos, voy a ver la bailabilidad de cada cluster para
'''

dfs = [datos.loc[datos['labels']==i] for i in range(cantidad_clusters)]
#calculo las medias de popularidad
medias_popularidad = [np.mean(i["popularity_mean"]) for i in dfs]
print(medias_popularidad)

#calculo las medias de bailabilidad
medias_tiempo = [np.mean(i["time_mean"]) for i in dfs]
print(medias_tiempo)

medias_energia = [np.mean(i["energy_mean"]) for i in dfs]
print(medias_energia)


for i in datos.columns[133:]:
    mean_cluster = [np.mean(j[i]) for j in dfs]
    if(np.var(mean_cluster)>1):
        print(f"{i}:  {mean_cluster} , {np.var(mean_cluster)}")
#df0 = datos.loc[datos['labels'] == 0]
#df1 = datos.loc[datos['labels'] == 1]
#df2 = datos.loc[datos['labels'] == 2]
#df3 = datos.loc[datos['labels'] == 4]

#bailabilidad_df0 = df0["popularity_mean"]
#bailabilidad_df1 = df1["popularity_mean"]
#bailabilidad_df2 = df2["popularity_mean"]
#bailabilidad_df3 = df3["popularity_mean"]






