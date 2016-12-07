#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "delete from matches;"
    c.execute(query)
    db.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM players"
    c.execute(query)
    db.commit()

def deleteTournaments():
    """remove all tournaments from database"""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM tournaments"
    c.execute(query)
    db.commit()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "select count(*)as num from players"
    c.execute(query)
    num_players = c.fetchone()[0]
    return num_players

def countPlayersInTournament(tournament_id):
    """Returns the number of players currently registered in a tournament."""
    db = connect()
    c = db.cursor()
    query = "select count(*)as num from players where tournament_id = %s"
    c.execute(query, (tournament_id,))
    num_players = c.fetchone()[0]
    return num_players

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    tournament_id = retrieveTournamentId()
    db = connect()
    c = db.cursor()
    query = "insert into players values (DEFAULT,%s,%s)"
    c.execute(query, (name, str(tournament_id),))
    db.commit()

def retrieveLastPlayerTournamentId():
    """Fetch the tournament_id of the last added player"""
    db = connect()
    c = db.cursor()
    query = "select tournament_id from players order by id desc"
    c.execute(query)
    tournament_id = c.fetchone()[0]
    return tournament_id

def retrieveAllTournamentId():
    """Retrieves a list of all the tournament_ids"""
    db = connect()
    c = db.cursor()
    query = "select id from tournaments order by id"
    c.execute(query)
    tournaments = c.fetchall()
    return tournaments

def retrieveTournamentId():
    """Retrieve tournament id of ongoing tournament or creates a new one"""
    db = connect()
    c = db.cursor()
    query_tournament = "select id from tournaments order by id desc"
    query_count_player_for_tournament = "select count(*) from players where tournament_id = %s"

    #Check if existing tournament
    c.execute(query_tournament)
    tournament_id = c.fetchone()
    if not tournament_id:
        #create new tournament
        tournament_id = createTournament()
        return tournament_id
    else:
        c.execute(query_count_player_for_tournament,(tournament_id,))
        num_players = c.fetchone()[0]
        if num_players >= 8: # Assuming max number of players in a tournament as 8
            #create new tournament
            tournament_id = createTournament()
            return tournament_id
        return tournament_id[0]

def createTournament():
    """Creates a new tournament"""
    db = connect()
    c = db.cursor()
    query_new_tournament = "insert into tournaments values (DEFAULT) returning id"
    c.execute(query_new_tournament)
    tournament_id = c.fetchone()[0]
    db.commit()
    return tournament_id

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []
    db = connect()
    c = db.cursor()
    query = """
       select players.id, players.name, count(m1.id) as wins, count(m2.id) as matches
       from players
       left outer join matches as m1 on players.id = m1.winner
       left outer join matches as m2 on players.id = m2.winner or players.id = m2.loser
       group by players.id
       order by wins desc
       """
    c.execute(query)
    for player in c.fetchall():
        standings.append(player)
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in cur.fetchall()]
    return standings

def playerStandingsForTournament(tournament_id):
    """Works like playerStandings() but for a selected tournament"""
    standings = []
    db = connect()
    c = db.cursor()
    query = """
       select players.id, players.name, count(m1.id) as wins, count(m2.id) as matches
       from players
       left outer join matches as m1 on players.id = m1.winner
       left outer join matches as m2 on players.id = m2.winner or players.id = m2.loser
       where players.tournament_id = %s
       group by players.id
       order by wins desc
       """
    c.execute(query, (tournament_id,))
    for player in c.fetchall():
        standings.append(player)
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    #win_query = "UPDATE players SET matches = matches+1, wins = wins+1 WHERE id = %s"
    #loss_query = "UPDATE players SET matches = matches+1 WHERE id = %s"
    match_query = "insert into matches values (default,%s,%s,%s)"
    tournament_id = player_tournament_id(winner)
    c.execute(match_query, (tournament_id,winner,loser,))
    #c.execute(win_query, (winner,))
    #c.execute(loss_query, (loser,))
    db.commit()

def player_tournament_id(player_id):
    """Retrieves the tournament_id of the player in the match"""
    db = connect()
    c = db.cursor()
    query = "select tournament_id from players where id = %s"
    c.execute(query, (player_id,))
    tournament_id = c.fetchone()[0]
    return tournament_id

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    db = connect()
    c = db.cursor()
    query = """select players.id, players.name, count(matches.id) as wins
               from players
               left outer join matches on players.id = matches.winner
               group by players.id
               order by wins desc;
    """
    # I can use sql to pair players!!!
    c.execute(query)
    players = c.fetchall()
    while len(players) > 0:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pair = (player1[0], player1[1], player2[0], player2[1])
        pairings.append(pair)
    return pairings

def swissPairingsForTournament(tournament_id):
    """Works as swissPairings() but for a defined tournament"""
    pairings = []
    db = connect()
    c = db.cursor()
    query = """select players.id, players.name, count(matches.id) as wins
               from players
               left outer join matches on players.id = matches.winner
               where players.tournament_id = %s
               group by players.id
               order by wins desc;
    """
    # I can use sql to pair players!!!
    c.execute(query, (tournament_id,))
    players = c.fetchall()
    while len(players) > 0:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pair = (player1[0], player1[1], player2[0], player2[1])
        pairings.append(pair)
    return pairings
