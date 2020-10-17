import dateutil.parser
from dateutil.relativedelta import *


class CalendarService():
    """Service for airtime schedule and calendar operations"""

    def __init__(self, app):
        self.logger = app.log
        self.config = app.config
        self.ep_repo = app.ep_repo
        # self.build_schedule(5)

    def build_schedule(self, number_of_days, id=None):
        """
        Given a number of days alone, the schedule will be generated from the values set in the config
        If a seed air time has been set with the sync command, that show can be used as the starting point
        for the generated schedule.
        Args:
            number_of_days: the number of days to project the schedule for, this is approximate
            id: the [season]-[episode] value which represents a unique id for an episode.

        Returns:

        """

        repo = self.ep_repo
        start_episode = None
        shows = repo.get_all_shows()

        seed_date = self.config.get('venture', 'schedule_seed_date')
        seed_id = self.config.get('venture', 'schedule_seed_episode')

        if (id != None):
            seed_id = id
            seed_episode = repo.get_airtime(seed_id)
            seed_date = seed_episode['air_time']

        current_start_time = dateutil.parser.parse(seed_date)

        # iterate to the seed episode and continue the loop for the number of times specified
        for i in range(0, int(number_of_days)):
            if i == 0:
                for show in shows:
                    if show['id'] == seed_id:
                        # save the air_time for the seed episode
                        start_episode = repo.get_show_by_id(seed_id)
                        current_start_time = self.save_air_time(current_start_time, show)

                    # continue with the calculation after the seed episode
                    if start_episode != None:
                        if show['season'] == start_episode['season']:
                            if show['episode'] > start_episode['episode']:
                                current_start_time = self.save_air_time(current_start_time, show)

                        # set air times for the remaining shows before the stream starts over
                        if show['season'] > start_episode['season']:
                            current_start_time = self.save_air_time(current_start_time, show)

            # stream has started over, continue with populating the schedule
            if i > 0:
                for show in shows:
                    current_start_time = self.save_air_time(current_start_time, show)

        print(repo.get_upcoming_schedule())

    def save_air_time(self, current_start_time, show):
        """
        Saves an air time for an episode and calculates the timestamp got the next episodes air time
        based on the current show's duration and the intermission time from the config.
        Args:
            current_start_time: timestamp for the air time
            show: the dictionary for the show being saved

        Returns: The start time for the next episode.

        """
        repo = self.ep_repo
        intermission_length = self.config.get('venture', 'intermission_length_seconds')
        repo.set_airtime(show['id'], current_start_time.isoformat())
        next_start_time = current_start_time + relativedelta(seconds=+intermission_length)
        next_start_time = next_start_time + relativedelta(minutes=+show['duration'])
        return next_start_time

    def reset(self):
        """
        Resets the data for the show schedule
        Returns:

        """
        self.ep_repo.get_air_times_table.truncate()
        print('air times have been cleared')
