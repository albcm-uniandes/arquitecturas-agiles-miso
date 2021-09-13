import json
import sys
  
def getRequestsAsDictionary(fileName):
    requestsDictionary = dict()
    f = open(fileName,)
    dictionaries = json.load(f)

    for dictionary in dictionaries:
        id = dictionary["id"]
        requestsDictionary[id] = dictionary

    f.close()
    return requestsDictionary

if __name__ == "__main__":
    dic1 = getRequestsAsDictionary(sys.argv[1])
    dic2 = getRequestsAsDictionary(sys.argv[2])
    totalPeticionesEnviadas = len(dic1)
    totalPeticionesRecibidas = len(dic2)

    print("Total peticiones enviadas: " + str(totalPeticionesEnviadas))
    print("Total peticiones recibidas: " + str(totalPeticionesRecibidas))

    totalPeticiones = 0

    for idPeticionEnviada in dic1:
        peticionEnviada = dic1[idPeticionEnviada]

        if idPeticionEnviada in dic2:
            peticionRecibida = dic2[idPeticionEnviada]

            if peticionEnviada["id"] == peticionRecibida["id"] and peticionEnviada["cedula"] == peticionRecibida["cedula"] and peticionEnviada["nombre"] == peticionRecibida["nombre"] and peticionEnviada["apellido"] == peticionRecibida["apellido"] and peticionEnviada["evento"] == peticionRecibida["evento"] and peticionEnviada["detalle"] == peticionRecibida["detalle"]:
                totalPeticiones = totalPeticiones + 1
        
    print("Porcentaje de peticiones enviadas que fueron recibidas: " + str((totalPeticiones/totalPeticionesEnviadas) * 100) + " %")

