#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 João Pedro Rodrigues
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unit Tests for `pdb_shiftres`.
"""

import os
import sys
import unittest

from config import data_dir, output_dir
from utils import OutputCapture


class TestTool(unittest.TestCase):
    """
    Generic class for testing tools.
    """

    def setUp(self):
        # Dynamically import the module
        name = 'bin.pdb_shiftres'
        self.module = __import__(name, fromlist=[''])
    
    def read_prepare(self, input_file, output_file):
        """
        Prepares input and output common to the different tests.
        """
        
        with OutputCapture() as output:
            try:
                self.module.main()
            except SystemExit as e:
                self.retcode = e.code

        self.stdout = output.stdout
        self.stderr = output.stderr
        
        with open(input_file) as ifile:
            self.len_original = len(ifile.readlines())
        
        with open(output_file) as ofile:
            self.output_data = [l.strip("\n") for l in ofile]
        
        return
    
    def test_valid_1(self):
        """
        pdb_shiftres - shifts 50
        """
        
        input_file = os.path.join(data_dir, 'full_example.pdb')
        output_file = os.path.join(output_dir, 'output_pdb_shiftres_1.pdb')
        
        sys.argv = ['', '-50', input_file]  # simulate
        # Execute the script
        
        self.read_prepare(input_file, output_file)
        
        self.assertEqual(self.retcode, 0)  # ensure the program exited gracefully.
        self.assertEqual(len(self.stdout), self.len_original)  # lines deleted
        self.assertEqual(len(self.stderr), 0)  # no errors
        self.assertEqual(self.stdout, self.output_data)
    
    def test_valid_2(self):
        """
        pdb_shiftres - shifts -10
        """
        
        input_file = os.path.join(data_dir, 'full_example.pdb')
        output_file = os.path.join(output_dir, 'output_pdb_shiftres_2.pdb')
        
        sys.argv = ['', '--10', input_file]  # simulate
        # Execute the script
        
        self.read_prepare(input_file, output_file)
        
        self.assertEqual(self.retcode, 0)  # ensure the program exited gracefully.
        self.assertEqual(len(self.stdout), self.len_original)  # lines deleted
        self.assertEqual(len(self.stderr), 0)  # no errors
        self.assertEqual(self.stdout, self.output_data)
    
    def test_FileNotFound(self):
        """
        pdb_shiftres - file not found
        """

        # Error (file not found)
        sys.argv = ['', '-1', os.path.join(data_dir, 'not_there.pdb')]
        # Execute the script
        with OutputCapture() as output:
            try:
                self.module.main()
            except SystemExit as e:
                retcode = e.code

        stdout = output.stdout
        stderr = output.stderr

        self.assertEqual(retcode, 1)  # ensure the program exited gracefully.
        self.assertEqual(len(stdout), 0)  # no output
        self.assertEqual(stderr[0][:39], "ERROR!! File not found or not readable:")
    
    def test_FileNotGiven(self):
        """
        pdb_shiftres - file not found
        """

        # Error (file not found)
        sys.argv = ['', '-1']
        # Execute the script
        with OutputCapture() as output:
            try:
                self.module.main()
            except SystemExit as e:
                retcode = e.code

        stdout = output.stdout
        stderr = output.stderr

        self.assertEqual(retcode, 1)  # ensure the program exited gracefully.
        self.assertEqual(len(stdout), 0)  # no output
        self.assertEqual(stderr[0][:27], "ERROR!! No data to process!")

    def test_InvalidOptionValue_1(self):
        """
        pdb_shiftres - argument is not an option
        """
        
        # Error (file not found)
        sys.argv = ['', '1', os.path.join(data_dir, 'pico.pdb')]
        # Execute the script
        with OutputCapture() as output:
            try:
                self.module.main()
            except SystemExit as e:
                retcode = e.code

        stdout = output.stdout
        stderr = output.stderr

        self.assertEqual(retcode, 1)
        self.assertEqual(len(stdout), 0)  # no output
        self.assertEqual(stderr[0][:45], "ERROR! First argument is not an option: '1'")
