import sqlite3
import json

import pandas as pd


class DB:
    def __init__(self):
        self.connection = sqlite3.connect("../SuperEventsSite/db.sqlite3")

    def getAllEvents(self):
        events = pd.read_sql("SELECT * FROM Events_event WHERE is_public = 1", self.connection)
        pages_ids = ','.join(map(str, events.page_ptr_id))
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id in ({pages_ids})", self.connection)
        results = pd.merge(pages, events, left_on='id', right_on='page_ptr_id')
        return results

    def getEvent(self, id):
        events = pd.read_sql(F"SELECT * FROM Events_event WHERE page_ptr_id = {id}", self.connection)
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id = {id}", self.connection)
        results = pd.merge(pages, events, left_on='id', right_on='page_ptr_id')
        return results
    
    def getHall(self, id):
        halls = pd.read_sql(F"SELECT * FROM Events_hall WHERE page_ptr_id = {id}", self.connection)
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id = {id}", self.connection)
        results = pd.merge(pages, halls, left_on='id', right_on='page_ptr_id')
        return results
    
    def getGame(self, id):
        games = pd.read_sql(F"SELECT * FROM Events_game WHERE page_ptr_id = {id}", self.connection)
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id = {id}", self.connection)
        results = pd.merge(pages, games, left_on='id', right_on='page_ptr_id')
        return results

    def getPerformances(self, id):
        performances = pd.read_sql(F"SELECT * FROM Events_performance WHERE page_ptr_id = {id}", self.connection)
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id = {id}", self.connection)
        results = pd.merge(pages, performances, left_on='id', right_on='page_ptr_id')
        return results

    def getHallsFromEvent(self, event):
        e_path = event["path"][0]
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE path LIKE '{e_path}____'", self.connection) 
        halls_ids = ','.join(map(str, pages.id))
        halls = pd.read_sql(f"SELECT * FROM Events_hall WHERE page_ptr_id in ({halls_ids})", self.connection)
        results = pd.merge(pages, halls, left_on='id', right_on='page_ptr_id')
        return results

    def getGamesFromEvent(self, event):
        e_path = event["path"][0]
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE path LIKE '{e_path}____'", self.connection) 
        games_ids = ','.join(map(str, pages.id))
        games = pd.read_sql(f"SELECT * FROM Events_game WHERE page_ptr_id in ({games_ids})", self.connection)
        results = pd.merge(pages, games, left_on='id', right_on='page_ptr_id')
        return results

    def getPerformancesFromHall(self, hall):
        h_path = hall["path"][0]
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE path LIKE '{h_path}____'", self.connection) 
        p_ids = ','.join(map(str, pages.id))
        p_s = pd.read_sql(f"SELECT * FROM Events_performance WHERE page_ptr_id in ({p_ids})", self.connection)
        results = pd.merge(pages, p_s, left_on='id', right_on='page_ptr_id')
        return results
    
    def tryCreateTgUser(self, id, username):
        try:
            pd.DataFrame([{
                "telegram_id": id,
                "telegram_username": username,
            }]).to_sql("Events_telegramusers", self.connection)
        except ValueError:
            pass
    
    def markGP(self, tg_user_id, game_id, gp_id):
        pd.DataFrame([{
            "telegram_id": tg_user_id,
            "game_id": game_id,
            "point_hash": gp_id,
        }]).to_sql("Events_gamepoint2telegramusers", self.connection)
    
    def getGamePoint(self, tg_user_id, game_id):
        return pd.read_sql(f"""
            SELECT * FROM Events_gamepoint2telegramusers
            WHERE (telegram_id = {tg_user_id}) AND (game_id = {game_id})
        """, self.connection) 
        
    
    def getAllGamePoint(self, game_id):
        df =  pd.read_sql(f"""
            SELECT * FROM Events_game
            WHERE (game_id = {game_id})
        """, self.connection)
        return map(lambda x: x["value"], json.loads(df.points[0])["point"])
