from qgis.core import QgsGeometry

import binascii

SRID_FLAG = 0x20000000


class GeometryTools():
    def ewkb2gqgis(self, ewkb):
        geom = QgsGeometry()

        geomType = int("0x" + self.decodeBinary(ewkb[2:10]), 0)
        if geomType & SRID_FLAG:
            ewkb = ewkb[:2] + self.encodeBinary(geomType ^ SRID_FLAG) + ewkb[18:]
        geom.fromWkb(binascii.a2b_hex(wkb))
        return geom


    def encodeBinary(self, value):
        # https://github.com/elpaso/quickwkt/blob/master/QuickWKT.py#L132
        wkb = binascii.a2b_hex("%08x" % value)
        wkb = wkb[::-1]
        wkb = binascii.b2a_hex(wkb)
        return wkb

    def decodeBinary(self, wkb):
        """Decode the binary wkb and return as a hex string"""
        value = binascii.a2b_hex(wkb)
        value = value[::-1]
        value = binascii.b2a_hex(value)
        return value