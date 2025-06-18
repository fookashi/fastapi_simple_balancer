-- migrate:up
CREATE TABLE cdn_config (
    id SERIAL PRIMARY KEY,
    cdn_host VARCHAR NOT NULL,
    distribution_rate INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
INSERT INTO cdn_config (cdn_host, distribution_rate) VALUES ('cdn.example.com', 10);

-- migrate:down
DROP TABLE IF EXISTS cdn_config;