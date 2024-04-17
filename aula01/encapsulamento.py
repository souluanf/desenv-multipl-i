class Carro:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.__velocidade = 0

    def acelerar(self, valor):
        if valor > 0:
            self.__velocidade += valor
            print(f"Acelerando: nova velocidade é {self.__velocidade} km/h")
        else:
            print("Valor de aceleração deve ser positivo")

    def frear(self):
        if self.__velocidade > 0:
            self.__velocidade = 0
            print("Carro parado")
        else:
            print("Carro já está parado")

    def get_velocidade(self):
        return self.__velocidade


meu_carro = Carro("Fiat", "Uno")
meu_carro.acelerar(20)
print(f"Velocidade atual do carro: {meu_carro.get_velocidade()} km/h")
meu_carro.frear()
meu_carro.frear()