CREATE OR REPLACE FUNCTION sp_get_reporte_inicial(
    p_fecha_inicio DATE,
    p_fecha_fin DATE
) RETURNS TABLE (
    ingresos NUMERIC,
    egresos NUMERIC,
    resultado NUMERIC
) LANGUAGE plpgsql AS $$
DECLARE
    v_ingresos NUMERIC;
    v_egresos_gastos NUMERIC;
    v_egresos_compras NUMERIC;
    v_egresos NUMERIC;
BEGIN
    -- Sumar ingresos por ventas
    SELECT COALESCE(SUM(m.monto_total), 0)
    INTO v_ingresos
    FROM public."MOVIMIENTOS" m
    JOIN public."TIPOS_MOVIMIENTOS" tm ON m.tipo_id = tm.id
    WHERE tm.tipo = 'VENTA'
      AND m.fecha::DATE BETWEEN p_fecha_inicio AND p_fecha_fin;

    -- Sumar egresos por gastos que afectan caja
    SELECT COALESCE(SUM(mg.importe), 0)
    INTO v_egresos_gastos
    FROM public."MOVIMIENTOS_GASTO" mg
    JOIN public."MOVIMIENTOS" m ON mg.movimiento_id = m.id
    WHERE mg.afecta_caja = TRUE
      AND m.fecha::DATE BETWEEN p_fecha_inicio AND p_fecha_fin;

    -- Sumar egresos por compras que afectan caja
    SELECT COALESCE(SUM(mc.costo_total), 0)
    INTO v_egresos_compras
    FROM public."MOVIMIENTOS_COMPRA" mc
    JOIN public."MOVIMIENTOS" m ON mc.movimiento_id = m.id
    WHERE mc.afecta_caja = TRUE
      AND m.fecha::DATE BETWEEN p_fecha_inicio AND p_fecha_fin;

    v_egresos := v_egresos_gastos + v_egresos_compras;

    RETURN QUERY SELECT v_ingresos, v_egresos, (v_ingresos - v_egresos);
END;
$$;