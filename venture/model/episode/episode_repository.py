import csv
import os

from cement.utils import fs
from tinydb import TinyDB, Query


class EpisodeRepository:
    def __init__(self, app):
        self.logger = app.log
        self.config = app.config
        self.init_tinydb()

    def init_tinydb(self):
        self.logger.info('extending application with tinydb')
        db_file = self.config.get('venture', 'db_file')
        db_file = fs.abspath(db_file)

        self.logger.info('tinydb database file is: %s' % db_file)
        db_dir = os.path.dirname(db_file)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self.db = TinyDB(db_file)

    def initialise_episode_repository(self):
        self.logger.info('initialising episode repository')
        self.clear_tables()
        vb_csv = self.config.get('venture', 'episode_source_file')
        with open(fs.abspath(vb_csv), newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                id = row[0]
                show = row[0].split('-')
                season = show[0]
                episode = show[1]
                duration = row[1]
                title = row[2]
                show = self.get_show_dict(season, episode, title, duration, id)
                self.insert_show(show)
                print('id:{4}, season: {0}, episode: {1}, duration: {3} - {2}'.format(season, episode, title, duration,
                                                                                      id))

    def get_show_dict(self, season="", episode="", title="", duration=0, id=""):

        if len(id):
            season = id.split('-')[0]
            episode = id.split('-')[1]

        return {
            'id': id,
            'season': int(season),
            'episode': int(episode),
            'title': title,
            'duration': int(duration),
        }

    def set_airtime(self, id, air_time):
        Stream = Query()
        table = self.get_air_times_table()
        table.upsert({'air_time': air_time, 'ep_id': id}, Stream.ep_id == id)

    def insert_show(self, show):
        show_table = self.get_shows_table()
        show_table.insert(show)

    def get_show_by_id(self, id):
        Show = Query()
        show_table = self.get_shows_table()
        show = self.get_show_dict(id=id)
        return show_table.get(Show.id == id)

    def get_upcoming_schedule(self):
        Stream = Query()
        table = self.get_air_times_table()
        return table.all()

    def get_all_shows(self):
        show_table = self.get_shows_table()
        shows = show_table.all()
        return sorted(shows, key=lambda i: (i['season'], i['episode']))

    def get_shows_table(self):
        return self.db.table('shows')

    def get_air_times_table(self):
        return self.db.table('air_times')

    def clear_tables(self):
        shows = self.get_shows_table()
        air_times = self.get_air_times_table()

        shows.truncate()
        air_times.truncate()
