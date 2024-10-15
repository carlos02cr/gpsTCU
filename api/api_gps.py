import serial
import requests
import time

# Configuración del puerto serial (ajusta el nombre del puerto según sea necesario)
ser = serial.Serial('/dev/serial10', 9600, timeout=1)

# URL de la API de prueba
url = 'https://httpbin.org/post'  # Cambia esta URL por la API real cuando estés listo

def parse_gprmc(data):
    """Parsea una línea GPRMC para extraer latitud y longitud."""
    if data[0:6] == b'$GPRMC':  # Verifica si la línea es un mensaje GPRMC
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
                "journey_id": 698453,  # ID estático de un "viaje"
                "timestamp": int(time.time()),  # Marca de tiempo en segundos desde 1970
                "latitude": latitude,
                "longitude": longitude,
                "altitude": 0.0,  # Altitud (se puede cambiar si se obtiene del GPS)
                "speed": 0.0,     # Velocidad (se puede cambiar si se obtiene del GPS)
                "bearing": 0.0,   # Dirección (puede ser del GPS)
                "odometer": 0.0   # Odometer (distancia recorrida)
            }

            # Mostrar los datos en la terminal antes de enviarlos
            print(f"Datos que se enviarán: {data}")
            
            # Envía los datos a la API
            response = requests.post(url, json=data)

            # Mostrar la respuesta de la API en la terminal
            print(f"Respuesta de la API: {response.status_code}, {response.text}")
        
        time.sleep(5)  # Espera 5 segundos antes de enviar los próximos datos

    except Exception as e:
        print(f"Error: {e}")
