    -- PGPASSWORD=postgres psql -U postgres -d sikayetvar -a -f create_table.sql
    
    DROP TABLE IF EXISTS brand CASCADE;
    CREATE TABLE brand (
        id BIGSERIAL PRIMARY KEY,
        href VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        replied_complaint BIGINT NOT NULL,
        total_complaint BIGINT NOT NULL,
        average_reply_sec INT NOT NULL,
        rating_count INT NOT NULL,
        rating INT NOT NULL
    );

    DROP TABLE IF EXISTS complained_item CASCADE;
    CREATE TABLE complained_item (
        id BIGSERIAL PRIMARY KEY,
        href VARCHAR(255) UNIQUE NOT NULL,
        upper_item_id BIGINT NOT NULL,
        brand_id BIGINT NOT NULL,
        name VARCHAR(255) NOT NULL,
        rating INT NOT NULL,
        rating_count INT NOT NULL,
        is_leaf BOOLEAN NOT NULL,
        FOREIGN KEY (upper_item_id) REFERENCES complained_item (id),
        FOREIGN KEY (brand_id) REFERENCES brand (id)
    );

    DROP TABLE IF EXISTS member CASCADE;
    CREATE TABLE member (
        id BIGSERIAL PRIMARY KEY,
        href VARCHAR(255) NOT NULL
    );
    
    DROP TABLE IF EXISTS complaint CASCADE;
    CREATE TABLE  complaint (
        id BIGSERIAL PRIMARY KEY,
        href VARCHAR(255) NOT NULL,
        complained_item_id BIGINT NOT NULL,
        title VARCHAR(255) NOT NULL,
        date TIMESTAMP NOT NULL,
        view_count INT NOT NULL,
        like_count INT NOT NULL,
        member_id BIGINT NOT NULL,
        rating INT NULL,
        solved BOOLEAN NULL,
        FOREIGN KEY (complained_item_id) REFERENCES complained_item (id),
        FOREIGN KEY (member_id) REFERENCES member (id)
    );

    DROP TABLE IF EXISTS reply CASCADE;
    CREATE TABLE reply (
        id BIGSERIAL PRIMARY KEY,
        complaint_id BIGINT NOT NULL,
        message TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        is_from_brand BOOLEAN NOT NULL,
        FOREIGN KEY (complaint_id) REFERENCES complaint(id)
    );