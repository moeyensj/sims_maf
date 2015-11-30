from lsst.sims.maf.maps import BaseMap
import numpy as np
from lsst.utils import getPackageDir
import os
import healpy as hp
from lsst.sims.maf.utils import radec2pix

__all__ = ['StellarDensityMap']

class StellarDensityMap(BaseMap):
    """
    Return the cumulative stellar luminosity function for each slicepoint. Units of stars per sq degree.
    Uses a healpix map of nside=64. Uses the nearest healpix point for other ra,dec values.
    """
    def __init__(self, keyname='starLumFunc'):
        """

        """
        self.keyNames = [keyname, 'starMapBins']
        self.mapDir = os.path.join(getPackageDir('sims_dustmaps'),'StarMaps')


    def _readMap(self):
        filename = 'starDensity_nside_64.npz'
        starMap = np.load(os.path.join(self.mapDir,filename))
        self.starMap = starMap['starDensity'].copy()
        self.starMapBins = starMap['bins'].copy()
        self.starmapNside = hp.npix2nside(np.size(self.starMap[:,0]))

    def run(self, slicePoints):
        self._readMap()

        if 'nside' in slicePoints.keys():
            if slicePoints['nside'] == self.starmapNside:
                slicePoints['starLumFunc'] = self.starMap
        else:
            # Compute the healpix for each slicepoint on the nside=64 grid
            indx = radec2pix(self.starmapNside, slicePoints['ra'], slicePoints['dec'])
            slicePoints['starLumFunc'] = self.starMap[indx,:]

        slicePoints['starMapBins'] = self.starMapBins
        return slicePoints
