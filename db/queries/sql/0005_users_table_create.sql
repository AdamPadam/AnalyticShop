create table if not exists analytic_shop.users (
    id uuid default uuid_generate_v4(),
    username text not null,
    password text not null,
    first_name text default '',
    last_name text default '',
    birth_date date,
    created timestamp not null default now(),

    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_username_uniq UNIQUE (username)
);