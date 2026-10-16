preço = float(input("Digite o preço do produto: R$ "))
quantidade = int(input("Digite a quantidade comprada: "))

valor_total = preço * quantidade

if valor_total >= 200:
    desconto = valor_total * 0.10
    valor_final = valor_total - desconto
    print(f"\nValor total: R$ {valor_total:.2f}")
    print(f"Desconto de 10%: R$ {desconto:.2f}")
    print(f"Valor final da compra: R$ {valor_final:.2f}")
else:
    print(f"\nValor total da compra: R$ {valor_total:.2f}")
    print("Não houve desconto.")