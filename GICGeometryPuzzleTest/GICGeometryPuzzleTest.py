import unittest
import io
from unittest.mock import patch
from GICGeometryPuzzle.GICGeometryPuzzleApp import *


class TestShapeChecker(unittest.TestCase):
    def test_is_valid_shape(self):
        # Test valid shape
        coords_valid = [(0, 0), (0, 2), (2, 2), (2, 0)]
        self.assertTrue(ShapeChecker.is_valid_shape(coords_valid))

        # Test invalid shape
        coords_invalid = [(0, 0), (0, 2), (0, 4)]
        self.assertFalse(ShapeChecker.is_valid_shape(coords_invalid))


class TestGeometryShape(unittest.TestCase):
    def test_is_complete(self):
        shape = GeometryShape([(0, 0), (0, 5), (5, 5)])
        self.assertTrue(shape.is_complete())

        shape = GeometryShape([(0, 0), (0, 5)])
        self.assertFalse(shape.is_complete())

    def test_add_coordinate(self):
        shape = GeometryShape([(0, 0), (0, 5), (5, 5)])
        self.assertFalse(shape.add_coordinate((0, 0)))
        self.assertFalse(shape.add_coordinate((0, 5)))
        self.assertTrue(shape.add_coordinate((5, 0)))
        self.assertFalse(shape.add_coordinate((5, 5)))

    def test_is_point_inside(self):
        shape = GeometryShape([(0, 0), (0, 5), (5, 5)])
        self.assertTrue(shape.is_point_inside((1, 2)))
        self.assertFalse(shape.is_point_inside((6, 6)))

    def test_generate_random_polygon(self):
        shape = GeometryShape.generate_random_polygon()
        self.assertTrue(3 <= len(shape.coordList) <= 8)


class TestApplicationRunner:
    def test_user_create_shape(self):
        # Test user inputting a valid shape
        with patch('builtins.input', side_effect=['1 1', '1 3', '3 3', '3 1', '#', '#']):
            with patch('sys.stdout', new=io.StringIO()) as fake_output:
                applicationContext = ApplicationContext(ApplicationConstants)
                app = ApplicationRunner(applicationContext)
                app.run()
                output = fake_output.getvalue().strip()
                print(output)
                assert "Your current shape is valid and is complete" in output
                assert "Your finalized shape is" in output
                assert "coordinates (2, 2) is within your finalized shape" in output

        # Test user inputting an invalid shape
        with patch('builtins.input', side_effect=['1 1', '2 2', '1 3', '#']):
            with patch('sys.stdout', new=io.StringIO()) as fake_output:
                applicationContext = ApplicationContext(ApplicationConstants)
                app = ApplicationRunner(applicationContext)
                app.run()
                output = fake_output.getvalue().strip()
                assert "Your current shape is incomplete" in output
                assert "New coordinates(2, 2) is invalid!!!" in output

    def test_generate_shape(self):
        # Test generating a random shape
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            applicationContext = ApplicationContext(ApplicationConstants)
            app = ApplicationRunner(applicationContext)
            with patch('builtins.input', side_effect=['2', '#']):
                app.run()
            output = fake_output.getvalue().strip()
            assert "Your random shape is" in output
            assert "coordinates (0, 3) is outside of your finalized shape" in output

    def test_invalid_application_mode(self):
        # Test invalid application mode
        with patch('builtins.input', side_effect=['3']):
            with patch('sys.stdout', new=io.StringIO()) as fake_output:
                applicationContext = ApplicationContext(ApplicationConstants)
                app = ApplicationRunner(applicationContext)
                app.run()
                output = fake_output.getvalue().strip()
                assert "Invalid application mode" in output

    def test_test_coordinate_in_shape(self):
        # Test point inside shape
        with patch('builtins.input', side_effect=['2 2', '#']):
            with patch('sys.stdout', new=io.StringIO()) as fake_output:
                applicationContext = ApplicationContext(ApplicationConstants)
                app = ApplicationRunner(applicationContext)
                shape = GeometryShape([(0, 0), (4, 0), (4, 4), (0, 4)])
                app._test_coordinate_in_shape(shape)
                output = fake_output.getvalue().strip()
                assert "Coordinates (2, 2) is within your finalized shape" in output

        # Test point outside shape
        with patch('builtins.input', side_effect=['5 5', '#']):
            with patch('sys.stdout', new=io.StringIO()) as fake_output:
                applicationContext = ApplicationContext(ApplicationConstants)
                app = ApplicationRunner(applicationContext)
                shape = GeometryShape([(0, 0), (4, 0), (4, 4), (0, 4)])
                app._test_coordinate_in_shape(shape)
                output = fake_output.getvalue().strip()
                assert "Sorry, coordinates (5, 5) is outside of your finalized shape" in output


if __name__ == '__main__':
    unittest.main()
