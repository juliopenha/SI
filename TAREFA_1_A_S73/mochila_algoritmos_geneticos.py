from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import random

def criar_mochilas():
    mochilas = list(product([0, 1], repeat=items))
    return mochilas

def calcular_peso(mochila):
    total = sum(pesos[i] for i in range(items) if mochila[i] == 1)
    return total

def calcular_valor(mochila):
    total = sum(valores[i] for i in range(items) if mochila[i] == 1)
    return total

def calcular_valores(mochilas):
    valores_calculados = []
    for mochila in mochilas:
        valor_atual = calcular_valor(mochila)
        valores_calculados.append(valor_atual)
    return valores_calculados

def plot_graph(lista, label, title):
    x_axys = list(range(0, len(lista)))
    y_axys = lista

    plt.figure()
    plt.plot(x_axys, y_axys)
    plt.scatter(x_axys, y_axys, marker='o') # type: ignore

    plt.xticks(x_axys)
    plt.yticks(np.arange(-1, max(lista))+1)

    plt.xlabel("Mochilas")
    plt.ylabel(label)
    plt.title(title)

def gerar_populacao(size):
    populacao = []
    for _ in range(size):
        genes = [0, 1]
        individuo = []
        for _ in range(items):
            individuo.append(random.choice(genes))
        populacao.append(individuo)
    return populacao

def calcular_fitness(individuo):
    peso = calcular_peso(individuo)
    valor = calcular_valor(individuo)
    if(debug):
        print("--> Avaliando: A mochila", individuo, "tem peso", peso)
    if(peso <= capacidade_mochila):
        return valor
    else:
        return 0

def selecionar_par(populacao):
    valores_fitness = []
    for individuo in populacao:
        valores_fitness.append(calcular_fitness(individuo))

    valores_fitness = [float(i) / sum(valores_fitness) for i in valores_fitness]

    par1 = random.choices(populacao, weights=valores_fitness, k=1)[0]
    par2 = random.choices(populacao, weights=valores_fitness, k=1)[0]

    return par1, par2

def crossover(par1, par2):
    ponto_crossover = random.randint(0, items-1)
    descendente1 = par1[0:ponto_crossover] + par2[ponto_crossover:]
    descendente2 = par2[0:ponto_crossover] + par1[ponto_crossover:]

    return descendente1, descendente2

def provocar_mutacao(individuo):
    ponto_mutacao = random.randint(0, items - 1)
    if individuo[ponto_mutacao] == 0:
        individuo[ponto_mutacao] = 1
    else:
        individuo[ponto_mutacao] = 0
    return individuo

def encontrar_melhor_individuo(populacao):
    valores_fitness = []
    for individuo in populacao:
        valores_fitness.append(calcular_fitness(individuo))

    individuo = max(valores_fitness)
    indice = valores_fitness.index(individuo)
    return populacao[indice], indice

def algoritmo_genetico():
    populacao = gerar_populacao(tamanho_populacao)
    for _ in range(quantidade_geracoes):
        par = selecionar_par(populacao)

        descendente1, descendente2 = crossover(par[0], par[1])

        probabilidade = random.uniform(0, 1)
        if(probabilidade < probabilidade_mutacao):
            descendente1 = provocar_mutacao(descendente1)

        probabilidade = random.uniform(0, 1)
        if(probabilidade < probabilidade_mutacao):
            descendente2 = provocar_mutacao(descendente2)
        
        populacao = [descendente1, descendente2] + populacao[2:]
    
    individuo, indice = encontrar_melhor_individuo(populacao)
    peso_do_melhor = calcular_peso(individuo)
    valor_do_melhor = calcular_valor(individuo)


    print("Melhor mochila encontrada:", individuo)
    print("Posicao no grafico:", indice)
    print("Peso da mochila encontrada:", peso_do_melhor)
    print("Valor da mochila encontrada:", valor_do_melhor)

# ---------------------------- #
debug = False

# Parâmetros do problema da mochila
pesos = [2, 3, 4, 5, 6]
valores = [3, 4, 5, 8, 9]
capacidade_mochila = 10
items = 5

# Parâmetros do algorimo genetico
tamanho_populacao = 100
probabilidade_mutacao = 0.2
quantidade_geracoes = 10


mochilas_possiveis = criar_mochilas()
valores_possiveis = calcular_valores(mochilas_possiveis)

print("----------")
print("Solucao para todas as {} mochilas possiveis:".format(len(mochilas_possiveis)))
algoritmo_genetico()
plot_graph(valores_possiveis, "Valores", "Valores possiveis")

plt.show()