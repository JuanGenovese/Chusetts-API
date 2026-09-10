CREATE OR REPLACE FUNCTION validar_turno_abierto()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM "TURNOS_CAJA" tc
    WHERE tc.id = NEW.turno_caja_id
      AND tc.fecha_hasta IS NULL
  ) THEN
    RAISE EXCEPTION 'El turno de caja % ya está cerrado o no existe.', NEW.turno_caja_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validar_turno_abierto ON "MOVIMIENTOS_VENTAS";

CREATE TRIGGER trg_validar_turno_abierto
  BEFORE INSERT ON "MOVIMIENTOS_VENTAS"
  FOR EACH ROW EXECUTE FUNCTION validar_turno_abierto();
