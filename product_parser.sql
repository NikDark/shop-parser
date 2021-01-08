-- Table: public.product_parser

-- DROP TABLE public.product_parser;

CREATE TABLE public.product_parser
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "group" text COLLATE pg_catalog."default" NOT NULL,
    link text COLLATE pg_catalog."default" NOT NULL,
    shop text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT product_parser_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.product_parser
    OWNER to postgres;