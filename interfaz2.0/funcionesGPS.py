import serial
import json
import threading

class DetenerLectura(Exception):
    pass

def manejarGPS(stop_event, process_gprmc_callback=print, 
               port='/dev/serial0', baudrate=9600, 
               json_output_file='gps_data.json', txt_output_file='gps_data.txt'):
    """
    Lee datos GPS del puerto serial, guarda en formato JSON y TXT, y ejecuta un callback para procesar los datos.
    
    :param stop_event: threading.Event para detener la lectura
    :param process_gprmc_callback: Función que procesa los datos GPRMC
    :param port: Puerto serial
    :param baudrate: Velocidad de baudios del puerto serial
    :param json_output_file: Archivo donde se sobrescriben los datos en JSON
    :param txt_output_file: Archivo donde se guardan los datos en texto
    """
    
    ser = serial.Serial(port, baudrate, timeout=10)  # Abrir puerto serial
    try:
        print(f"Guardando datos en {json_output_file} y {txt_output_file}. Presione CTRL+C para salir.")
        while not stop_event.is_set():  # Verifica si el evento de parada está activo
            line = ser.readline().decode('ascii', errors='replace').strip()  # Lee datos del puerto serial
            if line.startswith('$GPRMC'):  # Verifica si la línea contiene datos GPRMC
                print(line)
                
                # Guardar en archivo JSON (sobrescribiendo)
                json_data = {"gps_data": line}
                with open(json_output_file, 'w') as json_file:
                    json.dump(json_data, json_file)
                
                # Guardar en archivo de texto (append)
                with open(txt_output_file, 'a') as txt_file:
                    txt_file.write(line + '\n')
                
                # Procesar el mensaje con un callback (para integración con interfaz o procesamiento adicional)
                process_gprmc_callback(line)
                
    except KeyboardInterrupt:
        print("\nPrograma interrumpido. Cerrando...")
    finally:
        ser.close()  # Cerrar puerto serial
