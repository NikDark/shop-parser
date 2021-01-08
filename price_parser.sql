-- Table: public.price_parser

-- DROP TABLE public.price_parser;

CREATE TABLE public.price_parser
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    date date NOT NULL,
    price double precision NOT NULL,
    product_id integer NOT NULL,
    authorized boolean NOT NULL,
    shop text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT price_parser_pkey PRIMARY KEY (id),
    CONSTRAINT id_product_key FOREIGN KEY (product_id)
        REFERENCES public.product_parser (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.price_parser
    OWNER to postgres;
-- Index: fki_id_product_key

-- DROP INDEX public.fki_id_product_key;

CREATE INDEX fki_id_product_key
    ON public.price_parser USING btree
    (product_id ASC NULLS LAST)
    TABLESPACE pg_default;