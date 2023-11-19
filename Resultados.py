import random

class Equipos:
    def __init__(self, id_equipo, nombre, rendimiento_history):
        self.empates,self.victorias, self.derrotas = 0,0,0
        self.pJugadosE = 1
        self.id_equipo = id_equipo
        self.nombre = nombre
        self.rendimiento_history = rendimiento_history
    def getPuntos(self): 
        return (self.victorias*3) + (self.empates)
    def rendimiento(self):
        puntos = (self.victorias*3) + (self.empates)
        return puntos / self.pJugadosE

#creacion de los equipos
#Esta lista tiene un historico de puntos de los ultimos cuatro torneos de la Liga mexicana de futbol
LigaMx = {
        1: {"nombre": "Cruz Azul", "puntos": 107},
        2: {"nombre": "America", "puntos": 138},
        3: {"nombre": "Chivas", "puntos": 110},
        4: {"nombre": "Pumas", "puntos": 86},
        5: {"nombre": "Tigres", "puntos": 111},
        6: {"nombre": "Rayados", "puntos": 127},
        7: {"nombre": "San Luis", "puntos": 77},
        8: {"nombre": "Mazatlan", "puntos": 71},
        9: {"nombre": "Queretaro", "puntos": 77},
        10: {"nombre": "Santos", "puntos": 88},
        11: {"nombre": "Puebla", "puntos": 99},
        12: {"nombre": "Xolos", "puntos": 73},
        13: {"nombre": "Toluca", "puntos": 94},
        14: {"nombre": "Pachuca", "puntos": 114},
        15: {"nombre": "Leon", "puntos": 100},
        16: {"nombre": "Necaxa", "puntos": 63},
        17: {"nombre": "Juarez", "puntos": 59}, 
        18: {"nombre": "Atlas", "puntos": 90}
        }
equipos = [] #Este arreglo contendra todos los equipos de la liga mx los crearemos usando su nombre y un rendimiento historico

for i in range(1, 19):
    historico = float(int(LigaMx[i]["puntos"]) / 68) #el rendimiento historico se calcula dividiendo la cantidad de puntos entre el numero de partidos 
    equipo = Equipos(i, LigaMx[i]["nombre"], historico)
    equipos.append(equipo)

## A partir de aqui las funciones provienen de la pagina http://www.scielo.org.bo/scielo.php?script=sci_arttext&pid=S1683-07892005000100004 la cual tiene las formulas de probabilidad aqui utilizadas

def probEmpate(pJugados, pEmpatados): #probabilidad de que los equipos empaten en base a los partidos jugados y los partidos empatados 
    if ( pJugados == 0 or pEmpatados == 0 ): #en caso de que no se haya jugado ningun partido 
        PE = 20.4
    else:
        PE = min(0.15,max(0.25,(pEmpatados/pJugados))) #aqui se calcula la probabilidad de que los equipos empaten en base a la cantidad de empates registrados y la cantidad de partidos jugados
    return PE

def probLocal(pJugados, vLocal, equipoA, equipoB):
    Pa = max(0.5,(vLocal/pJugados)) #Probabilidad de que resulte vencedor el equipo local por su localia
    Py = equipoA.rendimiento_history / (equipoB.rendimiento_history + equipoA.rendimiento_history) #Py es la probabilidad de que el local sea ganador por el rendimiento historico de los equipos
    if(equipoB.rendimiento() + equipoA.rendimiento() == 0):
        Pb = Py
    else:
        Pb = equipoA.rendimiento() / (equipoB.rendimiento() + equipoA.rendimiento()) # Probabilidad de que el local sea vencedor por el rendimiento de A y B
    
    PA = (1 - probEmpate(pJugados, pEmpatados))*((2*Pa+2*Pb+Py)/5) #aqui se calcula la probabilidad total de que el equipo local gane
    return PA

def seleccionarGanador(equipoA, equipoB): #esta funcion usa valores aleatorios para compararlos con los valores de probabilidad calculados 
    # Simulación para seleccionar un ganador
    prob_empate = probEmpate(pJugados, pEmpatados)
    prob_local = probLocal(pJugados, vLocal, equipoA, equipoB)

    # Generar un número aleatorio entre 0 y 1
    resultado_aleatorio = random.random() #aqui se obtiene un valor aleatorio

    if resultado_aleatorio < prob_empate: # si la probabilidad de empate es muy alta sera mayor que el random salvo que ocurra algo extraño, lo cual en el futbol ocurre
        return "Empate"
    elif resultado_aleatorio < prob_empate + prob_local: #lo mismo con la probabilidad de que el local pierda ya que incluso suma la probabilidad de empate
        return equipoA
    else:
        return equipoB #aqui devulve el visitante si es que este pierde

