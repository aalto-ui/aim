from PIL import Image
from io import BytesIO
import base64
import cStringIO
from subprocess32 import call
from tornado.options import options


def generate_screenshot(url):
    call([options.chrome_path, "--headless", "--force-device-scale-factor", "--disable-gpu", "--screenshot=screenshots/" + options.name + ".png", "--window-size=1280,720", url])
    im = Image.open("screenshots/" + options.name + ".png")
    buffer = cStringIO.StringIO()
    im.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue())


def convert_png_to_jpg_b64(pngb64):
    im = Image.open(BytesIO(base64.b64decode(pngb64)))
    im = im.convert("RGB")
    buffer = cStringIO.StringIO()
    im.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue())
