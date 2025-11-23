-- Script para actualizar la tabla time_sessions con los nuevos campos

-- Agregar columnas faltantes si no existen
ALTER TABLE time_sessions 
ADD COLUMN IF NOT EXISTS is_paused BOOLEAN DEFAULT FALSE;

ALTER TABLE time_sessions 
ADD COLUMN IF NOT EXISTS resumed_at DATETIME NULL;

ALTER TABLE time_sessions 
ADD COLUMN IF NOT EXISTS last_activity_at DATETIME NULL;

ALTER TABLE time_sessions 
ADD COLUMN IF NOT EXISTS ended_at DATETIME NULL;

-- Actualizar valores por defecto para registros existentes
UPDATE time_sessions 
SET is_paused = FALSE 
WHERE is_paused IS NULL;

UPDATE time_sessions 
SET last_activity_at = started_at 
WHERE last_activity_at IS NULL AND started_at IS NOT NULL;

-- Asegurar que duration_seconds tenga valor por defecto
UPDATE time_sessions 
SET duration_seconds = 0 
WHERE duration_seconds IS NULL;

-- Asegurar que is_active tenga valor por defecto
UPDATE time_sessions 
SET is_active = FALSE 
WHERE is_active IS NULL;
