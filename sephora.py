"""
Autores: Ameyalli Sánchez y Ana Emilia Aparicio
Fecha: 13 de octubre de 2020
Descr: Situación problema
"""
#IMPORTACIONES
import time
import csv

#--------------Función que dibuja el menú de opciones y abre funciones
def Menu():
    global opcionU
    print("\t\tBienvenido a Sephora ♡\n")
    print("1. Realizar una compra.")
    print("2. Checar la disponibilidad de un producto.")
    print("3. Actualizar el inventario.")
    print("4. Productos Agotados.")
    print("5. Obtener Comision del empleado")
    print("6. Salir.")
    try:# "try" nos permite validar los errores del input del usuario 
        opcionU=int(input("\t\t¿Qué deseas hacer?, ingrese número ♡ "))
        #proceso a partir de la desición del usuario
        if opcionU==1:
            compra()
            time.sleep(1)#pausa el programa por 1 seg
            
        elif opcionU==2:
            disponibilidad()#aqui mandamos llamar la funcion "disponibilidad"
            time.sleep(1)#pausa el programa por 1 seg
            
        elif opcionU==3:
            actualizaInventario()#aqui mandamos llamar la funcion "inventario"
            time.sleep(1)#pausa el programa por 1 seg
            
        elif opcionU==4:
            agotados()#aqui mandamos llamar la funcion "agotados"
            time.sleep(1)#pausa el programa por 1 seg

        elif opcionU==5:
            obtenerComision()#aqui mandamos llamar la funcion "obtenerComision"
            time.sleep(1)#pausa el programa por 1 seg
            
        elif opcionU==6:
            salir()#aqui mandamos llamar la funcion "salir"
            time.sleep(1)#pausa el programa por 1 seg
    except ValueError:#aqui se cierra el "try"
        print ("\t¡Oops!\nLa entrada es incorrecta. Por favor escribe un numero entero. :C")
        time.sleep(3)
        #aqui se cierra el "try" y regresa a la funcion menu
        Menu()
#----termina la funcion menu
        
        
#Código/Funciones
#-------------------Función principal donde se abre el inventario desde el archivo "inventario.csv  
def compra():
    print("Catálogo de la tienda. ")
    time.sleep(1)
    getInventario()
    idProd = input('\n¿Qué producto usted necesita?, Ingrese el ID: \n').lower() 
    productos = generaMatriz("inventario.csv") #lo combierte en matriz llamando la funcion generaMatriz"
    for i in productos:
        if idProd == i[0]:#repite el proceso del ciclo, buscandolo en la matriz
            print('\nEl producto seleccionado es',i[1], 'y tiene un costo de MX$...', i[2],'\n')
            preg = input('\n¿Es el que requiere comprar? si o no \n').lower()
            if preg == 'si':
                
                dameDisponibilidad = hayDisponibilidad(idProd)#mandamos llamar la funcion hayDisponibilidad
                if (dameDisponibilidad > 0):
                    print("  ")
                    print("Vendedores:")
                    getEmpledos()#mandamos llamar a la funcion empleados para mostrarlos
                    idVend = input('\n¿Quien de nuestro equipo te ayudo?, Ingrese su ID\n').lower()
                    empleados = generaMatriz("empleados.csv")
                    for j in empleados:
                        if idVend == j[0]:
                            guardaComision(j[0], j[1], j[2], j[3], i[2], i[0])#mandamos llamar la funcion guardaComision
                            descuentaInventario(dameDisponibilidad, idProd)#mandamos llamr a la funcion descuentaInventario
                            finCompra = input('\n¿Desea realizar una nueva compra? si o no \n').lower()
                            if finCompra == 'no':
                                Menu()#cierra el programa 
                            else:
                                compra()#ciclo para volver a abrir menu
                else:
                    print("¡Disculpa! no tenemos disponibilidad de este producto :C")
                    time.sleep(3)
                    compra()
            else:
                compra()
#------termina la funcion compra
                

