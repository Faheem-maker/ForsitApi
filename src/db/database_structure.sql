-- MySQL Script generated by MySQL Workbench
-- Sun Nov 12 18:10:30 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema forsit_api
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forsit_api
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forsit_api` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `forsit_api` ;

-- -----------------------------------------------------
-- Table `forsit_api`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forsit_api`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `forsit_api`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forsit_api`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `base_amount` INT NULL DEFAULT NULL,
  `discount_amount` INT NULL DEFAULT NULL,
  `tax_amount` INT NULL DEFAULT NULL,
  `total_amount` INT GENERATED ALWAYS AS (((`base_amount` - `discount_amount`) - `tax_amount`)) VIRTUAL,
  `doctype` CHAR(2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `forsit_api`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forsit_api`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `price` INT NULL DEFAULT NULL,
  `created_at` DATE NOT NULL,
  `category_id` INT NULL DEFAULT NULL,
  `qty` INT NULL DEFAULT NULL,
  `minimum_qty` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `category_id` (`category_id` ASC) VISIBLE,
  CONSTRAINT `product_ibfk_1`
    FOREIGN KEY (`category_id`)
    REFERENCES `forsit_api`.`category` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `forsit_api`.`orders_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forsit_api`.`orders_products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `product_rate` INT NULL DEFAULT NULL,
  `product_qty` INT NULL DEFAULT NULL,
  `base_amount` INT GENERATED ALWAYS AS ((`product_rate` * `product_qty`)) VIRTUAL,
  `discount_amount` INT NULL DEFAULT NULL,
  `tax_amount` INT NULL DEFAULT NULL,
  `total_amount` INT GENERATED ALWAYS AS (((`base_amount` - `discount_amount`) - `tax_amount`)) VIRTUAL,
  PRIMARY KEY (`id`),
  INDEX `order_id` (`order_id` ASC) VISIBLE,
  INDEX `product_id` (`product_id` ASC) VISIBLE,
  CONSTRAINT `orders_products_ibfk_1`
    FOREIGN KEY (`order_id`)
    REFERENCES `forsit_api`.`orders` (`id`),
  CONSTRAINT `orders_products_ibfk_2`
    FOREIGN KEY (`product_id`)
    REFERENCES `forsit_api`.`product` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
