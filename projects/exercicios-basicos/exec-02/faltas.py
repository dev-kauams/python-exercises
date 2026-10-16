media = float(input("Digite a média final do aluno: "))
faltas = int(input("Digite a quantidade de faltas: "))

if media >= 6.0 and faltas <= 15:
    print("\nAluno FARMOU!")
else:
    print("\nAluno MOGGADO!")