from twisted.cred import portal
from twisted.conch import manhole_ssh

from carapace.app import cred
from carapace.util import ssh as util

from hydeyhole.app.shell import hyshell


def portalFactory(namespace):
    """
    """
    realm = hyshell.HyTerminalRealm(namespace)
    return portal.Portal(realm)


def getHyShellFactory(**namespace):
    """
    The "namespace" kwargs here contains the passed objects that will be
    accessible via the shell, namely:
     * "app"
     * "services"

    These two are passed in the call to hydeyhole.app.service.makeService.
    """
    sshRealm = hyshell.HyTerminalRealm(namespace)
    sshPortal = portal.Portal(sshRealm)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(cred.PublicKeyDatabase())
    return factory
