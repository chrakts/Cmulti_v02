from exif import Image
from os import listdir
from os.path import isfile, join
import pandas as pd

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        try:
            img = Image(src)
        except:
            #print('Datei nicht interpretierbar')
            return()
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                                     img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                                     img.gps_longitude_ref))
        except AttributeError:
            #print('No Coordinates')
            return()
        except:
            return()
            #print('anderer Fehler')
    else:
        #print('The Image has no EXIF information')
        return()
    return ({"imageTakenTime": img.datetime_original, "geolocation_lat": coords[0], "geolocation_lng": coords[1]})

mypath = "/home/christof/Daten/Bilder/_Fotos_2024/2024-10 Japan/Zusammen"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

rows_list = []
for files in onlyfiles:
    test = image_coordinates(mypath+"/"+files)
    if type(test)== dict:
        rows_list.append(test)
df = pd.DataFrame(rows_list)
df = df.sort_values(by='imageTakenTime')
print(df)
df.to_csv(mypath+"/gpstrack.csv",sep=';',decimal=',')
