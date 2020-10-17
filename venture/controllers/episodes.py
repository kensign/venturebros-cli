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

        # search the title

        # get all episode numbers

        # search by duration

    @ex(help=('reports the currently streaming episode'))
    def now(self):
        pass

    @ex(help=('reports the episode up next in the streaming queue'))
    def next(self):
        pass

    @ex(help=('reports the previous episide in the queue'))
    def last(self):
        pass

    @ex(help=('reports what episode will be playing at a given day and time'))
    def when(self):
        pass

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

        Returns:

        """
        id = self.app.pargs.id
        start_time = self.app.pargs.start_time

        if self.app.pargs.now == 'true':
            start_time = datetime.datetime.now().isoformat()

        self.app.ep_repo.get_air_times_table().truncate()
        self.app.ep_repo.set_airtime(id, start_time)
        print(self.app.ep_repo.get_airtime(id))

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
        ],
    )
    def schedule(self):
        """

        Returns:

        """
        if self.app.pargs.id == None:
            self.app.ep_repo.get_air_times_table().truncate()

        self.app.ep_calendar.build_schedule(self.app.pargs.days, self.app.pargs.id)

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
