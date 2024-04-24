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
CREATE TABLE IF NOT EXISTS bookparticipants (
    id SERIAL PRIMARY KEY,  -- New primary key column
    bookid INT,
    participantid INT,
    roleid INT,
    CONSTRAINT fk_book FOREIGN KEY (bookid) REFERENCES books(bookid),
    CONSTRAINT fk_participant FOREIGN KEY (participantid) REFERENCES participants(participantid),
    CONSTRAINT fk_role FOREIGN KEY (roleid) REFERENCES roles(roleid)
);

-- Creating table for the relationship between Books, Roles and Participants
CREATE TABLE IF NOT EXISTS bookparticipants (
    id SERIAL PRIMARY KEY,
    bookid INT,
    participantid INT,
    roleid INT,
    CONSTRAINT fk_book FOREIGN KEY (bookid) REFERENCES books(bookid) ON DELETE RESTRICT,
    CONSTRAINT fk_participant FOREIGN KEY (participantid) REFERENCES participants(participantid) ON DELETE RESTRICT,
    CONSTRAINT fk_role FOREIGN KEY (roleid) REFERENCES roles(roleid) ON DELETE RESTRICT
);
