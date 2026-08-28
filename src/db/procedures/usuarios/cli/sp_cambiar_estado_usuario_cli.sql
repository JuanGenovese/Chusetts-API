CREATE OR REPLACE FUNCTION sp_cambiar_estado_usuario_cli(
    p_id INT,
    p_estado BOOLEAN
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

    UPDATE public."USUARIOS_CLI" uc
    SET
        activo = p_estado
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
