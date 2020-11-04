# -*- coding: utf-8 -*-
# Some helpful wrappers here...

import pybase100


def encode(data, encoding="utf-8"):
    return pybase100.encode(data).decode(encoding)


def decode(data, encoding="utf-8"):
    return pybase100.decode(data.encode(encoding)
                            .replace(b"\xe2\x80\x8d\xe2\x99\x80\xef\xb8\x8f", b"")
                            .replace(b"\xe2\x80\x8d\xe2\x99\x82\xef\xb8\x8f", b"")
                            ).decode(encoding)
