CREATE OR REPLACE FUNCTION sp_cargar_gasto(
    p_turno_caja_id INT,
    p_tipo_movimiento_id INT,
    p_concepto VARCHAR(255),
    p_importe NUMERIC(12, 2),
    p_afecta_caja BOOLEAN DEFAULT TRUE
) RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
    v_movimiento_id INT;
    v_gasto_id INT;
BEGIN
    IF p_importe <= 0 THEN
        RAISE EXCEPTION 'El importe debe ser mayor a cero.';
    END IF;

    -- 1. Insertar en MOVIMIENTOS
    INSERT INTO public."MOVIMIENTOS" (
        turno_caja_id,
        tipo_id,
        monto_total,
        fecha
    ) VALUES (
        p_turno_caja_id,
        p_tipo_movimiento_id,
        p_importe,
        NOW()
    ) RETURNING id INTO v_movimiento_id;

    -- 2. Insertar en MOVIMIENTOS_GASTO
    INSERT INTO public."MOVIMIENTOS_GASTO" (
        movimiento_id,
        concepto,
        importe,
        afecta_caja
    ) VALUES (
        v_movimiento_id,
        p_concepto,
        p_importe,
        p_afecta_caja
    ) RETURNING id INTO v_gasto_id;

    RETURN v_gasto_id;
END;
$$;
