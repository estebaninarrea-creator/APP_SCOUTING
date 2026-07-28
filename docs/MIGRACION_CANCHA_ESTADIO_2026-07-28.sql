-- Migracion de modelo: Cancha como catalogo y relacion desde Estadio.
-- Fecha: 2026-07-28
-- Ejecutar en una ventana de mantenimiento y con backup previo.

BEGIN;

-- 1) Extender estructura de canchas para nuevo contrato.
ALTER TABLE canchas
  ADD COLUMN IF NOT EXISTS descripcion TEXT;

-- 2) Mover relacion a estadios.
ALTER TABLE estadios
  ADD COLUMN IF NOT EXISTS cancha_id UUID NULL;

-- 3) Migrar valores existentes (si habia una cancha por estadio).
--    Toma la primera cancha encontrada por estadio.
UPDATE estadios e
SET cancha_id = x.id
FROM (
  SELECT DISTINCT ON (c.estadio_id) c.estadio_id, c.id
  FROM canchas c
  WHERE c.estadio_id IS NOT NULL
  ORDER BY c.estadio_id, c.created_at ASC
) x
WHERE e.id = x.estadio_id
  AND e.cancha_id IS NULL;

-- 4) Crear FK nueva desde estadios hacia canchas.
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'fk_estadio_cancha'
  ) THEN
    ALTER TABLE estadios
      ADD CONSTRAINT fk_estadio_cancha
      FOREIGN KEY (cancha_id)
      REFERENCES canchas(id)
      ON UPDATE CASCADE
      ON DELETE RESTRICT;
  END IF;
END $$;

-- 5) Eliminar FK vieja cancha -> estadio.
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'fk_cancha_estadio'
  ) THEN
    ALTER TABLE canchas DROP CONSTRAINT fk_cancha_estadio;
  END IF;
END $$;

-- 6) Eliminar columnas antiguas de cancha.
ALTER TABLE canchas DROP COLUMN IF EXISTS estadio_id;
ALTER TABLE canchas DROP COLUMN IF EXISTS tipo_superficie;
ALTER TABLE canchas DROP COLUMN IF EXISTS iluminacion;
ALTER TABLE canchas DROP COLUMN IF EXISTS habilitada;

COMMIT;
