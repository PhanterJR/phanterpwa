// Transcrypt'ed from Python, 2021-03-12 03:29:37
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as helpers from './phanterpwa.frontend.helpers.js';
var __name__ = 'phanterpwa.frontend.components.gallery';
export var INPUT = helpers.XmlConstructor.tagger ('input', true);
export var I = helpers.XmlConstructor.tagger ('i');
export var DIV = helpers.XmlConstructor.tagger ('div');
export var FORM = helpers.XmlConstructor.tagger ('form');
export var XML = helpers.XML;
export var GalleryInput =  __class__ ('GalleryInput', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, el) {
		var config = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						default: config [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete config.__kwargtrans__;
			}
		}
		else {
		}
		self.el = $ (el);
		self.config = config;
		self.namespace = new Date ().getTime ();
		self.conf_default = dict ({'name': 'phanterpwa-gallery-file-input', 'button-upload': I (__kwargtrans__ ({_class: 'fas fa-cloud-upload-alt'})).xml (), 'width': 190, 'height': 200, 'view-width': null, 'view-height': null, 'cutter': false, 'z-index': 1005, 'current_image': null, 'put_in_form': true, 'img_name': 'PhanterpwaGalleryFile', 'hammerconf': dict ({'inputClass': (Hammer.SUPPORT_POINTER_EVENTS ? Hammer.PointerEventInput : Hammer.TouchInput)}), 'onError': null, 'beforeCut': null, 'afterCut': null});
		if (self.config === undefined) {
			self.config = dict ();
		}
		for (var d of self.conf_default.py_keys ()) {
			if (!__in__ (d, self.config)) {
				self.config [d] = self.conf_default [d];
			}
		}
		self.config ['namespace'] = self.namespace;
		self.config ['element'] = el;
		if (self.config ['view-width'] === null || self.config ['view-width'] === undefined) {
			self.config ['view-width'] = self.config ['width'];
		}
		if (self.config ['view-height'] === null || self.config ['view-height'] === undefined) {
			self.config ['view-height'] = self.config ['height'];
		}
		self.addInputPanel ();
	});},
	get getNewImage () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var inputChange = function (el) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'el': var el = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			var is_to_cut = self.config ['cutter'];
			var blob = $ (el) [0].files;
			var fileslength = blob.length;
			for (var i = 0; i < fileslength; i++) {
				var img_type = blob [i] ['type'];
				var img_name = blob [i] ['name'];
				self.config ['img_type'] = img_type;
				self.config ['img_name'] = img_name;
				if (img_type == 'image/png' || img_type == 'image/bmp' || img_type == 'image/gif' || img_type == 'image/jpeg') {
					var onloadend = function (reader, img_name, img_type) {
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'reader': var reader = __allkwargs0__ [__attrib0__]; break;
										case 'img_name': var img_name = __allkwargs0__ [__attrib0__]; break;
										case 'img_type': var img_type = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						var base64data = reader.result;
						var img1 = document.createElement ('IMG');
						img1.src = base64data;
						img1.alt = ((img_name + ' (') + img_type) + ')';
						if (is_to_cut) {
							var onImageLoad = function (img) {
								if (arguments.length) {
									var __ilastarg0__ = arguments.length - 1;
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
										var __allkwargs0__ = arguments [__ilastarg0__--];
										for (var __attrib0__ in __allkwargs0__) {
											switch (__attrib0__) {
												case 'img': var img = __allkwargs0__ [__attrib0__]; break;
											}
										}
									}
								}
								else {
								}
								if (window.PhanterPWA.DEBUG) {
									console.info (img.width);
									console.info (img.height);
								}
							};
							img1.onload = (function __lambda__ () {
								if (arguments.length) {
									var __ilastarg0__ = arguments.length - 1;
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
										var __allkwargs0__ = arguments [__ilastarg0__--];
										for (var __attrib0__ in __allkwargs0__) {
										}
									}
								}
								else {
								}
								return onImageLoad (this);
							});
							new GalleryCutter (base64data, self);
						}
						else {
							self.simpleView (base64data);
						}
					};
					var reader = new FileReader ();
					reader.readAsDataURL (blob [0]);
					reader.onloadend = (function __lambda__ () {
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
								}
							}
						}
						else {
						}
						return onloadend (reader, img_name, img_type);
					});
				}
				else {
					console.error ('The file has invalid type. It must be png, bmp, gif, jpeg type.');
				}
			}
		};
		var el_input = $ ('#phanterpwa-gallery-input-file-' + self.namespace);
		el_input.trigger ('click').off ('change.phanterpwa_gallery_input_' + self.namespace).on ('change.phanterpwa_gallery_input_' + self.namespace, (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return inputChange (this, self.config);
		}));
	});},
	get _afterRead () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (self.config ['current_image'] !== null && self.config ['current_image'] !== undefined) {
			self.simpleView (self.config ['current_image']);
		}
		else {
			$ ('#phanterpwa-gallery-upload-image-button-' + self.namespace).on ('click', (function __lambda__ () {
				if (arguments.length) {
					var __ilastarg0__ = arguments.length - 1;
					if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
						var __allkwargs0__ = arguments [__ilastarg0__--];
						for (var __attrib0__ in __allkwargs0__) {
						}
					}
				}
				else {
				}
				return self.getNewImage ();
			}));
		}
	});},
	get addInputPanel () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var other_inputs = '';
		if (self.config ['cutter']) {
			var cutter_vars = [INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-cutterSizeX' + self.namespace, _name: 'phanterpwa-gallery-input-cutterSizeX', _value: '', _type: 'text'})), INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-cutterSizeY' + self.namespace, _name: 'phanterpwa-gallery-input-cutterSizeY', _value: '', _type: 'text'})), INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-positionX' + self.namespace, _name: 'phanterpwa-gallery-input-positionX', _value: '', _type: 'text'})), INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-positionY' + self.namespace, _name: 'phanterpwa-gallery-input-positionY', _value: '', _type: 'text'})), INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-newSizeX' + self.namespace, _name: 'phanterpwa-gallery-input-newSizeX', _value: '', _type: 'text'})), INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-newSizeY' + self.namespace, _name: 'phanterpwa-gallery-input-newSizeY', _value: '', _type: 'text'})), INPUT (__kwargtrans__ ({_id: 'phanterpwa-gallery-input-rotation' + self.namespace, _name: 'phanterpwa-gallery-input-rotation', _value: '', _type: 'text'}))];
			var other_inputs = DIV (...cutter_vars, __kwargtrans__ ({_class: 'phanterpwa-gallery-inputs-container-' + self.namespace, _style: 'display: none'}));
		}
		var input_gallery = DIV (DIV (DIV (XML (self.config ['button-upload']), __kwargtrans__ ({_id: 'phanterpwa-gallery-upload-image-button-' + self.namespace, _class: 'phanterpwa-gallery-upload-image-button link', _phanterpwa_input: 'phanterpwa-gallery-input-file-' + self.namespace})), __kwargtrans__ ({_id: 'phanterpwa-gallery-upload-image-default-' + self.namespace, _class: 'phanterpwa-gallery-upload-image-default'})), INPUT (__kwargtrans__ ({_accept: 'image/png, image/jpeg, image/gif, image/bmp', _class: 'phanterpwa-gallery-upload-input-file', _type: 'file', _id: 'phanterpwa-gallery-input-file-' + self.namespace, _name: 'phanterpwa-gallery-file-input'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-input-container-' + self.namespace, _class: 'phanterpwa-gallery-input-container'}));
		var wrapper_gallery = DIV (input_gallery, other_inputs, __kwargtrans__ ({_id: 'phanterpwa-gallery-wrapper-' + self.namespace, _class: 'phanterpwa-gallery-wrapper'}));
		var html = DIV (DIV (DIV (DIV (wrapper_gallery, __kwargtrans__ ({_class: 'phanterpwa-centralizer-center'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-horizontal'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-vertical'})), __kwargtrans__ ({_class: 'phanterpwa-centralizer-wrapper', _style: 'width: {0}px; height: {1}px;'.format (self.config ['view-width'], self.config ['view-height'])}));
		$ (self.el).html (html.jquery ()).promise ().then ((function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self._afterRead ();
		}));
	});},
	get simpleView () {return __get__ (this, function (self, url) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'url': var url = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var namespace = self.config ['namespace'];
		var width = self.config ['width'];
		var height = self.config ['height'];
		var img_name = self.config ['img_name'];
		var cutted_img = document.createElement ('IMG');
		cutted_img.src = url;
		cutted_img.alt = img_name;
		var onImageLoad = function (img, namespace, width, height) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'img': var img = __allkwargs0__ [__attrib0__]; break;
							case 'namespace': var namespace = __allkwargs0__ [__attrib0__]; break;
							case 'width': var width = __allkwargs0__ [__attrib0__]; break;
							case 'height': var height = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			var width_view = width;
			var height_view = height;
			if (width_view == height_view) {
				if (img.width > img.height) {
					$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', '100% auto');
				}
				else {
					$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', 'auto 100%');
				}
			}
			else if (width_view > height_view) {
				if (img.width > img.height) {
					var rate = float (height_view) / img.height;
					var width = img.width * rate;
					if (width < width_view) {
						$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', '100% auto');
					}
					else {
						$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', 'auto 100%');
					}
				}
				else {
					$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', '100% auto');
				}
			}
			else if (width_view < height_view) {
				if (img.width < img.height) {
					var rate = float (height_view) / img.height;
					var width = img.width * rate;
					if (width > width_view) {
						$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', 'auto 100%');
					}
					else {
						$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', '100% auto');
					}
				}
				else {
					$ ('#phanterpwa-gallery-upload-image-simple-view-' + namespace).css ('background-size', 'auto 100%');
				}
			}
		};
		cutted_img.onload = (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return onImageLoad (this, namespace, width, height);
		});
		var html_simple_view = DIV (DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-sync'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-upload-image-simple-view-button-reload-' + namespace, _class: 'phanterpwa-gallery-upload-image-simple-view-button {0}'.format ('phanterpwa-gallery-upload-image-simple-view-button-reload')})), DIV (I (__kwargtrans__ ({_class: 'fas fa-trash-alt'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-upload-image-simple-view-button-delete-' + namespace, _class: 'phanterpwa-gallery-upload-image-simple-view-button {0}'.format ('phanterpwa-gallery-upload-image-simple-view-button-delete')})), __kwargtrans__ ({_class: 'phanterpwa-gallery-upload-image-simple-view-buttons'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-upload-image-simple-view-' + namespace, _class: 'phanterpwa-gallery-upload-image-simple-view', _alt: img_name, _style: "width: {0}px; height: {1}px; background-image: url('{2}'); {3}".format (width, height, url, 'background-position: center; overflow: hidden;')}));
		var activeButtonsView = function () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			$ ('#phanterpwa-gallery-upload-image-simple-view-button-reload-' + namespace).off ('click.button-reload-view').on ('click.button-reload-view', (function __lambda__ () {
				if (arguments.length) {
					var __ilastarg0__ = arguments.length - 1;
					if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
						var __allkwargs0__ = arguments [__ilastarg0__--];
						for (var __attrib0__ in __allkwargs0__) {
						}
					}
				}
				else {
				}
				return self.getNewImage ();
			}));
			$ ('#phanterpwa-gallery-upload-image-simple-view-button-delete-' + namespace).off ('click.button-reload-view').on ('click.button-reload-view', (function __lambda__ () {
				if (arguments.length) {
					var __ilastarg0__ = arguments.length - 1;
					if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
						var __allkwargs0__ = arguments [__ilastarg0__--];
						for (var __attrib0__ in __allkwargs0__) {
						}
					}
				}
				else {
				}
				return self.resetInputPanel ();
			}));
		};
		$ ('#phanterpwa-gallery-upload-image-default-' + namespace).html (html_simple_view.xml ()).promise ().then ((function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return activeButtonsView ();
		}));
	});},
	get resetInputPanel () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.config ['current_image'] = null;
		self.addInputPanel ();
	});}
});
export var GalleryCutter =  __class__ ('GalleryCutter', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self, base64data, GalleryInput) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'base64data': var base64data = __allkwargs0__ [__attrib0__]; break;
						case 'GalleryInput': var GalleryInput = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.base64data = base64data;
		self.GalleryInput = GalleryInput;
		self.config = GalleryInput.config;
		self.hammerconf = {};
		if (self.config ['hammerconf'] !== null || self.config ['hammerconf'] !== undefined) {
			for (var x of self.config ['hammerconf'].py_keys ()) {
				self.hammerconf [x] = self.config ['hammerconf'] [x];
			}
		}
		self.namespace = self.config ['namespace'];
		self.cutterSizeX = self.config ['width'];
		self.cutterSizeY = self.config ['height'];
		self.originalWidthImg = 0;
		self.originalHeightImg = 0;
		self.widthImg = 0;
		self.heightImg = 0;
		self.widthScreen = 0;
		self.heightScreen = 0;
		self.widthCutter = 0;
		self.heightCutter = 0;
		self.inicialPositionXBackground = 0;
		self.inicialPositionYBackground = 0;
		self.inicialPositionXImgToCut = 0;
		self.inicialPositionYImgToCut = 0;
		self.deslocationPositionXBackground = 0;
		self.deslocationPositionYBackground = 0;
		self.deslocationPositionXImgToCut = 0;
		self.deslocationPositionYImgToCut = 0;
		self.deslocationPositionZoom = 0;
		self.positionDefaultZoom = 89.0;
		self.widthImgAfterZoom = 0;
		self.heightImgAfterZoom = 0;
		self.positionXAfterZoom = 0;
		self.positionYAfterZoom = 0;
		self.activeViewImage = false;
		self.addCutterPanel ();
	});},
	get addCutterPanel () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var z_index = self.config ['z-index'];
		var cutter_panel = DIV (DIV (__kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-background-' + self.namespace, _class: 'phanterpwa-gallery-cutter-background'})), DIV (__kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-shadow-' + self.namespace, _class: 'phanterpwa-gallery-cutter-shadow'})), DIV (DIV (DIV (__kwargtrans__ ({_class: 'phanterpwa-gallery-panel-cutter-image', _id: 'phanterpwa-gallery-panel-cutter-image-' + self.namespace})), __kwargtrans__ ({_style: 'overflow: hidden; width: {0}px; height: {1}px;'.format (self.cutterSizeX, self.cutterSizeY), _id: 'phanterpwa-gallery-panel-cutter-size-container-' + self.namespace, _class: 'phanterpwa-gallery-panel-cutter-size-container'})), __kwargtrans__ ({_class: 'phanterpwa-gallery-panel-cutter'})), DIV (__kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-pad-' + self.namespace, _class: 'phanterpwa-gallery-cutter-pad'})), DIV (DIV (I (__kwargtrans__ ({_class: 'fas fa-times-circle close-circle'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-control-close-' + self.namespace, _class: 'phanterpwa-gallery-cutter-control'})), DIV (I (__kwargtrans__ ({_class: 'fas fa-eye image-view'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-control-view-' + self.namespace, _class: 'phanterpwa-gallery-cutter-control'})), DIV (I (__kwargtrans__ ({_class: 'fas fa-cut image-cut'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-control-cut-' + self.namespace, _class: 'phanterpwa-gallery-cutter-control'})), __kwargtrans__ ({_class: 'phanterpwa-gallery-cutter-controls-container'})), DIV (DIV (I (__kwargtrans__ ({_class: 'far fa-image image-decrease'})), DIV (DIV (__kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-zoom-control-' + self.namespace, _class: 'phanterpwa-gallery-cutter-zoom-control'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-cutter-zoom-control-container-' + self.namespace, _class: 'phanterpwa-gallery-cutter-zoom-control-container'})), I (__kwargtrans__ ({_class: 'far fa-image image-increase'})), __kwargtrans__ ({_class: 'phanterpwa-gallery-cutter-zoom-controls'})), __kwargtrans__ ({_class: 'phanterpwa-gallery-cutter-zoom-container'})), __kwargtrans__ ({_id: 'phanterpwa-gallery-panel-cutter-container-' + self.namespace, _class: 'phanterpwa-gallery-panel-cutter-container', _style: 'z-index: {0};'.format (z_index)}));
		$ ('#phanterpwa-gallery-wrapper-' + self.namespace).append (cutter_panel.xml ()).promise ().then (self._chargeEvents);
	});},
	get _chargeEvents () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.img1 = document.createElement ('IMG');
		self.img2 = document.createElement ('IMG');
		self.img1.onload = (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.onLoadImage (self.img1);
		});
		self.img1.src = self.base64data;
		self.img2.src = self.base64data;
		self.img1.onerror = (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.setError (true);
		});
	});},
	get prepareGestureMove () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		event.preventDefault ();
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).on ('panmove.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.gestureMoving (event);
		}));
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).on ('panend.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.stopGestureMove (event);
		}));
	});},
	get gestureMoving () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (window.PhanterPWA.DEBUG) {
			console.info (event.gesture.deltaX);
			console.info (event.gesture.deltaY);
		}
		self.deslocationPositionXBackground = event.gesture.deltaX * -(1);
		self.deslocationPositionYBackground = event.gesture.deltaY * -(1);
		self.deslocationPositionXImgToCut = event.gesture.deltaX * -(1);
		self.deslocationPositionYImgToCut = event.gesture.deltaY * -(1);
		self.calcPosition ();
	});},
	get stopGestureMove () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		event.preventDefault ();
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).off ('panmove.phanterpwa-gallery-moving');
		self.saveinicialPosition ();
	});},
	get gestureSizing () {return __get__ (this, function (self, event, inicialPosition, width, height) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						case 'inicialPosition': var inicialPosition = __allkwargs0__ [__attrib0__]; break;
						case 'width': var width = __allkwargs0__ [__attrib0__]; break;
						case 'height': var height = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		event.preventDefault ();
		var xDeslocamento = event.gesture.deltaX;
		if (inicialPosition + xDeslocamento > 0 && inicialPosition + xDeslocamento < 179) {
			self.movecutterZoom (xDeslocamento, inicialPosition, width, height);
		}
	});},
	get stopGestureSize () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		event.preventDefault ();
		self.savePositionZoom ();
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).off ('panmove.phanterpwa-gallery-sizing');
	});},
	get prepareGestureSize () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		event.preventDefault ();
		console.log (event);
		var inicialPosition = self.positionDefaultZoom;
		var width = self.widthImg;
		var height = self.heightImg;
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).on ('panmove.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.gestureSizing (event, inicialPosition, width, height);
		}));
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).on ('panend.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.stopGestureSize (event);
		}));
	});},
	get calcMidPosition () {return __get__ (this, function (self, sizeContainer, sizeContent, positionContent) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'sizeContainer': var sizeContainer = __allkwargs0__ [__attrib0__]; break;
						case 'sizeContent': var sizeContent = __allkwargs0__ [__attrib0__]; break;
						case 'positionContent': var positionContent = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var midsize1 = sizeContainer / 2.0;
		var midsize2 = sizeContent / 2.0;
		var relativeposition = midsize1 - midsize2;
		var finalPosition = relativeposition - positionContent;
		return finalPosition;
	});},
	get moveImage () {return __get__ (this, function (self, x, y) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'x': var x = __allkwargs0__ [__attrib0__]; break;
						case 'y': var y = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.deslocationPositionXBackground = x * -(1);
		self.deslocationPositionYBackground = y * -(1);
		self.deslocationPositionXImgToCut = x * -(1);
		self.deslocationPositionYImgToCut = y * -(1);
		self.calcPosition ();
	});},
	get viewImage () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		if (self.activeViewImage) {
			self.activeViewImage = false;
			$ ('#phanterpwa-gallery-cutter-control-view-' + self.namespace).removeClass ('enable');
			$ ('#phanterpwa-gallery-cutter-shadow-' + self.namespace).removeClass ('enable');
		}
		else {
			self.activeViewImage = true;
			$ ('#phanterpwa-gallery-cutter-control-view-' + self.namespace).addClass ('enable');
			$ ('#phanterpwa-gallery-cutter-shadow-' + self.namespace).addClass ('enable');
		}
	});},
	get closeImage () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).removeClass ('enable');
		$ ('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).addClass ('close');
	});},
	get cutImage () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).removeClass ('enable');
		$ ('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).addClass ('close');
		var canvas = document.createElement ('CANVAS');
		canvas.width = self.widthCutter;
		canvas.height = self.heightCutter;
		var ctx = canvas.getContext ('2d');
		var ratio = self.originalWidthImg / float (self.widthImgAfterZoom);
		var positionX = (self.positionXAfterZoom * -(1)) * ratio;
		var positionY = (self.positionYAfterZoom * -(1)) * ratio;
		var wX = self.cutterSizeX * ratio;
		var wY = self.cutterSizeY * ratio;
		$ ('#phanterpwa-gallery-input-cutterSizeX' + self.namespace).val (self.widthCutter);
		$ ('#phanterpwa-gallery-input-cutterSizeY' + self.namespace).val (self.heightCutter);
		$ ('#phanterpwa-gallery-input-positionX' + self.namespace).val (positionX);
		$ ('#phanterpwa-gallery-input-positionY' + self.namespace).val (positionY);
		$ ('#phanterpwa-gallery-input-newSizeX' + self.namespace).val (wX);
		$ ('#phanterpwa-gallery-input-newSizeY' + self.namespace).val (wY);
		ctx.clearRect (0, 0, canvas.width, canvas.height);
		ctx.drawImage (self.img1, positionX, positionY, wX, wY, 0, 0, self.widthCutter, self.heightCutter);
		self.config ['current_image'] = canvas.toDataURL ();
		self.GalleryInput.config = self.config;
		self.GalleryInput.simpleView (self.config ['current_image']);
		if (window.PhanterPWA.DEBUG) {
			console.info ('Cutting image');
		}
		if (callable (self.config.py_get ('afterCut'))) {
			self.config ['afterCut'] (self);
		}
	});},
	get movecutterZoom () {return __get__ (this, function (self, x, zoominicial, width, height) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'x': var x = __allkwargs0__ [__attrib0__]; break;
						case 'zoominicial': var zoominicial = __allkwargs0__ [__attrib0__]; break;
						case 'width': var width = __allkwargs0__ [__attrib0__]; break;
						case 'height': var height = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.deslocationPositionZoom = x * -(1);
		self.calcZoomPosition (zoominicial, width, height);
	});},
	get changeSizeImage () {return __get__ (this, function (self, ratio, width, height) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'ratio': var ratio = __allkwargs0__ [__attrib0__]; break;
						case 'width': var width = __allkwargs0__ [__attrib0__]; break;
						case 'height': var height = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var width = float (width) * ratio;
		var height = float (height) * ratio;
		self.img1.style.width = width + 'px';
		self.img1.style.height = height + 'px';
		self.img2.style.width = width + 'px';
		self.img2.style.height = height + 'px';
		self.widthImg = width;
		self.heightImg = height;
		self.widthImgAfterZoom = width;
		self.heightImgAfterZoom = height;
		self.calcPosition ();
	});},
	get calcZoomPosition () {return __get__ (this, function (self, zoominicial, width, height) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'zoominicial': var zoominicial = __allkwargs0__ [__attrib0__]; break;
						case 'width': var width = __allkwargs0__ [__attrib0__]; break;
						case 'height': var height = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var position = self.positionDefaultZoom - self.deslocationPositionZoom;
		var ratio = position / zoominicial;
		self.changeSizeImage (ratio, width, height);
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).css ('left', position + 'px');
	});},
	get calcPosition () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var widthImg = self.widthImg;
		var heightImg = self.heightImg;
		var widthScreen = window.innerWidth;
		var heightScreen = window.innerHeight;
		var widthCutter = self.widthCutter;
		var heightCutter = self.heightCutter;
		if (widthImg > 0 && heightImg > 0 && widthScreen > 0 && heightScreen > 0) {
			var fCalc = self.calcMidPosition;
			var iPXB = self.inicialPositionXBackground + self.deslocationPositionXBackground;
			var iPYB = self.inicialPositionYBackground + self.deslocationPositionYBackground;
			var iPXITC = self.inicialPositionXImgToCut + self.deslocationPositionXImgToCut;
			var iPYITC = self.inicialPositionYImgToCut + self.deslocationPositionYImgToCut;
			var relativePositionXBackground = fCalc (widthScreen, widthImg, iPXB);
			var relativePositionYBackground = fCalc (heightScreen, heightImg, iPYB);
			var relativePositionXImgToCut = fCalc (widthCutter, widthImg, iPXITC);
			var relativePositionYImgToCut = fCalc (heightCutter, heightImg, iPYITC);
			$ ('#phanterpwa-gallery-panel-cutter-size-container-' + self.namespace).css ('left', fCalc (widthScreen, widthCutter, 0) + 'px');
			$ ('#phanterpwa-gallery-panel-cutter-size-container-' + self.namespace).css ('top', fCalc (heightScreen, heightCutter, 0) + 'px');
			$ ('#phanterpwa-gallery-cutter-background-' + self.namespace).css ('left', relativePositionXBackground + 'px');
			$ ('#phanterpwa-gallery-cutter-background-' + self.namespace).css ('top', relativePositionYBackground + 'px');
			$ ('#phanterpwa-gallery-panel-cutter-image-' + self.namespace).css ('left', relativePositionXImgToCut + 'px');
			$ ('#phanterpwa-gallery-panel-cutter-image-' + self.namespace).css ('top', relativePositionYImgToCut + 'px');
			self.positionXAfterZoom = relativePositionXImgToCut;
			self.positionYAfterZoom = relativePositionYImgToCut;
		}
	});},
	get saveinicialPosition () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.inicialPositionXBackground += self.deslocationPositionXBackground;
		self.inicialPositionYBackground += self.deslocationPositionYBackground;
		self.inicialPositionXImgToCut += self.deslocationPositionXImgToCut;
		self.inicialPositionYImgToCut += self.deslocationPositionYImgToCut;
		self.deslocationPositionXBackground = 0;
		self.deslocationPositionYBackground = 0;
		self.deslocationPositionXImgToCut = 0;
		self.deslocationPositionYImgToCut = 0;
	});},
	get savePositionZoom () {return __get__ (this, function (self) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.positionDefaultZoom -= self.deslocationPositionZoom;
		self.deslocationPositionZoom = 0;
	});},
	get setBase64 () {return __get__ (this, function (self, value) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'value': var value = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.setBase64 = value;
	});},
	get onLoadImage () {return __get__ (this, function (self, img) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'img': var img = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		$ ('#phanterpwa-gallery-cutter-background-' + self.namespace).html (self.img1);
		$ ('#phanterpwa-gallery-panel-cutter-image-' + self.namespace).html (self.img2);
		$ ('#phanterpwa-gallery-cutter-control-view-' + self.namespace).removeClass ('enable');
		$ ('#phanterpwa-gallery-cutter-shadow-' + self.namespace).removeClass ('enable');
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).css ('left', '89px');
		$ ('#phanterpwa-gallery-cutter-control-view-' + self.namespace).on ('click', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.viewImage ();
		}));
		$ ('#phanterpwa-gallery-cutter-control-close-' + self.namespace).on ('click', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.closeImage ();
		}));
		$ ('#phanterpwa-gallery-cutter-control-cut-' + self.namespace).on ('click', (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.cutImage ();
		}));
		$ (window).off ('resize.phanterpwa-gallery-' + self.namespace).on ('resize.phanterpwa-gallery-' + self.namespace, (function __lambda__ () {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
					}
				}
			}
			else {
			}
			return self.calcPosition ();
		}));
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).on ('mousedown.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.prepareMove (event);
		}));
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).hammer (self.hammerconf).on ('touchstart.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.prepareGestureMove (event);
		}));
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).hammer (self.hammerconf).on ('touchstart.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.prepareGestureSize (event);
		}));
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).on ('mousedown.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.prepareSize (event);
		}));
		var imgWidth = img.width;
		var imgHeight = img.height;
		self.widthImg = imgWidth;
		self.heightImg = imgHeight;
		self.originalWidthImg = imgWidth;
		self.originalHeightImg = imgHeight;
		self.widthImgAfterZoom = imgWidth;
		self.heightImgAfterZoom = imgHeight;
		self.widthCutter = float (self.cutterSizeX);
		self.heightCutter = float (self.cutterSizeY);
		if (self.error) {
			console.error ('has Error');
		}
		else {
			self.calcPosition ();
			$ ('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).removeClass ('close');
			$ ('#phanterpwa-gallery-panel-cutter-container-' + self.namespace).addClass ('enable');
		}
	});},
	get setError () {return __get__ (this, function (self, bo) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'bo': var bo = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.error = bo;
		if (self.config ['onError'] !== null || self.config ['onError'] !== undefined) {
			self.config ['onError'] ();
		}
	});},
	get moving () {return __get__ (this, function (self, event, xInicial, yInicial) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						case 'xInicial': var xInicial = __allkwargs0__ [__attrib0__]; break;
						case 'yInicial': var yInicial = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var xDeslocamento = event.clientX - xInicial;
		var yDeslocamento = event.clientY - yInicial;
		self.moveImage (xDeslocamento, yDeslocamento);
	});},
	get stopMove () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.saveinicialPosition ();
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).off ('mousemove.phanterpwa-gallery-moving');
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).off ('mouseleave.phanterpwa-gallery-moving');
	});},
	get prepareMove () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var xInicial = event.clientX;
		var yInicial = event.clientY;
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).on ('mousemove.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.moving (event, xInicial, yInicial);
		}));
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).on ('mouseup.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.stopMove (event);
		}));
		$ ('#phanterpwa-gallery-cutter-pad-' + self.namespace).on ('mouseleave.phanterpwa-gallery-moving', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.stopMove (event);
		}));
	});},
	get sizing () {return __get__ (this, function (self, event, xInicial, inicialPosition, width, height) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						case 'xInicial': var xInicial = __allkwargs0__ [__attrib0__]; break;
						case 'inicialPosition': var inicialPosition = __allkwargs0__ [__attrib0__]; break;
						case 'width': var width = __allkwargs0__ [__attrib0__]; break;
						case 'height': var height = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var xDeslocamento = event.clientX - xInicial;
		if (inicialPosition + xDeslocamento > 0 && inicialPosition + xDeslocamento < 179) {
			self.movecutterZoom (xDeslocamento, inicialPosition, width, height);
		}
	});},
	get stopSize () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		self.savePositionZoom ();
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).off ('mousemove.phanterpwa-gallery-sizing');
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).off ('mouseleave.phanterpwa-gallery-sizing');
	});},
	get prepareSize () {return __get__ (this, function (self, event) {
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						case 'event': var event = __allkwargs0__ [__attrib0__]; break;
					}
				}
			}
		}
		else {
		}
		var xInicial = event.clientX;
		var inicialPosition = self.positionDefaultZoom;
		var width = self.widthImg;
		var height = self.heightImg;
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).on ('mousemove.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.sizing (event, xInicial, inicialPosition, width, height);
		}));
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).on ('mouseup.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.stopSize (event);
		}));
		$ ('#phanterpwa-gallery-cutter-zoom-control-' + self.namespace).on ('mouseleave.phanterpwa-gallery-sizing', (function __lambda__ (event) {
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							case 'event': var event = __allkwargs0__ [__attrib0__]; break;
						}
					}
				}
			}
			else {
			}
			return self.stopSize (event);
		}));
	});}
});

//# sourceMappingURL=phanterpwa.frontend.components.gallery.map