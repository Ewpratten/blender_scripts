import abc


class BlenderModule(metaclass=abc.ABCMeta):
    """A common base class for blender sub-modules in this project with their own entrypoints"""

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def register_blender_module(self):
        """To be called on module load"""
        raise NotImplementedError

    @abc.abstractmethod
    def unregister_blender_module(self):
        """To be called on module unload"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self) -> str:
        """Returns the name of the module"""
        raise NotImplementedError
