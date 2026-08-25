CREATE OR REPLACE FUNCTION sp_actualizar_rol_usuario_adm(
    p_id INT,
    p_rol_adm_id INT
) RETURNS table (
    id INT,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    rol_adm_id INT,
    activo BOOL
) LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM public."USUARIOS_ADM" ua WHERE ua.id = p_id
    ) THEN
        RAISE EXCEPTION 'El usuario con ID % no existe.', p_id;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM public."ROLES_ADM" WHERE id = p_rol_adm_id
    ) THEN
        RAISE EXCEPTION 'El rol ADM con ID % no existe.', p_rol_adm_id;
    END IF;

    UPDATE public."USUARIOS_ADM" ua
    SET
        rol_adm_id = p_rol_adm_id
    WHERE ua.id = p_id;
    
    RETURN QUERY
    SELECT
        ua.id,
        ua.nombre,
        ua.apellido, 
        ua.dni, 
        ua.rol_adm_id, 
        ua.activo
    FROM public."USUARIOS_ADM" ua
    WHERE ua.id = p_id;
END;
$$;