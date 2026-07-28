from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('GET /maestros/', client.get('/maestros/').status_code)
print('GET /jugadores/', client.get('/jugadores/').status_code)
print('POST /maestros/provincias', client.post('/maestros/provincias', json={'nombre': 'Buenos Aires'}).status_code)
print('POST /maestros/posiciones', client.post('/maestros/posiciones', json={'nombre': 'Lateral Derecho', 'codigo': 'LD'}).status_code)
print('POST /maestros/ciudades', client.post('/maestros/ciudades', json={'nombre': 'La Plata', 'provincia_id': None}).status_code)
