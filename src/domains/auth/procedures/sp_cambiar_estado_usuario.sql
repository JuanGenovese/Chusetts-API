CREATE OR REPLACE FUNCTION sp_cambiar_estado_usuario_adm(
    p_id INT,
    p_activo BOOLEAN
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

    UPDATE public."USUARIOS_ADM" ua
    SET
        activo = p_activo
    WHERE ua.id = p_id;
    
    RETURN QUERY
    SELECT
        ua.id,
        ua.nombre,
        ua.apellido, 
        ua.dni, 
        ua.rol_id, 
        ua.activo
    FROM public."USUARIOS_ADM" ua
    WHERE ua.id = p_id;
END;
$$;
