import glob
import seaborn as sns
import librosa
from sklearn import preprocessing
from sklearn import utils
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# resume file de la carpeta de recolectar youtube para poder medir los espectrogramas
def get_resume_of_file(filepath, k_values):
    # reading files with librosa
    samples, sampling_rate = librosa.load(filepath)
    # creating spectrogram
    sgram = librosa.stft(samples)
    # generating mel spectrogram
    sgram_mag, _ = librosa.magphase(sgram)
    mel_scale_sgram = librosa.feature.melspectrogram(S=sgram_mag, sr=sampling_rate)
    # re scaling mel pectrograms with PCA
    pca = PCA(
        n_components=k_values
    )  #    IMPORTANTE QUE ACA SE DECIDE CUANTOS VECTORES VAMOS A TENER
    pca.fit(mel_scale_sgram)
    values = pca.singular_values_
    print(values)
    return values


# se leen los datos
datos = pd.read_csv("completoSinRep.csv")
# pendiente a hacer inputting
for i in datos.columns:
    datos = datos.dropna(subset=[i])

artistas = [i for i in datos["artist"]]
vx = datos["x1_graphics"]
vy = datos["x2_graphics"]
vxl = [i for i in datos["x1_graphics"]]
vyl = [i for i in datos["x2_graphics"]]

# estos son los vectores descriptivos de la canción
vectores_descriptivos = [
    datos.iloc[i, 5:133].to_numpy() for i in range(len(datos["artist"]))
]


popularidades = datos["popularity_mean"]
media_popularidades = np.mean(popularidades)
max_popularidades = np.max(popularidades)
min_popularidades = np.min(popularidades)
print(
    f"popularidades:\nmedia={media_popularidades} , max={max_popularidades} , min={min_popularidades}"
)

# voy a definir a los artistas populares como los artistas que están sobre la
# media de la popularidad, sin embargo esto es una desición polémica pues para
# decir que alguien es popular se podría usar alguna otra métrica
artistas_populares = datos.loc[datos["popularity_mean"] > media_popularidades]
artistas_impopulares = datos.loc[datos["popularity_mean"] < media_popularidades]

# ahora calculo las matrices de los sonidos de los artistas populares según su sonido
vectores = [datos.iloc[i, 5:133].to_numpy() for i in range(len(datos["artist"]))]

vectores_artistas_populares = [
    datos.iloc[i, 5:133].to_numpy() for i in range(len(artistas_populares["artist"]))
]

vectores_artistas_impopulares = [
    datos.iloc[i, 5:133].to_numpy() for i in range(len(artistas_impopulares["artist"]))
]

vectores = np.array(vectores)
vectores_artistas_populares = np.array(vectores_artistas_populares)
vectores_artistas_impopulares = np.array(
    vectores_artistas_impopulares[0 : len(vectores_artistas_populares)]
)


# print(vectores_artistas_populares.shape)
# print(vectores_artistas_impopulares.shape)
popularidades = []
for i in datos["popularity_mean"]:
    popularidades.append(i)
popularidades = np.array(popularidades)
# toca preprocesar las popularidades para debuguear esto
lab_enc = preprocessing.LabelEncoder()
popularidades = lab_enc.fit_transform(popularidades)
# popularidades = np.array([i for i in range(len(vectores))])
# hacemos una regresión logistica para predecir si un artista es popular o no

print("running LogisticRegression regression")
lgreg = LogisticRegression()
lgreg.fit(vectores, popularidades)

reg_proms = []
for i in range(len(artistas)):
    intento = lgreg.predict(vectores[i].reshape(1, -1))[0]
    reg_proms.append(intento)

reg_proms_mean = np.mean(reg_proms)


print("running rdforest")
rdforest = RandomForestClassifier()
rdforest.fit(vectores, popularidades)

# ahora voy a poner 2 canciones , una famosa y otra no, y ver como predice su popularidad
means = []
for i in range(len(artistas)):
    pred = rdforest.predict(vectores[i].reshape(1, -1))[0]
    means.append(pred)
    print(pred, artistas[i])


pop_media = np.mean(means)
print(pop_media)

# ============================================

# valores_pepas = get_resume_of_file("pepas.mp3" , 128)
# valores_tambor = get_resume_of_file("tambor.mp3" , 128)
# valores_despacito = get_resume_of_file("despacito.mp3" , 128)
# pred_pepas = rdforest.predict(valores_pepas.reshape(1,-1))
# pred_tambor = rdforest.predict(valores_tambor.reshape(1,-1))
# pred_despacito = rdforest.predict(valores_despacito.reshape(1,-1))
# #HACER HISTOGRAMA DE ESTOS VALORES Y AÑADIR MAS VIDEOS DE YOUTUBE
#
#
# print(f"popularidad:\nde pepas:{pred_pepas} , prediccion de tambor:{pred_tambor} , prediccion de despacito:{pred_despacito}")


"""
esto aguantaba implementarlo para la regresion lineal pero al final no funciona
y solo funciona rdforest, el cual funciona bien
"""
# pred_pepas = lgreg.predict(valores_pepas.reshape(1,-1))
# pred_tambor = lgreg.predict(valores_tambor.reshape(1,-1))
# pred_despacito = lgreg.predict(valores_despacito.reshape(1,-1))
# print(f"para regresion_logistica: pepas:{pred_pepas} , tambor:{pred_tambor} , despacito:{pred_despacito}")

# lista = pd.DataFrame(lista)

# ====== Creación de DF para varios artistas:

nuevas = glob.glob("./newQuery/*")

# nuevas = ["pepas.mp3", "tambor.mp3", "despacito.mp3"]

res = {a: get_resume_of_file(a, 128) for a in nuevas}


complete = [
    {
        "Canción": r,
        "forest": f"{rdforest.predict(res[r].reshape(1,-1))}",
        "lr": f"{lgreg.predict(res[r].reshape(1,-1))}",
    }
    for r in res.keys()
]

df = pd.DataFrame.from_dict(complete)
print(df.to_markdown())


# forest = {
#     r:f"{rdforest.predict(res[r].reshape(1,-1))}" for r in res.keys()
# }
#
# logreg = {
#     r:f"{lgreg.predict(res[r].reshape(1,-1))}" for r in res.keys()
# }


# print( sns.load_dataset("penguins"))
#
#
# from pprint import pprint
#
# forest = [
#     {"Canción":"Luis Fonsi - Despacito ft. Daddy Yankee", "Indice de popularidad":123},
#     {"Canción":"Farruko - Pepas", "Indice de popularidad":96},
#     {"Canción":"N Hardem - Tambor", "Indice de popularidad":0},
# ]
#
# logreg = [
#     {
#         "Canción": "Luis Fonsi - Despacito ft. Daddy Yankee",
#         "Indice de popularidad":0
#     },
#     {"Canción": "Farruko - Pepas", "Indice de popularidad":0,},
#     {"Canción": "N Hardem - Tambor", "Indice de popularidad":82,}
# ]
#
# sns.set(style="darkgrid")
#
# dt = pd.DataFrame(forest)
#
# print( dt )
# sns.barplot(dt)
#
#
# plt.show()


pprint(forest)
pprint(logreg)
