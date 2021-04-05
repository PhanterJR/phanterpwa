from phanterpwa.frontend import helpers
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')

# it is ignored on transcrypt
window = jQuery = console = document = localStorage = Hammer =\
    sessionStorage = this = FileReader = JSON = js_undefined = navigator = __new__ = Date = 0

__pragma__('noskip')


INPUT = helpers.XmlConstructor.tagger("input", True)
I = helpers.XmlConstructor.tagger("i")
DIV = helpers.XmlConstructor.tagger("div")
FORM = helpers.XmlConstructor.tagger("form")
XML = helpers.XML

__pragma__('kwargs')


class GalleryInput():
    def __init__(self, el, **config):
        self.el = jQuery(el)
        self.config = config
        self.namespace = __new__(Date().getTime())
        self.conf_default = {
            "name": "phanterpwa-gallery-file-input",
            "button-upload": I(_class="fas fa-cloud-upload-alt").xml(),
            "width": 190,
            "height": 200,
            "view-width": None,
            "view-height": None,
            "cutter": False,
            "z-index": 1005,
            "current_image": None,
            "put_in_form": True,
            "img_name": "PhanterpwaGalleryFile",
            "hammerconf": {
                'inputClass': Hammer.PointerEventInput if Hammer.SUPPORT_POINTER_EVENTS else Hammer.TouchInput
            },
            "onError": None,
            "beforeCut": None,
            "afterCut": None,
            "data_view": False
        }
        if self.config is js_undefined:
            self.config = dict()
        for d in self.conf_default.keys():
            if d not in self.config:
                self.config[d] = self.conf_default[d]
        self.config["namespace"] = self.namespace
        self.config["element"] = el
        if self.config["view-width"] is None or self.config["view-width"] is js_undefined:
            self.config["view-width"] = self.config["width"]
        if self.config["view-height"] is None or self.config["view-height"] is js_undefined:
            self.config["view-height"] = self.config["height"]
        self._data_view = self.config.get("data_view", False)
        self.addInputPanel()

    def getNewImage(self):

        def inputChange(el):
            is_to_cut = self.config['cutter']
            blob = jQuery(el)[0].files
            fileslength = blob.length
            for i in range(fileslength):
                img_type = blob[i]['type']
                img_name = blob[i]['name']
                self.config["img_type"] = img_type
                self.config["img_name"] = img_name
                if img_type == "image/png" or\
                        img_type == "image/bmp" or\
                        img_type == "image/gif" or\
                        img_type == "image/jpeg":
                    def onloadend(reader, img_name, img_type):
                        base64data = reader.result
                        img1 = document.createElement("IMG")
                        img1.src = base64data
                        img1.alt = img_name + " (" + img_type + ")"
                        if is_to_cut:
                            def onImageLoad(img):
                                if window.PhanterPWA.DEBUG:
                                    console.info(img.width)
                                    console.info(img.height)
                            img1.onload = lambda: onImageLoad(this)

                            __new__(GalleryCutter(
                                base64data, self
                            ))
                        else:
                            self.simpleView(base64data)

                    reader = __new__(FileReader())
                    reader.readAsDataURL(blob[0])
                    reader.onloadend = lambda: onloadend(reader, img_name, img_type)
                else:
                    console.error("The file has invalid type. It must be png, bmp, gif, jpeg type.")
        el_input = jQuery("#phanterpwa-gallery-input-file-" + self.namespace)
        el_input.trigger(
            "click"
        ).off(
            "change.phanterpwa_gallery_input_" + self.namespace
        ).on(
            "change.phanterpwa_gallery_input_" + self.namespace,
            lambda: inputChange(this, self.config)
        )

    def _afterRead(self):
        if self.config['current_image'] is not None and self.config['current_image'] is not js_undefined:
            self.simpleView(self.config['current_image'])
        else:
            jQuery(
                "#phanterpwa-gallery-upload-image-button-" + self.namespace
            ).on(
                "click",
                lambda: self.getNewImage()
            )

    def addInputPanel(self):

        other_inputs = ""
        if self.config['cutter']:
            cutter_vars = [
                INPUT(
                    _id='phanterpwa-gallery-input-cutterSizeX' + self.namespace,
                    _name='phanterpwa-gallery-input-cutterSizeX',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-cutterSizeY' + self.namespace,
                    _name='phanterpwa-gallery-input-cutterSizeY',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-positionX' + self.namespace,
                    _name='phanterpwa-gallery-input-positionX',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-positionY' + self.namespace,
                    _name='phanterpwa-gallery-input-positionY',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-newSizeX' + self.namespace,
                    _name='phanterpwa-gallery-input-newSizeX',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-newSizeY' + self.namespace,
                    _name='phanterpwa-gallery-input-newSizeY',
                    _value="",
                    _type="text"
                ),
                INPUT(
                    _id='phanterpwa-gallery-input-rotation' + self.namespace,
                    _name='phanterpwa-gallery-input-rotation',
                    _value="",
                    _type="text"
                )
            ]
            other_inputs = DIV(
                *cutter_vars,
                _class="phanterpwa-gallery-inputs-container-" + self.namespace,
                _style="display: none"
            )
        input_gallery = DIV(
            DIV(
                DIV(
                    XML(self.config['button-upload']),
                    _id="phanterpwa-gallery-upload-image-button-" + self.namespace,
                    _class="phanterpwa-gallery-upload-image-button link",
                    _phanterpwa_input="phanterpwa-gallery-input-file-" + self.namespace
                ),
                _id="phanterpwa-gallery-upload-image-default-" + self.namespace,
                _class="phanterpwa-gallery-upload-image-default"
            ),
            INPUT(
                _accept="image/png, image/jpeg, image/gif, image/bmp",
                _class="phanterpwa-gallery-upload-input-file",
                _type="file",
                _id="phanterpwa-gallery-input-file-" + self.namespace,
                _name="phanterpwa-gallery-file-input"
            ),
            _id="phanterpwa-gallery-input-container-" + self.namespace,
            _class="phanterpwa-gallery-input-container"
        )
        wrapper_gallery = DIV(
            input_gallery,
            other_inputs,
            _id="phanterpwa-gallery-wrapper-" + self.namespace,
            _class="phanterpwa-gallery-wrapper"
        )

        html = DIV(
            DIV(
                DIV(
                    DIV(
                        wrapper_gallery,
                        _class="phanterpwa-centralizer-center"
                    ),
                    _class="phanterpwa-centralizer-horizontal"
                ),
                _class="phanterpwa-centralizer-vertical"
            ),
            _class="phanterpwa-centralizer-wrapper",
            _style="width: {0}px; height: {1}px;".format(self.config['view-width'], self.config['view-height'])
        )
        jQuery(self.el).html(
            html.jquery()
        ).promise().then(
            lambda: self._afterRead()
        )

    def simpleView(self, url):
        namespace = self.config['namespace']
        width = self.config["width"]
        height = self.config["height"]
        img_name = self.config["img_name"]

        cutted_img = document.createElement("IMG")
        cutted_img.src = url
        cutted_img.alt = img_name

        def onImageLoad(img, namespace, width, height):
            width_view = width
            height_view = height
            if width_view == height_view:
                if img.width > img.height:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                    ).css(
                        "background-size", "100% auto"
                    )
                else:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                    ).css(
                        "background-size", "auto 100%"
                    )
            elif width_view > height_view:
                if img.width > img.height:
                    rate = float(height_view) / img.height
                    width = img.width * rate
                    if width < width_view:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                        ).css(
                            "background-size", "100% auto"
                        )
                    else:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                        ).css(
                            "background-size", "auto 100%"
                        )
                else:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                    ).css(
                        "background-size", "100% auto"
                    )
            elif width_view < height_view:
                if img.width < img.height:
                    rate = float(height_view) / img.height
                    width = img.width * rate
                    if width > width_view:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                        ).css(
                            "background-size", "auto 100%"
                        )
                    else:
                        jQuery(
                            "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                        ).css(
                            "background-size", "100% auto"
                        )
                else:
                    jQuery(
                        "#phanterpwa-gallery-upload-image-simple-view-" + namespace
                    ).css(
                        "background-size", "auto 100%"
                    )
        cutted_img.onload = lambda: onImageLoad(this, namespace, width, height)
        xml_icons_view = ""
        if not self._data_view:
            xml_icons_view = DIV(
                DIV(
                    I(_class="fas fa-sync"),
                    _id="phanterpwa-gallery-upload-image-simple-view-button-reload-{0}".format(namespace),
                    _class="phanterpwa-gallery-upload-image-simple-view-button {0}".format(
                        "phanterpwa-gallery-upload-image-simple-view-button-reload"
                    )
                ),
                DIV(
                    I(_class="fas fa-trash-alt"),
                    _id="phanterpwa-gallery-upload-image-simple-view-button-delete-{0}".format(namespace),
                    _class="phanterpwa-gallery-upload-image-simple-view-button {0}".format(
                        "phanterpwa-gallery-upload-image-simple-view-button-delete"
                    )
                ),
                _class="phanterpwa-gallery-upload-image-simple-view-buttons"
            )
        html_simple_view = DIV(
            xml_icons_view,
            _id="phanterpwa-gallery-upload-image-simple-view-" + namespace,
            _class="phanterpwa-gallery-upload-image-simple-view",
            _alt=img_name,
            _style="width: {0}px; height: {1}px; background-image: url('{2}'); {3}".format(
                width,
                height,
                url,
                "background-position: center; overflow: hidden;"
            )
        )

        def activeButtonsView():
            jQuery(
                "#phanterpwa-gallery-upload-image-simple-view-button-reload-" + namespace
            ).off(
                "click.button-reload-view"
            ).on(
                "click.button-reload-view",
                lambda: self.getNewImage()
            )
            jQuery(
                "#phanterpwa-gallery-upload-image-simple-view-button-delete-" + namespace
            ).off(
                "click.button-reload-view"
            ).on(
                "click.button-reload-view",
                lambda: self.resetInputPanel()
            )

        jQuery("#phanterpwa-gallery-upload-image-default-" + namespace).html(html_simple_view.xml()).promise().then(
            lambda: activeButtonsView()
        )

    def resetInputPanel(self):
        self.config["current_image"] = None
        self.addInputPanel()


