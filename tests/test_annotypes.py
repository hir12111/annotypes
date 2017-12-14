import json
import unittest
import sys

from annotypes import WithCallTypes

from typing import Sequence


class TestAnnotypes(unittest.TestCase):
    def test_no_args_base_repr(self):

        class MyClass(WithCallTypes):
            pass

        assert repr(MyClass()) == "MyClass()"


class TestSimple(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3,):
            from annotypes.py2_examples.simple import Simple
        else:
            from annotypes.py3_examples.simple import Simple
        self.cls = Simple

    def test_simple(self):
        ct = self.cls.call_types
        assert list(ct) == ["exposure", "path"]
        assert ct["exposure"].description == "The exposure to be active for"
        assert ct["exposure"](3) == 3.0
        assert ct["path"].typ == str
        fname = "/tmp/fname.txt"
        inst = self.cls(0.1, fname)
        assert repr(inst) == \
            "Simple(exposure=0.1, path='/tmp/fname.txt')"
        inst.write_data("something")
        with open(fname) as f:
            assert f.read() == "Data: something\n"


class TestLong(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3,):
            from annotypes.py2_examples.long import Long
        else:
            from annotypes.py3_examples.long import Long
        self.cls = Long

    def test_long(self):
        ct = self.cls.call_types
        assert list(ct) == \
            ['axes', 'units', 'start', 'stop', 'size', 'alternate']
        assert ct["alternate"].description == \
            "Whether to reverse on alternate runs"
        assert ct["units"].typ == str
        assert ct["units"].is_array is True
        inst = self.cls("x", "mm", 0, 1, 10)
        assert repr(inst) == \
            "Long(axes=('x',), units=('mm',), start=(0,), stop=(1,), size=10, alternate=False)"


class TestComposition(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3,):
            from annotypes.py2_examples.composition import (
                CompositionClass, composition_func)
        else:
            from annotypes.py3_examples.composition import (
                CompositionClass, composition_func)
        self.cls = CompositionClass
        self.f = composition_func

    def test_composition_class(self):
        ct = self.cls.call_types
        assert list(ct) == ['exposure', 'path']
        assert ct["exposure"].description == \
            "The exposure to be active for"
        assert ct["exposure"].typ == float
        assert ct["path"].typ == str
        inst = self.cls(0.1, "/tmp/fname.txt")
        assert repr(inst) == \
            "CompositionClass(exposure=0.1, path='/tmp/fname.txt')"

    def test_composition_func(self):
        ct = self.f.call_types
        assert list(ct) == ['exposure', 'prefix']
        assert ct["exposure"].description == \
            "The exposure to be active for"
        assert ct["exposure"].typ == float
        assert ct["prefix"].description == \
               "The path prefix for the list of writers"
        insts = self.f(0.1, "/tmp")
        assert repr(insts[0]) == \
            "Simple(exposure=0.1, path='/tmp/one')"


class TestEnum(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3,):
            from annotypes.py2_examples.enumtaker import EnumTaker, Status
        else:
            from annotypes.py3_examples.enumtaker import EnumTaker, Status
        self.cls = EnumTaker
        self.e = Status

    def test_enum(self):
        ct = self.cls.call_types
        assert list(ct) == ['status']
        assert ct["status"].description == "The status"
        assert ct["status"].typ == self.e
        assert self.e['good'].name == 'good'
        inst = self.cls(self.e.good)
        assert repr(inst) == \
            "EnumTaker(status=<Status.good: 0>)"
