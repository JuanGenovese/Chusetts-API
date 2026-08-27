CREATE OR REPLACE FUNCTION sp_abrir_turno(
    p_usuario_adm_id INT,
    p_efectivo_inicial NUMERIC,
    p_observacion_apertura VARCHAR(100)
) RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
    v_turno_id INT;
BEGIN
    -- Validar que no exista un turno abierto previamente
    IF EXISTS (
        SELECT 1 
        FROM public."TURNOS_CAJA" 
        WHERE abierto = TRUE
    ) THEN
        RAISE EXCEPTION 'Ya existe un turno de caja abierto.';
    END IF;
    -- Insertar el nuevo turno
    INSERT INTO public."TURNOS_CAJA" (
        usuario_adm_id,
        fecha_desde,
        abierto,
        efectivo_inicial,
        observacion_apertura
    ) VALUES (
        p_usuario_adm_id,
        NOW(),
        TRUE,
        p_efectivo_inicial,
        p_observacion_apertura
    )
    RETURNING id INTO v_turno_id;
    RETURN v_turno_id;
END;
$$;