class GalleryCutter():
    def __init__(self, base64data, GalleryInput):
        self.base64data = base64data
        self.GalleryInput = GalleryInput
        self.config = GalleryInput.config
        __pragma__('jsiter')
        self.hammerconf = {}
        __pragma__('nojsiter')
        if self.config["hammerconf"] is not None or self.config["hammerconf"] is not js_undefined:
            for x in self.config["hammerconf"].keys():
                self.hammerconf[x] = self.config["hammerconf"][x]
        self.namespace = self.config['namespace']
        self.cutterSizeX = self.config['width']
        self.cutterSizeY = self.config['height']
        self.originalWidthImg = 0
        self.originalHeightImg = 0
        self.widthImg = 0
        self.heightImg = 0
        self.widthScreen = 0
        self.heightScreen = 0
        self.widthCutter = 0
        self.heightCutter = 0
        self.inicialPositionXBackground = 0
        self.inicialPositionYBackground = 0
        self.inicialPositionXImgToCut = 0
        self.inicialPositionYImgToCut = 0
        self.deslocationPositionXBackground = 0
        self.deslocationPositionYBackground = 0
        self.deslocationPositionXImgToCut = 0
        self.deslocationPositionYImgToCut = 0
        self.deslocationPositionZoom = 0
        self.positionDefaultZoom = 89.0
        self.widthImgAfterZoom = 0
        self.heightImgAfterZoom = 0
        self.positionXAfterZoom = 0
        self.positionYAfterZoom = 0
        self.activeViewImage = False
        self.addCutterPanel()

    def addCutterPanel(self):
        z_index = self.config["z-index"]
        cutter_panel = DIV(
            DIV(
                _id="phanterpwa-gallery-cutter-background-" + self.namespace,
                _class="phanterpwa-gallery-cutter-background"),
            DIV(
                _id="phanterpwa-gallery-cutter-shadow-" + self.namespace,
                _class="phanterpwa-gallery-cutter-shadow"),
            DIV(
                DIV(
                    DIV(
                        _class="phanterpwa-gallery-panel-cutter-image",
                        _id='phanterpwa-gallery-panel-cutter-image-' + self.namespace),
                    _style="overflow: hidden; width: {0}px; height: {1}px;".format(
                        self.cutterSizeX, self.cutterSizeY
                    ),
                    _id='phanterpwa-gallery-panel-cutter-size-container-' + self.namespace,
                    _class="phanterpwa-gallery-panel-cutter-size-container"
                ),
                _class="phanterpwa-gallery-panel-cutter"
            ),
            DIV(
                _id='phanterpwa-gallery-cutter-pad-' + self.namespace,
                _class="phanterpwa-gallery-cutter-pad"),
            DIV(
                DIV(
                    I(_class="fas fa-times-circle close-circle"),
                    _id='phanterpwa-gallery-cutter-control-close-' + self.namespace,
                    _class="phanterpwa-gallery-cutter-control"),
                DIV(
                    I(_class="fas fa-eye image-view"),
                    _id='phanterpwa-gallery-cutter-control-view-' + self.namespace,
                    _class="phanterpwa-gallery-cutter-control"),
                DIV(
                    I(_class="fas fa-cut image-cut"),
                    _id='phanterpwa-gallery-cutter-control-cut-' + self.namespace,
                    _class="phanterpwa-gallery-cutter-control"),
                _class='phanterpwa-gallery-cutter-controls-container'),
            DIV(
                DIV(
                    I(_class="far fa-image image-decrease"),
                    DIV(
                        DIV(_id='phanterpwa-gallery-cutter-zoom-control-' + self.namespace,
                            _class="phanterpwa-gallery-cutter-zoom-control"),
                        _id="phanterpwa-gallery-cutter-zoom-control-container-" + self.namespace,
                        _class="phanterpwa-gallery-cutter-zoom-control-container"
                    ),
                    I(_class="far fa-image image-increase"),
                    _class='phanterpwa-gallery-cutter-zoom-controls'),
                _class='phanterpwa-gallery-cutter-zoom-container'),
            _id='phanterpwa-gallery-panel-cutter-container-' + self.namespace,
            _class="phanterpwa-gallery-panel-cutter-container",
            _style="z-index: {0};".format(z_index)
        )
        jQuery(
            "#phanterpwa-gallery-wrapper-" + self.namespace
        ).append(
            cutter_panel.xml()
        ).promise().then(self._chargeEvents)

    def _chargeEvents(self):
        self.img1 = document.createElement("IMG")
        self.img2 = document.createElement("IMG")
        self.img1.onload = lambda: self.onLoadImage(self.img1)
        self.img1.src = self.base64data
        self.img2.src = self.base64data
        self.img1.onerror = lambda: self.setError(True)

    def prepareGestureMove(self, event):
        event.preventDefault()
        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).on(
            "panmove.phanterpwa-gallery-moving",
            lambda event: self.gestureMoving(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).on(
            "panend.phanterpwa-gallery-moving",
            lambda event: self.stopGestureMove(event)
        )

    def gestureMoving(self, event):
        if window.PhanterPWA.DEBUG:
            console.info(event.gesture.deltaX)
            console.info(event.gesture.deltaY)
        self.deslocationPositionXBackground = event.gesture.deltaX * (-1)
        self.deslocationPositionYBackground = event.gesture.deltaY * (-1)
        self.deslocationPositionXImgToCut = event.gesture.deltaX * (-1)
        self.deslocationPositionYImgToCut = event.gesture.deltaY * (-1)
        self.calcPosition()

    def stopGestureMove(self, event):
        event.preventDefault()
        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).off(
            "panmove.phanterpwa-gallery-moving"
        )
        self.saveinicialPosition()

    def gestureSizing(self, event, inicialPosition, width, height):
        event.preventDefault()
        xDeslocamento = event.gesture.deltaX
        if (((inicialPosition + xDeslocamento) > 0) and (inicialPosition + xDeslocamento) < 179):
            self.movecutterZoom(xDeslocamento, inicialPosition, width, height)

    def stopGestureSize(self, event):
        event.preventDefault()
        self.savePositionZoom()
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).off(
            'panmove.phanterpwa-gallery-sizing'
        )

    def prepareGestureSize(self, event):
        event.preventDefault()
        inicialPosition = self.positionDefaultZoom
        width = self.widthImg
        height = self.heightImg
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).on(
            'panmove.phanterpwa-gallery-sizing',
            lambda event: self.gestureSizing(event, inicialPosition, width, height)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).on(
            'panend.phanterpwa-gallery-sizing',
            lambda event: self.stopGestureSize(event)
        )

    def calcMidPosition(self, sizeContainer, sizeContent, positionContent):
        midsize1 = sizeContainer / 2.0
        midsize2 = sizeContent / 2.0
        relativeposition = midsize1 - midsize2
        finalPosition = relativeposition - positionContent
        return finalPosition

    def moveImage(self, x, y):
        self.deslocationPositionXBackground = x * (-1)
        self.deslocationPositionYBackground = y * (-1)
        self.deslocationPositionXImgToCut = x * (-1)
        self.deslocationPositionYImgToCut = y * (-1)
        self.calcPosition()

    def viewImage(self):
        if (self.activeViewImage):
            self.activeViewImage = False
            jQuery("#phanterpwa-gallery-cutter-control-view-" + self.namespace).removeClass("enable")
            jQuery("#phanterpwa-gallery-cutter-shadow-" + self.namespace).removeClass("enable")
        else:
            self.activeViewImage = True
            jQuery("#phanterpwa-gallery-cutter-control-view-" + self.namespace).addClass("enable")
            jQuery("#phanterpwa-gallery-cutter-shadow-" + self.namespace).addClass("enable")

    def closeImage(self):
        jQuery('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).removeClass("enable")
        jQuery('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).addClass("close")

    def cutImage(self):
        jQuery('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).removeClass("enable")
        jQuery('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).addClass("close")
        canvas = document.createElement("CANVAS")
        canvas.width = self.widthCutter
        canvas.height = self.heightCutter
        ctx = canvas.getContext('2d')
        ratio = self.originalWidthImg / float(self.widthImgAfterZoom)
        positionX = self.positionXAfterZoom * (-1) * ratio
        positionY = self.positionYAfterZoom * (-1) * ratio
        wX = self.cutterSizeX * ratio
        wY = self.cutterSizeY * ratio
        jQuery('#phanterpwa-gallery-input-cutterSizeX' + self.namespace).val(self.widthCutter)
        jQuery('#phanterpwa-gallery-input-cutterSizeY' + self.namespace).val(self.heightCutter)
        jQuery('#phanterpwa-gallery-input-positionX' + self.namespace).val(positionX)
        jQuery('#phanterpwa-gallery-input-positionY' + self.namespace).val(positionY)
        jQuery('#phanterpwa-gallery-input-newSizeX' + self.namespace).val(wX)
        jQuery('#phanterpwa-gallery-input-newSizeY' + self.namespace).val(wY)
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(self.img1, positionX, positionY, wX, wY, 0, 0, self.widthCutter, self.heightCutter)
        self.config["current_image"] = canvas.toDataURL()
        self.GalleryInput.config = self.config
        self.GalleryInput.simpleView(self.config["current_image"])
        if window.PhanterPWA.DEBUG:
            console.info("Cutting image")
        if callable(self.config.get("afterCut")):
            self.config["afterCut"](self)

    def movecutterZoom(self, x, zoominicial, width, height):
        self.deslocationPositionZoom = x * (-1)
        self.calcZoomPosition(zoominicial, width, height)

    def changeSizeImage(self, ratio, width, height):
        width = float(width) * ratio
        height = float(height) * ratio
        self.img1.style.width = width + "px"
        self.img1.style.height = height + "px"
        self.img2.style.width = width + "px"
        self.img2.style.height = height + "px"
        self.widthImg = width
        self.heightImg = height
        self.widthImgAfterZoom = width
        self.heightImgAfterZoom = height
        self.calcPosition()

    def calcZoomPosition(self, zoominicial, width, height):
        position = self.positionDefaultZoom - self.deslocationPositionZoom
        ratio = position / zoominicial
        self.changeSizeImage(ratio, width, height)
        jQuery('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).css("left", position + "px")

    def calcPosition(self):
        widthImg = self.widthImg
        heightImg = self.heightImg
        widthScreen = window.innerWidth
        heightScreen = window.innerHeight
        widthCutter = self.widthCutter
        heightCutter = self.heightCutter
        if((widthImg > 0) and (heightImg > 0) and (widthScreen > 0) and (heightScreen > 0)):
            fCalc = self.calcMidPosition
            iPXB = self.inicialPositionXBackground + self.deslocationPositionXBackground
            iPYB = self.inicialPositionYBackground + self.deslocationPositionYBackground
            iPXITC = self.inicialPositionXImgToCut + self.deslocationPositionXImgToCut
            iPYITC = self.inicialPositionYImgToCut + self.deslocationPositionYImgToCut
            relativePositionXBackground = fCalc(widthScreen, widthImg, iPXB)
            relativePositionYBackground = fCalc(heightScreen, heightImg, iPYB)
            relativePositionXImgToCut = fCalc(widthCutter, widthImg, iPXITC)
            relativePositionYImgToCut = fCalc(heightCutter, heightImg, iPYITC)
            jQuery('#phanterpwa-gallery-panel-cutter-size-container-' + self.namespace).css(
                "left", fCalc(widthScreen, widthCutter, 0) + "px")
            jQuery('#phanterpwa-gallery-panel-cutter-size-container-' + self.namespace).css(
                "top", fCalc(heightScreen, heightCutter, 0) + "px")
            jQuery("#phanterpwa-gallery-cutter-background-" + self.namespace).css(
                "left", relativePositionXBackground + "px")
            jQuery("#phanterpwa-gallery-cutter-background-" + self.namespace).css(
                "top", relativePositionYBackground + "px")
            jQuery('#phanterpwa-gallery-panel-cutter-image-' + self.namespace).css(
                "left", relativePositionXImgToCut + "px")
            jQuery('#phanterpwa-gallery-panel-cutter-image-' + self.namespace).css(
                "top", relativePositionYImgToCut + "px")
            self.positionXAfterZoom = relativePositionXImgToCut
            self.positionYAfterZoom = relativePositionYImgToCut

    def saveinicialPosition(self):
        self.inicialPositionXBackground += self.deslocationPositionXBackground
        self.inicialPositionYBackground += self.deslocationPositionYBackground
        self.inicialPositionXImgToCut += self.deslocationPositionXImgToCut
        self.inicialPositionYImgToCut += self.deslocationPositionYImgToCut
        self.deslocationPositionXBackground = 0
        self.deslocationPositionYBackground = 0
        self.deslocationPositionXImgToCut = 0
        self.deslocationPositionYImgToCut = 0

    def savePositionZoom(self):
        self.positionDefaultZoom -= self.deslocationPositionZoom
        self.deslocationPositionZoom = 0

    def setBase64(self, value):
        self.setBase64 = value

    def onLoadImage(self, img):
        jQuery("#phanterpwa-gallery-cutter-background-" + self.namespace).html(self.img1)
        jQuery("#phanterpwa-gallery-panel-cutter-image-" + self.namespace).html(self.img2)
        jQuery("#phanterpwa-gallery-cutter-control-view-" + self.namespace).removeClass("enable")
        jQuery("#phanterpwa-gallery-cutter-shadow-" + self.namespace).removeClass("enable")
        jQuery('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).css("left", "89px")
        jQuery("#phanterpwa-gallery-cutter-control-view-" + self.namespace).on('click',
            lambda: self.viewImage()
        )

        jQuery(
            '#phanterpwa-gallery-cutter-control-close-' + self.namespace
        ).on(
            'click',
            lambda: self.closeImage()
        )

        jQuery(
            '#phanterpwa-gallery-cutter-control-cut-' + self.namespace
        ).on(
            'click',
            lambda: self.cutImage()
        )

        jQuery(
            window
        ).off(
            "resize.phanterpwa-gallery-" + self.namespace
        ).on(
            "resize.phanterpwa-gallery-" + self.namespace,
            lambda: self.calcPosition()
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).on(
            'mousedown.phanterpwa-gallery-moving',
            lambda event: self.prepareMove(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).hammer(
            self.hammerconf
        ).on(
            "touchstart.phanterpwa-gallery-moving",
            lambda event: self.prepareGestureMove(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).hammer(
            self.hammerconf
        ).on(
            'touchstart.phanterpwa-gallery-sizing',
            lambda event: self.prepareGestureSize(event)
        )

        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).on(
            'mousedown.phanterpwa-gallery-sizing',
            lambda event: self.prepareSize(event)
        )
        imgWidth = img.width
        imgHeight = img.height
        self.widthImg = imgWidth
        self.heightImg = imgHeight
        self.originalWidthImg = imgWidth
        self.originalHeightImg = imgHeight
        self.widthImgAfterZoom = imgWidth
        self.heightImgAfterZoom = imgHeight

        self.widthCutter = float(self.cutterSizeX)
        self.heightCutter = float(self.cutterSizeY)
        if (self.error):
            console.error("has Error")
        else:
            self.calcPosition()
            jQuery('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).removeClass("close")
            jQuery('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).addClass("enable")

    def setError(self, bo):
        self.error = bo
        if self.config["onError"] is not None or self.config["onError"] is not js_undefined:
            self.config["onError"]()

    def moving(self, event, xInicial, yInicial):
        xDeslocamento = event.clientX - xInicial
        yDeslocamento = event.clientY - yInicial
        self.moveImage(xDeslocamento, yDeslocamento)

    def stopMove(self, event):
        self.saveinicialPosition()
        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).off(
            'mousemove.phanterpwa-gallery-moving'
        )

        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).off(
            'mouseleave.phanterpwa-gallery-moving'
        )

    def prepareMove(self, event):
        xInicial = event.clientX
        yInicial = event.clientY
        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).on(
            'mousemove.phanterpwa-gallery-moving',
            lambda event: self.moving(event, xInicial, yInicial)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).on(
            'mouseup.phanterpwa-gallery-moving',
            lambda event: self.stopMove(event)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-pad-' + self.namespace
        ).on(
            'mouseleave.phanterpwa-gallery-moving',
            lambda event: self.stopMove(event)
        )

    def sizing(self, event, xInicial, inicialPosition, width, height):
        xDeslocamento = event.clientX - xInicial
        if (((inicialPosition + xDeslocamento) > 0) and (inicialPosition + xDeslocamento) < 179):
            self.movecutterZoom(xDeslocamento, inicialPosition, width, height)

    def stopSize(self, event):
        self.savePositionZoom()
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).off(
            'mousemove.phanterpwa-gallery-sizing'
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).off(
            'mouseleave.phanterpwa-gallery-sizing'
        )

    def prepareSize(self, event):
        xInicial = event.clientX
        inicialPosition = self.positionDefaultZoom
        width = self.widthImg
        height = self.heightImg
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).on(
            'mousemove.phanterpwa-gallery-sizing',
            lambda event: self.sizing(event, xInicial, inicialPosition, width, height)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).on(
            'mouseup.phanterpwa-gallery-sizing',
            lambda event: self.stopSize(event)
        )
        jQuery(
            '#phanterpwa-gallery-cutter-zoom-control-' + self.namespace
        ).on(
            'mouseleave.phanterpwa-gallery-sizing',
            lambda event: self.stopSize(event)
        )


__pragma__('nokwargs')
