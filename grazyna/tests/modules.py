'''
Created on 01-04-2013

@author: firemark
'''
import unittest
import config
config.nick = "Test"
from ..modules import get_args_from_text, re_cmd, check_type
from ..utils.types import range_int


class ModuleTest(unittest.TestCase):

    @staticmethod
    def func_test(bot, arg1, arg2,
                  karg:range_int(0, 10)=0,
                  akarg:int=2):
        pass
    func_test.varkw = None
    func_test.varargs = None

    def test_cmd(self):
        for msg in (
                    "Test: cmd testing spaces",
                    ".cmd testing spaces"
                    ):
            cmd, text = re_cmd.match(msg).groups()
            self.assertEqual(cmd, "cmd", msg)
            self.assertEqual(text, "testing spaces", msg)

        for msg in (
                    "Test: another_cmd",
                    ".another_cmd"
                    ):
            cmd, text = re_cmd.match(msg).groups()
            self.assertEqual(cmd, "another_cmd", msg)
            self.assertEqual(text, None, msg)

    def test_get_args(self):
        max_args = 2

        for text, cor_args, cor_kwargs in (
                        ("firemark tiramo",
                         ["firemark", "tiramo"],
                         {}),

                        ("tiramo firemark with spaces",
                         ["tiramo", "firemark with spaces"],
                         {}),

                        ("tiramo firemark with spaces karg: 2 akarg: 5",
                         ["tiramo", "firemark with spaces"],
                         {"karg": "2", "akarg": "5"}),

                        ('"tiramo with spaces" firemark karg:" spaces "',
                         ["tiramo with spaces", "firemark"],
                         {"karg": " spaces "}),

                        ('karg: firemark arg2= 20 10 ',
                         ["10"],
                         {"karg": "firemark", "arg2": "20"}),

                            ):
            args, kwargs = get_args_from_text(text, max_args)
            self.assertListEqual(args, cor_args, text)
            self.assertDictEqual(kwargs, cor_kwargs, text)

    def test_check_type(self):
        for args, kwargs, result in (
                        #without kwargs
                         (["t1", "t2"], {},
                          {"arg1": "t1", "arg2": "t2", "karg": 0, "akarg": 2}),
                        #with optionals
                         (["t", "t", "-1", "-1"], {},
                          {"arg1": "t", "arg2": "t", "karg": 0, "akarg": -1}),
                        #mixing
                         (["ta", "t"], {"karg": "5", "akarg": "-1"},
                          {"arg1": "ta", "arg2": "t", "karg": 5, "akarg": -1}),
                        #another
                         (["t", "t"], {"karg": "15", "akarg": "10"},
                          {"arg1": "t", "arg2": "t", "karg": 10, "akarg": 10}),
                        #without args
                         ([], {"arg1": "a", "arg2": "c", "karg": "5", "akarg": "10"},
                          {"arg1": "a", "arg2": "c", "karg": 5, "akarg": 10}),
                         ):
            self.assertEqual(
                             check_type(args, kwargs, ModuleTest.func_test),
                             result
                             )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()