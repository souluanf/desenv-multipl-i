class Veiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo


class Carro(Veiculo):
    def __init__(self, marca, modelo, porta_malas):
        super().__init__(marca, modelo)
        self.porta_malas = porta_malas


meu_carro = Carro("Chevrolet", "Onix", "Grande")
print(f"{meu_carro.marca} {meu_carro.modelo} - Porta-malas: {meu_carro.porta_malas}")
