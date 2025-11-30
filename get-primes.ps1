# Cantidad de primos y número de dígitos
$cantidad = 10
$digitos = 12

# Crear nueva solicitud
try {
    $response = Invoke-RestMethod -Method Post -Uri http://localhost:30000/new `
        -Headers @{ "Content-Type" = "application/json" } `
        -Body (@{cantidad=$cantidad; digitos=$digitos} | ConvertTo-Json)
} catch {
    Write-Host "Error al crear la solicitud:" $_.Exception.Message
    exit
}

$id = $response.id
Write-Host "Solicitud creada. ID:" $id

# Esperar y mostrar estado mientras se procesan los primos
do {
    Start-Sleep -Seconds 2
    try {
        $status = Invoke-RestMethod -Method Get -Uri "http://localhost:30001/status/$id"
        Write-Host "Estado actual: $($status.actual) de $($status.total) primos generados"
    } catch {
        Write-Host "Error al consultar el estado:" $_.Exception.Message
        exit
    }
} while ($status.actual -lt $status.total)

# Obtener resultados finales
try {
    $result = Invoke-RestMethod -Method Get -Uri "http://localhost:30002/result/$id"
} catch {
    Write-Host "Error al obtener resultados:" $_.Exception.Message
    exit
}

# Mostrar resultados
if ($result -and $result.Count -gt 0) {
    Write-Host "`nResultados obtenidos:"
    $result | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "No se obtuvieron resultados."
    Write-Host "Verifica que los workers estén corriendo y que el servicio primes-result esté accesible."
}
