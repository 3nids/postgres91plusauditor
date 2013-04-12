"""
Qaudit 91 plus
Denis Rouzaud
denis.rouzaud@gmail.com
April. 2013
"""

def classFactory(iface):
    from postgresauditor91plus import PostgresAuditor91plus
    return PostgresAuditor91plus(iface)
    




