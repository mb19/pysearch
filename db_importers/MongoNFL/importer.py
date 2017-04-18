
from crawlers.nfl_crawler import NFLCrawler
from crawlers.scraper import Scraper
from crawlers.coach_scraper import CoachScraper
from crawlers.team_scraper import TeamScraper

from pymongo import MongoClient, TEXT

import urllib
import os

class NFLImporter(object):

    def __init__(self, db):
        self.__db = db

    def __reset(self):
        """ Resets the database by deleting every record in every table. """
        
        print "Resetting database state..."
        self.__db.teams.drop()
        self.__db.players.drop()
        print "Database reset"

    def __insertPlayers(self, players):
        insertedIds = self.__db.players.insert_many(players)
        self.__db.players.create_index([
            ('name', TEXT),
            ('url', TEXT),
            ('number', TEXT),
            ('team.name', TEXT),
            ('position.name', TEXT)], default_language='english')
        return insertedIds.inserted_ids

    def __insertTeams(self, teams):
        self.__db.teams.insert_many(teams)

    def __scrape(self):
        """ Main method for scraping all relevant data. """

        print "Scraping data..."
        # Build scrapers
        nfl = NFLCrawler()
        teamScraper = TeamScraper()
        team = Scraper()

        # Scrape data
        html = nfl.getClubsHtml()
        teams = team.scrape(html)

        # add the list of players to a team.
        for team in teams:
            players = teamScraper.scrape(team)
            playerIds = self.__insertPlayers(players)
            team['players'] = playerIds

        self.__insertTeams(teams)
        print "Done scraping data..."

    def import_data(self):
        self.__reset()
        self.__scrape()