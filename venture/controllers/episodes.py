import csv

from cement import Controller, ex


class Episodes(Controller):
    class Meta:
        label = 'episodes'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help=('list episodes'))
    def list(self):
        pass

    @ex(
        help=('Add an episode'),
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
    def create(self):
        season = self.app.pargs.season
        episode = self.app.pargs.episode
        title = self.app.pargs.title
        duration = self.app.pargs.duration
        self.app.log.info('Adding episode: %s to season %s' % (episode, season))
        repo = self.app.ep_repo
        show = repo.get_show_dict(season, episode, title, duration)

        repo.insert_show(show)




