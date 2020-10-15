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
            })
        ],
    )
    def list(self):
        season = self.app.pargs.season
        episode = self.app.pargs.episode
        title = self.app.pargs.title
        duration = self.app.pargs.duration
        self.app.log.info('searching for season %s, episode %s' % (season, episode))
        repo = self.app.ep_repo
        show = repo.get_show_dict(season, episode, title, duration)
        # self.app.log.info(show)

        self.app.log.info(repo.get_show_by_id(show))

    @ex(help=('reports the currently streaming episode'))
    def now(self):
        pass

    @ex(help=('reports the episode up next in the streaming queue'))
    def next(self):
        pass

    @ex(help=('reports the previous episide in the que'))
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
        id = self.app.pargs.id
        start_time = self.app.pargs.start_time

        if self.app.pargs.now == 'true':
            start_time = datetime.datetime.now().isoformat()

        self.app.ep_repo.synchronise(id, start_time)

    @ex(help=('initialise db'))
    def load(self):
        repo = self.app.ep_repo
        repo.initialise_episode_repository()
