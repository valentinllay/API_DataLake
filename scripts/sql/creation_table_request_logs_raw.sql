-- Création de la nouvelle table avec payload JSON
CREATE TABLE `request_logs_raw` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ip_address` VARCHAR(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `endpoint` VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payload` JSON DEFAULT NULL,
  `status_code` INT DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB
  AUTO_INCREMENT=38
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;