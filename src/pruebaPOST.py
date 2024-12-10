import requests

data = {
    "operator_id": "1234",
    "name": "nombrePrueba",
    "phone": "12345678",
    "email": "email@gmail.com"
}

try:
    response = requests.post("https://realtime.bucr.digital/api/operator",
                             json=data)
    print(response.status_code)
    if response.status_code == 200:
        print("Datos enviados exitosamente a la API.")
    else:
        print(f"Error al enviar datos: \
              {response.status_code} - {response.text}")
except requests.RequestException as e:
    print(f"Excepción al enviar datos a la API: {e}")
