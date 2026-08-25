CREATE OR REPLACE FUNCTION sp_crear_movimiento_caja(
    p_turno_caja_id INT,
    p_tipo_id INT,
    p_monto NUMERIC
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INT;
BEGIN
    IF p_turno_caja_id IS NULL THEN
        RAISE EXCEPTION 'El turno_caja_id no puede ser nulo';
    END IF;
    IF p_monto IS NULL OR p_monto <= 0 THEN
        RAISE EXCEPTION 'El monto debe ser mayor a cero';
    END IF;

    INSERT INTO public."MOVIMIENTOS" (
      turno_caja_id, 
      tipo_id,
      monto_total, 
      fecha
    )
    VALUES (
      p_turno_caja_id, 
      p_tipo_id, 
      p_monto,
      NOW()
    )
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;