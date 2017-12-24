# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


import glob
import unittest
import subprocess


class TestLicense(unittest.TestCase):

    def test_each_file_starts_with_license(self):
        license = [
            '# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)',
            '# Please find copy of license at "LICENSE"',
            '# at the root of the project.',
        ]
        files = glob.glob("**/*.py", recursive=True)
        for file_ in files:
            with open(file_) as file_obj:
                heading = file_obj.read(135)
            heading = heading.splitlines() if heading else []
            message = (
                "\nFile: {} is missing license note. It is compulsory to add a"
                "license note to each file."
            )
            self.assertListEqual(heading, license, message.format(file_))
