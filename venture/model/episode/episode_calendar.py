import dateutil.parser
from dateutil.relativedelta import *


class EpisodeCalendar():
    def __init__(self, app):
        self.logger = app.log
        self.config = app.config
        self.ep_repo = app.ep_repo
        # self.build_schedule(5)

    def build_schedule(self, number_of_days, id=None):

        repo = self.ep_repo
        intermission_length = self.config.get('venture', 'intermission_length_seconds')
        start_episode = None
        shows = repo.get_all_shows()

        seed_date = self.config.get('venture', 'schedule_seed_date')
        seed_id = self.config.get('venture', 'schedule_seed_episode')

        if (id != None):
            seed_id = id
            seed_episode = repo.get_airtime(seed_id)
            seed_date = seed_episode['air_time']
        else:
            repo.set_airtime(seed_id, seed_date)

        current_start_time = dateutil.parser.parse(seed_date)

        # iterate to the seed episode and continue the loop for the number of times specified
        for i in range(0, int(number_of_days)):
            if i == 0:
                for show in shows:
                    if show['id'] == seed_id:
                        start_episode = repo.get_show_by_id(seed_id)

                    # initially, start the calculation after the seed episode
                    if start_episode != None:
                        if show['season'] == start_episode['season']:
                            if show['episode'] > start_episode['episode']:
                                current_start_time = current_start_time + relativedelta(minutes=+show['duration'])
                                current_start_time = current_start_time + relativedelta(seconds=+intermission_length)
                                repo.set_airtime(show['id'], current_start_time.isoformat())

                        # set air times for the remaining shows before the stream starts over
                        if show['season'] > start_episode['season']:
                            current_start_time = current_start_time + relativedelta(minutes=+show['duration'])
                            current_start_time = current_start_time + relativedelta(seconds=+intermission_length)
                            repo.set_airtime(show['id'], current_start_time.isoformat())

            # stream has started over, continue with populating the schedule
            if i > 0:
                for show in shows:
                    current_start_time = current_start_time + relativedelta(minutes=+show['duration'])
                    current_start_time = current_start_time + relativedelta(seconds=+intermission_length)
                    repo.set_airtime(show['id'], current_start_time.isoformat())

        print(repo.get_upcoming_schedule())

    def seed_calendar(self, id, start_time):
        season = id.split('-')[0]
        episode = id.split('-')[1]

    def reset(self):
        pass
