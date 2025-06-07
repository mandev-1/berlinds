# W E L C O M E

```sql
-- Table: public.customers

-- DROP TABLE IF EXISTS public.customers;

CREATE TABLE IF NOT EXISTS public.customers
(
    event_type character varying(50) COLLATE pg_catalog."default",
    product_id integer,
    price numeric(10,2),
    user_id bigint,
    user_session uuid,
    event_time timestamp without time zone,
    category_id bigint,
    category_code character varying(255) COLLATE pg_catalog."default",
    brand character varying(255) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customers
    OWNER to mman;
```

> Fig.1 (above) - the 'customers' table as of June 2025.



₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ ₳ 