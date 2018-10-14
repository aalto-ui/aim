from unittest import TestCase

import segmentation
import test_data

class TestSegmentation(TestCase):
    def setUp(self):
        self.elements = segmentation.get_elements(test_data.load_test_data(), detailed=False)

    def test_returns_list(self):
        self.assertTrue(isinstance(self.elements, list))

    def test_list_contains_dicts(self):
        for element in self.elements:
            self.assertTrue(isinstance(element, dict))

    def test_elements_are_valid(self):
        for element in self.elements:
            self.assertTrue('id' in element)
            self.assertTrue('tag' in element)
            self.assertTrue('x_position' in element)
            self.assertTrue('y_position' in element)
            self.assertTrue('width' in element)
            self.assertTrue('height' in element)

            self.assertTrue(isinstance(element['id'], int))
            self.assertTrue(isinstance(element['tag'], basestring))
            self.assertTrue(isinstance(element['x_position'], int))
            self.assertTrue(isinstance(element['y_position'], int))
            self.assertTrue(isinstance(element['width'], int))
            self.assertTrue(isinstance(element['height'], int))
