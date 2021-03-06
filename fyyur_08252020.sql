--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Ubuntu 12.3-1.pgdg16.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: artist; Type: TABLE; Schema: public; Owner: rjqebgtsqoratb
--

CREATE TABLE public.artist (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    phone character varying(120),
    genres character varying(120)[],
    image_link character varying(500),
    website_link character varying(120),
    facebook_link character varying(120),
    seeking_venue boolean,
    seeking_description character varying(250),
    num_of_shows integer,
    deleted boolean
);


ALTER TABLE public.artist OWNER TO rjqebgtsqoratb;

--
-- Name: artist_id_seq; Type: SEQUENCE; Schema: public; Owner: rjqebgtsqoratb
--

CREATE SEQUENCE public.artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artist_id_seq OWNER TO rjqebgtsqoratb;

--
-- Name: artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rjqebgtsqoratb
--

ALTER SEQUENCE public.artist_id_seq OWNED BY public.artist.id;


--
-- Name: shows; Type: TABLE; Schema: public; Owner: rjqebgtsqoratb
--

CREATE TABLE public.shows (
    id integer NOT NULL,
    artist_id integer NOT NULL,
    venue_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    deleted boolean
);


ALTER TABLE public.shows OWNER TO rjqebgtsqoratb;

--
-- Name: shows_id_seq; Type: SEQUENCE; Schema: public; Owner: rjqebgtsqoratb
--

CREATE SEQUENCE public.shows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shows_id_seq OWNER TO rjqebgtsqoratb;

--
-- Name: shows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rjqebgtsqoratb
--

ALTER SEQUENCE public.shows_id_seq OWNED BY public.shows.id;


--
-- Name: venue; Type: TABLE; Schema: public; Owner: rjqebgtsqoratb
--

CREATE TABLE public.venue (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    address character varying(120),
    phone character varying(120),
    genres character varying(120)[],
    website_link character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    seeking_talent boolean,
    seeking_description character varying(250),
    num_of_shows integer,
    deleted boolean
);


ALTER TABLE public.venue OWNER TO rjqebgtsqoratb;

--
-- Name: venue_id_seq; Type: SEQUENCE; Schema: public; Owner: rjqebgtsqoratb
--

CREATE SEQUENCE public.venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venue_id_seq OWNER TO rjqebgtsqoratb;

--
-- Name: venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rjqebgtsqoratb
--

ALTER SEQUENCE public.venue_id_seq OWNED BY public.venue.id;


--
-- Name: artist id; Type: DEFAULT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.artist ALTER COLUMN id SET DEFAULT nextval('public.artist_id_seq'::regclass);


--
-- Name: shows id; Type: DEFAULT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.shows ALTER COLUMN id SET DEFAULT nextval('public.shows_id_seq'::regclass);


--
-- Name: venue id; Type: DEFAULT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.venue ALTER COLUMN id SET DEFAULT nextval('public.venue_id_seq'::regclass);


--
-- Data for Name: artist; Type: TABLE DATA; Schema: public; Owner: rjqebgtsqoratb
--

COPY public.artist (id, name, city, state, phone, genres, image_link, website_link, facebook_link, seeking_venue, seeking_description, num_of_shows, deleted) FROM stdin;
\.


--
-- Data for Name: shows; Type: TABLE DATA; Schema: public; Owner: rjqebgtsqoratb
--

COPY public.shows (id, artist_id, venue_id, start_time, deleted) FROM stdin;
\.


--
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: rjqebgtsqoratb
--

COPY public.venue (id, name, city, state, address, phone, genres, website_link, image_link, facebook_link, seeking_talent, seeking_description, num_of_shows, deleted) FROM stdin;
\.


--
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rjqebgtsqoratb
--

SELECT pg_catalog.setval('public.artist_id_seq', 1, false);


--
-- Name: shows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rjqebgtsqoratb
--

SELECT pg_catalog.setval('public.shows_id_seq', 1, false);


--
-- Name: venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rjqebgtsqoratb
--

SELECT pg_catalog.setval('public.venue_id_seq', 1, false);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: shows shows_pkey; Type: CONSTRAINT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_pkey PRIMARY KEY (id);


--
-- Name: venue venue_pkey; Type: CONSTRAINT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id);


--
-- Name: shows shows_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: shows shows_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rjqebgtsqoratb
--

ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venue(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: rjqebgtsqoratb
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO rjqebgtsqoratb;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO rjqebgtsqoratb;


--
-- PostgreSQL database dump complete
--

