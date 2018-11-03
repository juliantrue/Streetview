import sys, time
from optparse import OptionParser
import cv2

sys.path.append('./src')
from streetview import Core

parser = OptionParser() # Set up cmd line arg parsing
parser.add_option("-p", "--path", dest="raw_data_path",
                  help="Path to directory in which to save collected data.")
parser.add_option("-k", "--key", dest="API_KEY",
                  help="API_KEY for making calls to the Google streetview API")
parser.add_option("-u", "--url", dest="base_url",
                  default="https://maps.googleapis.com/maps/api/streetview?",
                  help="Path to directory in which to save collected data.")
parser.add_option("--logging_dir", dest="logging_dir",
                  help="Directory to store logs from Google API calls")


# Unpack CMD line options
(options, args) = parser.parse_args()

if not options.logging_dir:
    C = Core()
else:
    logging_dir = options.logging_dir
    C = Core(logging_dir)

raw_data_path = options.raw_data_path
base_url = options.base_url
API_KEY = options.API_KEY

# __main__
location = (43.657841, -79.377675)
search_string = "245 Church St, Toronto, ON M5B 2K3"
imgs = C.get_by_search(base_url,API_KEY,search_string,save_to=raw_data_path)

imgs = C.get_by_locaton(base_url,API_KEY,location,save_to=raw_data_path)
