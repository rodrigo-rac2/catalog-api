-- Inserção de papéis
INSERT INTO Role (Description) VALUES ('Author'), ('Translator'), ('Editor');

-- Inserção de participantes (autores e tradutores)
INSERT INTO Participants (Name) VALUES
('Machado de Assis'),
('Jorge Amado'),
('Clarice Lispector'),
('Paulo Coelho'),
('Guimarães Rosa'),
('Mark Lutz'),
('Luciano Ramalho'),
('Paul Deitel'),
('Zed A. Shaw'),
('Bruce Momjian');

-- Inserção de livros
-- Literatura Brasileira
INSERT INTO Books (Title, Description, EditionNumber, Publisher, PublicationPlace, PublicationDate, NumberOfPages, ISBN) VALUES
('Dom Casmurro', 'Um dos grandes romances de Machado de Assis', 1, 'Editora ABC', 'Rio de Janeiro', '1899-01-01', 256, '978-8535902778'),
('Gabriela, Cravo e Canela', 'Um romance de Jorge Amado', 1, 'Editora DEF', 'Salvador', '1958-01-01', 300, '978-8535911350'),
('A Hora da Estrela', 'Um dos últimos livros de Clarice Lispector', 1, 'Editora GHI', 'Rio de Janeiro', '1977-01-01', 88, '978-8532508126'),
('O Alquimista', 'Best-seller internacional de Paulo Coelho', 1, 'Editora JKL', 'Rio de Janeiro', '1988-01-01', 208, '978-8599296158'),
('Grande Sertão: Veredas', 'Uma das maiores obras da literatura brasileira por Guimarães Rosa', 1, 'Editora MNO', 'Rio de Janeiro', '1956-01-01', 624, '978-8535911695');

-- Livros Técnicos sobre Python e PostgreSQL
INSERT INTO Books (Title, Description, EditionNumber, Publisher, PublicationPlace, PublicationDate, NumberOfPages, ISBN) VALUES
('Learning Python', 'Livro abrangente sobre Python, por Mark Lutz', 5, 'O’Reilly Media', 'São Francisco', '2013-01-01', 1600, '978-1449355739'),
('Fluent Python', 'Claro, conciso e eficaz, por Luciano Ramalho', 1, 'O’Reilly Media', 'São Francisco', '2015-01-01', 792, '978-1491946008'),
('Python for Programmers', 'Com conceitos e aplicações práticas, por Paul Deitel', 1, 'Prentice Hall', 'Nova York', '2019-01-01', 640, '978-0135231364'),
('Learn Python the Hard Way', 'Um guia introdutório ao Python, por Zed A. Shaw', 3, 'Addison-Wesley', 'São Francisco', '2017-01-01', 320, '978-0134692883'),
('PostgreSQL: Introduction and Concepts', 'Por Bruce Momjian, uma introdução ao PostgreSQL', 1, 'Addison-Wesley', 'Nova York', '2000-01-01', 464, '978-0201703313');

-- Inserção de relações LivroParticipantes (assumindo papéis e participantes inseridos anteriormente)
INSERT INTO BookParticipants (BookId, ParticipantId, RoleId) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 1),
(7, 7, 1),
(8, 8, 1),
(9, 9, 1),
(10, 10, 1);
