import os, shutil, logging
import requests
import cv2
from .logging_facility import LoggingWrapper

class Core(object):

    def __init__(self,logs_folder=None):
        self.L = LoggingWrapper(log_folder_path=logs_folder)
        self.logger = logging.getLogger('Streetview_Module')
        self.logger.info("Streetview Module Initialized")

    """
    Usage:
    Pass in the base url on which to build the request on, followed by the API_KEY
    and the signature if needed. The request builder then takes as many kwargs as
    needed.
    Returns Request string
    """
    def request_builder(self, BASE_URL, API_KEY, kwargs, signature=None):
        request = BASE_URL
        for key in kwargs:
            request += "{}={}&".format(key,kwargs[key])

        request += "key={}".format(API_KEY)
        if(not(signature is None)):
            request += "&signature={}".format(signature)
        return request

    """
    Usage:
    See request builder. Builds request for metadata.
    Run this prior to sending image request to google servers. Confirms image
    availability as well as request validation.
    """
    def metadata_request_builder(self, BASE_URL, API_KEY, kwargs, signature=None):
        request = BASE_URL
        request = request[:-1] + "/" + "metadata?"
        for key in kwargs:
            request += "{}={}&".format(key,kwargs[key])

        request += "key={}".format(API_KEY)
        if(not(signature is None)):
            request += "&signature={}".format(signature)
        return request

    """
    Usage:
    Requires tuple of geographic coordinates in the format (lon,lat)
    Returns:
    List of images associated with that location unless save_to parameter is
    defined

    Example
    location = (43.656009, -79.380354)
    """
    def get_by_location(self, BASE_URL, API_KEY, location, save_to=None,
                        size=(600,400), signature=None):
        if(not(type(location) is tuple)):
            raise Exception("\'location\' must be of type tuple.")
        if(not(type(size) is tuple)):
            raise Exception("\'size\' must be of type tuple.")

        # Remove brackets from tuple input and convert to strings
        size_s = str(size[0])+"x"+str(size[1])
        loc_s = str(location)[1:][:-1]
        headings = [0, 90, 180, 270] # N E W S

        # Memory for images
        imgs = []

        user_repsonse = input("Are you sure you want to download {} images?(yes/no): ".format(len(headings)))
        if(not(user_repsonse == "yes")):
            raise Exception("User did not confirm image download.")
        # Build kwargs in order
        for heading in headings:
            head_s = str(heading)
            kwargs = {'size': size_s, 'location': loc_s, 'heading': head_s}

            # Request image metadata
            meta_req = self.metadata_request_builder(BASE_URL, API_KEY, kwargs)
            self.logger.info("Sending image metadata request: {}".format(meta_req))
            meta_r = requests.get(meta_req)
            response = meta_r.json()

            if self.L.debug_mode:
                self.logger.debug("Response: {}".format(meta_r.text))
            if(not(str(response['status']) == "OK")):
                raise Exception("Request status: {}".format(response['status']))

            # Request for each cardinal direction heading
            req = self.request_builder(BASE_URL, API_KEY, kwargs)
            to_file = req.split("&")[1]+ req.split("&")[2]

            self.logger.info("Sending image request: {}".format(req))
            r = requests.get(req, stream=True)

            # Save to file
            if not save_to == None:
                directory = os.path.join(save_to,req.split("&")[1])
                try:
                    os.mkdir(directory)
                except FileExistsError as e:
                    pass
                save_to_file = os.path.join(directory,to_file)
                self.logger.info("Saving to file: {}".format(save_to_file))
                with open('{}.png'.format(save_to_file), 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                del r
            # Save to temp file then to opencv img obj
            else:
                with open('./temp.png', 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                del r
                img = cv2.imread('./temp.png')
                imgs.append(img)
                os.remove('./temp.png')

        if save_to == None:
            return imgs

    """
    Usage:
    Requires address in string format. Address may resemble a google maps query
    or just the actual address.
    Returns:
    List of images associated with that address
    Optional: return only the first n images by specifying n.

    Example
    search_string = "245 Church St, Toronto, ON M5B 2K3"
    imgs = get_by_search(search_string, n=4)
    """
    def get_by_search(self, BASE_URL, API_KEY, search_string, save_to=None,
                      size=(600,400), signature=None):
        if(not(type(search_string) is type("string"))):
            raise Exception("\'location\' must be of type string.")
        if(not(type(size) is tuple)):
            raise Exception("\'size\' must be of type tuple.")

        # Convert to strings
        size_s = str(size[0])+"x"+str(size[1])
        loc_s = search_string.replace(" ", "%20")
        headings = [0, 90, 180, 270] # N E W S

        # Memory for images
        imgs = []

        user_repsonse = input("Are you sure you want to download {} images?(yes/no): ".format(len(headings)))
        if(not(user_repsonse == "yes")):
            raise Exception("User did not confirm image download.")
        # Build kwargs in order
        for heading in headings:
            head_s = str(heading)
            kwargs = {'size': size_s, 'location': loc_s, 'heading': head_s}

            # Request image metadata
            meta_req = self.metadata_request_builder(BASE_URL, API_KEY, kwargs)
            self.logger.info("Sending image metadata request: {}".format(meta_req))
            meta_r = requests.get(meta_req)
            response = meta_r.json()
            if self.L.debug_mode:
                self.logger.debug("Response: {}".format(meta_r.text))
            if(not(str(response['status']) == "OK")):
                raise Exception("Request status: {}".format(response['status']))

            # Request for each cardinal direction heading
            req = self.request_builder(BASE_URL, API_KEY, kwargs)
            to_file = req.split("&")[1]+ req.split("&")[2]

            self.logger.info("Sending image request: {}".format(req))
            r = requests.get(req, stream=True)

            # Save to file
            if not save_to == None:
                directory = os.path.join(save_to,req.split("&")[1])
                try:
                    os.mkdir(directory)
                except FileExistsError as e:
                    pass
                save_to_file = os.path.join(directory,to_file)
                self.logger.info("Saving to file: {}".format(save_to_file))
                with open('{}.png'.format(save_to_file), 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                del r
            # Save to temp file then to opencv img obj
            else:
                with open('./temp.png', 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                del r
                img = cv2.imread('./temp.png')
                imgs.append(img)
                os.remove('./temp.png')

        if save_to == None:
            return imgs
