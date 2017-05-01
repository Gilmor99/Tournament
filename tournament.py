#!/usr/bin/env python

"""
tournament.py--implementation of a Swiss - system tournament#
"""
import psycopg2



def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection and a cursor.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")



def deleteMatches():
    """
    Remove all the match records from the database.
    """
    DB, cursor = connect()
    query = "truncate matches CASCADE"
    cursor.execute(query)
    DB.commit()
    DB.close()


def deletePlayers():
    """
    Remove all the player records from the database.
    """
    DB, cursor = connect()
    query = "truncate players CASCADE"
    cursor.execute(query)
    DB.commit()
    DB.close()

def countPlayers():
    """
    Returns the number of players currently registered.
    """
    DB, cursor = connect()
    query = "select count(*) from players"
    cursor.execute(query)
    count = cursor.fetchone()
    DB.close()
    return count[0]

def registerPlayer(name):
    """
    Adds a player to the tournament database.

    The database assigns a unique serial id number
    for the player.(This should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the player 's full name (need not be unique).
    """
    DB, cursor = connect()
    query = "insert into players (player_name) values(%s)"
    parms = (name, )
    cursor.execute(query, parms)
    DB.commit()
    DB.close()

def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied
    for first place
    if there is currently a tie.

    Returns:
        A list of tuples, each of which contains(id, name, wins, matches):
        id: the player 's unique id (assigned by the database)
    name: the player 's full name (as registered)
    wins: the number of matches the player has won
    matches: the number of matches the player has played
    """
    DB, cursor = connect()
    query = "select player_id, player_name, ranked, played from ranking order by ranked desc, played desc"
    cursor.execute(query)
    standing = cursor.fetchall()
    DB.close()
    return standing

def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
        winner: the id number of the player who won
    loser: the id number of the player who lost
    """
    DB, cursor = connect()
    query = "insert into matches (winner, loser) values(%s,%s)"
    parms = (winner, loser)
    cursor.execute(query, parms)
    DB.commit()
    DB.close()

def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.Each player is paired with another
    player with an equal or nearly - equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
        A list of tuples, each of which contains(id1, name1, id2, name2)
    id1: the first player 's unique id
    name1: the first player 's name
    id2: the second player 's unique id
    name2: the second player 's name
    """
    id1 = 0
    id2 = 0
    name1 = ""
    name2 = ""
    pair = [id1, name1, id2, name2]
    pairings = []
    standing = playerStandings()
    for i in range(0, (len(standing) / 2)):
        pair = [standing[i*2][0], standing[i*2][1], standing[i*2+1][0], standing[i*2+1][1]]
        pairings.append(pair)
    return pairings