def obtener_puntos_equipo(equipo): #Esta funcion es para ordenar los equipos por su puntuaje
    return equipo.getPuntos()
    


#simulacion para las 17 fechas del futbol mexicano.
pJugados = 1
pEmpatados = 0
vLocal = 0
for i in range(18):
    #equipo[i].pJugadosE += 1
    resto = i + 1
    #print(equipos[i].nombre," vs \n")
    for j in range(resto,18):
        pJugados += i
        #print(equipos[j].nombre)
        if(j % 2 == 0): #si es par i sera local
            ganador = seleccionarGanador(equipos[i],equipos[j])
            if(ganador == "Empate"):
                equipos[i].empates +=1
                equipos[j].empates +=1
                pEmpatados +=1
            elif(ganador == equipos[i]):
                equipos[i].victorias +=1
                equipos[j].derrotas +=1
                vLocal +=1
            else:
                equipos[j].victorias +=1
                equipos[i].derrotas +=1
        else: #si no es par j sera local
            ganador = seleccionarGanador(equipos[j],equipos[i])
            if(ganador == "Empate"):
                equipos[i].empates += 1
                equipos[j].empates +=1
                pEmpatados +=1
            elif(ganador == equipos[i]):
                equipos[j].victorias +=1
                equipos[i].derrotas +=1
                vLocal +=1
            else:
                equipos[i].victorias +=1
                equipos[j].derrotas +=1
        
        equipos[i].pJugadosE += 1
        equipos[j].pJugadosE += 1
        pJugados += 1


# Ordenar la lista de equipos según los puntos
equipos_ordenados = sorted(equipos, key=obtener_puntos_equipo, reverse=True)
for i in range(18):
    print(f"{equipos_ordenados[i].nombre} puntos {equipos_ordenados[i].getPuntos()}")
    #print(equipos[i].pJugadosE - 1)

#simulación liguilla

def liguilla(equipos_ordenados):
    equipos_liguilla = equipos_ordenados[:6]
    equipos_liguilla = play_in(equipos_liguilla,equipos_ordenados[6],equipos_ordenados[7],equipos_ordenados[8],equipos_ordenados[9])

    cuartos = []
    for i in range(4):
        ganador = seleccionarGanador(equipos_liguilla[i],equipos_liguilla[7-i])
        if(ganador == "Empate"):
            cuartos.append(equipos_liguilla[i])
        else:
            cuartos.append(ganador)
    cuartos = sorted(cuartos, key=obtener_puntos_equipo, reverse=True)
    
    semis = []
    for i in range(2):
        ganador = seleccionarGanador(equipos_liguilla[i],equipos_liguilla[3-i])
        if(ganador == "Empate"):
            semis.append(equipos_liguilla[i])
        else:
            semis.append(ganador)
    
    campeonIda = seleccionarGanador(semis[0],semis[1])
    campeonVuelta = seleccionarGanador(semis[1],semis[0])

    while((campeonIda == "Empate" and campeonVuelta == "Empate")and(campeonIda == semis[0] and campeonVuelta == semis[1])and(campeonIda == semis[1] and campeonVuelta == semis[0])):
        campeonIda = seleccionarGanador(semis[0],semis[1])
        campeonVuelta = seleccionarGanador(semis[1],semis[0])
    
    if(campeonIda == "Empate"):
        campeon = campeonVuelta
    else:
        campeon = campeonIda
    
    print("El campeon es: ", campeon.nombre)

    

def play_in(equipos_liguilla,equipoA,equipoB,equipoC,equipoD):
    
    #Determinar el ganador de los lugares 7 y 8
    ganadorAB = seleccionarGanador(equipoA,equipoB)
    if (ganadorAB =="Empate"):
        equipos_liguilla.append(equipoA)
        perdedorAB = equipoB
    else:
        equipos_liguilla.append(ganadorAB)
        if(ganadorAB == equipoA):
            perdedorAB = equipoB
        else:
            perdedorAB = equipoA

    #Determinar el ganador de los equipos 9 y 10
    ganadorCD = seleccionarGanador(equipoC,equipoD)
    if (ganadorCD == "Empate"):
        ganadorCD = equipoC
    
    #Determinar el ganador entre el perdedro de AB y el ganador de CD
    ultimo_clasi = seleccionarGanador(perdedorAB,ganadorCD)
    if (ultimo_clasi =="Empate"):
        equipos_liguilla.append(perdedorAB)
    else:
        equipos_liguilla.append(ultimo_clasi)

    return equipos_liguilla

liguilla(equipos_ordenados)