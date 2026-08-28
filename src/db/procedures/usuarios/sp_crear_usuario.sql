CREATE OR REPLACE FUNCTION sp_crear_usuario_adm(
    p_nombre VARCHAR(50),
    p_apellido VARCHAR(50),
    p_dni VARCHAR(20),
    p_rol_adm_id INT
) RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
    v_usuario_id INT;
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM public."USUARIOS_ADM" 
        WHERE dni = p_dni
    ) THEN
        RAISE EXCEPTION 'El DNI % ya se encuentra registrado.', p_dni;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM public."ROLES_ADM" WHERE id = p_rol_adm_id
    ) THEN
        RAISE EXCEPTION 'El rol administrativo con ID % no existe.', p_rol_adm_id;
    END IF;

    INSERT INTO public."USUARIOS_ADM" (
        nombre,
        apellido,
        dni,
        rol_adm_id,
        activo
    ) VALUES (
        p_nombre,
        p_apellido,
        p_dni,
        p_rol_adm_id,
        TRUE
    )
    RETURNING id INTO v_usuario_id;

    RETURN v_usuario_id;
END;
$$;
