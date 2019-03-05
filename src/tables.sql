BEGIN TRANSACTION;
CREATE TABLE `areas` (
	`name`	TEXT,
	PRIMARY KEY(name)
);
CREATE TABLE `users` (
	`email`	TEXT,
	`name`	TEXT,
	`phone`	TEXT,
	PRIMARY KEY(email)
);
CREATE TABLE `sessions` (
	`name`	TEXT,
	`chair`	TEXT,
	PRIMARY KEY(name),
  	CONSTRAINT fk_chair
    		FOREIGN KEY (chair)
    		REFERENCES users(email)
);
CREATE TABLE "reviews" (
	`paper`	INTEGER,
	`reviewer`	TEXT,
	`originality`	INTEGER,
	`importance`	INTEGER,
	`soundness`	INTEGER,
	`overall`	INTEGER,
  	CONSTRAINT fk_reviewer
    		FOREIGN KEY (reviewer)
    		REFERENCES users(email),
  	CONSTRAINT fk_paper
    		FOREIGN KEY (paper)
    		REFERENCES papers(Id)
);
CREATE TABLE "papers" (
	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`title`	TEXT,
	`decision`	TEXT,
	`area`	TEXT,
	`author`	TEXT,
	`csession`	TEXT,
  	CONSTRAINT fk_author
    	     FOREIGN KEY (author)
    		REFERENCES users(email),
	CONSTRAINT fk_area
    	     FOREIGN KEY (area)
    		REFERENCES areas(name),
	CONSTRAINT fk_csession
    		FOREIGN KEY (csession)
    		REFERENCES sessions(name)
);
CREATE TABLE `expertise` (
	`area`	TEXT,
	`reviewer`	TEXT,
	CONSTRAINT fk_area
    		FOREIGN KEY (area)
    		REFERENCES areas(name),
	CONSTRAINT fk_reviewer
    		FOREIGN KEY (reviewer)
    		REFERENCES users(email)
);

COMMIT;
