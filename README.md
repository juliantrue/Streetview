# Streetview

This is a quick and dirty python module designed to make interacting with the Google Streetview API much easier.

# Usage
This module exposes two main methods:

    get_by_location(BASE_URL, API_KEY, location, save_to=None, size=(600,400), signature=None))

which returns the one image in each Cardinal direction for the given the (lon, lat) of the location in question and

    get_by_search(BASE_URL, API_KEY, search_string, save_to=None, size=(600,400), signature=None)

which also returns one image in each Cardinal direction given a search string matching what one would normally type into Google.

Both return a list of images or if the **save_to** parameter is specified, it will save to the specified file.

# Requirements
* requests==2.20.0
* opencv-python==3.4.2.17
