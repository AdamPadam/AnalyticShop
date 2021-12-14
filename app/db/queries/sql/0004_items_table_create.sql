create table if not exists analytic_shop.items (
    id uuid default uuid_generate_v4(),
    product_id uuid not null,
    shop_id uuid not null,
    quantity int not null default 0,
    discount_percent int not null default 0,
    price decimal not null default 0,
    created timestamp not null default now(),

    CONSTRAINT items_pk PRIMARY KEY (id),
    CONSTRAINT item_products_fk FOREIGN KEY (product_id) REFERENCES analytic_shop.products (id) ON DELETE CASCADE,
    CONSTRAINT item_shop_fk FOREIGN KEY (shop_id) REFERENCES analytic_shop.shops (id) ON DELETE CASCADE,
    CONSTRAINT items_product_shop_uniq UNIQUE (product_id, shop_id)
);