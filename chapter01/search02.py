"""
@version:01.00.00
@Author:Shenglong
"""
import requests

def geocode(address):
    parameters = {'address': address, 'sensor': 'false'}
    base = 'http://maps.googleapis.com/maps.api/geocode/json'
    response = requests.get(base,params = parameters)
    answer = response.json()
    print(answer['results'][0]['geometry']['location'])

def main():
    geocode('207 N. Defiance St, Archbold, OH')


if __name__ == '__main__':
    main()