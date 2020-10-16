import dateutil.parser
from dateutil.relativedelta import *

class EpisodeCalendar():
    def __init__(self, app):
        self.logger = app.log
        self.config = app.config
        self.ep_repo = app.ep_repo
        # self.build_schedule(5)

    def build_schedule(self, number_of_days):
        seed_date = self.config.get('venture', 'schedule_seed_date')
        seed_episode = self.config.get('venture', 'schedule_seed_episode')
        intermission_length = self.config.get('venture', 'intermission_length_minutes')
        repo = self.ep_repo
        repo.set_airtime(seed_episode, seed_date)
        shows = repo.get_all_shows()
        start_episode = None
        current_start_time = dateutil.parser.parse(seed_date)

        # start at the seed episode and continue the loop for the number of times specified

        for i in range(0, int(number_of_days)):
            if i == 0:
                for show in shows:
                    if show['id'] == seed_episode:
                        ep = repo.get_show_by_id(seed_episode)
                        start_episode = ep

                    if start_episode != None:
                        if show['season'] == start_episode['season']:
                            if show['episode'] > start_episode['episode']:
                                current_start_time = current_start_time + relativedelta(minutes=+show['duration'])
                                repo.set_airtime(show['id'], current_start_time.isoformat())

            if i > 0:
                pass

        print(repo.get_upcoming_schedule())

    def seed_calendar(self, id, start_time):
        season = id.split('-')[0]
        episode = id.split('-')[1]

    def reset(self):
        pass
