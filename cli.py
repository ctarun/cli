import optparse
import sys

from ConfigParser import ConfigParser
from inspect import getargs
from optparse import OptionParser

class Error(Exception):
    pass

class MainError(Error):
    pass

class Values(optparse.Values):
    delim = '.'

    def set(self, name, value):
        splitted = name.split(self.delim)
        parent = self

        # Build the Values tree.
        for n in name.split(self.delim):
            setattr(parent, n, self.__class__())
            print n
            parent = getattr(parent, n)

        setattr(parent, n, value)

    def update_from_config(self, config_file):
        # XXX: seed the parser with defaults here?
        parser = ConfigParser()
        parser.read(config_file)

        for section in parser.sections():
            for option in parser.options(section):
                name = self.delim.join((section, option))
                # XXX: hook in vars here?
                self.set(name, parser.get(section, option))

    config = property(None, update_from_config)

    def update_from_env(self, env):
        pass

    env = property(None, update_from_env)

    def update_from_cli(self, argv):
        # XXX: hook usage into here.
        parser = OptionParser()
        # add options here.

        opts, args = parser.parse_args(argv)

        return opts, args

    cli = property(None, update_from_cli)

class App(object):
    """A command-line application.

    Command-line applications (CLI apps) perform a task based in
    part on options and arguments passed on the command line. The
    App object makes it easy to develop simple CLI apps.

    Instantiated CLI apps parse options, arguments and (optionally)
    other configuration information and pass them to a single
    callable. This callable must support the App interface, which
    means its signature should be something like the following:

        def main(opts, args, app):

    Whether or not the callable actually _uses_ any of this
    information is optional, though it must accept them.
    """
    values_factory = Values

    def __init__(self, main=None, config_file=None, argv=None,
            env=None, exit_after_main=True):
        self.main = main
        self.config_file = config_file
        self.argv = argv
        self.env = env
        self.exit_after_main = exit_after_main

    @property
    def values(self):
        """Parse all application options.

        In addition to the standard CLI options and arguments, this
        also includes environment variables and configuration file
        directives which are resolved to options and arguments.
        Options specified in more than one of the above sources are
        resolved in the following order, with the rightmost source
        winning:

            configuration -> environment -> CLI

        Returns a tuple (opts, args).
        """
        values = self.values_factory()

        if self.config_file is not None:
            values.config = self.config_file
        if self.env is not None:
            values.env = self.env

        values.cli = self.argv

        return values

    @property
    def opts(self):
        return self.values[0]

    @property
    def args(self):
        return self.values[1]

    @property
    def usage(self):
        return self.main.__doc__ or ''

    def find_main(self, main=None):
        """Find a suitable main() callable.

        If the supplied 'main' argument is not a callable, search
        globals() for a suitable callable. If no callable is found
        or the chosen callable doesn't support the App interface
        (see cli.App.__doc__ for more information), raise MainError.
        """
        if not callable(main):
            main = globals().get('main', None)

        if not callable(main):
            raise MainError("Could not find main()")

        args, varargs, varkw = getargs(main.func_code)

        if len(args) != 3 or (varargs or varkw):
            raise MainError("main() must take three arguments or varargs/varkw")

        return main

    def run(self):
        """Run the application's callable.

        If the callable hasn't already been determined, discover it
        and pass it the resolved options, arguments and Application
        object. If the App.exit_after_main is True, call sys.exit()
        with the return value of the application's callable.
        Otherwise, return the result.
        """
        main = self.find_main(self.main)

        returned = main(self.opts, self.args, self)

        if self.exit_after_main:
            sys.exit(returned)
        else:
            return returned

def main(opts, args, app=None):
    print 'cli.App test!'

if __name__ == '__main__':
    values = Values()

    values.set('foo.bar', 'spam')

    print values.foo.bar

elif False and __name__ == '__main__':
    app = App(config_file='sample.config')

    print app.values
    print app.opts.frobnitz

    #app.run()
