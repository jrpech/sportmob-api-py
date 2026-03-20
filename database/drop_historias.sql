-- ============================================================================
-- Script para limpiar/resetear tablas de historias
-- CUIDADO: Esto eliminará TODOS los datos de historias
-- ============================================================================

USE sportmob_v2;

-- Desactivar verificación de foreign keys temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar tablas
DROP TABLE IF EXISTS historia_reaccion;
DROP TABLE IF EXISTS historia_vista;
DROP TABLE IF EXISTS historia;

-- Reactivar verificación
SET FOREIGN_KEY_CHECKS = 1;

-- Mensaje de confirmación
SELECT 'Tablas de historias eliminadas correctamente' as mensaje;

-- Ahora puedes ejecutar historias_schema.sql para recrear las tablas
