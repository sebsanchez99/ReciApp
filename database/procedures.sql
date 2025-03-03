USE ReciApp;
-- USUARIOS
-- CREAR UN USUARIO
CREATE PROCEDURE sp_crear_usuario(
    IN p_nombre VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_contraseña VARCHAR(255),
    IN p_documento VARCHAR(50),
    IN p_tipo_documento_id INT,
    IN p_rol_id INT
)
BEGIN
    INSERT INTO usuario (nombre, email, contraseña, documento, tipo_documento_id, rol_id) 
    VALUES (p_nombre, p_email, p_contraseña, p_documento, p_tipo_documento_id, p_rol_id);
END //

-- LISTAR USUARIOS
CREATE PROCEDURE sp_listar_usuarios()
BEGIN
    SELECT u.id, u.nombre, u.email, u.documento, td.nombre AS tipo_documento, r.nombre AS rol, u.fecha_registro 
    FROM usuario u
    JOIN tipo_documento td ON u.tipo_documento_id = td.id
    JOIN rol r ON u.rol_id = r.id;
END //


-- OBTENER UN USUARIO POR ID 
CREATE PROCEDURE sp_obtener_usuario(IN p_id INT)
BEGIN
    SELECT u.id, u.nombre, u.email, u.documento, td.nombre AS tipo_documento, r.nombre AS rol, u.fecha_registro 
    FROM usuario u
    JOIN tipo_documento td ON u.tipo_documento_id = td.id
    JOIN rol r ON u.rol_id = r.id
    WHERE u.id = p_id;
END //

-- OBTIENE DATOS USUARIOS USANDO EL CORREO ELECTRÓNICO
CREATE PROCEDURE sp_obtener_usuario_por_email(IN p_email VARCHAR(100))
BEGIN
    SELECT u.id, u.nombre, u.email, u.contraseña, u.documento, td.nombre AS tipo_documento, 
           r.nombre AS rol, u.rol_id, u.fecha_registro 
    FROM usuario u
    JOIN tipo_documento td ON u.tipo_documento_id = td.id
    JOIN rol r ON u.rol_id = r.id
    WHERE u.email = p_email;
END //


-- ACTUALIZAR USUARIO
CREATE PROCEDURE sp_actualizar_usuario(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_rol_id INT
)
BEGIN
    UPDATE usuario 
    SET nombre = p_nombre, email = p_email, rol_id = p_rol_id
    WHERE id = p_id;
END //

CREATE PROCEDURE sp_cambiar_contraseña(
    IN p_id INT,
    IN p_nueva_contraseña VARCHAR(255)
)
BEGIN
    UPDATE usuario 
    SET contraseña = p_nueva_contraseña
    WHERE id = p_id;
END //

-- 5. ELIMINAR USUARIO
CREATE PROCEDURE sp_eliminar_usuario(IN p_id INT)
BEGIN
    DELETE FROM usuario WHERE id = p_id;
END //

-- MATERIALES
--CREA UN MATERIAL
CREATE PROCEDURE sp_crear_material(
    IN p_nombre VARCHAR(100),
    IN p_precio_por_kg DECIMAL(10,2)
)
BEGIN
    INSERT INTO material (nombre, precio_por_kg) 
    VALUES (p_nombre, p_precio_por_kg);
END //

--LISTA MATERIALES
CREATE PROCEDURE sp_listar_materiales()
BEGIN
    SELECT id, nombre, precio_por_kg FROM material;
END //

--OBTIENE MATERIAL POR ID
CREATE PROCEDURE sp_obtener_material(IN p_id INT)
BEGIN
    SELECT id, nombre, precio_por_kg 
    FROM material 
    WHERE id = p_id;
END //

-- ACTUALIZA MATERIAL
CREATE PROCEDURE sp_actualizar_material(
    IN p_id INT,
    IN p_nombre VARCHAR(100),
    IN p_precio_por_kg DECIMAL(10,2)
)
BEGIN
    UPDATE material 
    SET nombre = p_nombre, precio_por_kg = p_precio_por_kg
    WHERE id = p_id;
END //

-- ELIMINAR MATERIAL
CREATE PROCEDURE sp_eliminar_material(IN p_id INT)
BEGIN
    DELETE FROM material WHERE id = p_id;
END //

-- VENTAS
-- REGISTRAR UNA VENTA
CREATE PROCEDURE sp_registrar_venta(
    IN p_reciclador_id INT,
    IN p_material_id INT,
    IN p_peso_kg DECIMAL(10,2)
)
BEGIN
    DECLARE v_precio_por_kg DECIMAL(10,2);
    DECLARE v_precio_total DECIMAL(10,2);

    -- Obtener el precio del material
    SELECT precio_por_kg INTO v_precio_por_kg FROM material WHERE id = p_material_id;

    -- Calcular el precio total
    SET v_precio_total = v_precio_por_kg * p_peso_kg;

    -- Insertar la venta
    INSERT INTO venta (reciclador_id, material_id, peso_kg, precio_total, fecha_venta) 
    VALUES (p_reciclador_id, p_material_id, p_peso_kg, v_precio_total, NOW());
END //


-- LISTAR TODAS LAS VENTAS 
CREATE PROCEDURE sp_listar_ventas()
BEGIN
    SELECT v.id, u.nombre AS reciclador, m.nombre AS material, v.peso_kg, v.precio_total, v.fecha_venta
    FROM venta v
    JOIN usuario u ON v.reciclador_id = u.id
    JOIN material m ON v.material_id = m.id;
END //


-- REGISTRAR UNA COMPRA
CREATE PROCEDURE sp_registrar_compra(
    IN p_empresa_id INT,
    IN p_venta_id INT
)
BEGIN
    INSERT INTO compra (empresa_id, venta_id, fecha_compra) 
    VALUES (p_empresa_id, p_venta_id, NOW());
END //


-- LISTAR TODAS LAS COMPRAS 
CREATE PROCEDURE sp_listar_compras()
BEGIN
    SELECT c.id, e.nombre AS empresa, r.nombre AS reciclador, m.nombre AS material, v.precio_total, c.fecha_compra
    FROM compra c
    JOIN usuario e ON c.empresa_id = e.id
    JOIN venta v ON c.venta_id = v.id
    JOIN material m ON v.material_id = m.id
    JOIN usuario r ON v.reciclador_id = r.id;
END //


-- GENERAR UNA FACTURA
CREATE PROCEDURE sp_generar_factura(
    IN p_compra_id INT
)
BEGIN
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_numero_factura VARCHAR(50);

    -- Obtener el total de la compra
    SELECT v.precio_total INTO v_total 
    FROM compra c
    JOIN venta v ON c.venta_id = v.id
    WHERE c.id = p_compra_id;

    -- Generar número de factura único
    SET v_numero_factura = CONCAT('FAC-', p_compra_id, '-', UNIX_TIMESTAMP());

    INSERT INTO factura (compra_id, numero_factura, total, fecha_emision) 
    VALUES (p_compra_id, v_numero_factura, v_total, NOW());
END //
