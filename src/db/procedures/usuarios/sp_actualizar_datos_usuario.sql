CREATE OR REPLACE FUNCTION sp_actualizar_datos_usuario_adm(
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
        SELECT 1 FROM public."USUARIOS_ADM" ua WHERE ua.id = p_id
    ) THEN
        RAISE EXCEPTION 'El usuario con ID % no existe.', p_id;
    END IF;

    IF p_dni IS NOT NULL AND EXISTS (
        SELECT 1 FROM public."USUARIOS_ADM" ua WHERE ua.dni = p_dni AND ua.id <> p_id
    ) THEN
        RAISE EXCEPTION 'El DNI % ya pertenece a otro usuario.', p_dni;
    END IF;

    UPDATE public."USUARIOS_ADM" ua
    SET
        nombre   = COALESCE(p_nombre, ua.nombre),
        apellido = COALESCE(p_apellido, ua.apellido),
        dni = COALESCE(p_dni, ua.dni)
    WHERE ua.id = p_id;
    
    RETURN QUERY
    SELECT
        ua."id",
        ua."nombre",
        ua."apellido", 
        ua."dni", 
        ua."rol_adm_id", 
        ua."activo"
    FROM public."USUARIOS_ADM" ua
    WHERE ua.id = p_id;
END;
$$;