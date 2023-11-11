import numpy 

class Cidades:
    def __init__(self, nomeCidades:list = []) -> None:
        self.nomeCidades = nomeCidades
        self.grafoCidades = []

    def __str__(self) -> str:
        pass

    def getGrafoCidades(self):
        return self.grafoCidades

    def leArquivoCidades(self):
        pass

    def criaGrafoCidades(self):
        pass

    def getIndiceCidadePorNome(self, cidade: str)->int:
        pass

    def getDistanciaDuaCidades(self, c1:str, c2:str):
        pass

