
import logging
import voluptuous as vol
from datetime import timedelta
import requests

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "JF Daily Cartoon"
SCAN_INTERVAL = timedelta(minutes=60)
# API Endpoint
API_URL = "https://jahoo.gr/jf/api.php?date=today"
# Viewer Endpoint
VIEWER_BASE_URL = "https://jahoo.gr/jf/?mode=viewer"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    name = config.get(CONF_NAME)
    add_entities([JFCartoonSensor(name)], True)

class JFCartoonSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
    
    @property
    def icon(self):
        """Icon to use in the frontend."""
        return "mdi:emoticon-happy-outline"

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(API_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'title' in data:
                    self._state = data['title']
                    
                    # Construct Viewer URL for tap_action
                    viewer_url = f"{VIEWER_BASE_URL}&date={data.get('date', '')}"
                    
                    # Get Images
                    images = data.get('images', [])
                    main_image = images[0] if images else None
                    
                    self._attributes = {
                        "description": data.get('description', ''),
                        "images": images,
                        "date": data.get('date', ''),
                        "image_url": main_image,
                        "viewer_url": viewer_url
                    }
                else:
                    self._state = "No Cartoon Today"
                    self._attributes = {
                        "image_url": None,
                        "viewer_url": VIEWER_BASE_URL
                    }
        except Exception as e:
            _LOGGER.error(f"Error updating JF Cartoon: {e}")
