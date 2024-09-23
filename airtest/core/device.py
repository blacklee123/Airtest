class MetaDevice(type):

    REGISTRY = {}

    def __new__(cls, name, bases, class_dict):
        cls = super().__new__(cls, name, bases, class_dict)
        cls.REGISTRY[name] = cls
        return cls


class Device(metaclass=MetaDevice):
    """Base class for test device"""

    def __init__(self):
        super().__init__()

    def to_json(self):
        try:
            uuid = repr(self.uuid)
        except:
            uuid = None
        return f"<{self.__class__.__name__} {uuid}>"

    @property
    def uuid(self):
        self._raise_not_implemented_error()

    def shell(self, *args, **kwargs):
        self._raise_not_implemented_error()

    def snapshot(self, *args, **kwargs):
        self._raise_not_implemented_error()

    def touch(self, target, **kwargs):
        self._raise_not_implemented_error()

    def double_click(self, target):
        raise NotImplementedError

    def swipe(self, t1, t2, **kwargs):
        self._raise_not_implemented_error()

    def keyevent(self, key, **kwargs):
        self._raise_not_implemented_error()

    def text(self, text, enter=True):
        self._raise_not_implemented_error()

    def start_app(self, package, **kwargs):
        self._raise_not_implemented_error()

    def stop_app(self, package):
        self._raise_not_implemented_error()

    def clear_app(self, package):
        self._raise_not_implemented_error()

    def list_app(self, **kwargs):
        self._raise_not_implemented_error()

    def install_app(self, uri, **kwargs):
        self._raise_not_implemented_error()

    def uninstall_app(self, package):
        self._raise_not_implemented_error()

    def get_current_resolution(self):
        self._raise_not_implemented_error()

    def get_render_resolution(self):
        self._raise_not_implemented_error()

    def get_ip_address(self):
        self._raise_not_implemented_error()

    def set_clipboard(self, text):
        self._raise_not_implemented_error()

    def get_clipboard(self):
        self._raise_not_implemented_error()

    def paste(self):
        self.text(self.get_clipboard())

    def _raise_not_implemented_error(self):
        platform = self.__class__.__name__
        raise NotImplementedError("Method not implemented on %s" % platform)

    def disconnect(self):
        pass
