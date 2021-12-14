create table if not exists analytic_shop.groups (
    id uuid default uuid_generate_v4(),
    name text not null,
    permission_type int not null default 0,
    created timestamp not null default now(),

    CONSTRAINT groups_pk PRIMARY KEY (id),
    CONSTRAINT groups_name_uniq UNIQUE (name)
);