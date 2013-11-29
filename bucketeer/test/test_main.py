import unittest
from bucketeer import main

class MainTest(unittest.TestCase):

  def setUp(self):

    return

  def tearDown(self):

    return

  ### Test Methods

  def test_main(self):
    # True if module loaded successfully, False if not
    self.assertTrue(main)

  ###

if __name__ == '__main__':
  unittest.main(buffer = True)
