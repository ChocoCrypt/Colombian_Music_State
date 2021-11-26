import seaborn as sns
from sklearn.cross_decomposition import CCA
from sklearn.linear_model import LinearRegression
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
    datos.iloc[i,5:133].to_numpy() for i in range(len(datos["artist"]))
]
vectores = np.array(vectores)
popularidades = np.array([float(i) for i in datos["popularity_mean"]])


#intento
#x = np.array([np.mean(x) for x in vectores])


err = 0
descriptors = []
for i in datos["song_descriptor"]:
    print(type(i))
    try:
        print(float(i))
        descriptors.append(float(i))
    except:
        err += 1

x = np.array(descriptors)
y = np.array(popularidades[1:])

x = np.array([x for x in datos["x1_graphics"]])
y = np.array(popularidades)

print(x.shape , y.shape)


sns.set_style("darkgrid")
plt.title("Correlación entre popularidad y sonido de la banda")
plt.xlabel("Sonido descriptivo de la banda")
plt.ylabel("Popularidad de la banda")
sns.regplot(x = x, y=y)
plt.show()
plt.savefig("correlation.png")
