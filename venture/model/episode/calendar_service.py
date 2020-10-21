from datetime import datetime

import dateutil.parser
import dateutil.tz
from dateutil.relativedelta import *


class CalendarService:
    """Service for airtime schedule and calendar operations"""

    def __init__(self, app):
        self.logger = app.log
        self.config = app.config
        self.ep_repo = app.ep_repo
        self.nztz = dateutil.tz.gettz('Pacific/Auckland')
        self.pdt = dateutil.tz.gettz('US/Pacific')
        self.est = dateutil.tz.gettz('US/Eastern')

        # self.build_schedule(5)

    def build_schedule(self, number_of_days, ep_id=None):
        """
        Given a number of days alone, the schedule will be generated from the values set in the config
        If a seed air time has been set with the sync command, that show can be used as the starting point
        for the generated schedule.
        Args:
            number_of_days: the number of days to project the schedule for, this is approximate
            ep_id: the [season]-[episode] value which represents a unique id for an episode.

        Returns:

        """

        repo = self.ep_repo
        shows = repo.get_all_shows()

        seed_date = self.config.get('venture', 'schedule_seed_date')
        seed_id = self.config.get('venture', 'schedule_seed_episode')

        if ep_id is not None:
            seed_id = ep_id
            seed_episode = repo.get_air_time(seed_id)
            seed_date = seed_episode[0]['air_time']

        current_start_time = dateutil.parser.parse(seed_date)

        start_episode = repo.get_show_by_id(seed_id)

        # iterate to the seed episode and continue the loop for the number of times specified
        for i in range(0, int(number_of_days)):
            if i == 0:
                for show in shows:
                    # save the air_time for the seed episode
                    if show['id'] == seed_id:
                        current_start_time = self.save_air_time(current_start_time, show)

                    # continue with the calculation for the seed's season after the seed episode
                    if show['season'] == start_episode['season']:
                        if show['episode'] > start_episode['episode']:
                            current_start_time = self.save_air_time(current_start_time, show)

                    # set air times for the remaining seasons before the stream starts over
                    if show['season'] > start_episode['season']:
                        current_start_time = self.save_air_time(current_start_time, show)

            # stream has started over, continue with populating the schedule
            if i > 0:
                for show in shows:
                    current_start_time = self.save_air_time(current_start_time, show)

    def save_air_time(self, current_start_time, show):
        """
        Saves an air time for an episode and calculates the timestamp for the next episode's air time
        based on the current show's duration and the intermission time from the config.
        Args:
            current_start_time: timestamp for the air time
            show: the dictionary for the show being saved

        Returns: The start time for the next episode.

        """
        repo = self.ep_repo
        intermission_length = self.config.get('venture', 'intermission_length_seconds')
        show_time = show['duration'].split(':')
        repo.set_air_time(show['id'], current_start_time.isoformat())
        next_start_time = current_start_time + relativedelta(minutes=+int(show_time[0]), seconds=+int(show_time[1]))
        next_start_time = next_start_time  + relativedelta(seconds=+intermission_length)
        return next_start_time

    def reset(self):
        """
        Resets the data for the show schedule
        Returns:

        """
        self.ep_repo.get_air_times_table().truncate()
        print('air times have been cleared')

    def view_current_episode(self):
        """
        Filters the currently loaded shows and air times and displays the episode scheduled
        to air at the time the command was executed.
        Returns:

        """
        repo = self.ep_repo
        shows = self.ep_repo.get_upcoming_schedule()
        for show in shows:
            air_time = datetime.fromisoformat(show['air_time'])
            episode = repo.get_show_by_id(show['id'])
            show_time = episode['duration'].split(':')
            end_time = air_time + relativedelta(minutes=+int(show_time[0]), seconds=+int(show_time[1]))
            now = datetime.now()

            if now > air_time and now < end_time:
                episode.update(show)
                self.print_episode(episode)

            # print(air_time)

    def view_episode_air_times(self, ep_id):
        """
        Takes an episode ID, and shows the airtime information bases
        on the loaded shows and air time schedule.
        Args:
            ep_id: [season]-[episode]

        Returns:

        """
        repo = self.ep_repo
        episodes = repo.get_air_time(ep_id)

        for episode in episodes:
            self.print_episode(episode)

    def print_episode(self, episode):
        air_time = datetime.fromisoformat(episode['air_time'])
        print(episode['id'] + ' ' + episode['title'])
        print('runtime: ' + str(episode['duration']) + ' min')
        air_time.replace(tzinfo=self.nztz)
        print('NZT: ' + air_time.isoformat())
        print('PDT: ' + air_time.astimezone(self.pdt).isoformat())
        print('EST: ' + air_time.astimezone(self.est).isoformat())
        print('\n')
