create database if not exists Antivirus_Proyecto_Redes2_LSJ;
USE  Antivirus_Proyecto_Redes2_LSJ;

drop TABLE tb_ArchivosContaminados;
CREATE TABLE if not exists tb_ArchivosContaminados (
codigo 				int					not null auto_increment ,
hashMalisioso 		VARCHAR(100) 		not null,
CONSTRAINT ArchivosContaminados_pk PRIMARY KEY (codigo)	
 )engine = INNODB;
 
CREATE TABLE if not exists tb_ArchivosMalisiosos (
codigo 				int					not null auto_increment ,
hashMalisioso 		VARCHAR(100) 		not null,
nombre 				VARCHAR(100) 		not null,
CONSTRAINT ArchivosContaminados_pk PRIMARY KEY (codigo)	
 )engine = INNODB;
 
CREATE TABLE if not exists tb_Usuarios (
codigo 				int					not null auto_increment ,
nombre 				VARCHAR(50) 		not null,
contrasena 			VARCHAR(50) 		not null,
CONSTRAINT Usuarios_pk PRIMARY KEY (codigo)	
 )engine = INNODB;
 
 insert into tb_ArchivosContaminados (hashMalisioso )values("182336943eb3e2ef7688c4f7fc3e69fb");
insert into tb_ArchivosMalisiosos (hashMalisioso,nombre )values("182336943eb3e2ef7688c4f7fc3e69fb", 'prueba1');

 select * from  tb_ArchivosMalisiosos;
 
 insert into tb_Usuarios (nombre,contrasena )values('Luis','123');
 select * from  tb_Usuarios;
 
 insert into tb_Usuarios (nombre,contrasena )values("qwe","123")
 
 
 
 