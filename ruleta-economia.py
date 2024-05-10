import sys
import random
import matplotlib.pyplot as plt
import numpy as np

# Asignacion de Parametros de Usuario
# -----------------------------------------------------------------------------------------------------------------------------------------------
if (
    len(sys.argv) != 11
    or sys.argv[1] != "-c"
    or sys.argv[3] != "-n"
    or sys.argv[5] != "-e"
    or sys.argv[7] != "-s"
    or sys.argv[9] != "-a"
):
    print(
        "Uso: python programa.py -c <num_corridas> -n <nro_tiradas> -e <color_elegido> -s <m: martingale | d: d´alambert | f:fibonacci | p:paroli> -a <i:infinito | f:finito>"
    )
    sys.exit(1)

# asignamos el valor del capital inicial
CAPITAL_DADO = 20000
APUESTA_INICIAL = 2000

# asignamos el color elegido
if sys.argv[6] == "r":
    color_elegido = "rojo"
elif sys.argv[6] == "n":
    color_elegido = "negro"
else:
    print("Estrategia inexistente. Opciones: <n: negro | r: rojo>")
    sys.exit(1)

# asignamos cantidad de corridas
corridas = int(sys.argv[2])

# asignamos cantidad de tiradas
tiradas = int(sys.argv[4])

# asignamos estrategia
if sys.argv[8] == "m":
    estrategia = "martingale"
elif sys.argv[8] == "d":
    estrategia = "d'alambert"
elif sys.argv[8] == "f":
    estrategia = "fibonacci"
elif sys.argv[8] == "p":
    estrategia = "paroli"
else:
    print(
        "Estrategia inexistente. Opciones: <m: martingale | d: d´alambert | f:fibonacci | p:paroli>"
    )
    sys.exit(1)

# asignamos tipo de capital
if sys.argv[10] == "i":
    capital = "infinito"
elif sys.argv[10] == "f":
    capital = "finito"
else:
    print("Capital Inexistente")
    sys.exit(1)


# Definicion de Funciones
# -----------------------------------------------------------------------------------------------------------------------------------------------
def tirada():
    """emite un valor aleatorio entre 0 y 36"""
    numero = random.randint(0, 36)
    if numero % 2 == 0:
        color = "rojo"
    else:
        color = "negro"
    return numero, color


def martingale(color, apuesta_inicial):
    """juega n tiradas con la estrategia martingale"""
    jugadas = 0
    pozo = CAPITAL_DADO
    while jugadas != tiradas:
        cont = 1
        apostado = apuesta_inicial
        while cont <= 5 and jugadas != tiradas:
            if pozo >= apostado or capital == "infinito":
                jugadas += 1
                res_numero, res_color = tirada()
                if res_color == color:
                    pozo += apostado
                    apostado = apuesta_inicial
                    cont = 1
                    tiradas_exitosas.append(jugadas)
                else:
                    pozo -= apostado
                    cont += 1
                    apostado *= 2
                capital_corrida_n.append(pozo)
            elif pozo <= apostado and capital == "finito":
                pozo = "bancarrota"
                break
        if pozo == "bancarrota":
            break


def dalambert(color, apuesta_inicial):
    """juega n tiradas con la estrategia d'alambert"""
    jugadas = 0
    pozo = CAPITAL_DADO
    capital_corrida_n.append(pozo)
    apostado = apuesta_inicial
    while jugadas != tiradas:
        if pozo > 0 or capital == "infinito":
            jugadas += 1
            res_numero, res_color = tirada()
            if res_color == color:
                pozo += apostado
                tiradas_exitosas.append(jugadas)
                if apostado > 1:
                    apostado -= 1
            elif res_color != color:
                pozo -= apostado
                apostado += 1
            capital_corrida_n.append(pozo)
        else:
            pozo = "bancarrota"
            break


