from generate_campaign_report import generate_campaign_report
from generar_numeros import main

def mostrar_menu():
    print("\nMenú de opciones")
    print("1. Crear y suministrar numeros a la base de datos")
    print("2. Generar archivos access")
    print("3. Generar reporte de una campaña")
    print("4. Salir")
    print()

def ejecutar_opcion(opcion):
    if opcion == 1:
        localidad = input("Ingrese el nombre de la localidad: ")
        cantidad = input("Ingrese la cantidad de numeros a generar: ")
        main(localidad,int(cantidad))
    elif opcion == 2:
        print("Has seleccionado la Opción 2: Agregando datos...")
    elif opcion == 3:
        id_campania = input("Ingrese la ID de la campaña para generar un reporte: ")
        generate_campaign_report(id_campania)
    elif opcion == 4:
        print("Saliendo del programa. ¡Hasta luego!")
    else:
        print("Opción no válida. Por favor, elige una opción del menú.")

def menu():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Selecciona una opción (1-4): "))
            if opcion == 4: 
                ejecutar_opcion(opcion)
                break
            ejecutar_opcion(opcion)
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entre 1 y 4.")

if __name__ == "__main__":
    menu()
