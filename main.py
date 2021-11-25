from claseVista import VentanaPrincipal
from claseControlador import Controlador
from claseModelo import Modelo

def main():
    modelo = Modelo()
    vista = VentanaPrincipal()
    controlador = Controlador(vista,modelo)
    vista.setControlador(controlador)
    controlador.iniciar()

if __name__ == "__main__":
    main()