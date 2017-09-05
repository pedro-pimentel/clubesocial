drop table if exists rooms;
create table rooms (
	id integer primary key,
	name text not null
);
drop table if exists devices;
create table devices (
	id integer primary key,
	pin integer not null,
	name text not null,
	status text not null,
	id_rooms integer not null,
	FOREIGN KEY(id_rooms) REFERENCES rooms(id)
);