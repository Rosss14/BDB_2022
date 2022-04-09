DROP DATABASE IF EXISTS `isoforms`;
CREATE DATABASE `isoforms` /*!40100 DEFAULT CHARACTER SET latin1 */;

use isoforms;

CREATE TABLE `organism` (
  `tax_id` int(11) NOT NULL,
  `nombre` varchar(55) NOT NULL,
  PRIMARY KEY (`tax_id`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `gene` (
  `id` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `organism` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gene_organism_key_idx` (`organism`),
  CONSTRAINT `gene_organism_key` FOREIGN KEY (`organism`) REFERENCES `organism` (`tax_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `protein` (
  `id` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `revisado` tinyint(4) DEFAULT NULL,
  `longitud` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `locus` (
  `gene` int(11) NOT NULL,
  `chromosome` varchar(10) NOT NULL,
  `map_location` varchar(45) DEFAULT NULL,
  `start` int(11) DEFAULT NULL,
  `end` int(11) DEFAULT NULL,
  `exon_count` int(11) DEFAULT NULL,
  KEY `locus_gene_idx` (`gene`),
  CONSTRAINT `locus_gene_key` FOREIGN KEY (`gene`) REFERENCES `gene` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `gene_protein` (
  `gene_id` int(11) NOT NULL,
  `protein_id` varchar(20) NOT NULL,
  KEY `gene_key_idx` (`gene_id`),
  KEY `protein_key_idx` (`protein_id`),
  CONSTRAINT `gene_key` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `protein_key` FOREIGN KEY (`protein_id`) REFERENCES `protein` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `isoform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `protein_id` varchar(20) NOT NULL,
  `isoform_num` int(11) NOT NULL,
  `longitud` int(11) NOT NULL,
  `secuencia` varchar(3000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `isofrom_protein_key_idx` (`protein_id`),
  CONSTRAINT `isofrom_protein_key` FOREIGN KEY (`protein_id`) REFERENCES `protein` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;





