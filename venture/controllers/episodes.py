import datetime

from cement import Controller, ex


class Episodes(Controller):
    class Meta:
        label = 'episodes'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(
        help=('list episodes'),
        arguments=[
            (['--season'],
             {'help': 'Season number',
              'action': 'store',
              'dest': 'season'}),
            (['--episode'], {
                'help': 'Episode number',
                'action': 'store',
                'dest': 'episode'
            }),
            (['--title'], {
                'help': 'Episode title',
                'action': 'store',
                'dest': 'title'
            }),
            (['--duration'], {
                'help': 'Runtime in minutes',
                'action': 'store',
                'dest': 'duration'
            }),
            (['--all'], {
                'help': 'All episodes, ordered by season, episode',
                'action': 'store',
                'dest': 'show_all'
            })
        ],
    )
    def list(self):
        """
        Lists the episode catalogue
        Returns:

        """
        season = self.app.pargs.season
        episode = self.app.pargs.episode
        title = self.app.pargs.title
        duration = self.app.pargs.duration
        show_all = self.app.pargs.show_all

        repo = self.app.ep_repo
        # show = repo.get_show_dict(season, episode, title, duration)
        # self.app.log.debug(show_all, 'show_all')

        # self.app.log.info(repo.get_show_by_id(show))
        if show_all == 'true':
            shows = repo.get_all_shows()
            for show in shows:
                print(show)

            return

        if season != None and episode != None:
            self.app.log.info('searching for season %s, episode %s' % (season, episode))
            id = season + "-" + episode
            show = repo.get_show_by_id(id)
            print(show)
            return

        # get all episodes in a season
        if season != None and episode == None:
            shows = repo.get_episodes_by_season(int(season))

            for show in shows:
                print(show)

            return

        # search by the title

        # get all episode numbers

        # search by duration

    @ex(help=('reports the currently streaming episode'))
    def now(self):
        print('current episode')
        self.app.ep_calendar.view_current_episode()

    @ex(help=('reports the episode up next in the streaming queue'))
    def next(self):
        print('next episode')

    @ex(help=('reports the previous episide in the queue'))
    def last(self):
        print('previous episode')

    @ex(help=('resets the calandar'))
    def reset(self):
        self.app.ep_calendar.reset()

    @ex(
        help=('reports when an give episode will be playing at a given day and time'),
        arguments=[
            (['--id'],
             {'help': 'The unique identifier for the episode synchronisation. Ex: 7-1, (season 7 episode 1)',
              'action': 'store',
              'dest': 'id'})
        ],
    )
    def when(self):
        print('Scheduled air times')
        self.app.ep_calendar.view_episode_air_times(self.app.pargs.id)

    @ex(
        help=('Provide an episode id and time to synchronise the application with the AS stream'),
        arguments=[
            (['--id'],
             {'help': 'The unique identifier for the episode synchronisation. Ex: 7-1, (season 7 episode 1)',
              'action': 'store',
              'dest': 'id'}),
            (['--time'],
             {'help': 'ISO timestamp that marks the beginning of the related episode. Ex: 2020-10-15T22:55:02.291090',
              'action': 'store',
              'dest': 'start_time'}),
            (['--now'],
             {'help': 'use the current local time as the ISO timestamp for the show\'s start time',
              'action': 'store',
              'dest': 'now'})
        ],

    )
    def sync(self):
        """
        Syncs the calendar with the provided episode.
        Returns:

        """
        id = self.app.pargs.id
        start_time = self.app.pargs.start_time

        if self.app.pargs.now == 'true':
            start_time = datetime.datetime.now().isoformat()

        self.app.ep_calendar.reset()
        self.app.ep_repo.set_air_time(id, start_time)
        # self.app.ep_calendar.build_schedule(7, id)
        print(self.app.ep_repo.get_air_time(id))

    @ex(help=('initialise db'))
    def load(self):
        repo = self.app.ep_repo
        repo.initialise_episode_repository()

    @ex(
        help=('Set stream schedule. The schedule can be based on an existing airtime record for an episode'),
        arguments=[
            (['--id'],
             {'help': 'Identifier for the season and episode from which to schedule should be based on. Ex: 5-4',
              'action': 'store',
              'dest': 'id'}),
            (['--days'],
             {'help': 'The number of days to build the schedule for. ',
              'action': 'store',
              'dest': 'days'}),
            (['--list'],
             {'help': 'Print the currently generated schedule ',
              'dest': 'list'}),

        ],
    )
    def schedule(self):
        """
        Create the schedule for a number of days, based off an existing air time or the config. Defaults to config if no id is
        specified.

        Returns:

        """
        if self.app.pargs.id == None and self.app.pargs.list is None:
            self.app.ep_calendar.reset()

        if self.app.pargs.list is not None:
            self.print_schedule()
            return

        if self.app.pargs.days is not None:
            self.app.ep_calendar.build_schedule(self.app.pargs.days, self.app.pargs.id)
            self.print_schedule()

    def print_schedule(self):
        shows = self.app.ep_repo.get_upcoming_schedule()
        for show in shows:
            print(show)

    # self.app.log.info('start index:', start_index)

    # @ex(
    #     help=(''),
    #     arguments=[
    #         ([''],
    #          {'':'',
    #           '':'',
    #           '':''}),
    #     ],
    # )
    # def (self):
