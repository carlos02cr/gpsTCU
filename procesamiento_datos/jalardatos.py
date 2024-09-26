import json
def extract_gprmc_from_file(path):
    gprmc_lineas = []
    with open(path, 'r') as file:
        for lineas in file:
            lineas = lineas.strip()
            if lineas.startswith("$GPRMC"):
                gprmc_lineas.append(lineas)
    
    return gprmc_lineas

def save_gprmc_to_json(gprmc_lineas, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(gprmc_lineas, json_file, indent=4)


path = 'gps_data.txt'  
output_file = 'gprmc_data.json'  
gprmc_lineas = extract_gprmc_from_file(path)
save_gprmc_to_json(gprmc_lineas, output_file)
print(f"Se han guardado {len(gprmc_lineas)} líneas GPRMC en {output_file}.")
