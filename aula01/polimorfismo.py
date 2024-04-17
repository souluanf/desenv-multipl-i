class Veiculo:
    def buzinar(self):
        print("Buzina genérica")


class Carro(Veiculo):
    def buzinar(self):
        print("Buzina do carro")


class Moto(Veiculo):
    def buzinar(self):
        print("Buzina da moto")


def testar_buzina(veiculo):
    veiculo.buzinar()


carro = Carro()
moto = Moto()
testar_buzina(carro)
testar_buzina(moto)
