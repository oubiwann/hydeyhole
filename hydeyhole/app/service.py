import sys

from twisted.application import service, internet
from twisted.python import usage

from carapace.sdk import const as sshConst, registry, scripts

from hydeyhole import meta
from hydeyhole.app.shell.service import getHyShellFactory


config = registry.getConfig()


class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class Options(usage.Options):
    """
    """
    subCommands = [
        [sshConst.KEYGEN, None, SubCommandOptions,
         "Generate ssh keys for the server"],
        [sshConst.SHELL, None, SubCommandOptions, "Login to the server"],
        [sshConst.STOP, None, SubCommandOptions, "Stop the server"]]

    def parseOptions(self, options):
        usage.Options.parseOptions(self, options)
        # check options
        if self.subCommand == sshConst.KEYGEN:
            scripts.KeyGen()
            sys.exit(0)
        elif self.subCommand == sshConst.SHELL:
            scripts.ConnectToShell()
            sys.exit(0)
        elif self.subCommand == sshConst.STOP:
            scripts.StopDaemon()
            sys.exit(0)


def makeSSHService(options, application, services):
    """
    Setup SSH for HydeyHole.
    """
    sshFactory = getHyShellFactory(app=application, services=services)
    sshServer = internet.TCPServer(config.ssh.port, sshFactory)
    sshServer.setName(config.ssh.servicename)
    sshServer.setServiceParent(services)
    return sshServer


def makeService(options):
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)
    makeSSHService(options, application, services)
    return services
