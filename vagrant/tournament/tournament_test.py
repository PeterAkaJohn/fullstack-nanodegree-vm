#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    registerPlayer("Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches()
    standings = playerStandings()
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."

def testMultipleTournamentsCountAndRegister():
    """Test count players in all tournaments and their registration"""
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    tournament_id_1 = retrieveLastPlayerTournamentId()
    registerPlayer("Bob")
    registerPlayer("Rainbow sh")
    registerPlayer("Rainbow ash")
    registerPlayer("Rainbow h")
    registerPlayer("ow Dash")
    registerPlayer("inbow Dash")
    registerPlayer("Raow Dash")
    registerPlayer("RainbDash")
    tournament_id_2 = retrieveLastPlayerTournamentId()
    if tournament_id_1 == tournament_id_2:
        raise ValueError("After 9 players, a new tournament must be created for the ninth player")
    print "11. After 9 player the last player has a different tournament_id"
    registerPlayer("Rainbow ")
    tournament_id_3 = retrieveLastPlayerTournamentId()
    if tournament_id_3 == tournament_id_2 or tournament_id_3 == tournament_id_2:
        raise ValueError("After 17 players, a new tournament must be created for the 17th player")
    print "12. After 17 player the last player has a different tournament_id and a new tournament has been created"

    tournaments = retrieveAllTournamentId()
    for tournament_id in tournaments:
        num_players = countPlayersInTournament(tournament_id)
        if num_players not in [1,8,8]:
            raise ValueError("Players should be 1,8,8")
    print "13. Number of players in each tournament is correct."

def testMultipleTournamentsReportMatches():
    """Test for multiple tournaments """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    registerPlayer("Bob")
    registerPlayer("Rainbow sh")
    registerPlayer("Rainbow ash")
    registerPlayer("Rainbow h")
    registerPlayer("ow Dash")
    registerPlayer("inbow Dash")
    registerPlayer("Raow Dash")
    registerPlayer("RainbDash")
    tournaments = retrieveAllTournamentId()
    first_tournament = tournaments[0][0]  #access first element of the tuple which is the id
    second_tournament = tournaments[1][0]
    standings_first_tournament = playerStandingsForTournament(first_tournament)
    standings_second_tournament = playerStandingsForTournament(second_tournament)
    """Test First Tournament"""
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings_first_tournament]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    standings_first_tournament = playerStandingsForTournament(first_tournament)
    for (i, n, w, m) in standings_first_tournament:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3, id5, id7) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4, id6, id8) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "14. After a match, players have updated standings."
    deleteMatches()
    standings_first_tournament = playerStandingsForTournament(first_tournament)
    if len(standings_first_tournament) != 8:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings_first_tournament:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "15. After match deletion, player standings are properly reset.\n16. Matches are properly deleted."

    """Test Second Tournament"""
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings_second_tournament]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    standings_second_tournament = playerStandingsForTournament(second_tournament)
    for (i, n, w, m) in standings_second_tournament:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3, id5, id7) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4, id6, id8) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "17. After a match, players have updated standings."
    deleteMatches()
    standings_second_tournament = playerStandingsForTournament(second_tournament)
    if len(standings_second_tournament) != 8:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings_second_tournament:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "18. After match deletion, player standings are properly reset.\n19. Matches are properly deleted."

def testMultipleTournamentsSwissPairings():
    """Test for swiss pairings for multiple tournaments"""
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    registerPlayer("Bob")
    registerPlayer("Rainbow sh")
    registerPlayer("Rainbow ash")
    registerPlayer("Rainbow h")
    registerPlayer("ow Dash")
    registerPlayer("inbow Dash")
    registerPlayer("Raow Dash")
    registerPlayer("RainbDash")
    tournaments = retrieveAllTournamentId()
    first_tournament_id = tournaments[0][0] # tournaments[0][0] is the first tournament_id
    second_tournament_id = tournaments[1][0] # second tournament_id
    standings_first_tournament = playerStandingsForTournament(first_tournament_id)
    standings_second_tournament = playerStandingsForTournament(second_tournament_id)
    """Test First Tournament"""
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings_first_tournament]
    first_tournament_pairings = swissPairingsForTournament(first_tournament_id)
    if len(first_tournament_pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(first_tournament_pairings)))
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    first_tournament_pairings = swissPairingsForTournament(first_tournament_id)
    if len(first_tournament_pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(first_tournament_pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = first_tournament_pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "19. After one match, players with one win are properly paired."

    """Test Second Tournament"""
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings_second_tournament]
    second_tournament_pairings = swissPairingsForTournament(second_tournament_id)
    if len(second_tournament_pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(second_tournament_pairings)))
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    second_tournament_pairings = swissPairingsForTournament(second_tournament_id)
    if len(second_tournament_pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(second_tournament_pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = second_tournament_pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "20. After one match, players with one win are properly paired."
    if first_tournament_pairings == second_tournament_pairings:
        raise ValueError("Pairings of different tournaments should be different")
    print "21. Pairs are different"

if __name__ == '__main__':
    """Required tests"""
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "End of required tests!!!!!!!!"
    """Multiple Tournaments tests"""
    print "Start of multiple tournaments tests!!!!!!!!!"
    testMultipleTournamentsCountAndRegister()
    testMultipleTournamentsReportMatches()
    testMultipleTournamentsSwissPairings()
    print "Success!  All tests pass!"
