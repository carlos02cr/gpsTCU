# processing_functions.py
def process_gprmc_message(message):
    """
    Processes a GPRMC message by parsing it and performing desired actions.

    :param message: Raw GPRMC NMEA sentence.
    """
    gprmc_data = parse_gprmc(message)
    if gprmc_data:
        # Example action: Log to a separate file
        log_gprmc_data(gprmc_data)

        # Example action: Send data to an external service
        # send_to_service(gprmc_data)

def parse_gprmc(message):
    """
    Parses a GPRMC NMEA sentence and extracts relevant data.

    :param message: Raw GPRMC NMEA sentence.
    :return: Dictionary with parsed data or None if parsing fails.
    """
    parts = message.split(',')
    if len(parts) < 12:
        print("Mensaje GPRMC incompleto.")
        return None
    try:
        gprmc_data = {
            'time_utc': parts[1],
            'status': parts[2],
            'latitude': convert_to_decimal_degrees(parts[3], parts[4]),
            'longitude': convert_to_decimal_degrees(parts[5], parts[6]),
            'speed_knots': parts[7],
            'track_angle': parts[8],
            'date': parts[9],
            'magnetic_variation': parts[10],
            'magnetic_var_direction': parts[11].split('*')[0]  # Remove checksum
        }
        return gprmc_data
    except (IndexError, ValueError) as e:
        print(f"Error al analizar el mensaje GPRMC: {e}")
        return None

def convert_to_decimal_degrees(raw_value, direction):
    """
    Converts NMEA coordinate format to decimal degrees.

    :param raw_value: Raw coordinate value from NMEA sentence.
    :param direction: Direction character ('N', 'S', 'E', 'W').
    :return: Decimal degrees as float or None if conversion fails.
    """
    try:
        if not raw_value:
            return None
        degrees = int(raw_value[:2])
        minutes = float(raw_value[2:])
        decimal_degrees = degrees + minutes / 60
        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        return decimal_degrees
    except ValueError as e:
        print(f"Error al convertir coordenadas: {e}")
        return None

def log_gprmc_data(data):
    """
    Logs the parsed GPRMC data to a separate log file.

    :param data: Dictionary containing parsed GPRMC data.
    """
    with open('gprmc_log.txt', 'a') as log_file:
        log_file.write(f"{data}\n")
