# funcionesGPS.py
import serial
import threading


class DetenerLectura(Exception):
    pass


def manejarGPS(stop_event, port='/dev/serial0', baudrate=9600,
               output_file='gps_data.txt'):
    ser = serial.Serial(port, baudrate, timeout=1)  # Open serial port

    try:
        with open(output_file, 'a') as file:
            print(f"Guardando datos en {output_file}." +
                  "Presione CTRL+C para salir.")
            while not stop_event.is_set():
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line:
                    print(line)
                    file.write(line + '\n')
    except Exception as e:
        print(f"Error en manejarGPS: {e}")
    finally:
        ser.close()
        print("Puerto serial cerrado.")
