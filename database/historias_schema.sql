-- ============================================================================
-- SQL para crear las tablas de Historias en MySQL
-- Base de datos: sportmob_v2
-- ============================================================================

USE sportmob_v2;

-- ----------------------------------------------------------------------------
-- Tabla: historia
-- Almacena las historias (stories) de los usuarios
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS historia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    
    -- Tipo de contenido
    tipo ENUM('imagen', 'video') NOT NULL,
    
    -- URLs de archivos
    url_archivo VARCHAR(500) NOT NULL,
    url_miniatura VARCHAR(500),
    nombre_archivo VARCHAR(255),
    
    -- Contenido
    descripcion TEXT,
    duracion_segundos INT DEFAULT 5 COMMENT 'Duración en la app (segundos)',
    
    -- Metadata del archivo
    ancho INT,
    alto INT,
    tamano_bytes BIGINT,
    duracion_video INT COMMENT 'Duración del video (segundos)',
    
    -- Temporalidad
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion DATETIME COMMENT 'NULL si es destacada',
    activa BOOLEAN DEFAULT TRUE,
    
    -- Feature: Destacada (no expira)
    destacada BOOLEAN DEFAULT FALSE COMMENT 'Si es true, no expira en 24h',
    
    -- Estadísticas
    vistas_totales INT DEFAULT 0,
    
    -- Índices
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha_creacion (fecha_creacion),
    INDEX idx_fecha_expiracion (fecha_expiracion),
    INDEX idx_activa (activa),
    INDEX idx_destacada (destacada),
    
    -- Foreign key
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------------------
-- Tabla: historia_vista
-- Registra qué usuarios vieron cada historia
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS historia_vista (
    id INT PRIMARY KEY AUTO_INCREMENT,
    historia_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_vista DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Analytics
    tiempo_visto_segundos INT DEFAULT 0,
    completo BOOLEAN DEFAULT FALSE COMMENT 'Si vio la historia completa',
    
    -- Índices
    INDEX idx_historia (historia_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha_vista (fecha_vista),
    
    -- Constraint: un usuario solo puede ver una historia una vez
    UNIQUE KEY unique_vista (historia_id, usuario_id),
    
    -- Foreign keys
    FOREIGN KEY (historia_id) REFERENCES historia(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------------------
-- Tabla: historia_reaccion (OPCIONAL)
-- Almacena las reacciones a las historias
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS historia_reaccion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    historia_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo_reaccion ENUM('like', 'love', 'fire', 'clap', 'sad') DEFAULT 'like',
    fecha_reaccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_historia (historia_id),
    INDEX idx_usuario (usuario_id),
    
    -- Constraint: un usuario solo puede reaccionar una vez
    UNIQUE KEY unique_reaccion (historia_id, usuario_id),
    
    -- Foreign keys
    FOREIGN KEY (historia_id) REFERENCES historia(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================================
-- Triggers y Procedimientos (OPCIONAL)
-- ============================================================================

-- Trigger para actualizar automáticamente vistas_totales
-- (Alternativa: hacerlo en el código de la API)

DELIMITER $$

CREATE TRIGGER IF NOT EXISTS actualizar_vistas_totales
AFTER INSERT ON historia_vista
FOR EACH ROW
BEGIN
    UPDATE historia 
    SET vistas_totales = vistas_totales + 1 
    WHERE id = NEW.historia_id;
END$$

DELIMITER ;


-- ============================================================================
-- Índices adicionales para optimización (OPCIONAL)
-- ============================================================================

-- Índice compuesto para consultas de feed
CREATE INDEX idx_feed ON historia(activa, fecha_expiracion, fecha_creacion);

-- Índice para historias destacadas
CREATE INDEX idx_destacadas ON historia(destacada, activa, usuario_id);


-- ============================================================================
-- Consultas de ejemplo para verificar
-- ============================================================================

-- Ver estructura de las tablas
DESCRIBE historia;
DESCRIBE historia_vista;
DESCRIBE historia_reaccion;

-- Contar registros
SELECT 'Historias totales' as descripcion, COUNT(*) as total FROM historia
UNION ALL
SELECT 'Historias activas', COUNT(*) FROM historia WHERE activa = TRUE
UNION ALL
SELECT 'Historias destacadas', COUNT(*) FROM historia WHERE destacada = TRUE
UNION ALL
SELECT 'Vistas totales', COUNT(*) FROM historia_vista
UNION ALL
SELECT 'Reacciones totales', COUNT(*) FROM historia_reaccion;
