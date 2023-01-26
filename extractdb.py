# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 22:26:20 2022

@author: AA40000

"""

import pandas as pd
import numpy as np
#import csv
from datetime import datetime



# Lectura del diccionario
def readDic(path,       #   Path
            sepr,       #   Separador de variable
            numid,      #   Identificador de la variable
            numchar,    #   Numero de caracteres
            numtype     #   Tipo de carcter
            ):
    #Leemos nuestro archivo y lo almacenamos como un df
    archivo = pd.read_table(
        str(path),header = None,sep = str(sepr))
    # Estos arreglos son para vincular la variable con cus caracteres
    variable = []
    caracteres = []
    # Se itera por un identificador, en este caso el nombre de cada variable
    for i in range(len(archivo[numchar])):
        # Reglas para contraccion de variables por bloques
        if (str(archivo[numtype][i]).strip()=="t"):
            # Iteramos sobre la cantidad de bloques de la regla
            for j in range(int(archivo[numchar][i])):
                if(int(archivo[numchar][i+2])==2):
                    # Agregamos el numero de variables a nuestro arreglo x2
                    caracteres.append(int(archivo[numchar][i+2]))    
                else:
                    caracteres.append(int(archivo[numchar][i+2]))
                variable.append((str(archivo[numid][i]).strip())+"_"+str(j+1))
            archivo.iloc[i+2,numchar]=np.nan
        else:
            # Aqui descartamos los valores nulos
            if(np.isnan(archivo[numchar][i])):
                i=i+1
            else:
                variable.append(str(archivo[numid][i]).strip())
                caracteres.append(int(archivo[numchar][i]))
    # Aqui tenemos un df sin reglas de contracción
    dic = pd.DataFrame(
        data = None,
        columns = ["ID","NumChar"]
        )
    
    dic["ID"] = variable
    dic["NumChar"] = caracteres
    return dic
def readDict2(path, sepa):
    return(pd.read_csv(path, sep=sepa))
    
#Agregar cada fila de la data a un arreglo para no perder caracteres ¿Podriamos optimizar esto?
def readDataAsarray(names): # ¿Que es name?
    name = str(names)
    lines = []
    with open(name,"r") as data:
         for line in data:
             lines.append(line)
    return lines
# Esta función hace la extraccion de una sub cadena sin leer toda la cadena
def extractString(array, # arreglo para extraer
                  ini, # inicio
                  numC): # Fin
    temp = []
    for i in range(numC):
        temp.append(str(array[i+ini]))
    y = "".join(temp)    
    return str(y) 
# Crear una columna apartir del diccionario y la data
def makeColumn(data,length,numC,ini):
    col=[]
    for i in range(length):
        #Agrega el elemento de data[i] con numero de caracteres = num C y el inicio de la indentacion en ini
        col.append(str(extractString(data[i], ini, numC)))
    return col
# Creamos la tabla grande
def makeDB(dic,         # Diccionario 
           data,        # Informacion
           ID_col,      # Columna de identificador del diccionario
           Numchar_col  # Columna de los numeros de caracteres de cada variable
           ):
    ini = 0
    db = pd.DataFrame(
        data = None,
        columns = dic[ID_col]
        )
    for i in range(len(dic[ID_col])):
        if(np.isnan(dic[Numchar_col][i])):
            None
        else:
            tmpi = int(dic[Numchar_col][i])
            db.iloc[:,i] = makeColumn(data,len(data), tmpi,ini)
            ini = ini + tmpi
    return db
# Exportamos la base concatenando el dia de ejecucion (hay que permitir extraer un dia en particular)
def exportDB(db, name):
    date = datetime.today().strftime('%Y%m%d')
    path = name +date+".csv"
    # Nombre del archivo tratado:INSTIGP_date.csv
    # Tambien debemos definir un path de salida
    db.to_csv(path,sep=",")
# Crea un diccionario apartir de una base
def makeColumnDic(columna):
    columna = columna.astype(str)
    return len(max(columna, key = len))
# Crea un archivo de texto plano apartir de una base
def makeDic(data_frame):
    col_names = [column for column in data_frame.columns]
    num_char = [makeColumnDic(data_frame[column]) for column in data_frame.columns]
    dic = pd.DataFrame()
    dic['Nombres'] = col_names
    dic['Numero de Caracteres'] = num_char
    dic.to_csv('dictionary.txt', sep=':', index=False)
    return dic
def makeArrayData(column, n_char):
    n = n_char - len(str(column))
    return (str(str(column).ljust(len(str(column)) + n )))
# Pasamos la data de un data frame a un texto plano
def makeData(data_frame,ID, dic):
    with open("DATA.txt", "w") as file:
        for j in range(len(data_frame[str(ID)])):
            array_aux = []
            #print(j)
            for column in data_frame.columns:
                #print(column)
                array_aux.append(str(data_frame[str(column)][j]))
            string_to_write = ''
            for i in range(len(array_aux)):
                string_to_write +=  str(makeArrayData(array_aux[i],dic['Numero de Caracteres'][i]))
        file.write(string_to_write+'\n')
        #file.write(str(j)+'\n')
    file.close()

# Generar datos de prueba
data = np.random.randint(1,1000,size=(2000,10))
# Crear data frame
data_test_1 = pd.DataFrame(data, columns= 
        ['ID','col1','col2','col3','col4','col5','col6','col7','col8','col9'])
#print(data_test)
data_test_1 = data_test_1.apply(lambda x: x.astype(str))
data_test = pd.read_csv('data_test_2.csv', sep=',')
print(data_test.shape)
dic = makeDic(data_test)
print(dic)
makeData(data_test, 'Clave Municipio',dic)
PATH_1 = "dictionary.txt"
PATH_2 = "DATA.txt"
dic_1 = readDict2(PATH_1, ':')
data_2 = readDataAsarray(PATH_2)
db = makeDB(dic_1, 
            data_2,
            "Nombres",
            "Numero de Caracteres")
exportDB(db,'nueva_tabla_')

