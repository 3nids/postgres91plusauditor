"""
Qaudit 91 plus
Denis Rouzaud
denis.rouzaud@gmail.com
April. 2013


﻿ QgsDataSourceURI(   layer.dataProvider().dataSourceUri()    ).geometryColumn()


"""

def classFactory(iface):
    from qaudit91plus import Qaudit91plus
    return Qaudit91plus(iface)
    




