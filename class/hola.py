def duplicar(x):
    return x*2

numeros = [1,5,3,7,8,9]

resultado = map(duplicar, numeros)

print(list(resultado))