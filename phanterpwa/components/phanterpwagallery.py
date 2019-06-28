# -*- coding: utf-8 -*-
# author: PhanterJR<junior.conex@gmail.com>
# license: MIT

__author__ = "PhanterJR<junior.conex@gmail.com>"
__version__ = "1.0.0"

from ..helpers import DIV, I, INPUT, CANVAS, CONCATENATE
from ..xmlconstructor import XmlConstructor
import io
import os
from PIL import Image as PILImage


class PhanterpwaGalleryInput(XmlConstructor):

    def __init__(self, src_img="", cut_size=(300, 300), global_id=None, zindex=None, **attributes):
        """
        @src_img: source_img

        @cut_size: Cut image size

        @global_id: Adds in all ids of the elements this id, in this way it is
            possible to add 2 distinct inputs without conflicts
        """
        if "_class" in attributes:
            new_class = " ".join([attributes['_class'].strip(), "phanterpwa-gallery-inert-container"])
            attributes['_class'] = new_class
        else:
            attributes['_class'] = "phanterpwa-gallery-inert-container"
        self.cut_size = cut_size
        self.title_button = "Upload Image"
        self._image_button = I(_class="phanterwebsvg upload-cloud")
        self.global_id = global_id
        self._src_img = src_img
        self.zindex = zindex
        XmlConstructor.__init__(self, 'div', False, **attributes)

    @property
    def just_cutter_panel(self):
        self.xml()
        return self._just_cutter_panel

    @property
    def just_buttom(self):
        self.xml()
        return self._just_buttom

    @property
    def zindex(self):
        return self._zindex

    @zindex.setter
    def zindex(self, value):
        if isinstance(value, (int, type(None))):
            self._zindex = value
        else:
            raise TypeError("The zindex value must be integer")

    @property
    def global_id(self):
        return self._global_id

    @global_id.setter
    def global_id(self, _id):
        if isinstance(_id, (str, int, type(None))):
            if isinstance(_id, str):
                _id = _id.strip()
                if " " in _id:
                    raise ValueError("The id can't have empty space")
                else:
                    self._global_id = _id
            elif _id is None:
                self._global_id = ""
            else:
                self._global_id = _id
        else:
            raise TypeError("The global_id must be string or integer or None")

    @property
    def title_button(self):
        """
        Get or Set title button
        """
        return self._title_button

    @title_button.setter
    def title_button(self, title):
        if isinstance(title, (str, XmlConstructor)):
            if isinstance(title, XmlConstructor):
                title = title.xml()
            self._title_button = title
        else:
            raise TypeError("The title must be string")

    @property
    def image_button(self):
        """
        Get or Set title button
        """
        return self._image_button

    @image_button.setter
    def image_button(self, img_button):
        if isinstance(img_button, (str, XmlConstructor)):
            if isinstance(img_button, XmlConstructor):
                img_button = img_button.xml()
            self._image_button = img_button
        else:
            raise TypeError("The image_button must be " +
                            "string or XmlConstructor instance")

    def xml(self):
        global_id = self._global_id
        self._html_input(global_id)
        xml = ""
        if self.content and not self.singleton:
            xml = "".join([self.tag_begin, self.xml_content, self.tag_end])
        elif self.singleton:
            xml = self.tag_begin
        else:
            xml = "".join([self.tag_begin, self.tag_end])
        return xml

    def _html_input(self, _id=""):
        zindex = self._zindex
        style_zindex = None
        if zindex:
            style_zindex = "z-index:%s;" % zindex
        title_button = self._title_button
        image_button = self._image_button
        cut_size = self.cut_size
        ids_elements = {
            '_data-object': 'phanterpwa-gallery_object',
            '_data-upload-form-container':
                'phanterpwa-gallery_upload-form-container',
            '_data-upload-input': 'phanterpwa-gallery_upload-input-file',
            '_data-cutter-pad':
                'phanterpwa-gallery_cutter-pad',
            '_data-cutter-background':
                'phanterpwa-gallery_cutter-background',
            '_data-panel-cutter-container':
                'phanterpwa-gallery_panel-cutter-container',
            '_data-cutter-shadow':
                'phanterpwa-gallery_cutter-shadow',
            '_data-cutter-control-close':
                'phanterpwa-gallery_cutter-control-close',
            '_data-cutter-control-view':
                'phanterpwa-gallery_cutter-control-view',
            '_data-cutter-control-cut':
                'phanterpwa-gallery_cutter-control-cut',
            '_data-panel-cutter-size-container':
                'phanterpwa-gallery_panel-cutter-size-container',
            '_data-panel-cutter-image':
                'phanterpwa-gallery_panel-cutter-image',
            '_data-cutter-zoom-control':
                'phanterpwa-gallery_cutter-zoom-control',
            '_data-target-view':
                'phanterpwa-gallery_target-view',
            '_data-target-view-container':
                'phanterpwa-gallery_target-view-container',
            '_data-upload-messages':
                'phanterpwa-gallery_upload-messages',
            '_data-upload-area-progress':
                'phanterpwa-gallery_upload-area-progress',
            '_data-upload-image-button':
                'phanterpwa-gallery_upload-image-button',
            '_data-upload-title-button':
                'phanterpwa-gallery_upload-title-button',
            '_data-imagecuted-control-erase':
                'phanterpwa-gallery-imagecuted-control-erase',
            '_data-imagecuted-control-change':
                'phanterpwa-gallery-imagecuted-control-change',
            '_data-input-name-cutterSizeX':
                'phanterpwa-gallery-input-name-cutterSizeX',
            '_data-input-name-cutterSizeY':
                'phanterpwa-gallery-input-name-cutterSizeY',
            '_data-input-name-positionX':
                'phanterpwa-gallery-input-name-positionX',
            '_data-input-name-positionY':
                'phanterpwa-gallery-input-name-positionY',
            '_data-input-name-newSizeX':
                'phanterpwa-gallery-input-name-newSizeX',
            '_data-input-name-newSizeY':
                'phanterpwa-gallery-input-name-newSizeY',
        }
        if _id:
            for x in ids_elements:
                ids_elements[x] = "-".join([ids_elements[x], _id])
        ids_elements['_data-cutter-size-x'] = str(cut_size[0])
        ids_elements['_data-cutter-size-y'] = str(cut_size[1])
        ids_elements['_data-upload-src-img'] = self._src_img
        self._just_cutter_panel = DIV(
            DIV(
                _id=ids_elements["_data-cutter-background"],
                _class="phanterpwa-gallery-cutter-background"),
            DIV(
                _id=ids_elements["_data-cutter-shadow"],
                _class="phanterpwa-gallery-cutter-shadow"),
            DIV(
                DIV(
                    DIV(
                        _class="phanterpwa-gallery-panel-cutter-image",
                        _id=ids_elements['_data-panel-cutter-image']),

                    _style="overflow: hidden; width: %spx; height: %spx;" %
                           (cut_size[0], cut_size[1]),
                    _id=ids_elements['_data-panel-cutter-size-container'],
                    _class="phanterpwa-gallery-panel-cutter-size-container"
                ),
                _class="phanterpwa-gallery-panel-cutter"
            ),
            DIV(
                _id=ids_elements['_data-cutter-pad'],
                _class="phanterpwa-gallery-cutter-pad"),
            DIV(
                DIV(
                    I(_class="phanterwebsvg close-circle"),
                    _id=ids_elements['_data-cutter-control-close'],
                    _class="phanterpwa-gallery-cutter-control"),
                DIV(
                    I(_class="phanterwebsvg image-view"),
                    _id=ids_elements['_data-cutter-control-view'],
                    _class="phanterpwa-gallery-cutter-control"),
                DIV(
                    I(_class="phanterwebsvg image-cut"),
                    _id=ids_elements['_data-cutter-control-cut'],
                    _class="phanterpwa-gallery-cutter-control"),
                _class='phanterpwa-gallery_cutter-controls-container'),
            DIV(
                DIV(
                    I(_class="phanterwebsvg image-decrease"),
                    DIV(
                        DIV(_id=ids_elements['_data-cutter-zoom-control'],
                            _class="phanterpwa-gallery-cutter-zoom-control"),
                        _class="phanterpwa-gallery-cutter-zoom-control" +
                               "-container"
                    ),
                    I(_class="phanterwebsvg image-increase"),
                    _class='phanterpwa-gallery_cutter-zoom-controls'),
                _class='phanterpwa-gallery_cutter-zoom-container'),
            _id=ids_elements['_data-panel-cutter-container'],
            _class="phanterpwa-gallery-panel-cutter-container",
            _style=style_zindex
        )
        self._just_buttom = CONCATENATE(
            DIV(
                DIV(
                    DIV(
                        DIV(
                            I(_class="phanterwebsvg recycle"),
                            _id=ids_elements["_data-imagecuted-control-erase"],
                            _class="phanterpwa-gallery" +
                                   "_imagecuted-control"
                        ),
                        DIV(
                            I(_class="phanterwebsvg image-reload"),
                            _id=ids_elements["_data-imagecuted" +
                                             "-control-change"],
                            _class="phanterpwa-gallery" +
                                   "_imagecuted-control"
                        ),
                        _class="phanterpwa-gallery" +
                               "_imagecuted-controls"),
                    CANVAS(_id=ids_elements['_data-target-view']),
                    _class='phanterpwa-gallery-center-content',
                ),
                _id=ids_elements['_data-target-view-container'],
                _style="overflow: hidden; width: %spx; height: %spx;" %
                       (cut_size[0], cut_size[1]),
                _class="phanterpwa-gallery-target-view-container%s" %
                       (" actived" if self._src_img else ""),
            ),
            DIV(
                DIV(
                    DIV(
                        DIV(image_button,
                            _id=ids_elements["_data-upload-image-button"],
                            _class="phanterpwa-gallery-upload-image-button"),
                        DIV(title_button,
                            _id=ids_elements["_data-upload-title-button"],
                            _class="phanterpwa-gallery-upload-title-button"),
                        _class="phanterpwa-gallery-upload-button"
                    ),
                    _class="phanterpwa-gallery-container-upload-button"
                ),
                _id=ids_elements['_data-object'],
                _class="phanterpwa-gallery-object%s" %
                       (" actived" if not self._src_img else ""),
                **ids_elements
            ),
            DIV(
                DIV(
                    INPUT(
                        _accept="image/png, image/jpeg, image/gif, image/bmp",
                        _id=ids_elements["_data-upload-input"],
                        _class="phanterpwa-gallery-upload-input-file",
                        _type="file",
                        _name=ids_elements["_data-upload-input"]
                    ),
                    _class="input-field"),
                INPUT(_id=ids_elements['_data-input-name-cutterSizeX'],
                    _name=ids_elements['_data-input-name-cutterSizeX'],
                    _value="",
                    _type="text"),
                INPUT(_id=ids_elements['_data-input-name-cutterSizeY'],
                    _name=ids_elements['_data-input-name-cutterSizeY'],
                    _value="",
                    _type="text"),
                INPUT(_id=ids_elements['_data-input-name-positionX'],
                    _name=ids_elements['_data-input-name-positionX'],
                    _value="",
                    _type="text"),
                INPUT(_id=ids_elements['_data-input-name-positionY'],
                    _name=ids_elements['_data-input-name-positionY'],
                    _value="",
                    _type="text"),
                INPUT(_id=ids_elements['_data-input-name-newSizeX'],
                    _name=ids_elements['_data-input-name-newSizeX'],
                    _value="",
                    _type="text"),
                INPUT(_id=ids_elements['_data-input-name-newSizeY'],
                    _name=ids_elements['_data-input-name-newSizeY'],
                    _value="",
                    _type="text"),
                _id=ids_elements["_data-upload-form-container"],
                _class="phanterpwa-gallery-upload-form-container",
                _style="display: none;"
            ),

            DIV(_id=ids_elements['_data-upload-messages'],
                _class="phanterpwa-gallery-upload-messages"),
            DIV(
                DIV(
                    DIV(
                        DIV(_class="phanterpwa-gallery-progressbar-movement"),
                        _class="phanterpwa-gallery-progressbar"),
                    _id=ids_elements['_data-upload-area-progress'],
                    _class="phanterpwa-gallery-upload-area-progress"
                ),
                _class="phanterpwa-gallery-progressbar-container")
        )
        html = CONCATENATE(self._just_buttom, self._just_cutter_panel)
        self.content = [html]

    @property
    def cut_size(self):
        return self._cut_size

    @cut_size.setter
    def cut_size(self, cut_size):
        if isinstance(cut_size, (tuple, list)):
            if len(cut_size) == 2:
                if isinstance(cut_size[0], (int, float)) and \
                        isinstance(cut_size[1], (int, float)):
                    self._cut_size = (cut_size[0], cut_size[1])
                else:
                    raise TypeError("Values of list or tuple must be " +
                                    "integers or float")
            else:
                raise SyntaxError("There must be at least 2 values")
        else:
            raise TypeError("The value has to be a tuple or a list")


