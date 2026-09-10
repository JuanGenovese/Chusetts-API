CREATE OR REPLACE FUNCTION sp_actualizar_datos_usuario(
    p_id INT,
    p_nombre VARCHAR(100) DEFAULT NULL,
    p_apellido VARCHAR(100) DEFAULT NULL,
    p_dni VARCHAR(20) DEFAULT NULL
) RETURNS table (
    id INT,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    rol_id INT,
    activo BOOL
) LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM public."USUARIOS" u WHERE u.id = p_id
    ) THEN
        RAISE EXCEPTION 'El usuario con ID % no existe.', p_id;
    END IF;

    IF p_dni IS NOT NULL AND EXISTS (
        SELECT 1 FROM public."USUARIOS" u WHERE u.dni = p_dni AND u.id <> p_id
    ) THEN
        RAISE EXCEPTION 'El DNI % ya pertenece a otro usuario.', p_dni;
    END IF;

    UPDATE public."USUARIOS" u
    SET
        nombre   = COALESCE(p_nombre, u.nombre),
        apellido = COALESCE(p_apellido, u.apellido),
        dni = COALESCE(p_dni, u.dni)
    WHERE u.id = p_id;
    
    RETURN QUERY
    SELECT
        u."id",
        u."nombre",
        u."apellido", 
        u."dni", 
        u."rol_id", 
        u."activo"
    FROM public."USUARIOS" u
    WHERE u.id = p_id;
END;
$$;