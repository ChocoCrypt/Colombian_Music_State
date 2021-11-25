from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#se leen los datos
datos = pd.read_csv("completoSinRep.csv")[0:100]
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
inertias = []
for i in range(1, 15):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(vectores)
    inertia = kmeans.inertia_
    print(f"la inercia de {i} cortes en Kmeans es de {inertia}")
    inertias.append(inertia)

x = [i for i in range(1,15)]
y = inertias


#sns.lineplot(x = x , y = y)
#plt.show()
'''
se puede apreciar por la ley del codo que el corte de clusters mas adecuado es
3 clusters, esto quiere decir que hay 3 tipos de bandas diferentes
'''


kmeans = KMeans(n_clusters = 3)
kmeans.fit(vectores)
labels = kmeans.predict(vectores)



#uno de los problemas es que al poner estos labels por alguna razón se daña el darkgrid de seaborn
for i in range(len(artistas)):
    plt.text(vxl[i] +0.2 , vyl[i]+0.2 , artistas[i])

sns.set_style("darkgrid")
plt.title('Grafica de Custering de artistas')
plt.xlabel("x1 reducción de PCA")
plt.ylabel("x2 reducción de PCA")
sns.scatterplot(x = vx , y = vy , hue = labels)
plt.show()
plt.savefig("clusters.png")
