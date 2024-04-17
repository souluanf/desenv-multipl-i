from abc import ABC, abstractmethod


class Veiculo(ABC):
    @abstractmethod
    def acelerar(self):
        pass


class Carro(Veiculo):
    def acelerar(self):
        print("Acelerando o carro")


class Moto(Veiculo):
    def acelerar(self):
        print("Acelerando a moto")


carro = Carro()
moto = Moto()

carro.acelerar()
moto.acelerar()
