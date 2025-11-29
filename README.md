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

Este archivo será completado con instrucciones de instalación, despliegue y pruebas.
