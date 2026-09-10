CREATE OR REPLACE FUNCTION sp_cambiar_estado_usuario(
    p_id INT,
    p_estado BOOLEAN
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

    UPDATE public."USUARIOS" u
    SET
        activo = p_estado
    WHERE u.id = p_id;
    
    RETURN QUERY
    SELECT
        u.id,
        u.nombre,
        u.apellido, 
        u.dni, 
        u.rol_id, 
        u.activo
    FROM public."USUARIOS" u
    WHERE u.id = p_id;
END;
$$;
