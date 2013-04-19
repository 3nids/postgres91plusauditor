
from PyQt4.QtCore import QString
from qgis.core import QgsFeature

import re

# regexp to parse data from hstore
fieldRe = lambda(fieldName): re.compile('("%s"|%s)\s*=\>\s*' % (fieldName, fieldName))
dataReWithQuote = re.compile('\s*".*?[^\\\\]"')
dataReWithoutQuote = re.compile('.*?, ')


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
            data = data[p.end():]
            p = dataReWithQuote.match(data)
            if p:
                return data[p.start()+1:p.end()-1]
            p = dataReWithoutQuote.match(data)
            if p:
                return data[p.start():p.end()-1]
        return None

    def dateStr(self):
        return self.date.toString("ddd dd MMM yyyy hh:mm")

    def user(self):
        return self.logFeature.attribute("session_user_name").toString()

    def action(self):
        action = self.logFeature.attribute("action").toString()
        if action == "I":
            return "insert"
        if action == "U":
            return "update"
        if action == "D":
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
        if geometry is None:
            return ""
        else:
            return QString(u"\u2713")  # check sign

    def data(self):
        out = dict()
        for field in self.fields:
            out[field.name()] = self.getFieldValue(self.logData, field.name())
        return out

