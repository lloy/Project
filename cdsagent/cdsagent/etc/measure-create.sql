/* drop database if exists open_cloudoss; */
/* create database open_cloudoss; */

use open_cloudoss;

drop table if exists flow_measure; 
create table flow_measure(
	instance_uuid CHAR(38) NOT NULL,
	ip CHAR(15) NOT NULL,
    rpackets INT UNSIGNED NOT NULL,
    rbytes INT UNSIGNED NOT NULL,
    tpackets INT UNSIGNED NOT NULL,
    tbytes INT UNSIGNED NOT NULL,
    inster_timestamp DATETIME NOT NULL,
	PRIMARY KEY (instance_uuid, ip, rpackets, rbytes, tpackets, tbytes, insert_timestamp)
);
