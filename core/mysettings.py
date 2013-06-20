"""
Postgres Auditor 91 plus
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
"""

from ..qgissettingmanager import *

pluginName = "postgres91plusauditor"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)
        self.addSetting("panShowGeometry", "bool", "global", True)
        self.addSetting("columns", "stringlist", "global",
                        ("Date", "User", "Action", "Changed geometry", "Changed fields"))

        # project
        self.addSetting("redefineSubset", "bool", "project", True)
        self.addSetting("logLayer", "string", "project", "")
