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

        self.addSetting("displayColumnDate", "bool", "global", True)
        self.addSetting("displayColumnUser", "bool", "global", True)
        self.addSetting("displayColumnAction", "bool", "global", True)
        self.addSetting("displayColumnChangedFields", "bool", "global", True)
        self.addSetting("displayColumnChangedGeometry", "bool", "global", True)
        self.addSetting("displayColumnApplication", "bool", "global", False)
        self.addSetting("displayColumnClientIP", "bool", "global", False)
        self.addSetting("displayColumnClientPort", "bool", "global", False)

        self.addSetting("searchOnlyGeometry", "bool", "global", False)
        self.addSetting("panShowGeometry", "bool", "global", True)

        # project
        self.addSetting("redefineSubset", "bool", "project", False)
        self.addSetting("logLayer", "string", "project", "")
