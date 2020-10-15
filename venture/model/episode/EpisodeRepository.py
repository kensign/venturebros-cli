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
        self.db.truncate()
        vb_csv = self.config.get('venture', 'episode_source_file')
        with open(fs.abspath(vb_csv), newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                show = row[0].split('-')
                season = show[0]
                episode = show[1]
                duration = row[1]
                title = row[2]
                show = self.get_show_dict(season, episode, title, duration)
                self.insert_show(show)
                print('season: {0}, episode: {1}, duration: {3} - {2}'.format(season, episode, title, duration))

    def get_show_dict(self, season, episode, title, duration):
        return {
            'season': season,
            'episode': episode,
            'title': title,
            'duration': duration,
            'start_time': "",
        }

    def insert_show(self, show):
        show_table = self.db.table('shows')
        show_table.insert(show)

    def get_show_by_id(self, show):
        Show = Query()
        show_table = self.db.table('shows')

        return show_table.get((Show.season == show['season']) & (Show.episode == show['episode']))

    def synchronise(self, id, start_time):
        Show = Query()
        season = id.split('-')[0]
        episode = id.split('-')[1]

        show_table = self.db.table('shows')

        id = show_table.update({'start_time': start_time}, (Show.season == season) & (Show.episode == episode))

        self.logger.info(self.get_show_by_id({'season': season, 'episode': episode}))
