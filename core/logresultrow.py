
from PyQt4.QtCore import QString
from qgis.core import QgsFeature, QgsGeometry

import re

from geometrytools import GeometryTools

# regexp to parse data from hstore
fieldRe = lambda(fieldName): re.compile('("%s"|%s)\s*=\>\s*' % (fieldName, fieldName))
dataReWithQuote = re.compile('\s*".*?[^\\\\]"')
dataReWithoutQuote = re.compile('.*?,')


class LogResultRow():
    def __init__(self, logFeature, layerFeature, pkeyName, geomColumn):
        self.fields = layerFeature.fields()
        self.logFeature = QgsFeature(logFeature)
        self.geomColumn = geomColumn
        self.date = logFeature.attribute("action_tstamp_tx").toDateTime()
        self.dateMs = self.date.toMSecsSinceEpoch()
        self.logData = self.logFeature.attribute("row_data").toString()
        self.logFeatureId = self.getFieldValue(self.logData, pkeyName).toInt()[0]

    def getFieldValue(self, data, fieldName):
        p = fieldRe(fieldName).search(data)
        if p:
            value = ""
            data = data[p.end():]
            p = dataReWithQuote.match(data)
            if p:
                value = data[p.start()+1:p.end()-1]
            else:
                p = dataReWithoutQuote.match(data)
                if p:
                    value = data[p.start():p.end()-1]
            if value == "NULL":
                value = ""
            return value
        return None

    def dateStr(self):
        return self.date.toString("ddd dd MMM yyyy hh:mm")

    def user(self):
        return self.logFeature.attribute("session_user_name").toString()

    def action(self):
        action = self.logFeature.attribute("action").toString()
        if action == "I":
            #return QString(u"\u002B") # plus sign
            return "insert"
        if action == "U":
            #return QString(u"\u2713") # check sign
            return "update"
        if action == "D":
            #return QString(u"\u2A2F") # cross sign
            return "delete"
        raise NameError("Invalid action %s" % action)

    def application(self):
        return self.logFeature.attribute("application_name").toString()

    def clientIP(self):
        return self.logFeature.attribute("client_addr").toString()

    def clientPort(self):
        return self.logFeature.attribute("client_port").toString()

    def changedFields(self):
        data = self.logFeature.attribute("changed_fields").toString()
        columns = ""
        for field in self.fields:
            if self.getFieldValue(data, field.name()) is not None:
                columns += field.name() + ", "
        return columns[:-2]

    def changedGeometry(self):
        data = self.logFeature.attribute("changed_fields").toString()
        geometry = self.getFieldValue(data, self.geomColumn)
        return geometry is not None

    def changedGeometryStr(self):
        if self.changedGeometry():
            return QString(u"\u2713")  # i.e. check sign
        else:
            return ""

    def geometry(self):
        if self.geomColumn is None:
            return QgsGeometry()
        ewkb = "%s" % self.getFieldValue(self.logData, self.geomColumn)
        return GeometryTools().ewkb2gqgis(ewkb)

    def data(self):
        out = dict()
        for field in self.fields:
            out[field.name()] = self.getFieldValue(self.logData, field.name())
        return out

    def restoreFeature(self):
        pass

