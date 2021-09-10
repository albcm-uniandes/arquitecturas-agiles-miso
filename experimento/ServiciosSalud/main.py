import json
import producer

class ServiciosSaludDispatcher:
    """
    Clase principal que funciona como dispatcher de datos a la cola de mensajeria
    este nos permite probar la manera en como el servicio "ServiciosSalud" enviaría los eventos al broker
    luego de correr la logica necesaria para construir los eventos relacionados a las Historias de los pacientes
    """

    @staticmethod
    def read_mock_file(file_name):
        """
        Con este metodo estatico abrimos un archivo y cargamos los datos en memoria de nuestros 1000 datos 
        de prueba generados aleatoriamente relacionados al caso de uso.
        """
        with open(file_name) as file:
            return json.loads(file.read())
    
    @staticmethod
    def send_to_producer(list_of_data):
        """
        Con este metodo utilizamos el publicer usando pika para
        enviar uno a uno los mensajes al recibir una lista de json de datos en memoria 
        """
        for message in list_of_data:
            producer.publish(message)

if __name__ == '__main__':
    # Instancia de la clase ServiciosSaludDispatcher
    _ = ServiciosSaludDispatcher()
    # Cargar datos del archivo de pruebas en memoria
    data = _.read_mock_file("MOCK_DATA.json")
    # Enviar cada uno de los datos como mensaje al broker de RabbitMQ
    _.send_to_producer(data)