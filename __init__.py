"""
Qaudit 91 plus
Denis Rouzaud
denis.rouzaud@gmail.com
April. 2013
"""


def classFactory(iface):
    from postgres91plusauditor import Postgres91plusAuditor
    return Postgres91plusAuditor(iface)
    




