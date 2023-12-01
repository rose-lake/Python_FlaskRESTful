INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN101', 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 5.99, 10);
    
INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN102', 'The Hunger Games', 'Suzanne Collins', 4.99, 4);
    
INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN103', 'Stormbreaker', 'Anthony Horowitz', 6.99, 3);

INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN106', 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 8.99, 5);

INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN107', 'Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 7.99, 8);

INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN108', 'Harry Potter and the Goblet of Fire', 'J.K. Rowling', 12.99, 1);

INSERT INTO bookshop.book (book_id, title, author, price)
	VALUES ('ISBN109', 'Harry Potter and the Order of the Phoenix', 'J.K. Rowling', 7.99);

INSERT INTO bookshop.book (book_id, title, author, quantity)
	VALUES ('ISBN110', 'Harry Potter and the Half Blood Prince', 'J.K. Rowling', 1);

-- accidentally gave ISBN110 the wrong title, so I deleted it, as below
-- DELETE FROM bookshop.book WHERE book_id = 'ISBN110';
-- then added it again with the correct title this time

INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN113', 'A Storm of Swords', 'George R. R. Martin', 0.99, 0);

INSERT INTO bookshop.book (book_id, title, author, price, quantity)
	VALUES ('ISBN114', 'A Feast for Crows', 'George R. R. Martin', 0.99, 1);

select * from book;