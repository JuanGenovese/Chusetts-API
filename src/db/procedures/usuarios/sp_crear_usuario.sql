CREATE OR REPLACE FUNCTION sp_crear_usuario(
    p_nombre VARCHAR(50),
    p_apellido VARCHAR(50),
    p_dni VARCHAR(20),
    p_rol_id INT
) RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
    v_usuario_id INT;
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM public."USUARIOS" 
        WHERE dni = p_dni
    ) THEN  
        RAISE EXCEPTION 'El DNI % ya se encuentra registrado.', p_dni;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM public."ROLES" WHERE id = p_rol_id
    ) THEN
        RAISE EXCEPTION 'El rol con ID % no existe.', p_rol_id;
    END IF;

    INSERT INTO public."USUARIOS" (
        nombre,
        apellido,
        dni,
        rol_id,
        activo
    ) VALUES (
        p_nombre,
        p_apellido,
        p_dni,
        p_rol_id,
        TRUE
    )
    RETURNING id INTO v_usuario_id;

    RETURN v_usuario_id;
END;
$$;
