# 🚗 Parqueadero Autos Colombia

Sistema web de gestión para parqueadero mensual que permite administrar usuarios, celdas, entradas, salidas y pagos de manera eficiente.

---

# 📌 Descripción

Aplicación web desarrollada con Flask para el control integral de un parqueadero. Incluye funcionalidades completas para la gestión operativa y visualización del estado del sistema.

---

# 🛠️ Tecnologías utilizadas

- Python (Flask)
- SQL Server
- HTML5
- CSS3
- JavaScript

---

# ⚙️ Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/Davidcalle77/SISTEMA-DE-GESTI-N-DE-PARQUEADERO.git
cd SISTEMA-DE-GESTI-N-DE-PARQUEADERO
# Parqueadero Autos Colombia - Sistema de Gestión 🚗

[cite_start]Este repositorio contiene el diseño y la documentación técnica del sistema de información para el **Parqueadero Autos Colombia**, desarrollado bajo una metodología iterativa e incremental (Scrum)[cite: 21, 77].

## 👥 Autores
* [cite_start]**Juan David Calle Correa** [cite: 3]
* [cite_start]**Edinson Mena** [cite: 4]

## 🛠️ Sobre el Proyecto
[cite_start]El sistema busca modernizar las operaciones diarias del parqueadero, eliminando registros manuales y centralizando la información en una arquitectura robusta de tres capas[cite: 15, 74].

### Iteración 3: Gestión de Pagos (Actual)
[cite_start]Esta fase final consolida el componente económico del negocio[cite: 17, 68]:
* [cite_start]**Registro de Pagos:** Control de cobros mensuales y selección de métodos (Efectivo, Transferencia, PSE)[cite: 18].
* [cite_start]**Cálculo Automático de Pagos:** Sistema inteligente que calcula automáticamente el valor a pagar según el tiempo de permanencia del vehículo en la celda, sin necesidad de ingreso manual.
  - Obtiene la fecha de entrada desde `celdas.fecha_asignacion` o `entradas_salidas.fecha_hora`
  - Calcula horas transcurridas desde entrada hasta el momento actual
  - Aplica tarifa configurable (por defecto $2,000 por hora, mínimo 1 hora)
  - Muestra resultado en tiempo real desde la interfaz del modal de celdas
* [cite_start]**Control de Cartera:** Identificación de usuarios al día, próximos a vencer y morosos[cite: 18].
* [cite_start]**Notificaciones:** Sistema automático de alertas de vencimiento mediante tareas programadas[cite: 29, 52].
* [cite_start]**Reportes:** Dashboard administrativo con KPIs de recaudación mensual[cite: 28, 40].

## 🏗️ Arquitectura del Sistema
[cite_start]El diseño sigue los estándares UML 2.5 y se divide en[cite: 21, 54]:
1. [cite_start]**Presentación:** Frontend Web (UI para Pagos, Entradas/Salidas y Dashboard)[cite: 56, 59].
2. [cite_start]**Lógica de Negocio:** API REST con controladores y servicios (Flask)[cite: 57, 60].
3. [cite_start]**Persistencia:** Base de Datos relacional en PostgreSQL[cite: 58, 61].

## 📂 Contenido del Repositorio
* [cite_start]`/docs`: Documentación detallada de requerimientos y plan de pruebas[cite: 20, 62].
* [cite_start]`/design`: Mockups de alta fidelidad realizados en Figma[cite: 33, 34].
* [cite_start]`/diagrams`: Diagramas de secuencia y componentes actualizados que integran las 3 iteraciones[cite: 41, 53].

## 📚 Referencias Principales
* [cite_start]Pressman & Maxim (2021) - Ingeniería del Software[cite: 87].
* [cite_start]Sommerville (2016) - Software Engineering[cite: 89].
* [cite_start]Schwaber & Sutherland (2020) - Guía de Scrum[cite: 88].

## Estados del usuario
"""
USUARIO ACTIVO

Es un cliente que tiene mensualidad vigente en el parqueadero
Tiene una celda asignada (espacio físico reservado para su vehículo)
Puede registrar pagos mensuales
Aparece en el listado de usuarios activos
Su celda figura como ocupada en el mapa de celdas


USUARIO INACTIVO

Es un cliente que dejó de usar el servicio del parqueadero
Su registro no se elimina de la base de datos (se conserva por trazabilidad histórica)
Su celda se libera automáticamente y queda disponible para otro usuario
No puede recibir pagos mientras esté inactivo
Solo el Administrador puede inactivar un usuario
"""
