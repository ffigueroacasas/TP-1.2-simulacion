import sys
import random
import matplotlib.pyplot as plt

# Asignacion de Parametros de Usuario
# ---------------------------------------------------------------------------------------------- #
if (
    len(sys.argv) != 11
    or sys.argv[1] != "-c"
    or sys.argv[3] != "-n"
    or sys.argv[7] != "-s"
    or sys.argv[9] != "-a"
):
    print(
        "Uso: python programa.py -c <num_corridas> -n <nro_tiradas> -e <nro_elegido> -s <m: martingale | d: d´alambert | f:fibonacci | p:paroli> -a <i:infinito | f:finito>"
    )
    sys.exit(1)

if sys.argv[5] == "-e":
    nro_elegido = int(sys.argv[6])

CAPITAL_DADO = 50

corridas = int(sys.argv[2])

tiradas = int(sys.argv[4])

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

if sys.argv[10] == "i":
    capital = float("inf")
elif sys.argv[10] == "f":
    capital = CAPITAL_DADO
else:
    print("Capital Inexistente")
    sys.exit(1)


# Definicion de Funciones
# ---------------------------------------------------------------------------------------------- #
### PREGUNTAS AL PROFESOR
### - como funciona el infinito; literalmente capital = float("inf") o simplemente no se corta cuando entra en bancarrota
### - se puede apostar a un numero solo?
### - estrategia paroli - a veces se rompe
### - informe


def tirada():
    """emite un valor aleatorio entre 0 y 36"""
    numero = random.randint(0, 36)
    # if numero == 0:
    #     color = "verde"
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
        print(tiradas, jugadas)
        cont = 1
        apostado = apuesta_inicial
        while cont <= 5 and jugadas != tiradas:
            if pozo >= apostado:  # capaz chequear bancarrota aca
                jugadas += 1
                res_numero, res_color = tirada()
                resultados.append(res_numero)
                if res_color == color:
                    pozo += apostado
                    apostado = apuesta_inicial
                    cont = 1
                else:
                    pozo -= apostado
                    cont += 1
                    apostado *= 2
                capital_corrida_n.append(pozo)
            elif pozo <= apostado:
                pozo = "bancarrota"
                break
        if pozo == "bancarrota":
            break
    return pozo


def dalambert(color, apuesta_inicial):
    """juega n tiradas con la estrategia d'alambert"""
    jugadas = 0
    pozo = CAPITAL_DADO
    capital_corrida_n.append(pozo)
    apostado = apuesta_inicial
    while jugadas != tiradas:
        if pozo > 0:
            jugadas += 1
            res_numero, res_color = tirada()
            resultados.append(res_numero)
            if res_color == color:
                pozo += apostado
                if apostado > 1:
                    apostado -= 1
            elif res_color != color:
                pozo -= apostado
                apostado += 1
            capital_corrida_n.append(pozo)
        else:
            pozo = "bancarrota"
            break
    return pozo


def fibonacci(color, apuesta_inicial):
    """juega n tiradas con la estrategia fibonacci"""
    valores_apostados = []
    jugadas = 0
    pozo = CAPITAL_DADO
    capital_corrida_n.append(pozo)
    apostado = apuesta_inicial
    valores_apostados.append(apuesta_inicial)
    valores_apostados.append(apuesta_inicial)
    valores_apostados.append(apuesta_inicial)
    while jugadas != tiradas:
        if pozo >= valores_apostados[-1]:
            jugadas += 1
            res_numero, res_color = tirada()
            resultados.append(res_numero)
            if color != res_color:
                pozo -= valores_apostados[-1]
                valores_apostados.append(valores_apostados[-1] + valores_apostados[-2])
            elif color == res_color:
                pozo += valores_apostados[-1]
                valores_apostados.append(valores_apostados[-3])
            capital_corrida_n.append(pozo)
        else:
            pozo = "bancarrota"
            break

    return pozo


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
        while victorias < 3:
            if pozo >= proxima_apuesta:
                jugadas += 1
                res_numero, res_color = tirada()
                resultados.append(res_numero)
                if res_color == color:
                    pozo += proxima_apuesta
                    proxima_apuesta *= 2
                    victorias += 1
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
    return pozo


def graficar_evolucion_capital(evoluciones):
    """Grafica la evolución del capital a lo largo de las tiradas, durante una corrida dada"""
    print(len(evoluciones))
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
    plt.legend()
    plt.grid(True)
    plt.xlabel("Número de tirada")
    plt.ylabel("Cantidad de Capital")
    plt.show()


evolucion_capital = []
resultados = []
for i in range(corridas):
    capital_corrida_n = []
    resultados_corrida_n = []
    color = "negro" if (nro_elegido % 2 == 0) else "rojo"
    if estrategia == "martingale":
        capital = martingale(color, apuesta_inicial=1)
    elif estrategia == "d'alambert":
        capital = dalambert(color, apuesta_inicial=5)
    elif estrategia == "fibonacci":
        capital = fibonacci(color, apuesta_inicial=3)
    elif estrategia == "paroli":
        capital = paroli(color, apuesta_inicial=10)
    evolucion_capital.append(capital_corrida_n)
    print(len(evolucion_capital))
graficar_evolucion_capital(evolucion_capital)
