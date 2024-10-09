import serial
import requests
import time

# Configuración del puerto serial (ajusta el nombre del puerto según sea necesario)
ser = serial.Serial('/dev/serial10', 9600, timeout=1)

# URL de la API real o de prueba
url = 'https://httpbin.org/post'  # Cambia esto por tu URL real cuando estés listo

def parse_gprmc(data):
    """Parsea una línea GPRMC para extraer latitud y longitud."""
    if data[0:6] == b'$GPRMC':
        parts = data.decode('ascii').split(',')
        if parts[2] == 'A':  # Verifica si el mensaje es válido
            # Obtiene latitud
            lat_raw = parts[3]
            lat_dir = parts[4]
            lat = float(lat_raw[:2]) + float(lat_raw[2:]) / 60.0
            if lat_dir == 'S':
                lat = -lat

            # Obtiene longitud
            lon_raw = parts[5]
            lon_dir = parts[6]
            lon = float(lon_raw[:3]) + float(lon_raw[3:]) / 60.0
            if lon_dir == 'W':
                lon = -lon

            return lat, lon
        elif parts[2] == 'V':  # El mensaje no es válido
            print("No se ha recibido señal del satélite.")
    return None, None

while True:
    try:
        # Lee línea desde el módulo GPS
        line = ser.readline()
        
        # Parsear la línea GPRMC
        latitude, longitude = parse_gprmc(line)
        
        if latitude and longitude:
            # Crea los datos para enviar
            data = {
                "journey_id": 698453,
                "timestamp": int(time.time()),
                "latitude": latitude,
                "longitude": longitude,
                "altitude": 0.0,
                "speed": 0.0,
                "bearing": 0.0,
                "odometer": 0.0
            }

            # Envía los datos a la API real o de prueba
            response = requests.post(url, json=data)
            print(f"Enviando datos: {data}")
            print(f"Respuesta de la API: {response.status_code}, {response.text}")

        time.sleep(5)  # Envía datos cada 5 segundos

    except Exception as e:
        print(f"Error: {e}")
