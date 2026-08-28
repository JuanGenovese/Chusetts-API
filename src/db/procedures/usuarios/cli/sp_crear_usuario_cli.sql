CREATE OR REPLACE FUNCTION sp_crear_usuario_cli(
    p_nombre VARCHAR(50),
    p_apellido VARCHAR(50),
    p_dni VARCHAR(20),
    p_email VARCHAR(150),
    p_telefono VARCHAR(50),
    p_fecha_nac DATE,
    p_rol_cli_id INT
) RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
    v_usuario_id INT;
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM public."USUARIOS_CLI" 
        WHERE dni = p_dni
    ) THEN
        RAISE EXCEPTION 'El DNI % ya se encuentra registrado.', p_dni;
    END IF;

    IF EXISTS (
        SELECT 1 
        FROM public."USUARIOS_CLI" 
        WHERE email = p_email
    ) THEN
        RAISE EXCEPTION 'El email % ya se encuentra registrado.', p_email;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM public."ROLES_CLI" WHERE id = p_rol_cli_id
    ) THEN
        RAISE EXCEPTION 'El rol de cliente con ID % no existe.', p_rol_cli_id;
    END IF;

    INSERT INTO public."USUARIOS_CLI" (
        nombre,
        apellido,
        dni,
        email,
        telefono,
        fecha_nac,
        rol_cli_id,
        activo
    ) VALUES (
        p_nombre,
        p_apellido,
        p_dni,
        p_email,
        p_telefono,
        p_fecha_nac,
        p_rol_cli_id,
        TRUE
    )
    RETURNING id INTO v_usuario_id;

    RETURN v_usuario_id;
END;
$$;
