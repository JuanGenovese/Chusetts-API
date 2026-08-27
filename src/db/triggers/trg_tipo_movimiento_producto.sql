CREATE OR REPLACE FUNCTION sp_valida_tipo_movimiento_producto() RETURNS trigger AS $$
BEGIN
  IF (
    SELECT t.tipo 
    FROM "MOVIMIENTOS_VENTAS" mv 
    JOIN "MOVIMIENTOS" m ON mv.movimiento_id = m.id 
    JOIN "TIPOS_MOVIMIENTOS" t ON m.tipo_id = t.id 
    WHERE mv.id = NEW.id_movimiento_venta
  ) NOT IN ('VENTA', 'COMPRA') THEN
    RAISE EXCEPTION 'PRODUCTOS_X_MOVIMIENTOS solo admite movimientos de venta o compra';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_valida_tipo_mov_producto ON "PRODUCTOS_X_MOVIMIENTOS";

CREATE TRIGGER trg_valida_tipo_mov_producto
BEFORE INSERT OR UPDATE ON "PRODUCTOS_X_MOVIMIENTOS"
FOR EACH ROW EXECUTE FUNCTION sp_valida_tipo_movimiento_producto();