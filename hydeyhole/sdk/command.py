from pprint import pprint
from operator import itemgetter

from carapace.sdk import registry

from hydeyhole.app import shell


config = registry.getConfig()


class CommandRegistry(object):
    """
    This class provides a global registry that tracks all the "commands"
    (API methods) that have been set as allowed for exposure to end users.
    """
    registry = []

    def add(self, func):
        """
        This methods is intended to be used as a decorator on API methods. Any
        method that has been decorated with it will have an entry in the command
        registry.
        """
        self.registry.append(func.func_name)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.wrapper = func
        return wrapper

    def __iter__(self):
        for x in self.registry:
            yield x

commands = CommandRegistry()


class Helper(object):
    """
    Type (help object) for help about an object.
    """
    def __init__(self):
        import pydoc
        self.pydoc = pydoc

    def __repr__(self):
        return self.__doc__

    def __call__(self, *args, **kwargs):
        if not args and not kwargs:
            print repr(self)
            return
        if args and hasattr(args[0], "wrapper"):
            newargs = (args[0].wrapper,)
            return self.pydoc.help(*newargs, **kwargs)
        return self.pydoc.help(*args, **kwargs)


class BaseAPI(object):
    """
    """
    _commands = commands
    _subAPIs = {}

    def __init__(self):
        from hydeyhole.sdk import command
        self.command = command

    def _getNonSubAPIs(self):
        return [self.command.BaseAPI, object]

    def getAPILookup(self):
        if self._subAPIs:
            return self._subAPIs
        skip = self._getNonSubAPIs()
        for klass in self.__class__.__mro__:
            if klass in skip:
                continue
            for command in self._commands:
                if hasattr(klass, command):
                    self._subAPIs.update({command: klass.__name__})
        return self._subAPIs

    def getCommands(self):
        """
        """
        return list(self._commands)


class ShellAPI(BaseAPI):
    """
    """
    def __init__(self):
        super(ShellAPI, self).__init__()
        self.namespace = None
        self.terminal = None
        self.appData = None
        self.appOrig = None
        self.helper = Helper()

    def setNamespace(self, namespace):
        self.namespace = namespace

    def setTerminal(self, terminal):
        self.terminal = terminal

    def setAppData(self):
        if not self.namespace:
            return
        if not self.appData:
            self.appData = {
                "servicecollection": self.appOrig._adapterCache.get(
                    "twisted.application.service.IServiceCollection"),
                "multiservice": self.appOrig._adapterCache.get(
                    "twisted.application.service.IService"),
                "process": self.appOrig._adapterCache.get(
                    "twisted.application.service.IProcess")}

    def getAppData(self):
        return pprint(self.appData)

    def fixupName(self, value, name):
        if not hasattr(value, "wrapper"):
            return name
        return self.getAPILookup().get(value.wrapper.func_name)

    @commands.add
    def app(self):
        return self.appData

    @commands.add
    def help(self, *args, **kwargs):
        return self.helper(*args, **kwargs)

    @commands.add
    def dir(self, obj=None):
        if obj is None:
            data = self.namespace.keys()
        else:
            data = dir(obj)
        return sorted(
            [x.replace("_", "-") for x in data])

    @commands.add
    def ls(self, sortby="name"):
        """
        List the objects in the current namespace, sorted by name (default)
        or by module.

        If you wish to sort by module, simply do the following:
            (ls sortby="moduule")
        """
        width = max([len(x) for x in self.namespace.keys()])
        data = []
        for key, value in self.namespace.items():
            if key == "_":
                continue
            info = ""
            if (isinstance(value, dict) or
                isinstance(value, list) or
                key == "services"):
                info = "data"
            elif type(value).__name__ == "module":
                info = value.__name__
            elif type(value).__name__ == "function":
                info = "%s.%s" % (value.__module__, value.__name__)
            elif type(value).__name__ == "instance":
                info = "%s.%s" % (
                    value.__module__,
                    self.fixupName(value, value.__class__.__name__))
            elif hasattr(value, "im_class"):
                info = "%s.%s.%s" % (
                    value.im_class.__module__,
                    self.fixupName(value, value.im_class.__name__),
                    key)
            elif hasattr(value, "__class__") and hasattr(value, "__module__"):
                info = "%s.%s.%s" % (
                    value.__module__,
                    self.fixupName(value, value.__class__.__name__),
                    key)
            else:
                info = "<Unknown>"
            data.append((key, info))
        if sortby == "name":
            data = sorted(data)
        elif sortby == "module":
            data = sorted(data, key=itemgetter(1))
        for key, datum in data:
            print "\t%s - %s" % (key.replace("_", "-").ljust(width), datum)

    @commands.add
    def banner(self):
        """
        Display the login banner and associated help or info.
        """
        print shell.hyshell.renderBanner(
            help=config.ssh.banner_help,
            welcome=config.ssh.banner_welcome)

    @commands.add
    def clear(self):
        self.terminal.reset()

    @commands.add
    def quit(self):
        self.terminal.loseConnection()


class CommandAPI(ShellAPI):
    """
    Gather all of the command APIs together.
    """
    def _getNonSubAPIs(self):
        return [self.command.CommandAPI] + super(
            CommandAPI, self)._getNonSubAPIs()
