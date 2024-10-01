import serial
import threading


class DetenerLectura(Exception):
    pass


def manejarGPS(stop_event, process_gprmc_callback=print, port='/dev/serial0',
               baudrate=9600,
               output_file='gps_data.txt'):
    """
    Reads GPS data from the serial port, writes it to a file,
    and processes GPRMC messages.

    :param stop_event: threading.
        Event object to signal stopping the reading loop.
    :param process_gprmc_callback: Function to process GPRMC messages.
    :param port: Serial port to read from.
    :param baudrate: Baud rate for serial communication.
    :param output_file: File to log all GPS data.
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=1)  # Open serial port
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial {port}: {e}")
        return

    try:
        with open(output_file, 'a') as file:
            print(f"Guardando datos en {output_file}. Presione CTRL+C para salir.")
            while not stop_event.is_set():
                line_bytes = ser.readline()
                if not line_bytes:
                    continue  # Timeout occurred, loop again
                try:
                    line = line_bytes.decode('ascii', errors='replace').strip()
                except UnicodeDecodeError as e:
                    print(f"Error al decodificar línea: {e}")
                    continue  # Skip to next iteration

                if line:
                    print(line)
                    file.write(line + '\n')
                    if line.startswith('$GPRMC'):  # NMEA sentences start with '$'
                        process_gprmc_callback(line)
    except Exception as e:
        print(f"Error en manejarGPS: {e}")
    finally:
        ser.close()
        print("Puerto serial cerrado.")