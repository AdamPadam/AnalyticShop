create table if not exists analytic_shop.wishlist_items (
    id uuid default uuid_generate_v4(),
    user_id uuid not null,
    product_id uuid not null,
    created timestamp not null default now(),

    CONSTRAINT wishlist_items_pk PRIMARY KEY (id),
    CONSTRAINT wishlist_item_users_fk FOREIGN KEY (user_id) REFERENCES analytic_shop.users (id) ON DELETE CASCADE,
    CONSTRAINT wishlist_item_products_fk FOREIGN KEY (product_id) REFERENCES analytic_shop.products (id) ON DELETE CASCADE,
    CONSTRAINT wishlist_items_user_product_uniq UNIQUE (user_id, product_id)
);