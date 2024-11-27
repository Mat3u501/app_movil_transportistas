-- Datos iniciales para la tabla de usuarios
INSERT INTO users (nombre, email, password, tipo_usuario) VALUES
('Juan Pérez', 'juan.perez@example.com', '$2b$12$Lx8klVkkHqIx1CNvjkp85e8snTjDnB8WhYPZizYKx4pQWBs3u7ICW', 'transportista'), -- Contraseña: 'password123'
('Maria López', 'maria.lopez@example.com', '$2b$12$hJNRQQrUosK/Bm7Kbq/Tvuwlt.JWwhU8ZBpQPLpoREXdcft0ovXbq', 'bocamina');   -- Contraseña: 'admin123'

-- Datos iniciales para la tabla de turnos
INSERT INTO turnos (user_id, vehiculo, matricula, fecha_turno, estado) VALUES
(1, 'Camión Ford', 'ABC123', '2024-11-25 08:00:00', 'pendiente'),
(1, 'Volqueta Toyota', 'XYZ789', '2024-11-25 09:00:00', 'pendiente'),
(2, 'Camión Volvo', 'LMN456', '2024-11-26 10:30:00', 'completado');
