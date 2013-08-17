from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

from zope.interface import moduleProvides

from carapace.config import Config, Configurator, main, ssh
from carapace.sdk import interfaces

from hydeyhole import meta


moduleProvides(interfaces.IConfig)


# Main
main.config.datadir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.installedfile = os.path.join(
    main.config.datadir, main.config.localfile)


# SSH Server for game
ssh.servicename = meta.description
ssh.port = 9222
ssh.keydir = os.path.join(main.config.datadir, "ssh")
ssh.userdirtemplate = os.path.join(main.config.datadir, "users", "{{USER}}")
ssh.userauthkeys = os.path.join(ssh.userdirtemplate, "authorized_keys")
ssh.usesystemkeys = True
ssh.banner = """:
: Welcome to
:  _         _         _       _
: | |_ _ _ _| |___ _ _| |_ ___| |___
: |   | | | . | -_| | |   | . | | -_|
: |_|_|_  |___|___|_  |_|_|___|_|___|
:     |___|       |___|
:
: You have logged into a HydeyHole Shell Server.
: {{WELCOME}}
: {{HELP}}
:
: Enjoy!
:
"""
ssh.banner_welcome = """
: You have logged onto a HydeyHole Server; you are currently at a Hy
: command prompt. Hy is a Lisp dialect of Python of which you can
: learn more about here:
:   https://github.com/hylang/hy
:"""
ssh.banner_help = """
: Type '(ls)' or '(dir)' to see the objects in the current namespace.
: Use (help ...) to get API docs for available objects."""


class HydeyHoleConfigurator(object):
    """
    """
    def __init__(self, main=None, ssh=None):
        self.main = main
        self.ssh = ssh

    def buildDefaults(self):
        config = super(HydeyHoleConfigurator, self).buildDefaults()
        config.set("SSH", "welcome", self.ssh.welcome)
        config.set("SSH", "banner_help", self.ssh.banner_help)
        config.set("SSH", "banner_welcome", self.ssh.banner_welcome)
        return config

    def updateConfig(self):
        config = super(HydeyHoleConfigurator, self).updateConfig()
        if not config:
            return
        ssh = self.ssh
        ssh.banner_welcome = config.get("SSH", "banner_welcome")
        ssh.banner_help = config.get("SSH", "banner_help")
        return config


def configuratorFactory():
    return HydeyHoleConfigurator(main, ssh)


def updateConfig():
    configurator = configuratorFactory()
    configurator.updateConfig()
