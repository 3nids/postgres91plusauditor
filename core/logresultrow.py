
from PyQt4.QtCore import QString, QVariant
from qgis.core import QgsFeature, QgsGeometry, QgsFeatureRequest

import re

from geometrytools import GeometryTools

# regexp to parse data from hstore
fieldRe = lambda(fieldName): re.compile('("%s"|%s)\s*=\>\s*' % (fieldName, fieldName))
dataReWithQuote = re.compile('\s*".*?[^\\\\]*?"')
dataReWithoutQuote = re.compile('.*?,')

geometryTools = GeometryTools()


class LogResultRow():
    def __init__(self, logFeature, featureLayer, pkeyName, geomColumn):
        self.featureLayer = featureLayer
        self.fields = featureLayer.dataProvider().fields()
        self.logFeature = QgsFeature(logFeature)
        self.geomColumn = geomColumn
        self.date = logFeature.attribute("action_tstamp_clk").toDateTime()
        self.dateMs = self.date.toMSecsSinceEpoch()
        self.logData = self.logFeature.attribute("row_data").toString()
        self.layerFeatureId = self.getFieldValue(self.logData, pkeyName).toInt()[0]

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
        return geometryTools.ewkb2gqgis(ewkb)

    def data(self):
        out = dict()
        for field in self.fields:
            out[field.name()] = self.getFieldValue(self.logData, field.name())
        return out

    def getLayerFeature(self):
        layerFeature = QgsFeature()
        featReq = QgsFeatureRequest().setFilterFid(self.layerFeatureId)
        if not self.featureLayer.hasGeometryType():
            featReq.setFlags(QgsFeatureRequest.NoGeometry)
        if self.featureLayer.getFeatures(featReq).nextFeature(layerFeature):
            return layerFeature
        else:
            return None

    def restoreFeature(self):
        if not self.featureLayer.isEditable():
            return False

        currentFeature = self.getLayerFeature()
        editBuffer = self.featureLayer.editBuffer()
        if currentFeature is not None:
            fid = currentFeature.id()
            for idx, field in enumerate(self.fields):
                value = self.getFieldValue(self.logData, field.name())
                if value == "":
                    value = None
                editBuffer.changeAttributeValue(fid, idx, value)
            if self.featureLayer.hasGeometryType():
                editBuffer.changeGeometry(fid, self.geometry())
        else:
            newFeature = QgsFeature()
            newFeature.setFields(self.fields)
            newFeature.initAttributes(self.fields.size())
            for field in self.fields:
                value = self.getFieldValue(self.logData, field.name())
                newFeature[field.name()] = QVariant(value)
            if self.featureLayer.hasGeometryType():
                newFeature.setGeometry(self.geometry())
            editBuffer.addFeature(newFeature)

