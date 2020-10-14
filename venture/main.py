import csv
import os

from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal

from venture.model.episode.EpisodeRepository import EpisodeRepository
from .controllers.base import Base
from .controllers.episodes import Episodes
from .core.exc import ventureError

# configuration defaults
CONFIG = init_defaults('venture')
CONFIG['venture']['db_file'] = '~/.venture/db.json'
CONFIG['venture']['episode_source_file'] = './data/vb.csv'



def initialise_episode_repository(app):
    # app.episode_repository = EpisodeRepository(app)
    app.extend('ep_repo', EpisodeRepository(app))

class venture(App):
    """Venture Bros Stream Service primary application."""

    class Meta:
        hooks = [

            ('post_setup', initialise_episode_repository),
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
