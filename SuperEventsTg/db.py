import sqlite3
import pandas as pd


class DB:
    def __init__(self):
        self.connection = sqlite3.connect("../SuperEventsSite/db.sqlite3")

    def getAllEvents(self):
        events = pd.read_sql("SELECT * FROM Events_event WHERE is_public = 1", self.connection)
        pages_ids = ','.join(map(str, events.page_ptr_id))
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id in ({pages_ids})", self.connection)
        results = pages.join(events)
        return results

    def getEvent(self, id):
        events = pd.read_sql(F"SELECT * FROM Events_event WHERE page_ptr_id = {id}", self.connection)
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE id = {id}", self.connection)
        results = pages.join(events)
        return results

    def getHallsFromEvent(self, event):
        e_path = event["path"][0]
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE path LIKE '{e_path}____'", self.connection) 
        halls_ids = ','.join(map(str, pages.id))
        halls = pd.read_sql(f"SELECT * FROM Events_hall WHERE page_ptr_id in ({halls_ids})", self.connection)
        results = pages.join(halls)
        return results

    def getPerformancesFromHall(self, hall):
        h_path = hall["path"][0]
        pages = pd.read_sql(f"SELECT * FROM wagtailcore_page WHERE path LIKE '{h_path}____'", self.connection) 
        p_ids = ','.join(map(str, pages.id))
        halls = pd.read_sql(f"SELECT * FROM Events_performance WHERE page_ptr_id in ({p_ids})", self.connection)
        results = pages.join(halls)
        return results

