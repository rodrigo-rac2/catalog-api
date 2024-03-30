-- Creating Participants table
CREATE TABLE IF NOT EXISTS Participants (
    ParticipantId SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Creating Role table
CREATE TABLE IF NOT EXISTS Role (
    RoleId SERIAL PRIMARY KEY,
    Description VARCHAR(255) UNIQUE NOT NULL
);

-- Creating Books table
CREATE TABLE IF NOT EXISTS Books (
    BookId SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    EditionNumber INT,
    Publisher VARCHAR(255),
    PublicationPlace VARCHAR(255),
    PublicationDate DATE,
    NumberOfPages INT,
    ISBN VARCHAR(255) UNIQUE NOT NULL
);

-- Creating table for the relationship between Books and Participants
CREATE TABLE IF NOT EXISTS BookParticipants (
    BookId INT,
    ParticipantId INT,
    RoleId INT,
    CONSTRAINT PK_BookParticipant PRIMARY KEY (BookId, ParticipantId, RoleId),
    CONSTRAINT FK_Book FOREIGN KEY (BookId) REFERENCES Books(BookId),
    CONSTRAINT FK_Participant FOREIGN KEY (ParticipantId) REFERENCES Participants(ParticipantId),
    CONSTRAINT FK_Role FOREIGN KEY (RoleId) REFERENCES Role(RoleId)
);
