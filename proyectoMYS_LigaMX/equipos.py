class Equipos:
    def __init__(self, id_equipo, nombre, rendimiento_history):
        self.empates, self.victorias, self.derrotas = 0, 0, 0
        self.pJugadosE = 1
        self.id_equipo = id_equipo
        self.nombre = nombre
        self.rendimiento_history = rendimiento_history

    def getPuntos(self):
        return (self.victorias * 3) + (self.empates)

    def rendimiento(self):
        puntos = (self.victorias * 3) + (self.empates)
        return puntos / self.pJugadosE
