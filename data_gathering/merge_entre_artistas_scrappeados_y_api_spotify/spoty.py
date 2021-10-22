import requests
from os import system
import pprint
import datetime
from urllib.parse import urlencode
import base64



class SpotApi:
    """
    DESCRIPCIÓN:
    ----
        Clase para manejar todo lo relacionado con la API de Spotify, desde la
        autentificación hasta los requests para artistas.
    """


    def __init__(self,id_cliente:str,secreto_cliente:str):
        self.id_cliente = id_cliente
        self.secreto_cliente = secreto_cliente
        self.token_acceso = None
        self.token_acceso_vence = datetime.datetime.now()
        self.token_a_vencido = True
        self.token_url = "https://accounts.spotify.com/api/token"


    def obtener_credenciales(self):
        """
        DESCRIPCIÓN:
        ----
            Toma el id_cliente y el secreto_cliente y los transforma en un
            elemento apto para el query.
        RETORNA:
        ----
            string codificado en base64
        """

        if self.id_cliente is None or self.secreto_cliente is None:
            raise Exception("El id_cliente y el secreto_cliente deben ser asignados")

        cli_cred = f"{self.id_cliente}:{self.secreto_cliente}"
        cli_cred_b64 = base64.b64encode(cli_cred.encode())

        return cli_cred_b64.decode()


    def obtener_informacion_token(self):
        """
        DESCRIPCIÓN:
        ----
            Diccionario indicando que lo que se entrega son las credenciales
            de acceso.
        RETORNA:
        ----
            dict
        """

        return {"grant_type": "client_credentials"}


    def obtener_encabezado_token(self):
        """
        DESCRIPCIÓN:
        ----
            Adapta las credenciales a el formato necesario para el encabezado
            del query.
        RETORNA:
        ----
            dict
        """

        cli_cred_b64 = self.obtener_credenciales()

        return { "Authorization" : f"Basic {cli_cred_b64}"}


    def realizar_aut(self):
        """
        DESCRIPCIÓN:
        ----
            Realiza el query y asigna un nuevo token
        RETORNA:
        ----
            Booleano
        """

        r = requests.post(self.token_url,data=self.obtener_informacion_token(),headers=self.obtener_encabezado_token())

        if ( r.status_code not in range(200,299) ):
            raise Exception("No se pudo realizar la autentificacion :(")

        data = r.json()
        ahora = datetime.datetime.now()
        se_vence_en = data['expires_in']

        self.token_acceso = data['access_token']
        self.token_acceso_vence = ahora + datetime.timedelta(seconds=se_vence_en)
        self.token_a_vencido = self.token_acceso_vence < ahora

        return True


    def obtener_token(self):
        """
        DESCRIPCIÓN:
        ----
            En el caso de que el token esté funcionando retorna el toke, en la
            situacón inversa vuelve a solicitar el token.
        RETORNA:
        ----
            string
        """

        token = self.token_acceso
        se_vence_en = self.token_acceso_vence
        ahora = datetime.datetime.now()

        if se_vence_en < ahora or token is None:
            self.realizar_aut()
            return self.obtener_token()

        return token


    def obtener_encabezado_recursos(self):
        """
        DESCRIPCIÓN:
        ----
            Adapta el token al formato necesario para el encabezado del query.
        RETORNA:
        ----
            dict
        """

        token_acceso = self.obtener_token()
        return { "Authorization": f"Bearer {token_acceso}" }


    def obtener_recursos(self,id_busqueda:str,tipo_busqueda="artists", version="v1",relacionados=False):
        """
        DESCRIPCIÓN:
        ----
            busqueda de elementos en spotify utilizando id.
        RETORNA:
        ----
            dict
        """

        endpoint = f"https://api.spotify.com/{version}/{tipo_busqueda}/{id_busqueda}"

        if ( relacionados and tipo_busqueda == "artists" ):
            endpoint += "/related-artists"

        encabezado = self.obtener_encabezado_recursos()
        r = requests.get(endpoint,headers=encabezado)

        if ( r.status_code not in range(200,299) ):
            return {}

        return r.json()


    def base_de_busqueda(self,parametros):
        """
        DESCRIPCIÓN:
        ----
            Realiza el query y entrega la información que retorna la API de
            Spotify.
        RETORNA:
        ----
            dict
        """

        encabezados = self.obtener_encabezado_recursos()
        endpoint = "https://api.spotify.com/v1/search"
        url_de_busqueda = f"{endpoint}?{parametros}"

        r = requests.get(url_de_busqueda,headers=encabezados)

        if ( r.status_code not in range(200,299) ):
            return {}

        return r.json()


    def buscando_ando(self,query=None, operador=None, busqueda_operador=None, tipo_busqueda = 'artist'):
        """
        DESCRIPCIÓN:
        ----
            buscador de elementos en spotify como: artistas, albums, canciones,
            etc...
        RETORNA:
        ----
            dict
        """

        if query is None:
            raise Exception("Una query es necesaria para realizar la busqueda!")

        if isinstance(query,dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operador != None and busqueda_operador != None:
            if operador.lower() == "or" or operador.lower() == "not":
                operador = operador.upper()
                if ( isinstance(busqueda_operador,str) ):
                    query = f"{query} {operador} {busqueda_operador}"

        parametros_q = urlencode({"q":query,"type":tipo_busqueda.lower()})

        return self.base_de_busqueda(parametros_q)


    # def obtener_artista_nombre(self,nombre:str):
    #     """
    #     DESCRIPCIÓN:
    #     ----
    #         Interfaz de terminal para obtener artista por nombre.
    #     RETORNA:
    #     ----
    #         dict
    #     """

    #     artistas = self.buscando_ando(query=nombre,tipo_busqueda="artist")
    #     try:
    #         n_artistas = len(artistas['artists']['items'])
    #     except:
    #         print(artistas)
    #         raise Exception("no se encntró artista buscado")

    #     if ( n_artistas == 1 ):

    #         return artistas['artists']['items'][0]

    #     else:

    #         system("clear")
    #         mssg = "Listado de artistas posibles:\n"
    #         mssg +="=============================\n"
    #         for i in range(0,n_artistas):
    #             mssg += f"{i}) {artistas['artists']['items'][i]['name']}\n"

    #         print(mssg)
    #         ni = int(input("Número del artista que estas buscando:\n> "))

    #         return artistas['artists']['items'][ni]

    def obtener_artista_nombre(self,nombre:str):
        """
        DESCRIPCIÓN:
        ----
            Interfaz de terminal para obtener artista por nombre.
        RETORNA:
        ----
            dict
        """

        artistas = self.buscando_ando(query=nombre,tipo_busqueda="artist")
        try:
            n_artistas = len(artistas['artists']['items'])
            return artistas['artists']['items'][0]
        except IndexError:
            raise Exception("no se encntró artista buscado")

    def obtener_artista_id(self,_id:str):
        return self.obtener_recursos(_id,tipo_busqueda="artists")

    def obtener_relacionados_id(self,_id:str):
        return self.obtener_recursos(_id,tipo_busqueda="artists",relacionados=True)
