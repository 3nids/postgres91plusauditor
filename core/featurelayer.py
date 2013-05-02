

def primaryKey(layer):
    """
    Returns the layer primary key
    :param layer: qgis vector layer
    :return:  return the field name of the primary key
    """
    if layer is None:
        return None
    pkeyIdx = layer.dataProvider().pkAttributeIndexes()
    if len(pkeyIdx) == 0:
        return None
    return layer.pendingFields()[pkeyIdx[0]].name()