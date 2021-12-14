create table if not exists analytic_shop.products (
    id uuid default uuid_generate_v4(),
    name text not null,
    description text not null default '',
    code text not null,
    characteristic jsonb default '{}',
    rating decimal not null default 0,
    category text not null,
    created timestamp not null default now(),

    CONSTRAINT products_pk PRIMARY KEY (id),
    CONSTRAINT products_name_uniq UNIQUE (name),
    CONSTRAINT products_code_uniq UNIQUE (code)
);