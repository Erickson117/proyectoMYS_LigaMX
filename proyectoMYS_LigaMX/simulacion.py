import random
from equipos import Equipos
from liga_mx import LigaMx

equipos = [] #Este arreglo contendra todos los equipos de la liga mx los crearemos usando su nombre y un rendimiento historico
for i in range(1, 19):
    historico = float(int(LigaMx[i]["puntos"]) / 68)
    equipo = Equipos(i, LigaMx[i]["nombre"], historico)
    equipos.append(equipo)

## A partir de aqui las funciones provienen de la pagina http://www.scielo.org.bo/scielo.php?script=sci_arttext&pid=S1683-07892005000100004 la cual tiene las formulas de probabilidad aqui utilizadas
def probEmpate(pJugados, pEmpatados): #probabilidad de que los equipos empaten en base a los partidos jugados y los partidos empatados
    if (pJugados == 0 or pEmpatados == 0): #en caso de que no se haya jugado ningun partido
        PE = 20.4
    else:
        PE = min(0.15, max(0.25, (pEmpatados / pJugados)))#aqui se calcula la probabilidad de que los equipos empaten en base a la cantidad de empates registrados y la cantidad de partidos jugados
    return PE


def probLocal(pJugados, vLocal, equipoA, equipoB):
    Pa = max(0.5, (vLocal / pJugados))
    Py = equipoA.rendimiento_history / (equipoB.rendimiento_history + equipoA.rendimiento_history)
    if (equipoB.rendimiento() + equipoA.rendimiento() == 0):
        Pb = Py
    else:
        Pb = equipoA.rendimiento() / (equipoB.rendimiento() + equipoA.rendimiento())

    PA = (1 - probEmpate(pJugados, pEmpatados)) * ((2 * Pa + 2 * Pb + Py) / 5)
    return PA


def seleccionarGanador(equipoA, equipoB):
    prob_empate = probEmpate(pJugados, pEmpatados)
    prob_local = probLocal(pJugados, vLocal, equipoA, equipoB)
    resultado_aleatorio = random.random()

    if resultado_aleatorio < prob_empate:
        return "Empate"
    elif resultado_aleatorio < prob_empate + prob_local:
        return equipoA
    else:
        return equipoB


def obtener_puntos_equipo(equipo):
    return equipo.getPuntos()


pJugados = 1
pEmpatados = 0
vLocal = 0
for i in range(18):
    resto = i + 1
    for j in range(resto, 18):
        pJugados += i
        if (j % 2 == 0):
            ganador = seleccionarGanador(equipos[i], equipos[j])
            if (ganador == "Empate"):
                equipos[i].empates += 1
                equipos[j].empates += 1
                pEmpatados += 1
            elif (ganador == equipos[i]):
                equipos[i].victorias += 1
                equipos[j].derrotas += 1
                vLocal += 1
            else:
                equipos[j].victorias += 1
                equipos[i].derrotas += 1
        else:
            ganador = seleccionarGanador(equipos[j], equipos[i])
            if (ganador == "Empate"):
                equipos[i].empates += 1
                equipos[j].empates += 1
                pEmpatados += 1
            elif (ganador == equipos[i]):
                equipos[j].victorias += 1
                equipos[i].derrotas += 1
                vLocal += 1
            else:
                equipos[i].victorias += 1
                equipos[j].derrotas += 1

        equipos[i].pJugadosE += 1
        equipos[j].pJugadosE += 1
        pJugados += 1

equipos_ordenados = sorted(equipos, key=obtener_puntos_equipo, reverse=True)
for i in range(18):
    print(f"{equipos_ordenados[i].nombre} puntos {equipos_ordenados[i].getPuntos()}")


def liguilla(equipos_ordenados):
    equipos_liguilla = equipos_ordenados[:6]
    equipos_liguilla = play_in(equipos_liguilla, equipos_ordenados[6], equipos_ordenados[7], equipos_ordenados[8],
                               equipos_ordenados[9])

    cuartos = []
    for i in range(4):
        ganador = seleccionarGanador(equipos_liguilla[i], equipos_liguilla[7 - i])
        if (ganador == "Empate"):
            cuartos.append(equipos_liguilla[i])
        else:
            cuartos.append(ganador)
    cuartos = sorted(cuartos, key=obtener_puntos_equipo, reverse=True)

    semis = []
    for i in range(2):
        ganador = seleccionarGanador(equipos_liguilla[i], equipos_liguilla[3 - i])
        if (ganador == "Empate"):
            semis.append(equipos_liguilla[i])
        else:
            semis.append(ganador)

    campeonIda = seleccionarGanador(semis[0], semis[1])
    campeonVuelta = seleccionarGanador(semis[1], semis[0])

    while ((campeonIda == "Empate" and campeonVuelta == "Empate") and (
            campeonIda == semis[0] and campeonVuelta == semis[1]) and (
                   campeonIda == semis[1] and campeonVuelta == semis[0])):
        campeonIda = seleccionarGanador(semis[0], semis[1])
        campeonVuelta = seleccionarGanador(semis[1], semis[0])

    if (campeonIda == "Empate"):
        campeon = campeonVuelta
    else:
        campeon = campeonIda

    print("El campeon es: ", campeon.nombre)


def play_in(equipos_liguilla, equipoA, equipoB, equipoC, equipoD):
    ganadorAB = seleccionarGanador(equipoA, equipoB)
    if (ganadorAB == "Empate"):
        equipos_liguilla.append(equipoA)
        perdedorAB = equipoB
    else:
        equipos_liguilla.append(ganadorAB)
        if (ganadorAB == equipoA):
            perdedorAB = equipoB
        else:
            perdedorAB = equipoA

    ganadorCD = seleccionarGanador(equipoC, equipoD)
    if (ganadorCD == "Empate"):
        ganadorCD = equipoC

    ultimo_clasi = seleccionarGanador(perdedorAB, ganadorCD)
    if (ultimo_clasi == "Empate"):
        equipos_liguilla.append(perdedorAB)
    else:
        equipos_liguilla.append(ultimo_clasi)

    return equipos_liguilla


liguilla(equipos_ordenados)


