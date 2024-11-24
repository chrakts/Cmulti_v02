from PIL import Image
import piexif
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

#codec = 'ISO-8859-1'


def check_gps_info(image_path):
    try:
        # Open image and extract EXIF data
        image = Image.open(image_path)
        exif_data = piexif.load(image.info['exif'])

        # Check if GPSInfo tag exists in EXIF data
        if 'GPS' in exif_data and exif_data['GPS']:
            print("GPS information found in the image.")
            return False
        else:
            print("No GPS information found in the image.")
            return True

    except KeyError:
        print("No EXIF data found in the image.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def get_datetime_original(image_path):
    try:
        # Open the image and load EXIF data
        image = Image.open(image_path)
        exif_data = piexif.load(image.info['exif'])

        # Get the DateTimeOriginal tag (0x9003 in EXIF)
        datetime_original = exif_data["Exif"].get(piexif.ExifIFD.DateTimeOriginal)

        if datetime_original:
            # Decode bytes to string (if necessary)
            datetime_original = datetime_original.decode("utf-8")
            print("DateTimeOriginal:", datetime_original)
            return datetime_original
        else:
            print("No DateTimeOriginal found in EXIF data.")
            return None

    except KeyError:
        print("No EXIF data found in the image.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


"""def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    #thumbnail = exif_dict.pop('thumbnail')
    #exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict"""


#def decdeg2dms(dd):
#    mult = -1 if dd < 0 else 1
#    mnt, sec = divmod(abs(dd)*3600, 60)
#    deg, mnt = divmod(mnt, 60)
#    return mult*deg, mult*mnt, mult*sec


#def to_deg(value, loc):
#    """Convert decimal coordinates into degrees, minutes, and seconds with direction."""
#    if value < 0:
#        loc_value = loc[0]
#    else:
#        loc_value = loc[1]
#    abs_value = abs(value)
#    degrees = int(abs_value)
#    minutes = int((abs_value - degrees) * 60)
#    seconds = round((abs_value - degrees - minutes / 60) * 3600, 5)
#    return degrees, minutes, seconds, loc_value


def convert_to_dms(value):
    """Helper function to convert a latitude/longitude to degrees, minutes, seconds format."""
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes / 60) * 3600
    return [(degrees, 1), (minutes, 1), (int(seconds * 100), 100)]  # Represent seconds as fraction


def add_gps_and_comment(image_path, output_path, latitude, longitude, comment):
    try:
        # Open the image and load existing EXIF data
        image = Image.open(image_path)
        exif_data = piexif.load(image.info['exif']) if 'exif' in image.info else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        # Add or update the UserComment tag
        exif_data["Exif"][piexif.ExifIFD.UserComment] = comment.encode('utf-8')

        # Set GPS data
        # GPSLatitudeRef and GPSLongitudeRef define the N/S and E/W hemisphere respectively
        exif_data["GPS"][piexif.GPSIFD.GPSLatitudeRef] = 'N' if latitude >= 0 else 'S'
        exif_data["GPS"][piexif.GPSIFD.GPSLongitudeRef] = 'E' if longitude >= 0 else 'W'

        # Convert latitude and longitude to DMS format
        exif_data["GPS"][piexif.GPSIFD.GPSLatitude] = convert_to_dms(abs(latitude))
        exif_data["GPS"][piexif.GPSIFD.GPSLongitude] = convert_to_dms(abs(longitude))

        # Insert updated EXIF data back into the image and save
        exif_bytes = piexif.dump(exif_data)
        image.save(output_path, "jpeg", exif=exif_bytes)
        print("GPS data and comment added to EXIF successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


mypath = "/home/christof/Daten/Bilder/_Fotos_2024/2024-10 Japan/Zusammen"

df = pd.read_csv(mypath+"/gpstrack.csv", sep=';', decimal=',')
df['timestamp'] = pd.to_datetime(df['imageTakenTime'], format="%Y:%m:%d %H:%M:%S").astype(int) // 10**9

mypath = "/home/christof/Daten/Bilder/_Fotos_2024/2024-10 Japan/Zusammen"
outputpath = "/home/christof/Daten/Bilder/_Fotos_2024/2024-10 Japan/TestMitGPS"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

rows_list = []
for files in onlyfiles:
    if check_gps_info(mypath+"/"+files):
        xtime = get_datetime_original(mypath+"/"+files)
        print(xtime)
        xtime = pd.to_datetime(xtime, format="%Y:%m:%d %H:%M:%S").timestamp()
        latnew = np.interp(xtime, df["timestamp"], df["geolocation_lat"])
        lngnew = np.interp(xtime, df["timestamp"], df["geolocation_lng"])
        print(files, xtime, latnew, lngnew)
        add_gps_and_comment(mypath+"/"+files, outputpath+"/"+files, latnew, lngnew, "gps modified")
        #35°50'59.4"N 139°08'33.3"E
