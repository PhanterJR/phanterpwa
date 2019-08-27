import os
import io
from PIL import Image as PILImage


class PhanterpwaGalleryCutter(object):

    def __init__(self, imageName, imageBytes, cutterSizeX, cutterSizeY, force_png=False):
        self.imageBytes = imageBytes
        self.cutterSizeX = cutterSizeX
        self.cutterSizeY = cutterSizeY
        self.force_png = force_png
        if isinstance(imageBytes, bytes):
            self._img = PILImage.open(io.BytesIO(imageBytes))
        else:
            self._img = PILImage.open(imageBytes)
        if self._img.mode == "P":
            self._img = PILImage.open(imageBytes).convert("RGBA")
            self.content_type = "image/png"
            self._format = "PNG"
            self.extension = "png"
        elif self._img.mode == "RGBA" or force_png:
            self.content_type = "image/png"
            self._format = "PNG"
            self.extension = "png"
        else:
            self.content_type = "image/jpeg"
            self._format = "JPEG"
            self.extension = "jpg"
        self.image_name = imageName
        self.data = None

    @property
    def cutterSizeX(self):
        return self._cutterSizeX

    @cutterSizeX.setter
    def cutterSizeX(self, value):
        try:
            value = int(float(value))
        except Exception:
            raise ValueError("The cutterSizeX must be intenger. Given: {0}".format(type(value)))
        else:
            self._cutterSizeX = value

    @property
    def cutterSizeY(self):
        return self._cutterSizeY

    @cutterSizeY.setter
    def cutterSizeY(self, value):
        try:
            value = int(float(value))
        except Exception:
            raise ValueError("The cutterSizeY must be intenger. Given: {0}".format(type(value)))
        else:
            self._cutterSizeY = value

    @property
    def positionX(self):
        return self._positionX

    @positionX.setter
    def positionX(self, value):
        try:
            value = int(float(value))
        except Exception:
            raise ValueError("The positionX must be intenger. Given: {0}".format(type(value)))
        else:
            self._positionX = value

    @property
    def positionY(self):
        return self._positionY

    @positionY.setter
    def positionY(self, value):
        try:
            value = int(float(value))
        except Exception:
            raise ValueError("The positionY must be intenger. Given: {0}".format(type(value)))
        else:
            self._positionY = value

    @property
    def newSizeX(self):
        return self._newSizeX

    @newSizeX.setter
    def newSizeX(self, value):
        try:
            value = int(float(value))
        except Exception:
            raise ValueError("The newSizeX must be intenger. Given: {0}".format(type(value)))
        else:
            self._newSizeX = value

    @property
    def newSizeY(self):
        return self._newSizeY

    @newSizeY.setter
    def newSizeY(self, value):
        try:
            value = int(float(value))
        except Exception:
            raise ValueError("The newSizeY must be intenger. Given: {0}".format(type(value)))
        else:
            self._newSizeY = value

    @property
    def force_png(self):
        return self._force_png

    @force_png.setter
    def force_png(self, value):
        if isinstance(value, bool):
            self._force_png = value
        else:
            raise ValueError("The force_png must be boolean. Given: {0}".format(type(value)))

    @property
    def image_name(self):
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        if "." in os.path.basename(image_name):
            self._image_name = "{0}.{1}".format(
                "".join(os.path.basename(image_name).split(".")[:-1]),
                self.extension
            )

    def specific_cut(self, newSizeX, newSizeY, positionX, positionY):
        img = self._img
        cutterSizeX = self.cutterSizeX
        cutterSizeY = self.cutterSizeY
        self.newSizeX = newSizeX
        self.newSizeY = newSizeY
        self.positionX = positionX
        self.positionY = positionY
        img = img.crop((self.positionX, self.positionY,
                      self.positionX + self.newSizeX,
                      self.positionY + self.newSizeY))
        img = img.resize((cutterSizeX, cutterSizeY),
                       PILImage.ANTIALIAS)
        img_buffer = io.BytesIO()
        if self._format == "PNG":
            img.save(img_buffer, format=self._format)
        else:
            img.save(img_buffer, format=self._format, quality=100)
        img_buffer.seek(0)
        data = img_buffer.read()
        self.data = data
        return [self.image_name, data, self.content_type]

    def auto_cut(self, crop_type='middle'):
        crop_t = ["top", "middle", "bottom"]
        if crop_type not in crop_t:
            raise ValueError("".join(["The crop_type must be top, middle or bottom",
                " (default: middle). Given: ", str(crop_type)]))
        img = self._img
        img_ratio = img.size[0] / float(img.size[1])
        ratio = self.cutterSizeX / float(self.cutterSizeY)
        newSizeX = self.cutterSizeX * (img.size[1] / self.cutterSizeY)
        newSizeY = self.cutterSizeY * (img.size[0] / self.cutterSizeX)
        if ratio > img_ratio:
            if crop_type == 'top':
                box = (0, 0, img.size[0], newSizeY)
            elif crop_type == 'middle':
                box = (0, (img.size[1] - newSizeY) / 2, img.size[0], (img.size[1] + newSizeY) / 2)
            elif crop_type == 'bottom':
                box = (0, img.size[1] - newSizeY, img.size[0], img.size[1])
            img = img.crop(box)

        elif ratio < img_ratio:
            if crop_type == 'top':
                box = (0, 0, newSizeX, img.size[1])
            elif crop_type == 'middle':
                box = ((img.size[0] - newSizeX) / 2, 0, (img.size[0] + newSizeX) / 2, img.size[1])
            elif crop_type == 'bottom':
                box = (img.size[0] - newSizeX, 0, img.size[0], img.size[1])
            img = img.crop(box)
        img = img.resize((self.cutterSizeX, self.cutterSizeY),
                PILImage.ANTIALIAS)

        img_buffer = io.BytesIO()
        if self._format == "PNG":
            img.save(img_buffer, format=self._format)
        else:
            img.save(img_buffer, format=self._format, quality=100)

        img_buffer.seek(0)
        data = img_buffer.read()
        self.data = data
        return [self.image_name, data, self.content_type]

    def save(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            if not self.data:
                self.auto_cut()
            with open(os.path.join(path, self.image_name), "wb") as g:
                g.write(self.data)
        else:
            raise ValueError("The path not exists or is not a dir")
