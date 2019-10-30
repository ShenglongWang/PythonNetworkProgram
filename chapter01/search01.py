"""
@version:01.00.00
@Author:Shenglong
"""
from pygeocoder import Geocoder

def main():
    address = '207 N. Defiance St, Archbold, OH'
    print(Geocoder.geocode(address)[0].coordinates)
if __name__ == '__main__':
    main()