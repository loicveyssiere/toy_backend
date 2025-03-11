-- Enable the UUID extension if not already enabled.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE condition_type AS ENUM ('new', 'good', 'acceptable', 'damaged', 'fragile', 'bad');

CREATE TABLE IF NOT EXISTS "book_reference" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    published_date DATE,
    "disabled": BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS "book_copy" (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    condition condition_type,
    "disabled": BOOLEAN DEFAULT false,
    book_reference_id UUID NOt NULL,
    CONSTRAINT fk_book_reference_id
        FOREIGN KEY (book_reference_id) 
        REFERENCES "book_reference" (id)
);
