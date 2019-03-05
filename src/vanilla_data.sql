insert into areas values ('DB');
insert into areas values ('SE');

insert into users values ('Tom@Email', 'Tom', '123');
insert into users values ('Jerry@Email', 'Jerry', '123');
insert into users values ('Mickey@Email', 'Mickey', '123');
insert into users values ('Donald@Email', 'Donald', '123');
insert into users values ('Minnie@Email', 'Minnie', '123');
insert into users values ('Pluto@Email', 'Pluto', '123');
insert into users values ('Darth@Email', 'Darth', '123');
insert into users values ('Anakin@Email', 'Anakin', '123');
insert into users values ('R2D2@Email', 'R2D2', '123');
insert into users values ('C3P0@Email', 'C3P0', '123');
insert into users values ('Harry@Email', 'Harry', '123');
insert into users values ('Ron@Email', 'Ron', '123');
insert into users values ('Hermoine@Email', 'Hermoine', '123');
insert into users values ('Snape@Email', 'Snape', '123');
insert into users values ('Albus@Email', 'Albus', '123');


insert into sessions values ('DB', 'Mickey@Email');
insert into sessions values ('SE', 'Pluto@Email');


insert into expertise values ('SE', 'Tom@Email');
insert into expertise values ('SE', 'Jerry@Email');
insert into expertise values ('DB', 'Mickey@Email');
insert into expertise values ('DB', 'Donald@Email');
insert into expertise values ('SE', 'Anakin@Email');
insert into expertise values ('SE', 'Darth@Email');
insert into expertise values ('SE', 'Pluto@Email');
insert into expertise values ('SE', 'Minnie@Email');
insert into expertise values ('SE', 'Donald@Email');
insert into expertise values ('SE', 'Mickey@Email');
insert into expertise values ('SE', 'R2D2@Email');
insert into expertise values ('SE', 'C3P0@Email');


insert into papers values (1, 'Bass players are undervalued big time',  'A', 'DB', 'Harry@Email', 'DB');
insert into papers values (2, 'System of a Down rocks!', 'A', 'SE', 'Harry@Email', 'SE');
insert into papers values (3, 'Three moons are better than one', 'A', 'SE', 'Ron@Email', 'SE');
insert into papers values (4, 'Donald was not always been a duck', 'R', 'SE', 'Hermoine@Email', 'SE');
insert into papers values (5, 'Mickey and Anakin are bothers', 'R', 'SE', 'Snape@Email', 'SE');
insert into papers values (6, 'Previous text here caused an error', 'A', 'DB', 'Harry@Email', 'DB');


insert into reviews values (1, 'Minnie@Email', 4,4,4,5);
insert into reviews values (1, 'Donald@Email', 4,3,4,4);
insert into reviews values (1, 'Mickey@Email', 4,4,3,5);
insert into reviews values (2, 'Minnie@Email', 4,2,1,2);
insert into reviews values (2, 'Donald@Email', 4,3,4,4);
insert into reviews values (2, 'Mickey@Email', 4,3,4,3);
insert into reviews values (3, 'Anakin@Email', 4,4,3,3);
insert into reviews values (3, 'Darth@Email', 3,4,4,3);
insert into reviews values (3, 'Pluto@Email', 4,3,4,3);
insert into reviews values (4, 'Anakin@Email', 3,3,4,3);
insert into reviews values (4, 'Darth@Email', 2,4,4,2);
insert into reviews values (4, 'Pluto@Email', 4,4,2,5);
insert into reviews values (5, 'C3P0@Email', 4,4,1,3);
insert into reviews values (5, 'R2D2@Email', 1,4,4,5);
insert into reviews values (5, 'Tom@Email', 4,2,4,3);
