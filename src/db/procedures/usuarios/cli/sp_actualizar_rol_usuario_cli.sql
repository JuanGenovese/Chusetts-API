CREATE OR REPLACE FUNCTION sp_actualizar_rol_usuario_cli(
    p_id INT,
    p_rol_id INT
) RETURNS table (
    id INT,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    email VARCHAR,
    telefono VARCHAR,
    fecha_nac DATE,
    rol_cli_id INT,
    activo BOOL
) LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM public."USUARIOS_CLI" uc WHERE uc.id = p_id
    ) THEN
        RAISE EXCEPTION 'El usuario cliente con ID % no existe.', p_id;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM public."ROLES_CLI" rc WHERE rc.id = p_rol_id
    ) THEN
        RAISE EXCEPTION 'El rol de cliente con ID % no existe.', p_rol_id;
    END IF;

    UPDATE public."USUARIOS_CLI" uc
    SET
        rol_cli_id = p_rol_id
    WHERE uc.id = p_id;

    RETURN QUERY
    SELECT
        uc.id,
        uc.nombre,
        uc.apellido, 
        uc.dni, 
        uc.email,
        uc.telefono,
        uc.fecha_nac,
        uc.rol_cli_id, 
        uc.activo
    FROM public."USUARIOS_CLI" uc
    WHERE uc.id = p_id;
END;
$$;
