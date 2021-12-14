create table if not exists analytic_shop.feedbacks (
    id uuid default uuid_generate_v4(),
    title text not null,
    positive_msg text default '',
    negative_msg text default '',
    message text default '',
    user_id uuid not null,
    product_id uuid,
    shop_id uuid,
    created timestamp not null default now(),

    CONSTRAINT feedbacks_pk PRIMARY KEY (id),
    CONSTRAINT feedback_users_fk FOREIGN KEY (user_id) REFERENCES analytic_shop.users (id) ON DELETE CASCADE,
    CONSTRAINT feedback_products_fk FOREIGN KEY (product_id) REFERENCES analytic_shop.products (id) ON DELETE CASCADE,
    CONSTRAINT feedback_shops_fk FOREIGN KEY (shop_id) REFERENCES analytic_shop.shops (id) ON DELETE CASCADE
);