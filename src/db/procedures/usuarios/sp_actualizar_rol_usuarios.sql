CREATE OR REPLACE FUNCTION sp_actualizar_rol_usuario(
    p_id INT,
    p_rol_id INT
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

    IF NOT EXISTS (
        SELECT 1 FROM public."ROLES" r WHERE r.id = p_rol_id
    ) THEN
        RAISE EXCEPTION 'El rol con ID % no existe.', p_rol_id;
    END IF;

    UPDATE public."USUARIOS" u
    SET
        rol_id = p_rol_id
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