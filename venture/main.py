from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal

from venture.model.episode.calendar_service import CalendarService
from venture.model.episode.episode_repository import EpisodeRepository
from .controllers.base import Base
from .controllers.episodes import Episodes
from .core.exc import ventureError

# configuration defaults
CONFIG = init_defaults('venture')
CONFIG['venture']['db_file'] = '~/.venture/db.json'
CONFIG['venture']['episode_source_file'] = './venture/data/vb.csv'
CONFIG['venture']['intermission_length_seconds'] = 120
CONFIG['venture']['schedule_seed_date'] = '2020-10-17T12:13:49.443835'
CONFIG['venture']['schedule_seed_episode'] = '6-1'
CONFIG['venture']['debug'] = True


# handlers for hooks, build dependencies, do DI
def inject_episode_repository(app):
    app.extend('ep_repo', EpisodeRepository(app))


def inject_calendar(app):
    app.extend('ep_calendar', CalendarService(app))


class venture(App):
    """Venture Bros Stream Service primary application."""

    class Meta:
        hooks = [
            ('post_setup', inject_episode_repository),
            ('post_setup', inject_calendar)
        ]

        label = 'venture'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Episodes
        ]


class ventureTest(TestApp, venture):
    """A sub-class of venture that is better suited for testing."""

    class Meta:
        label = 'venture'


def main():
    with venture() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except ventureError as e:
            print('ventureError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
