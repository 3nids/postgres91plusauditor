
from PyQt4.QtCore import QString
from qgis.core import QgsFeature, QgsGeometry

import re
import binascii

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
        SRID_FLAG = 0x20000000

        geom = QgsGeometry()
        if self.geomColumn is None:
            return geom
        wkb = "%s" % self.getFieldValue(self.logData, self.geomColumn)
        geomType = int("0x" + self.decodeBinary(wkb[2:10]), 0)
        if geomType & SRID_FLAG:
            wkb = wkb[:2] + self.encodeBinary(geomType ^ SRID_FLAG) + wkb[18:]
        geom.fromWkb(binascii.a2b_hex(wkb))
        return geom

    def data(self):
        out = dict()
        for field in self.fields:
            out[field.name()] = self.getFieldValue(self.logData, field.name())
        return out

    def encodeBinary(self, value):
        # https://github.com/elpaso/quickwkt/blob/master/QuickWKT.py#L132
        wkb = binascii.a2b_hex("%08x" % value)
        wkb = wkb[::-1]
        wkb = binascii.b2a_hex(wkb)
        return wkb

    def decodeBinary(self, wkb):
        """Decode the binary wkb and return as a hex string"""
        print wkb
        value = binascii.a2b_hex(wkb)
        value = value[::-1]
        value = binascii.b2a_hex(value)
        return value