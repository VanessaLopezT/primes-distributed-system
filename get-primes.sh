# Cantidad de primos y número de dígitos
cantidad=10
digitos=12

# Crear nueva solicitud
echo "Creando nueva solicitud..."
response=$(curl -s -X POST http://localhost:30000/new \
    -H "Content-Type: application/json" \
    -d "{\"cantidad\":$cantidad,\"digitos\":$digitos}")

id=$(echo $response | jq -r '.id')

if [ "$id" == "null" ] || [ -z "$id" ]; then
    echo "Error al crear la solicitud: $response"
    exit 1
fi

echo "Solicitud creada. ID: $id"

# Esperar y consultar estado progresivamente
actual=0
total=0

echo "Esperando a que los workers generen los primos..."
while [ "$actual" -lt "$cantidad" ]; do
    sleep 2
    status=$(curl -s "http://localhost:30001/status/$id")
    actual=$(echo $status | jq -r '.actual')
    total=$(echo $status | jq -r '.total')
    echo "Estado actual: $actual de $total primos generados"
done

# Obtener resultados 
result=$(curl -s "http://localhost:30002/result/$id")

if [ -z "$result" ]; then
    echo "No se obtuvieron resultados. Verifica que los workers estén corriendo y el servicio primes-result esté accesible."
    exit 1
fi

# Mostrar resultados
echo -e "\nResultados obtenidos:"
echo "$result"