def fibonacci(color, apuesta_inicial):
    """juega n tiradas con la estrategia fibonacci"""
    valores_apostados = []
    jugadas = 0
    pozo = CAPITAL_DADO
    capital_corrida_n.append(pozo)
    apostado = apuesta_inicial
    for i in range(3):
        valores_apostados.append(apuesta_inicial)
    while jugadas != tiradas:
        if pozo >= valores_apostados[-1] or capital == "infinito":
            jugadas += 1
            res_numero, res_color = tirada()
            if color != res_color:
                pozo -= valores_apostados[-1]
                valores_apostados.append(valores_apostados[-1] + valores_apostados[-2])
            elif color == res_color:
                pozo += valores_apostados[-1]
                valores_apostados.append(valores_apostados[-3])
                tiradas_exitosas.append(jugadas)
            capital_corrida_n.append(pozo)
        else:
            pozo = "bancarrota"
            break


def paroli(color, apuesta_inicial):
    """juega n tiradas con la estrategia paroli"""
    valores_apostados = []
    jugadas = 0
    pozo = CAPITAL_DADO
    capital_corrida_n.append(pozo)
    proxima_apuesta = apuesta_inicial
    while jugadas != tiradas:
        victorias = 0
        proxima_apuesta = apuesta_inicial
        while victorias < 3 and jugadas != tiradas:
            if pozo >= proxima_apuesta or capital == "infinito":
                jugadas += 1
                res_numero, res_color = tirada()
                if res_color == color:
                    pozo += proxima_apuesta
                    proxima_apuesta *= 2
                    victorias += 1
                    tiradas_exitosas.append(jugadas)
                else:
                    pozo -= proxima_apuesta
                    proxima_apuesta = apuesta_inicial
                    victorias = 0
                capital_corrida_n.append(pozo)
            else:
                pozo = "bancarrota"
                break
        if pozo == "bancarrota":
            break


def graficar_evolucion_capital(evoluciones):
    """Grafica la evolución del capital a lo largo de las tiradas, durante una corrida dada"""
    plt.figure(figsize=(10, 6))
    for e, evolucion in enumerate(evoluciones):
        plt.plot(
            evolucion,
            label=f"Flujo de Caja para la corrida {e + 1}",
        )
    plt.plot(
        [CAPITAL_DADO] * tiradas,
        label="Flujo de caja inical",
        color="red",
    )
    plt.title("Flujo de Caja")
    # plt.legend()
    plt.grid(True)
    plt.xlabel("Número de tirada")
    plt.ylabel("Cantidad de Capital")
    plt.show()


def graficar_tiradas_exitosas(tiradas_exitosas):
    fig, ax = plt.subplots()
    valores_unicos, frecuencias = np.unique(tiradas_exitosas, return_counts=True)
    ax.bar(valores_unicos, frecuencias)
    ax.set_xlabel("n (numero de tirada)")
    ax.set_ylabel("Frecuencia Relativa")
    ax.set_title("Frecuencia Relativa de ganar en la tirada n")
    plt.show()


# inicializacion de variables globales y programa principal
# ------------------------------------------------------------------------------------------------------------------------------------------------
evolucion_capital = []
# este arreglo contiene los numeros de tirada en los que el apostador acierta, para graficarlos
tiradas_exitosas = []

for i in range(corridas):
    capital_corrida_n = []
    resultados_corrida_n = []
    tiradas_exitosas_corrida_n = []
    if estrategia == "martingale":
        martingale(color_elegido, APUESTA_INICIAL)
    elif estrategia == "d'alambert":
        dalambert(color_elegido, APUESTA_INICIAL)
    elif estrategia == "fibonacci":
        fibonacci(color_elegido, APUESTA_INICIAL)
    elif estrategia == "paroli":
        paroli(color_elegido, APUESTA_INICIAL)
    evolucion_capital.append(capital_corrida_n)
graficar_evolucion_capital(evolucion_capital)
graficar_tiradas_exitosas(tiradas_exitosas)
