-- Crear la base de datos
CREATE DATABASE ReciApp;
USE ReciApp;

-- Tabla de roles
CREATE TABLE rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla tipo de documento
CREATE TABLE tipo_documento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de usuarios
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    documento VARCHAR(50) UNIQUE NOT NULL,  
    tipo_documento_id INT NOT NULL,
    rol_id INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_documento_id) REFERENCES tipo_documento(id) ON DELETE RESTRICT,
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE RESTRICT
);

-- Tabla de materiales reciclables
CREATE TABLE material (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    precio_por_kg DECIMAL(10,2) NOT NULL CHECK (precio_por_kg > 0)
);

-- Tabla de ventas (reciclador vende materiales)
CREATE TABLE venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reciclador_id INT NOT NULL,
    material_id INT NOT NULL,
    peso_kg DECIMAL(10,2) NOT NULL CHECK (peso_kg > 0),
    precio_total DECIMAL(10,2) NOT NULL CHECK (precio_total > 0),
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reciclador_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE
);

-- Tabla de compras (empresa compra materiales)
CREATE TABLE compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    venta_id INT NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (venta_id) REFERENCES venta(id) ON DELETE CASCADE
);

-- Tabla de facturas (asociada a compras)
CREATE TABLE factura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (compra_id) REFERENCES compra(id) ON DELETE CASCADE
);
