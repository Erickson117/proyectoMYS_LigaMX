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
            if(ganador == "Empate"): #Si los equipos empatan se le suma 1 empate a cada uno
                equipos[i].empates +=1
                equipos[j].empates +=1
                pEmpatados +=1
            elif(ganador == equipos[i]): #si el ganador es el equipo local se le suman una victoria y una derrota al perdedor 
                equipos[i].victorias +=1
                equipos[j].derrotas +=1
                vLocal +=1
            else:
                equipos[j].victorias +=1 #caso contrario se suma una victoria al visitante y una derrota al local
                equipos[i].derrotas +=1
        else: #si no es par j sera local
            ganador = seleccionarGanador(equipos[j],equipos[i]) #Aqui se hace el mismo proceso pero se alterna el orden de visita
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

def liguilla(equipos_ordenados): #Esta funcion genera los encuentros entre los equipos clasificados para obtener un campeon
    equipos_liguilla = equipos_ordenados[:6] #Aqui se obtienen los equipos clasificados de manera directa
    equipos_liguilla = play_in(equipos_liguilla,equipos_ordenados[6],equipos_ordenados[7],equipos_ordenados[8],equipos_ordenados[9]) #Aqui se obtienen los equipos del play in

    cuartos = [] # aqui se almacenaran los equipos resultantes de los cuartos de final
    for i in range(4):
        ganador = seleccionarGanador(equipos_liguilla[i],equipos_liguilla[7-i]) #El equipo más bajo de los que quedan juega contra el más alto
        if(ganador == "Empate"): #En caso de empate pasa el equipo mejor posicionado
            cuartos.append(equipos_liguilla[i])
        else: #En caso de que el resultado no sea empate pasa el equipo ganador
            cuartos.append(ganador)
    cuartos = sorted(cuartos, key=obtener_puntos_equipo, reverse=True)
    
    semis = [] #Aqui se almacenaran los ganadores de las semifinales
    for i in range(2):
        ganador = seleccionarGanador(equipos_liguilla[i],equipos_liguilla[3-i]) #al igual que en los cuartos de final se enfrentan los equipos top con los low
        if(ganador == "Empate"): #En caso de empate pasa el mejor posicionado 
            semis.append(equipos_liguilla[i])
        else: #En caso de que no sea empate pasa el vencedor 
            semis.append(ganador)
    
    campeonIda = seleccionarGanador(semis[0],semis[1]) #obtenemos el campeon de ida
    campeonVuelta = seleccionarGanador(semis[1],semis[0]) #Obtenemos el campeon de la vuelta

    #El siguiente while esta diseñado para evitar 3 situacionbes que no nos darian un campeon, empate en ambos juegos o victorias de ambos equipos 
    #si sucede se repetira hasta obtener un resultado valido que nos de un campeon
    while((campeonIda == "Empate" and campeonVuelta == "Empate")and(campeonIda == semis[0] and campeonVuelta == semis[1])and(campeonIda == semis[1] and campeonVuelta == semis[0])):
        campeonIda = seleccionarGanador(semis[0],semis[1])
        campeonVuelta = seleccionarGanador(semis[1],semis[0])
    
    #Si en la ida se empato el partido quiere decir que en el ganador de la vuelta es el equipo campeon
    if(campeonIda == "Empate"):
        campeon = campeonVuelta
    else: #En caso contrario quiere decir que el equipo que gano en la ida empato en la vuelta o que gano ambas finales por lo tanto el campeon de Ida sera el campeon
        campeon = campeonIda
    
    print("El campeon es: ", campeon.nombre) #Imprime a nuestro campeon.

    

def play_in(equipos_liguilla,equipoA,equipoB,equipoC,equipoD): #El play in es un sistema que la liga mx usa para obtener los participantes de cuartos que no clasificaron directo
    
    #Determinar el ganador de los lugares 7 y 8
    ganadorAB = seleccionarGanador(equipoA,equipoB) #Seleccionamos un ganador de los equipos que terminaron en la posiucion 7 y 8 de la tabla general
    if (ganadorAB =="Empate"): # en caso de ser empate el equipo mejor posicionado pasa a cuartos 
        equipos_liguilla.append(equipoA)
        perdedorAB = equipoB #El perdedor se guarda ya que tiene otra oportunidad de clasificarse al enfrentar al ganador del emfrentamiento del equipo 9 y 10
    else:
        equipos_liguilla.append(ganadorAB) # En caso de que el resultado no sea empate agregamos al vencedor a los cuartos de final
        if(ganadorAB == equipoA): #en caso de sea el equipo A el B se almacenara como el equipo perdedor
            perdedorAB = equipoB
        else:
            perdedorAB = equipoA #caso contrario el A sera asignado al equipo perdedor

    #Determinar el ganador de los equipos 9 y 10
    ganadorCD = seleccionarGanador(equipoC,equipoD) #Obtenemos un ganador en la serie del 9 contra el 10
    if (ganadorCD == "Empate"): #En caso de empate el equipo que enfrentara al perdedor de la ronda anterior sera el mejor posicionado, caso contrario se mantiene el valor anterior
        ganadorCD = equipoC
    
    #Determinar el ganador entre el perdedro de AB y el ganador de CD
    ultimo_clasi = seleccionarGanador(perdedorAB,ganadorCD)
    if (ultimo_clasi =="Empate"): #En caso de empate tiene prioridad el perdedor de la primera ronda al estar mejor posicionado en la tabla
        equipos_liguilla.append(perdedorAB)
    else:
        equipos_liguilla.append(ultimo_clasi) #En caso de que el resultado no sea un empate agregamos al vencedor 

    return equipos_liguilla #enviamos la nueva lista con los equipos clasificados del play in

liguilla(equipos_ordenados)# llamamos a la funcion liguilla usando los equipos ordenados 