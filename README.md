# Distributed Prime Generator System

Este repositorio contiene una arquitectura distribuida basada en microservicios, workers, una cola de mensajes y una base de datos, todo desplegado sobre Kubernetes.

## Componentes obligatorios incluidos en este proyecto

- Microservicio New recibe cantidad y dígitos y crea una solicitud.
- Microservicio Status: informa el progreso de una solicitud.
- Microservicio Result: entrega la lista de números primos generados.
- Workers: consumen solicitudes desde la cola y generan números primos sin repetir por solicitud.
- Base de Datos PostgreSQL
- Cola de Mensajes Redis
- Manifiestos de Kubernetes para todos los componentes.


   #                                             Primes Distributed System COMO MONTAR DESDE CERO

Este proyecto permite generar números primos grandes de manera distribuida usando microservicios, workers, Redis y PostgreSQL, desplegado en Kubernetes.

##              FASE 1:     IMÁGENES
-
-
-
-

**1️ Construir imágenes localmente**

Windows / PowerShell y Ubuntu/Linux:

docker build -t tuusuario/primes-new:1.0 ./microservices/new
docker build -t tuusuario/primes-status:1.0 ./microservices/status
docker build -t tuusuario/primes-result:1.0 ./microservices/result
docker build -t tuusuario/primes-worker:1.0 ./workers


**2 Loguearse en Docker Hub**

docker login

**3 Subir las imágenes al repositorio**

docker push tuusuario/primes-new:1.0
docker push tuusuario/primes-status:1.0
docker push tuusuario/primes-result:1.0
docker push tuusuario/primes-worker:1.0


-
-
-
-

##          FASE 2:     APLICAR EN KUBERNETES

-
-
-
-

**1 Crear namespace**

kubectl create namespace primes

**2 Aplicar los manifests de infraestructura (Redis y Postgres)**

kubectl apply -n primes -f manifests/redis.yaml
kubectl apply -n primes -f manifests/postgres.yaml

**3 Inicializar la base de datos**

Copiar el script `init.sql` al pod:
Windows / PowerShell:

powershell: 
    kubectl cp db/scripts/init.sql primes/postgres-6f96978bb8-dg4g4:/init.sql -n primes

Ubuntu / Linux:: 
    kubectl cp db/scripts/init.sql primes/postgres-6f96978bb8-dg4g4:/init.sql -n primes


**Entrar al pod y ejecutar psql:**

kubectl exec -n primes -it postgres-6f96978bb8-dg4g4 -- psql -U primesuser -d primesdb


Dentro de psql:

\i /init.sql
\dt         <----- Para verificar que las tablas se crearon


### 4 Aplicar los manifests de microservicios

kubectl apply -n primes -f manifests/microservices-new.yaml
kubectl apply -n primes -f manifests/microservices-status.yaml
kubectl apply -n primes -f manifests/microservices-result.yaml

### 5 Aplicar el manifest de workers

kubectl apply -n primes -f manifests/workers.yaml

### 6 Verificar el estado de los pods

kubectl get pods -n primes

### 7 Revisar logs de pods para identificar errores

kubectl logs -n primes pod/primes-new-6cf876f5b7-4knrl
kubectl logs -n primes pod/primes-status-76765449c-9stkh
kubectl logs -n primes pod/primes-result-c78fff485-zwktj
kubectl logs -n primes pod/primes-workers-667b5dd9bb-xp84h

### 8 Documentación de FastAPI de los microservicios

## DOCUMENTACION de FastAPI de los microservicios 
primes-new. ---> http://localhost:30000/docs

primes-result. ---> http://localhost:30002/docs

primes-status ---> http://localhost:30001/docs
-
-
-
-

##              FASE 3:     PRUEBAS

-
-
-
-

### 1 Crear nueva solicitud (POST)

**Windows / PowerShell:**

powershell: 
    Invoke-RestMethod -Method Post -Uri http://localhost:30000/new `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body '{"cantidad":10,"digitos":12}'


Ubuntu / Linux:
    curl -X POST http://localhost:30000/new \
    -H "Content-Type: application/json" \
    -d '{"cantidad":10,"digitos":12}'


### 2 Obtener resultados -----  Reemplaza `<ID>` con el ID que devuelve el POST.

### PUEDES SI QUIERES USAR SIMPLEMENTE el script

powershell:
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\get-primes.ps1


 Ubuntu:
    sudo apt update && sudo apt install -y jq
    chmod +x get-primes.sh
    ./get-primes.sh


### O PROBAR TODO CON LOS SIGUINTES COMANDOS: -----  Reemplaza `<ID>` con el ID que devuelve el POST.

Windows / PowerShell:
powershell:
    Invoke-RestMethod -Method Get -Uri "http://localhost:30002/result/<ID>"     <----- Reemplaza `<ID>` con el ID que devuelve el POST. 


Ubuntu / Linux:
    curl http://localhost:30002/result/<ID>     <----- Reemplaza `<ID>` con el ID que devuelve el POST. 


Ejemplo:
powershell: 
    Invoke-RestMethod -Method Get -Uri "http://localhost:30002/result/740fa159-858e-4cdd-aa8f-d7db5d15e46b"


### 3 Consultar estado de la solicitud -----  Reemplaza `<ID>` con el ID que devuelve el POST.

Devuelve:

> * `total` = número total de primos solicitados
> * `actual` = número de primos generados hasta el momento

Windows / PowerShell:
powershell
    nvoke-RestMethod -Method Get -Uri http://localhost:30001/status/<ID> <----- Reemplaza `<ID>` con el ID que devuelve el POST. 

Ubuntu / Linux:
    curl http://localhost:30001/status/<ID> <----- Reemplaza `<ID>` con el ID que devuelve el POST. 


Ejemplo:

powershell
Invoke-RestMethod -Method Get -Uri http://localhost:30001/status/740fa159-858e-4cdd-aa8f-d7db5d15e46b

