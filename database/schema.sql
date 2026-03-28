-- =============================================
-- Parqueadero Autos Colombia - Schema SQL Server
-- Ejecutar en SQL Server Management Studio
-- =============================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'ParqueaderoAutoColombia')
    CREATE DATABASE ParqueaderoAutoColombia;
GO

USE ParqueaderoAutoColombia;
GO

-- Tabla usuarios
IF OBJECT_ID('usuarios','U') IS NULL
CREATE TABLE usuarios (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    cedula         VARCHAR(20)   NOT NULL UNIQUE,
    nombre         VARCHAR(100)  NOT NULL,
    telefono       VARCHAR(20)   NOT NULL,
    correo         VARCHAR(100)  NULL,
    tipo_vehiculo  VARCHAR(10)   NOT NULL CHECK (tipo_vehiculo IN ('auto','moto')),
    placa          VARCHAR(10)   NOT NULL UNIQUE,
    estado         VARCHAR(10)   NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo','inactivo')),
    fecha_registro DATETIME      NOT NULL DEFAULT GETDATE(),
    fecha_baja     DATETIME      NULL
);
GO

-- Tabla celdas
IF OBJECT_ID('celdas','U') IS NULL
CREATE TABLE celdas (
    id               INT IDENTITY(1,1) PRIMARY KEY,
    codigo           VARCHAR(10)  NOT NULL UNIQUE,
    tipo             VARCHAR(10)  NOT NULL CHECK (tipo IN ('auto','moto')),
    sector           VARCHAR(5)   NOT NULL,
    estado           VARCHAR(15)  NOT NULL DEFAULT 'libre' CHECK (estado IN ('libre','ocupada','mantenimiento')),
    usuario_id       INT          NULL REFERENCES usuarios(id),
    fecha_asignacion DATETIME     NULL
);
GO

-- Tabla mantenimientos
IF OBJECT_ID('mantenimientos','U') IS NULL
CREATE TABLE mantenimientos (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    celda_id     INT          NOT NULL REFERENCES celdas(id),
    motivo       VARCHAR(200) NOT NULL,
    fecha_inicio DATETIME     NOT NULL DEFAULT GETDATE(),
    fecha_fin    DATETIME     NULL
);
GO

-- Tabla entradas_salidas
IF OBJECT_ID('entradas_salidas','U') IS NULL
CREATE TABLE entradas_salidas (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    placa          VARCHAR(10)  NOT NULL,
    tipo_vehiculo  VARCHAR(10)  NOT NULL CHECK (tipo_vehiculo IN ('auto','moto')),
    tipo_registro  VARCHAR(10)  NOT NULL CHECK (tipo_registro IN ('entrada','salida')),
    celda_id       INT          NULL REFERENCES celdas(id),
    usuario_id     INT          NULL REFERENCES usuarios(id),
    fecha_hora     DATETIME     NOT NULL DEFAULT GETDATE(),
    observacion    VARCHAR(200) NULL
);
GO

-- Tabla pagos
IF OBJECT_ID('pagos','U') IS NULL
CREATE TABLE pagos (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id  INT           NOT NULL REFERENCES usuarios(id),
    monto       DECIMAL(10,2) NOT NULL,
    fecha_pago  DATETIME      NOT NULL DEFAULT GETDATE(),
    mes_pagado  VARCHAR(20)   NOT NULL,
    estado      VARCHAR(10)   NOT NULL DEFAULT 'pagado' CHECK (estado IN ('pagado','pendiente')),
    observacion VARCHAR(200)  NULL
);
GO

-- Insertar celdas iniciales si no existen
IF NOT EXISTS (SELECT 1 FROM celdas)
BEGIN
    INSERT INTO celdas (codigo,tipo,sector) VALUES
    ('A-01','auto','A'),('A-02','auto','A'),('A-03','auto','A'),
    ('A-04','auto','A'),('A-05','auto','A'),('A-06','auto','A'),
    ('A-07','auto','A'),('A-08','auto','A'),('A-09','auto','A'),
    ('A-10','auto','A'),('A-11','auto','A'),('A-12','auto','A'),
    ('B-01','moto','B'),('B-02','moto','B'),('B-03','moto','B'),
    ('B-04','moto','B'),('B-05','moto','B'),('B-06','moto','B'),
    ('B-07','moto','B'),('B-08','moto','B');
    PRINT 'Celdas insertadas correctamente';
END
GO

PRINT 'Base de datos lista';
GO
