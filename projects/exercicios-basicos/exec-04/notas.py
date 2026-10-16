notas = [7.5, 8.0, 6.5, 9.0, 5.5]

soma = 0
maior = notas[0]
menor = notas[0]

for nota in notas:
    soma += nota

    if nota > maior:
        maior = nota

    if nota < menor:
        menor = nota

# Calcula a média
media = soma / len(notas)

# Resultados
print(f"Aura da Turma: {media:.2f}")
print(f"+1000 de Aura: {maior}")
print(f"-1000 de Aura: {menor}")