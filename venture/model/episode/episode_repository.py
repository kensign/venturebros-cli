import csv
import os

from cement.utils import fs
from tinydb import TinyDB, Query


class EpisodeRepository:
    """
    Persistence operations for episodes and airtimes
    """

    def __init__(self, app):
        """
        Constructor, sets logger and config and initialises the db.
        Args:
            app:
        """
        self.logger = app.log
        self.config = app.config
        self.db = self.init_tinydb()

    def init_tinydb(self):
        """
        Initialises TinyDB.
        Returns:

        """
        self.logger.info('extending application with tinydb')
        db_file = self.config.get('venture', 'db_file')
        db_file = fs.abspath(db_file)

        self.logger.info('tinydb database file is: %s' % db_file)
        db_dir = os.path.dirname(db_file)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        return TinyDB(db_file)

    def initialise_episode_repository(self):
        """
        Loads the episodes from CSV data into TinyDB
        Returns:

        """
        self.logger.info('initialising episode repository')
        self.clear_tables()
        vb_csv = self.config.get('venture', 'episode_source_file')
        with open(fs.abspath(vb_csv), newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                ep_id = row[0]
                show = row[0].split('-')
                season = show[0]
                episode = show[1]
                duration = row[1]
                title = row[2]
                show = EpisodeRepository.get_show_dict(season, episode, title, duration, ep_id)
                self.insert_show(show)
                print('id:{4}, season: {0}, episode: {1}, duration: {3} - {2}'.format(season, episode, title, duration,
                                                                                      ep_id))

    @staticmethod
    def get_show_dict(season='', episode='', title='', duration='', ep_id=''):
        """

        Args:
            season:
            episode:
            title:
            duration:
            ep_id:

        Returns:

        """
        if len(ep_id):
            season = ep_id.split('-')[0]
            episode = ep_id.split('-')[1]

        return {
            'id': ep_id,
            'season': int(season),
            'episode': int(episode),
            'title': title,
            'duration': duration,
        }

    def set_air_time(self, ep_id, air_time):
        """

        Args:
            ep_id:
            air_time:

        Returns:

        """
        table = self.get_air_times_table()
        table.insert({'air_time': air_time, 'id': ep_id})

    def get_air_time(self, ep_id):
        """

        Args:
            ep_id:

        Returns:

        """
        q = Query()
        table = self.get_air_times_table()
        episodes = table.search(q.id == ep_id)
        shows = []
        for episode in episodes:
            show = self.get_show_by_id(episode['id'])
            show.update(episode)
            shows.append(show)
        return shows

    def insert_show(self, show):
        """

        Args:
            show:

        Returns:

        """
        table = self.get_shows_table()
        table.insert(show)

    def get_show_by_id(self, ep_id):
        """

        Args:
            ep_id:

        Returns:

        """
        q = Query()
        table = self.get_shows_table()
        return table.get(q.id == ep_id)

    def get_upcoming_schedule(self):
        """

        Returns:

        """
        table = self.get_air_times_table()
        return table.all()

    def get_episodes_by_season(self, season):
        q = Query()
        table = self.get_shows_table()
        return table.search(q.season == season)

    def get_all_shows(self):
        """

        Returns:

        """
        table = self.get_shows_table()
        shows = table.all()
        return sorted(shows, key=lambda i: (i['season'], i['episode']))

    def get_shows_table(self):
        """

        Returns:

        """
        return self.db.table('shows')

    def get_air_times_table(self):
        """

        Returns:

        """
        return self.db.table('air_times')

    def clear_tables(self):
        """

        Returns:

        """
        shows = self.get_shows_table()
        air_times = self.get_air_times_table()

        shows.truncate()
        air_times.truncate()