class PhanterpwaGalleryCutter(object):

    def __init__(self,
                 imageName,
                 imageBytes,
                 cutterSizeX, cutterSizeY,
                 positionX, positionY,
                 newSizeX, newSizeY, force_png=False):
        self.imageBytes = imageBytes
        self.cutterSizeX = cutterSizeX
        self.cutterSizeY = cutterSizeY
        self.positionX = positionX
        self.positionY = positionY
        self.newSizeX = newSizeX
        self.newSizeY = newSizeY
        self.force_png = force_png
        if force_png:
            self.extensao = 'png'
        else:
            self.extensao = 'jpg'
        self.nome_da_imagem = imageName

    def getImage(self):
        imageBytes = self.imageBytes
        nome_da_imagem = self.nome_da_imagem
        im = PILImage.open(imageBytes)
        newSizeX = int(float(self.newSizeX))
        newSizeY = int(float(self.newSizeY))
        cutterSizeX = int(float(self.cutterSizeX))
        cutterSizeY = int(float(self.cutterSizeY))
        positionX = float(self.positionX)
        positionY = float(self.positionY)
        nome_do_arquivo, extensao = os.path.splitext(nome_da_imagem)
        im = im.crop((positionX, positionY,
                      positionX + newSizeX,
                      positionY + newSizeY))
        im = im.resize((cutterSizeX, cutterSizeY),
                       PILImage.ANTIALIAS)
        jpeg_image_buffer = io.BytesIO()
        if extensao.lower() == '.png' or self.force_png:
            self.extensao = 'png'
            self.nome_da_imagem = "%s.%s" % (nome_do_arquivo, "png")
            im.save(jpeg_image_buffer, 'png')
        else:
            self.extensao = 'jpg'
            self.nome_da_imagem = "%s.%s" % (nome_do_arquivo, "jpg")
            im.save(jpeg_image_buffer, format='JPEG', quality=100)
        jpeg_image_buffer.seek(0)
        data = jpeg_image_buffer.read()
        return data


class PhanterpwaGalleryImageBytes(object):

    def __init__(self, imageName, imageBytes, force_png=False):
        self.nome_da_imagem = imageName
        self.imageBytes = imageBytes
        if force_png:
            self.extensao = 'png'
        else:
            self.extensao = 'jpg'

    def getImage(self, formatOut='png'):
        nome_da_imagem = self.nome_da_imagem
        nome_do_arquivo, extensao = os.path.splitext(nome_da_imagem)
        im = PILImage.open(self.imageBytes)
        jpeg_image_buffer = io.BytesIO()
        if extensao.lower() == '.png' or self.force_png:
            self.extensao = 'png'
            self.nome_da_imagem = "%s.%s" % (nome_do_arquivo, "png")
            im.save(jpeg_image_buffer, 'png')
        else:
            self.extensao = 'jpg'
            self.nome_da_imagem = "%s.%s" % (nome_do_arquivo, "jpg")
            im.save(jpeg_image_buffer, format='JPEG', quality=100)
        jpeg_image_buffer.seek(0)
        data = jpeg_image_buffer.read()
        return data