#--------------Función que nos ayuda a abrir el inventario desde archivos 
def getInventario():
    with open('inventario.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)#quita cabeceras de los archivos
        for registroInv in csv_reader:
            print("ID:",registroInv[0], "...",registroInv[1], ".....MX",registroInv[2])
            time.sleep(.1)
#---------------termina la funcion getInventario

#--------------Función que nos ayuda a abrir el archivo empleados             
def getEmpledos():
    with open('empleados.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)#quita cabeceras de los archivos
        for registroEmp in csv_reader:
            print("ID: ", registroEmp[0], registroEmp[2], ":", registroEmp[1])
#---------------termina la funcion getEmpledos
            
#--------------Función que nos ayuda a convertir a matriz           
def generaMatriz(dameNombre):
    #variable
    listProd = []
    with open(dameNombre) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)#quita cabeceras de los archivos
        for registroMatriz in csv_reader:
            listProd.append(registroMatriz) 
    return listProd
#---------------termina la funcion getEmpledos


#---------------Función que guarda la comisón por cada artículo vendido, al empleado correspondiente.    
def guardaComision(id, name, posicion, comision, costo, IDProducto):
    comVenta = float(costo) * float(comision)#Hace la operación para calcular cuánto recibirá el vendedor de comisión.
    archivoComisiones = open('comisiones.txt','a+')
    archivoComisiones.write(id+","+name+","+str(comVenta)+","+str(IDProducto)+'\n')#Guarda la nueva comisión.
    archivoComisiones.close()
#---------------fin de la función para las comisiones.


#---------------Función para checar la disponibilidad de un producto del inventario.
def hayDisponibilidad(idProd):
    with open('disponibilidad.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        for row in csv_reader:#checa los datos indicados
              if (idProd == row[0]):
                  if (int(row[1])>0):
                      return int(row[1])#indica que este artículo sí está disponible
                  else:
                      return 0#indica que ese artículo no está disponible
#---------------Fin de la función para la disponibilidad
                    
#---------------Función para aclarar de que producto se busca la disponibilidad                
def disponibilidad():
    getInventario()
    idProd = input('\n¿De que producto busca disponibilidad?, Ingrese el ID: \n').lower()    
    dameDisponibilidad = hayDisponibilidad(idProd)#checa si el producto mencionado está disponible o no
    print("Tenemos disponibles", dameDisponibilidad , "ejemplares de este producto :)")#imprime la cantidad de unidades que hay en existencia de ese producto
    time.sleep(3.5)
    Menu()
#--------------Fin de la función para checar la disponibilidad de producto
        
#--------------Función de la función que actualizará el inventario   
def actualizaInventario():
    filename = "disponibilidad.csv"
    getInventario()
    idProducto = input('\n¿Qué producto necesita actualizar?, Ingrese el ID: \n').lower()#se ingresa el ID para identificar de que producto se trata.
    idCantidad = int(input('\n¿Que cantidad desea agregar?, Ingrese la cantidad: \n').lower())#Se ingresa la cantidad de productos que llegaron.
    dameDisponibilidad = hayDisponibilidad(idProducto)
    sumaDisponibilidad = dameDisponibilidad + idCantidad#actualiza el inventario según las unidades nuevas y las que ya estaban
    restaIndice = int (idProducto) - 1#localiza el ID del producto correctamente

    with open(filename, newline= "") as file:
        readData = [row for row in csv.DictReader(file)]
        readData[restaIndice]['DIS'] = sumaDisponibilidad#le asigna los nuevos valores a la variable correspondiente
        
    readHeader = readData[restaIndice].keys()
    escribecsv(readHeader, readData, filename, "update")#muestra los datos que ya fueron actualizados (anteriores+nuevos)
    print("¡Súper! El producto con el ID: ", idProducto, "fue actualizado. ♡")
    time.sleep(4.5)
    Menu()
#--------------Fin de la función actualizaInventario
    
#--------------Función para restarle productos al inventario
#esta funcion ira 
def descuentaInventario(dis, IdProd):
    filename = "disponibilidad.csv"
    restaCompra = dis - 1#le resta a la disponibilidad
    restaIndice = int (IdProd) - 1#indica la posición de los datos en el archivo a partir del ID dado
    with open(filename, newline= "") as file:
        readData = [row for row in csv.DictReader(file)]
        readData[restaIndice]['DIS'] = restaCompra#resta los datos ingresados al archivo de texto en la sección correspondiente
        
    readHeader = readData[restaIndice].keys()#actualiza el archivo con los nuevos datos
    escribecsv(readHeader, readData, filename, "update")
#--------------Fin de la función que le resta artículos al inventario
    
#--------------Función que abre el archivo seleccionado para escribir sobre este
def escribecsv(header, data, filename, option):
        with open (filename, "w", newline = "") as csvfile:#menciona que se está abriendo el archivo como un .csv
            if option == "update":
                writer = csv.DictWriter(csvfile, fieldnames = header)#indica los datos que se están escribiendo en el archivo de texto
                writer.writeheader()#escribe el título en el archivo
                writer.writerows(data)#escribe el cuerpo del archivo
#--------------Fin de la función que escribe el texto
                
                
                
#--------------Función para mostrar artículos agotados
def agotados():
    with open('disponibilidad.csv') as csv_file:#delimita el archivo que se abrirá y que es un .csv
        csv_reader = csv.reader(csv_file, delimiter=',')#indica que será solo lectura
        next(csv_file)
        for row in csv_reader:#la lectura será de linea en linea
            totalInventario = int(row[1])
            if totalInventario == 0:
                print("Los productos con el ID", row[0], "estan agotados :C")
                time.sleep(3.5)
                Menu()
#--------------Fin de la función de artículos agotados
                
#--------------Función para calcular la comisión a partir de la venta realizada
def obtenerComision():
    print("    ")
    print("Vendedores")
    getEmpledos()
    idVendedor = input("\n¿De que integrante de nuestro equipo deseas revisar comisiones de venta?\nIngresa su ID:").lower()
    file = open("comisiones.txt","r")#abre directamente el archivo que contiene las comisiones por empleado
    suma = 0
    for line in file:#va de linea en linea dentro del archivo 
        fields = line.split(",")
        if (idVendedor == fields[0]):#a partir del ID proporcionado busca la localización exacta en el archivo de texto
            suma = suma + float(fields[2])#hace la operación para sumar la comisón existente con la nueva
            print("El empleado tuvo una comision de MX$", fields[2], "del producto con el ID",fields[3])
    print("El total de comisiones es de: MX$", suma)#muestra la comisión total que tiene el vendedor
    time.sleep(4)
    Menu()
#--------------Fin de la función para calcular la comisión


#--------------Función salida  
def salir():
    print("Gracias por su compra ♡")
    print("Vuelva pronto!")
#---------------Fin del último def de las opciones del menú


Menu()