-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE tournaments (
    id          SERIAL PRIMARY KEY,
    created     timestamp default now()
  );

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    tournament_id integer REFERENCES tournaments
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    tournament_id integer REFERENCES tournaments(id),
    winner integer REFERENCES players(id),
    loser integer REFERENCES players(id)
);
