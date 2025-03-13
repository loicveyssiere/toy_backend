-- Enable the UUID extension if not already enabled.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

drop table if exists "user" cascade;
drop table if exists "user_account" cascade;
drop table if exists "book_reference" cascade;
drop table if exists "book_copy";
drop table if exists"book_loan";
drop type if exists condition_type;
drop type if exists role_type;

CREATE TYPE condition_type AS ENUM ('new', 'good', 'acceptable', 'damaged', 'fragile', 'bad');
CREATE TYPE role_type as ENUM ('admin', 'user');

CREATE TABLE IF NOT EXISTS "user" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "user_account" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    role role_type,
    user_id UUID NOT NULL,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id) 
        REFERENCES "user" (id)
);

CREATE TABLE IF NOT EXISTS "book_reference" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    published_date DATE,
    "disabled" BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    created_by UUID NOT NULL,
    CONSTRAINT fk_created_by
        FOREIGN KEY (created_by) 
        REFERENCES "user_account" (id)
);

CREATE TABLE IF NOT EXISTS "book_copy" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    condition condition_type,
    "disabled" BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    book_reference_id UUID NOT NULL,
    CONSTRAINT fk_book_reference_id
        FOREIGN KEY (book_reference_id) 
        REFERENCES "book_reference" (id)
);

CREATE TABLE IF NOT EXISTS "book_loan" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    start_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    book_copy_id UUID NOT NULL,
    account_id UUID NOT NULL,
    CONSTRAINT fk_book_copy_id
        FOREIGN KEY (book_copy_id) 
        REFERENCES "book_copy" (id),
    CONSTRAINT fk_account_id
        FOREIGN KEY (account_id) 
        REFERENCES "user_account" (id)
);

INSERT INTO "user"  (id, "name") VALUES ('6df2f5ef-4680-4b44-919f-830137c233e3', 'John Doe');
INSERT INTO user_account (id, "role", user_id) VALUES ('e526e575-1fc5-486c-82f2-efbe797b96e0', 'user', '6df2f5ef-4680-4b44-919f-830137c233e3');
INSERT INTO user_account (id, "role", user_id) VALUES ('d65af1f5-8db3-43af-9a90-4a48e585435c', 'admin', '6df2f5ef-4680-4b44-919f-830137c233e3');


INSERT INTO "book_reference" (id, title, author, published_date, "disabled", created_at, updated_at, created_by)
VALUES
    ('f061c9ff-12ba-474d-95c0-5b4df038bb37', '1984', 'George Orwell', '1949-06-08', false, NOW(), NOW(), 'd65af1f5-8db3-43af-9a90-4a48e585435c'),
    ('7b7523d4-5e0c-433f-96c4-01869c73b83d', 'To Kill a Mockingbird', 'Harper Lee', '1960-07-11', false, NOW(), NOW(), 'd65af1f5-8db3-43af-9a90-4a48e585435c'),
    ('bdfe0834-b0a9-400a-a382-69c0d92f9c66', 'The Great Gatsby', 'F. Scott Fitzgerald', '1925-04-10', false, NOW(), NOW(), 'd65af1f5-8db3-43af-9a90-4a48e585435c'),
    ('8b468eb6-0e03-48cc-8f16-cf72b142c6a4', 'Moby-Dick', 'Herman Melville', '1851-10-18', false, NOW(), NOW(), 'd65af1f5-8db3-43af-9a90-4a48e585435c'),
    ('d5e51406-ae06-4a0c-8e67-39729e382622', 'Pride and Prejudice', 'Jane Austen', '1813-01-28', false, NOW(), NOW(), 'd65af1f5-8db3-43af-9a90-4a48e585435c');

INSERT INTO "book_copy" (condition, "disabled", created_at, updated_at, book_reference_id)
VALUES
    -- Copies for '1984'
    ('new', false, NOW(), NOW(), 'f061c9ff-12ba-474d-95c0-5b4df038bb37'),
    ('good', false, NOW(), NOW(), 'f061c9ff-12ba-474d-95c0-5b4df038bb37'),
    ('acceptable', false, NOW(), NOW(), 'f061c9ff-12ba-474d-95c0-5b4df038bb37'),

    -- Copies for 'To Kill a Mockingbird'
    ('new', false, NOW(), NOW(), '7b7523d4-5e0c-433f-96c4-01869c73b83d'),
    ('good', false, NOW(), NOW(), '7b7523d4-5e0c-433f-96c4-01869c73b83d'),
    ('fragile', false, NOW(), NOW(), '7b7523d4-5e0c-433f-96c4-01869c73b83d'),

    -- Copies for 'The Great Gatsby'
    ('new', false, NOW(), NOW(), 'bdfe0834-b0a9-400a-a382-69c0d92f9c66'),
    ('acceptable', false, NOW(), NOW(), 'bdfe0834-b0a9-400a-a382-69c0d92f9c66'),
    ('bad', false, NOW(), NOW(), 'bdfe0834-b0a9-400a-a382-69c0d92f9c66'),

    -- Copies for 'Moby-Dick'
    ('new', false, NOW(), NOW(), '8b468eb6-0e03-48cc-8f16-cf72b142c6a4'),
    ('good', false, NOW(), NOW(), '8b468eb6-0e03-48cc-8f16-cf72b142c6a4'),
    ('damaged', false, NOW(), NOW(), '8b468eb6-0e03-48cc-8f16-cf72b142c6a4'),

    -- Copies for 'Pride and Prejudice'
    ('new', false, NOW(), NOW(), 'd5e51406-ae06-4a0c-8e67-39729e382622'),
    ('fragile', false, NOW(), NOW(), 'd5e51406-ae06-4a0c-8e67-39729e382622'),
    ('bad', false, NOW(), NOW(), 'd5e51406-ae06-4a0c-8e67-39729e382622');