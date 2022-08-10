from comvest.clear_notas import limpeza_notas, presenca

def main():
    limpeza_notas.extraction()
    presenca.get()

if __name__ == '__main__':
    main()