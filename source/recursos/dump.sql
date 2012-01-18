BEGIN TRANSACTION;
DELETE FROM sqlite_sequence;
CREATE TABLE usuario_carta(
id integer primary key,
id_usuario integer references usuario(id),
id_carta integer references carta(id));
INSERT INTO "usuario_carta" VALUES(1,1,1);
INSERT INTO "usuario_carta" VALUES(2,1,2);
INSERT INTO "usuario_carta" VALUES(3,1,3);
INSERT INTO "usuario_carta" VALUES(4,1,4);
INSERT INTO "usuario_carta" VALUES(5,1,5);
INSERT INTO "usuario_carta" VALUES(6,1,6);
CREATE TABLE sesion (
id integer primary key,
id_usuario integer references Usuario(id),
acceso date not null);
INSERT INTO "sesion" VALUES(1,1,'2011-12-27 19:19:13.577364');
INSERT INTO "sesion" VALUES(2,2,'2012-01-14 16:44:04.385205');
INSERT INTO "sesion" VALUES(3,1,'2012-01-14 16:49:45.709512');
INSERT INTO "sesion" VALUES(4,2,'2012-01-14 16:51:46.766257');
INSERT INTO "sesion" VALUES(5,1,'2012-01-14 16:53:35.707447');
INSERT INTO "sesion" VALUES(6,2,'2012-01-17 15:09:02.513251');
INSERT INTO "sesion" VALUES(7,1,'2012-01-17 15:31:07.249125');
CREATE TABLE "carta"(
id integer primary key,
right integer not null,
top integer not null,
clase varchar(20) not null,
nombre varchar(25) not null,
descripcion varchar(200) not null,
precio integer not null,
campo varchar(8) not null,
tipo varchar(12) not null,
charge integer not null,
clasebase varchar(20));
INSERT INTO "carta" VALUES(1,0,0,'LanzaGuisantes','Lanzaguisantes','',100,'tierra','dia',10,NULL);
INSERT INTO "carta" VALUES(2,65,0,'Girasol','Girasol','',50,'tierra','dia',8,NULL);
INSERT INTO "carta" VALUES(3,0,195,'Nenufar','Nenufar','',25,'agua','dia',8,NULL);
INSERT INTO "carta" VALUES(4,195,488,'ColaDeGato','Cola de Gato','',225,'agua','dia',14,'Nenufar');
INSERT INTO "carta" VALUES(5,195,0,'Nuez','Nuez','',50,'tierra','dia',15,NULL);
INSERT INTO "carta" VALUES(6,130,0,'PetaCereza','Petacereza','',150,'tierra','dia',14,NULL);
CREATE TABLE usuario(
id integer primary key,
nombre varchar(15),
dinero integer);
INSERT INTO "usuario" VALUES(1,'Eysenck',0);
INSERT INTO "usuario" VALUES(2,'Sara',0);
CREATE TABLE objeto(
id integer primary key,
nombre varchar(20),
descripcion varchar(200),
costo integer);
INSERT INTO "objeto" VALUES(1,'Lampa','',0);
CREATE TABLE usuario_objeto(
id integer primary key,
id_usuario integer references usuario(id),
id_objeto integer references objeto(id));
INSERT INTO "usuario_objeto" VALUES(1,1,1);
COMMIT;
