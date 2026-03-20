-- ============================================================================
-- Datos de prueba para las tablas de historias
-- ============================================================================

USE sportmob_v2;

-- Nota: Asegúrate de tener usuarios en la tabla 'usuario' primero

-- ============================================================================
-- Insertar historias de ejemplo
-- ============================================================================

-- Historia normal (expira en 24h)
INSERT INTO historia (
    usuario_id, tipo, url_archivo, url_miniatura, 
    descripcion, duracion_segundos, ancho, alto, 
    tamano_bytes, activa, destacada, fecha_expiracion
) VALUES (
    1, -- Cambia por un usuario_id real
    'imagen',
    'http://localhost:8000/uploads/historias/2026/03/20/historia_test_001.jpg',
    'http://localhost:8000/uploads/historias/miniaturas/2026/03/20/thumb_historia_test_001.jpg',
    'Mi primera historia de prueba!',
    5,
    1080,
    1920,
    524288,
    TRUE,
    FALSE,
    DATE_ADD(NOW(), INTERVAL 24 HOUR)
);

-- Historia destacada (no expira)
INSERT INTO historia (
    usuario_id, tipo, url_archivo, url_miniatura,
    descripcion, duracion_segundos, ancho, alto,
    tamano_bytes, activa, destacada, fecha_expiracion
) VALUES (
    1,
    'imagen',
    'http://localhost:8000/uploads/historias/2026/03/20/historia_destacada_001.jpg',
    'http://localhost:8000/uploads/historias/miniaturas/2026/03/20/thumb_historia_destacada_001.jpg',
    'Esta es una historia destacada que no expira',
    7,
    1080,
    1920,
    612352,
    TRUE,
    TRUE,
    NULL -- NULL porque es destacada
);

-- Historia de video
INSERT INTO historia (
    usuario_id, tipo, url_archivo, url_miniatura,
    descripcion, duracion_segundos, ancho, alto,
    tamano_bytes, duracion_video, activa, destacada, fecha_expiracion
) VALUES (
    1,
    'video',
    'http://localhost:8000/uploads/historias/2026/03/20/historia_video_001.mp4',
    'http://localhost:8000/uploads/historias/miniaturas/2026/03/20/thumb_historia_video_001.jpg',
    'Video de ejemplo',
    10,
    1080,
    1920,
    2097152,
    15, -- 15 segundos de video
    TRUE,
    FALSE,
    DATE_ADD(NOW(), INTERVAL 24 HOUR)
);


-- ============================================================================
-- Insertar vistas de ejemplo
-- ============================================================================

-- Usuario 2 ve la historia 1 del usuario 1
INSERT INTO historia_vista (historia_id, usuario_id, tiempo_visto_segundos, completo)
VALUES (1, 2, 5, TRUE);

-- Usuario 3 ve la historia 1 del usuario 1
INSERT INTO historia_vista (historia_id, usuario_id, tiempo_visto_segundos, completo)
VALUES (1, 3, 3, FALSE);


-- ============================================================================
-- Insertar reacciones de ejemplo
-- ============================================================================

INSERT INTO historia_reaccion (historia_id, usuario_id, tipo_reaccion)
VALUES (1, 2, 'like');

INSERT INTO historia_reaccion (historia_id, usuario_id, tipo_reaccion)
VALUES (1, 3, 'fire');


-- ============================================================================
-- Consultas de verificación
-- ============================================================================

-- Ver todas las historias
SELECT 
    h.id,
    h.usuario_id,
    u.nombre,
    h.tipo,
    h.descripcion,
    h.destacada,
    h.vistas_totales,
    h.fecha_creacion,
    h.fecha_expiracion,
    CASE 
        WHEN h.destacada THEN 'Destacada'
        WHEN h.fecha_expiracion > NOW() THEN 'Activa'
        ELSE 'Expirada'
    END as estado
FROM historia h
JOIN usuario u ON h.usuario_id = u.id
ORDER BY h.fecha_creacion DESC;

-- Ver vistas de historias
SELECT 
    h.id as historia_id,
    h.descripcion,
    u.nombre as visto_por,
    hv.fecha_vista,
    hv.completo
FROM historia_vista hv
JOIN historia h ON hv.historia_id = h.id
JOIN usuario u ON hv.usuario_id = u.id
ORDER BY hv.fecha_vista DESC;

-- Ver reacciones
SELECT 
    h.id as historia_id,
    h.descripcion,
    u.nombre as reaccion_de,
    hr.tipo_reaccion,
    hr.fecha_reaccion
FROM historia_reaccion hr
JOIN historia h ON hr.historia_id = h.id
JOIN usuario u ON hr.usuario_id = u.id
ORDER BY hr.fecha_reaccion DESC;
