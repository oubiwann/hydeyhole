from twisted.application.service import ServiceMaker


HydeyHoleSSHService = ServiceMaker(
    "HydeyHole SSH Server",
    "hydeyhole.app.service",
    ("A highly flexible pure-Python, Twisted-based SSH Server with a "
     "Hy (Python Lisp) shell."),
    "hydeyhole")
