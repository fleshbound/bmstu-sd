import abc
import collections.abc


class KeyTransformDictionaryBase(dict, abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def __key_transform__(self, key):
        raise NotImplementedError

    def __init__(self, data=None, /, **kwargs):
        super().__init__()
        if data is not None:
            self.update(data)
        if kwargs:
            super().update(self._iter_key_transform(kwargs.items(), False))

    def copy(self):
        copy = self.__class__()
        super(KeyTransformDictionaryBase, copy).update(self)
        return copy

    def __contains__(self, key):
        return super().__contains__(self.__key_transform__(key))

    def __getitem__(self, key):
        return super().__getitem__(self.__key_transform__(key))

    def __setitem__(self, key, value):
        return super().__setitem__(self.__key_transform__(key), value)

    def __delitem__(self, key):
        return super().__delitem__(self.__key_transform__(key))

    def get(self, key, default=None):
        return super().get(self.__key_transform__(key), default)

    def setdefault(self, key, default=None):
        return super().setdefault(self.__key_transform__(key), default)

    def pop(self, key, *default):
        return super().pop(self.__key_transform__(key), *default)

    @classmethod
    def _check_dict_instance(cls, obj):
        if not isinstance(obj, dict):
            raise TypeError(
                f"Cannot merge {type(obj).__qualname__!r} into "
                    f"{cls.__qualname__!r}")

    def _iter_key_transform(self, items, check_type=True):
        if check_type and isinstance(items, collections.abc.Mapping):
            items = items.items()
        return ((self.__key_transform__(k), v) for k, v in items)

    def __ior__(self, other):
        self._check_dict_instance(other)
        super().update(self._iter_key_transform(other.items(), False))
        return self

    def __or__(self, other):
        self._check_dict_instance(other)
        result = self.copy()
        result.update(self._iter_key_transform(other.items(), False))
        return result

    def update(self, /, *args, **kwargs):
        super().update(*map(self._iter_key_transform, args))
        if kwargs:
            super().update(self._iter_key_transform(kwargs, False))
