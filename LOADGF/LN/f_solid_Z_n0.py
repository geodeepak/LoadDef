# *********************************************************************
# FUNCTION TO PROPAGATE TRANSFORMED Y-SOLUTIONS THROUGH SOLID LAYER (n=0)
#
# Copyright (c) 2014-2019: HILARY R. MARTENS, LUIS RIVERA, MARK SIMONS         
#
# This file is part of LoadDef.
#
#    LoadDef is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    LoadDef is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with LoadDef.  If not, see <https://www.gnu.org/licenses/>.
#
# *********************************************************************

import numpy as np
from scipy import interpolate

def main(si,Z,tck_lnd,tck_mnd,tck_rnd,tck_gnd,wnd,ond,piG,alpha):

    # Interpolate Parameters at Current Radius
    lndi = interpolate.splev(si,tck_lnd,der=0)
    rndi = interpolate.splev(si,tck_rnd,der=0)
    mndi = interpolate.splev(si,tck_mnd,der=0)
    gndi = interpolate.splev(si,tck_gnd,der=0)

    # Compute Beta and Delta Parameters 
    bndi = 1./(lndi+2.*mndi)
    dndi = 2.*mndi*(3.*lndi + 2.*mndi)*bndi

    # Build A Matrix (where dY/dr = A Y)
    # See Smylie (2013)
    c11 = -2.*lndi*bndi/si
    c12 = bndi
    c15 = 0.
    c16 = 0.
    
    c21 = (-2.*rndi/si)*(2.*gndi+si*(ond**2))+ \
        (2.*dndi/(si**2)) - (rndi*(wnd**2))
    c22 = -4.*mndi*bndi/si
    c25 = 0.
    c26 = -rndi

    c51 = 4.*piG*rndi
    c52 = 0.
    c55 = 0.
    c56 = 1.

    c61 = 0.
    c62 = 0.
    c65 = 0.
    c66 = -2./si

    # Modify A Matrix Due to Variable Transformation
    c12 = c12/si
    c21 = c21*si
    c26 = c26*si
    c51 = c51/si
    c56 = c56/si
    c65 = c65*si

    # Z-Variable A Matrix (A';Smylie 2013)
    Aprime = np.array([[c11, c12, c15, c16], \
       	[c21, c22, c25, c26], \
	[c51, c52, c55, c56], \
	[c61, c62, c65, c66]])

    # Z-Variable "Correction" Array
    Zc1 = ((alpha+1.)/si)*Z[0]
    Zc2 = (alpha/si)*Z[1]
    Zc5 = ((alpha+2.)/si)*Z[2]
    Zc6 = ((alpha+1.)/si)*Z[3]
    Zc  = np.array([Zc1,Zc2,Zc5,Zc6])

    # USE PROPAGATOR MATRIX TECHNIQUE TO COMPUTE dY/dr
    ZP = np.dot(Aprime,Z) - Zc

    # RETURN UPDATED DERIVATIVES
    return ZP

