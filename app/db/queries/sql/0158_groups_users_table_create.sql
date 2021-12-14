create table if not exists analytic_shop.users_groups (
    user_id uuid not null,
    group_id uuid not null,

    CONSTRAINT users_groups_users_fk FOREIGN KEY (user_id) REFERENCES analytic_shop.users (id) ON DELETE CASCADE,
    CONSTRAINT users_groups_groups_fk FOREIGN KEY (group_id) REFERENCES analytic_shop.groups (id) ON DELETE CASCADE
);