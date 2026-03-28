# Parqueadero Autos Colombia

Sistema web de gestion para parqueadero mensual.
**Stack:** Python (Flask) + HTML/CSS/JavaScript + SQL Server

## Pasos para ejecutar

### 1. Activar entorno virtual e instalar dependencias
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Ejecutar el schema en SQL Server
Abre SQL Server Management Studio y ejecuta:
```
database/schema.sql
```

### 3. Configurar .env
Edita el archivo `.env` con tus datos:
```
DB_SERVER=localhost
DB_DATABASE=ParqueaderoAutoColombia
DB_USERNAME=sa
DB_PASSWORD=TU_PASSWORD
```

### 4. Correr la aplicacion
```bash
python run.py
```
Abre: **http://localhost:5000**

## Modulos
| Modulo | URL |
|--------|-----|
| Panel | / |
| Usuarios | /usuarios |
| Celdas | /celdas |
| Entradas/Salidas | /entradas |
| Pagos | /pagos |

## Integrantes
- Juan David Calle Correa
- Edinson Mena

Universidad Digital de Antioquia — Ingenieria de Software 2025
