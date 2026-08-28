CREATE OR REPLACE FUNCTION sp_actualizar_datos_usuario_cli(
    p_id INT,
    p_nombre VARCHAR(100) DEFAULT NULL,
    p_apellido VARCHAR(100) DEFAULT NULL,
    p_dni VARCHAR(20) DEFAULT NULL,
    p_email VARCHAR(150) DEFAULT NULL,
    p_telefono VARCHAR(50) DEFAULT NULL,
    p_fecha_nac DATE DEFAULT NULL
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

    IF p_dni IS NOT NULL AND EXISTS (
        SELECT 1 FROM public."USUARIOS_CLI" uc WHERE uc.dni = p_dni AND uc.id <> p_id
    ) THEN
        RAISE EXCEPTION 'El DNI % ya pertenece a otro usuario.', p_dni;
    END IF;

    IF p_email IS NOT NULL AND EXISTS (
        SELECT 1 FROM public."USUARIOS_CLI" uc WHERE uc.email = p_email AND uc.id <> p_id
    ) THEN
        RAISE EXCEPTION 'El email % ya pertenece a otro usuario.', p_email;
    END IF;

    UPDATE public."USUARIOS_CLI" uc
    SET
        nombre    = COALESCE(p_nombre, uc.nombre),
        apellido  = COALESCE(p_apellido, uc.apellido),
        dni       = COALESCE(p_dni, uc.dni),
        email     = COALESCE(p_email, uc.email),
        telefono  = COALESCE(p_telefono, uc.telefono),
        fecha_nac = COALESCE(p_fecha_nac, uc.fecha_nac)
    WHERE uc.id = p_id;
    
    RETURN QUERY
    SELECT
        uc."id",
        uc."nombre",
        uc."apellido", 
        uc."dni", 
        uc."email",
        uc."telefono",
        uc."fecha_nac",
        uc."rol_cli_id", 
        uc."activo"
    FROM public."USUARIOS_CLI" uc
    WHERE uc.id = p_id;
END;
$$;
