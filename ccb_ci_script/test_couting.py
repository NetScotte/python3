# -*- coding=utf-8 -*-
import unittest
import os

import faker
from click.testing import CliRunner

from ext_count import counting


class Counting(unittest.TestCase):
    def test_counting(self):
        runner = CliRunner()
        fk = faker.Faker()
        with runner.isolated_filesystem():
            for extension in ['py', 'java', 'class']:
                for _ in range(5):
                    filename = fk.file_name(extension=extension)
                    with open(filename, 'w') as f:
                        f.write(fk.text())
            result = runner.invoke(counting, ['dir', os.getcwd(), '-e', 'py'])
        self.assertEqual(result.exit_code, 0)
        self.assertRegex(result.output, r'py')
