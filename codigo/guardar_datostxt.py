import serial				# Se importa librería Serial

# Configuración puerto serial
port = '/dev/serial0'			# Se define puerto
baudrate = 9600				# Frecuencia/velocidad de trabajo

output_file = 'gps_data.txt'		# Se crea una rchivo donde se guarda la info

ser = serial.Serial(port, baudrate, timeout=1) # Se abre puerto serial

try:
	with open(output_file, 'a') as file:
		print(f"Guardando datos en {output_file}. Presione CTRL+C para salir.")
		while True:
			line = ser.readline().decode('ascii', errors='replace').strip()
			if line:
				print(line)
				file.write(line + '\n')
except KeyboardInterrupt:
	print("\nPrograma interrupido. Cerrando...")
finally:
	ser.close()

