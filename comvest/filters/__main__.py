from comvest.filters import pedido_1, pedido_2, pedido_3


def main():
    pedido_1.extract()
    pedido_2.extract()
    pedido_3.extract()


if __name__ == "__main__":
    main()
