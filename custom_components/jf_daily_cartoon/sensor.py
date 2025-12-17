
import logging
import requests
import time
import random
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15) # Less frequent auto-scan, rely on manual or camera update
API_BASE = "https://jahoo.gr/jf/api.php"
VIEWER_BASE_URL = "https://jahoo.gr/jf/?mode=viewer"

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([JFCartoonSensor()], True)

class JFCartoonSensor(SensorEntity):
    def __init__(self):
        self._attr_name = "JF Daily Cartoon"
        self._attr_unique_id = "jf_daily_cartoon_sensor"
        self._attr_native_value = "Ready"
        self._attr_extra_state_attributes = {}

    @property
    def icon(self):
        return "mdi:emoticon-happy-outline"

    def update(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            ts = int(time.time())
            
            # Simple metadata fetch
            url = f"{API_BASE}?date={today}&ts={ts}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'title' in data:
                    self._attr_native_value = data['title']
                    self._attr_extra_state_attributes = {
                        "description": data.get('description', ''),
                        "viewer_url": f"{VIEWER_BASE_URL}&date={data.get('date', '')}",
                        "last_updated": ts
                    }
        except Exception as e:
            _LOGGER.error(f"Sensor update failed: {e}")
