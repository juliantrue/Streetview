.PHONY: all clean

# API Parameters
API_KEY = "" # Your Google API Key
BASE_URL = "https://maps.googleapis.com/maps/api/streetview?"

# Directories
RAW_DATA = "./data/raw/"
INTRIM_DATA = "./data/interim/"
LOGS = "./logs/"

clean:
	rm -rf $(RAW_DATA)*
	rm -f $(INTRIM_DATA)*.png
	rm -f $(LOGS)*.log

All:
	python3 ./example.py --path $(RAW_DATA) --logging_dir $(LOGS) --key $(API_KEY) --url $(BASE_URL)
