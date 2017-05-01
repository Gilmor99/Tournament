-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Create tournament database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

-- Create Players table
DROP TABLE IF EXISTS players CASCADE;
create table players (player_id serial primary key, player_name text);

-- create matched table
DROP TABLE IF EXISTS matches;
create table matches(match_id serial primary key , winner int references players(player_id) default 0,  loser int references players(player_id) default  0);

-- create ranking view
DROP VIEW IF EXISTS ranking;
create view ranking as
    select
       players.player_id,
       players.player_name,
      (SELECT COALESCE (
           (select
               COUNT(players.player_id)
           where
               players.player_id = matches.winner
           )
           , 0)
        )
        as ranked,
        (SELECT COALESCE (
            (select
               COUNT(players.player_id)
            where
               (
                   players.player_id = matches.winner
                   or players.player_id = matches.loser
               )
            )
            , 0)
        )
        as played
   from
       players
    LEFT OUTER JOIN matches
    ON players.player_id = matches.winner OR players.player_id = matches.loser
    group by
        players.player_id,
        matches.winner,
        matches.loser
   order by
       ranked DESC,
       played DESC;


-- create num of matches playerStandings view
--DROP VIEW IF EXISTS matches_played;
--create view matches_played as
--    select players.player_id, players.player_name, matches.winner, matches.loser,
--    (select COUNT(players.player_id) where (players.player_id = matches.winner or players.player_id = matches.loser) group by players.player_id) as played
--    from players, matches group by players.player_id, matches.winner, matches.loser order by played  DESC;
