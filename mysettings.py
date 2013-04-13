"""
Postgres Auditor 91 plus
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
"""

from qgistools.pluginsettings import *

pluginName = "postgres91plusauditor"


mySettings = [
    # global settings
    Bool(pluginName,"displayColumnDate"           , "global", True ),
    Bool(pluginName,"displayColumnUser"           , "global", True ),
    Bool(pluginName,"displayColumnAction"         , "global", True ),
    Bool(pluginName,"displayColumnChangedFields"  , "global", True ),
    Bool(pluginName,"displayColumnChangedGeometry", "global", True ),
    Bool(pluginName,"displayColumnApplication"    , "global", False ),
    Bool(pluginName,"displayColumnClientIP"       , "global", False ),
    Bool(pluginName,"displayColumnClientPort"     , "global", False ),
    Bool(pluginName,"searchOnlyGeometry"          , "global", False ),
    Integer(pluginName,"displayMode", "global", 1),

    # project
    String(pluginName, "logLayer", "project"," ")
]

class MySettings(PluginSettings):
    def __init__(self):
        PluginSettings.__init__(self, pluginName, mySettings)







