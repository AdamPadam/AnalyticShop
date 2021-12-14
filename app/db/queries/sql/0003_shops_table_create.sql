create table if not exists analytic_shop.shops (
    id uuid default uuid_generate_v4(),
    name text not null,
    description text not null default '',
    address text,
    website text not null,
    rating decimal not null default 0,
    created timestamp not null default now(),

    CONSTRAINT shops_pk PRIMARY KEY (id),
    CONSTRAINT shops_name_uniq UNIQUE (name),
    CONSTRAINT shops_website_uniq UNIQUE (website)
);