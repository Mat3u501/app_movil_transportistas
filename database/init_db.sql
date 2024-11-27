CREATE DATABASE transportistas_app;

USE transportistas_app;

-- Tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('transportista', 'bocamina') NOT NULL
);

-- Tabla de turnos
CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehiculo VARCHAR(50),
    matricula VARCHAR(20),
    fecha_turno DATETIME NOT NULL,
    estado ENUM('pendiente', 'cancelado', 'completado') DEFAULT 'pendiente',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
