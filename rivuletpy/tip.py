'''
This tip submodule is used for storing information of tips.
'''


class Tip(object):
    def __init__(self, tvalue=None, boundary=None, radius=None, xyz=None, pos=None):
        self._tvalue = tvalue
        self._xmin = 0
        self._xmax = 0
        self._ymin = 0
        self._ymax = 0

        if boundary is not None:
            self._xmin = boundary[0]
            self._xmax = boundary[1]
            self._ymin = boundary[2]
            self._ymax = boundary[3]
        self._radius = radius
        self._xyz = xyz
        self._pos = pos
        
    def xmin(self):
        return self._xmin
    def xmax(self):
        return self._xmax
    def ymin(self):
        return self._ymin
    def ymax(self):
        return self._ymax
    def radius(self):
        return self._radius
    def tvalue(self):
        return self._tvalue
    def xyz(self):
        return self._xyz
    def pos(self):
        return self._pos
