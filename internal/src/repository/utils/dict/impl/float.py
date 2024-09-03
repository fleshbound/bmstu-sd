from internal.src.repository.utils.dict.dict import KeyTransformDictionaryBase


class FloatKeyDictionary(KeyTransformDictionaryBase):
    __slots__ = ("rounding_ndigits",)

    def __init__(self, rounding_ndigits, data=None):
        if (rounding_ndigits is not None
            and not isinstance(rounding_ndigits, int)
        ):
            raise TypeError
        super().__init__()
        self.rounding_ndigits = rounding_ndigits
        if data is not None:
            self.update(data)

    def copy(self):
        copy = FloatKeyDictionary(self.rounding_ndigits)
        dict.update(copy, self)
        return copy

    def __key_transform__(self, key):
        return round(key, self.rounding_ndigits)
