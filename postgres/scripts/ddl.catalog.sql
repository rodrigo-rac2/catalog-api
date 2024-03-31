-- Creating Participants table
create table if not exists participants (
    participantid serial primary key,
    name varchar(255) not null
);

-- Creating Role table
create table if not exists roles (
    roleid serial primary key,
    description varchar(255) unique not null
);

-- Creating Books table
create table if not exists books (
    bookid serial primary key,
    title varchar(255) not null,
    description text,
    editionnumber int,
    publisher varchar(255),
    publicationplace varchar(255),
    publicationdate date,
    numberofpages int,
    isbn varchar(255) unique not null
);

-- Creating table for the relationship between Books and Participants
create table if not exists bookparticipants (
    bookid int,
    participantid int,
    roleid int,
    constraint pk_bookparticipant primary key (bookid, participantid, roleid),
    constraint fk_book foreign key (bookid) references books(bookid),
    constraint fk_participant foreign key (participantid) references participants(participantid),
    constraint fk_role foreign key (roleid) references roles(roleid)
);
