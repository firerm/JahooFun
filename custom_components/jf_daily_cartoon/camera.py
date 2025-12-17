
import logging
import requests
import time
import random
from datetime import datetime, timedelta
from homeassistant.components.camera import Camera
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=10)
API_BASE = "https://jahoo.gr/jf/api.php"

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([JFCartoonCamera()], True)

class JFCartoonCamera(Camera):
    def __init__(self):
        super().__init__()
        self._attr_name = "JF Daily Cartoon"
        self._attr_unique_id = "jf_daily_cartoon_camera"
        self._image_bytes = None
        self._attr_is_streaming = False

    def camera_image(self, width=None, height=None):
        """Return the bytes of the image."""
        return self._image_bytes

    def update(self):
        """
        Fetch the image. This method is called by the 'homeassistant.update_entity' service.
        We do NOT check if it's the same image. We just download it.
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            ts = int(time.time())
            rand = random.randint(100000, 999999)

            # 1. Get Metadata
            meta_url = f"{API_BASE}?date={today}&meta_ts={ts}_{rand}"
            meta_resp = requests.get(meta_url, timeout=10)
            
            if meta_resp.status_code == 200:
                data = meta_resp.json()
                if data and 'images' in data and len(data['images']) > 0:
                    
                    # 2. Get Image Bytes (No Caching)
                    image_url = data['images'][0]
                    # Append garbage to URL to bypass proxies
                    sep = "&" if "?" in image_url else "?"
                    dl_url = f"{image_url}{sep}force_dl={ts}_{rand}"
                    
                    img_resp = requests.get(dl_url, timeout=20)
                    if img_resp.status_code == 200:
                        self._image_bytes = img_resp.content
                        
                        # 3. Force HA to see a state change
                        self._attr_extra_state_attributes = {
                            "last_fetch_ts": ts,
                            "force_refresh_id": rand,
                            "image_size": len(self._image_bytes)
                        }
                    else:
                        _LOGGER.warning("Could not download image bytes")
                else:
                    self._image_bytes = None
        except Exception as e:
            _LOGGER.error(f"Camera update error: {e}")
            # Don't clear old image on error, simpler UX
