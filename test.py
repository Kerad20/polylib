import unittest
import intpolylib
from parameterized import parameterized

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

class TestFindDivisors(ParametrizedTestCase): # testy funkcji znajdującej dzielniki

    @parameterized.expand([
        ["test1", 1048576, [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]],
        ["test2", 4294967296, [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 
        2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296]],
        ["test3", 5247145, [1, 5, 1049429, 5247145]],
        ["test4", 25000, [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500, 625, 1000, 1250, 2500, 3125, 5000, 6250, 12500, 25000]],
        ["test5", 20988580, [1, 2, 4, 5, 10, 20, 1049429, 2098858, 4197716, 5247145, 10494290, 20988580]],
        ["test6", 9064457, [1, 9064457]],
        ["test7", 1, [1]],
        ["test9", 2183462912, [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 33317, 65536, 66634, 133268, 
        266536, 533072, 1066144, 2132288, 4264576, 8529152, 17058304, 34116608, 68233216, 136466432, 272932864, 545865728, 1091731456, 2183462912]]
    ])

    def test_divisors(self, name, data, correct_answer):
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        minus = [-i for i in correct_answer]
        correct_answer = sorted(correct_answer + minus)
        self.assertEqual(result, correct_answer)

    def test8(self): # faktoryzacja 0
        data = 0
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = []
        self.assertEqual(result, correctAnswer)

    def test10(self): # testy dzielników mniejszych liczb
        base = intpolylib.BasePolynomial()
        for i in range(1, 10000):
            result = base.findDivisors(i)
            correctAnswer = [number for number in range(1, i+1) if i % number == 0]
            minus = [-i for i in correctAnswer]
            correctAnswer = sorted(correctAnswer + minus)
            with self.subTest(i=i):
                self.assertEqual(correctAnswer, result)

class TestFactorization(ParametrizedTestCase): # testy faktoryzacji

    @parameterized.expand([
        ["test1", "x^5-x^4-2x^3-8x^2+6x-1", ["x^2-3x+1", "x^3+2x^2+3x-1"]],
        ["test2", "x^4+x^2-20", ["x-2", "x+2", "x^2+5"]],
        ["test3", "14x^4-46x^3-82x^2+138x+120", ['7x+5', 'x-4', '2x^2-6']],
        ["test4", "x^6+3x^3-4", ["x-1", "x^2+x+1", "x^3+4"]],
        ["test5", "2x^14-512x^6", ["x", "x", "x", "x", "x", "x", "x-2", "x+2", "x^2+4", "2x^4+32"]],
        ["test6", "-7x^8-x^5+x^3-x^2-8x-1", ["-7x^8-x^5+x^3-x^2-8x-1"]],
        ["test8", "6x^7+3x^4-9x^3", ["x", "x", "x","x-1", "6x^3+6x^2+6x+9"]],
        ["test9", "7x+7x^3+x^4+x^6", ['x', 'x^2+1', 'x^3+7']],
        ["test10", "x^2-20x+100", ['x-10', 'x-10']],
        ["test11", "x^4-25", ['-x^2+5', '-x^2-5']],
        ["test12", "3x^4-3x^3-36x^2", ['x', 'x', 'x-4','x+3', '3']],
        ["test13", "x^4+x^2-20", ['x-2', 'x+2', 'x^2+5']],
        ["test14", "6x^6+x^3-2", ['-2x^3+1', '-3x^3-2']],
        ["test15", "2x^8-14x^4+20", ['-x^4+2', '-2x^4+10']],
        ["test16", "3x^5-17x^4-28x^3", ['x', 'x', 'x', 'x-7', '3x+4']]
    ])

    def test_factorization(self, name, poly_str, correct_answer): # testy faktoryzacji bez pierwiastków
        poly = self.param(poly_str)
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        self.assertEqual(result, correct_answer)

    def test7(self): # wielokrotny pierwiastek
        poly = self.param("x+4")
        poly = poly * poly * poly * poly
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x+4", "x+4", "x+4", "x+4"]
        self.assertEqual(result, correctAnswer)

class TestDerivative(ParametrizedTestCase): # testy pochodnej

    @parameterized.expand([
        ["test1", "x^3+x^2-10x+8", "3x^2+2x-10"],
        ["test2", "x^4+2x^3-13x^2+4x-30", "4x^3+6x^2-26x+4"],
        ["test3", "x^8+2x^7+x^6", "8x^7+14x^6+6x^5"],
        ["test4", "x-1", "1"],
        ["test5", "2x^3-5x^2+4x+1", "6x^2-10x+4"],
        ["test6", "5", "0"]
    ])

    def test_derivative(self, name, poly_str, correct_answer):
        poly = self.param(poly_str)
        result = str(poly.derivative())
        self.assertEqual(result, correct_answer) 

class TestStr(ParametrizedTestCase): # testy zamiany wielomianu z str na listę i z listy na str

    @parameterized.expand([
        ["test1", "x-2", "x-2"],
        ["test2", "x^10-12457x^4-3x^3+2", "x^10-12457x^4-3x^3+2"],
        ["test3", "-x^99-1", "-x^99-1"],
        ["test4", "0", "0"],
        ["test5", "12345779", "12345779"],
        ["test6", "-88x", "-88x"],
        ["test7", "-x^105", "-x^105"],
        ["test8", "x+x^100-7-x^2+80x^3", "x^100+80x^3-x^2+x-7"]
    ])

    def test_str(self, name, poly_str, correct_answer):
        poly = self.param(poly_str)
        result = str(poly)
        self.assertEqual(result, correct_answer)

    @parameterized.expand([
        ["test1", "x^10+2x^10"],
        ["test2", "x-5x"],
        ["test3", "3+5"]
    ])

    def test_errors(self, name, poly_str): # wielomiany muszą mieć różne potęgi jednomianów
        with self.assertRaises(ValueError):
            self.param(poly_str)

class TestBasicOperations(ParametrizedTestCase):
    def test1(self): # odejmowanie tych samych wielomianów
        poly = self.param("x-2")
        correctAnswer = "0"
        result = str(poly-poly)
        self.assertEqual(result, correctAnswer)

    def test2(self): # testowanie zerowej reszty
        poly = self.param("x^2-1")
        poly2 = self.param("x-1")
        correctAnswer = "0"
        result = str(poly%poly2)
        self.assertEqual(result, correctAnswer)     

    def test3(self): # testowanie zerowego wyniku
        poly = self.param("x^2-1")
        poly2 = self.param("x-1")
        correctAnswer = "0"
        result = str(poly2 // poly)
        self.assertEqual(result, correctAnswer)     

    def test4(self): # dodawanie
        poly = self.param("x^2-1")
        poly2 = self.param("x-1")
        correctAnswer = "x^2+x-2"
        result = str(poly + poly2)
        self.assertEqual(result, correctAnswer)  

    def test5(self): # dodawanie przeciwnych wielomianów
        poly = self.param("x^100-5")
        poly2 = self.param("-x^100+5")
        correctAnswer = "0"
        result = str(poly2 + poly)
        self.assertEqual(result, correctAnswer)  

    def test6(self): # dodawanie wielokrotne
        poly = self.param("x^100-5")
        poly2 = self.param("-x^100+5")
        correctAnswer = "0"
        result = str(poly2 + poly + poly + poly2)
        self.assertEqual(result, correctAnswer)  

    def test7(self): # odejmowanie
        poly = self.param("x^10-x^2")
        poly2 = self.param("-x+1")
        correctAnswer = "x^10-x^2+x-1"
        result = str(poly - poly2)
        self.assertEqual(result, correctAnswer)  

    def test8(self): # mnożenie wielokrotne
        poly = self.param("x^3")
        correctAnswer = "x^15"
        result = str(poly * poly * poly * poly * poly)
        self.assertEqual(result, correctAnswer)  

    def test9(self): # mnożenie 
        poly = self.param("2x+1")
        poly2 = self.param("3x^2-x+4")
        correctAnswer = "6x^3+x^2+7x+4"
        result = str(poly * poly2)
        self.assertEqual(result, correctAnswer)

    def test10(self): # dzielenie
        poly = self.param("4x^2-5x-21")
        poly2 = self.param("x-3")
        correctAnswer = "4x+7"
        result = str(poly // poly2)
        self.assertEqual(result, correctAnswer)  

    def test11(self): # dzielenie
        poly = self.param("5x^5-4x^4+3x^3+x^2-10")
        poly2 = self.param("5x^3+x^2-6x-7")
        correctAnswer = "x^2-x+2"
        result = str(poly // poly2)
        self.assertEqual(result, correctAnswer) 

    def test12(self): # reszta z dzielenia
        poly = self.param("5x^5-4x^4+3x^3+x^2-10")
        poly2 = self.param("5x^3+x^2-6x-7")
        correctAnswer = "5x+4"
        result = str(poly % poly2)
        self.assertEqual(result, correctAnswer) 

    def test13(self): # dzielenie wielokrotne
        poly = self.param("x^3-3x^2+3x-1")
        poly2 = self.param("x-1")
        correctAnswer = "1"
        result = str(poly // poly2 // poly2 // poly2)
        self.assertEqual(result, correctAnswer) 

    def test14(self): # dzielenie wielokrotne
        poly = self.param("x^3-3x^2+3x-1")
        poly2 = self.param("x-1")
        correctAnswer = "1"
        result = str(poly // poly2 // poly2 // poly2)
        self.assertEqual(result, correctAnswer) 

    def test15(self): # reszta z dzielenia jako liczba
        poly = self.param("2x^2+7x-4")
        poly2 = self.param("x-3")
        correctAnswer = "35"
        result = str(poly % poly2)
        self.assertEqual(result, correctAnswer) 

    def test16(self): # dzielenie - w wyniku wielomian z jednomianami o potęgach niebędących w dzielnej
        poly = self.param("3x^4-12x+5")
        poly2 = self.param("x+1")
        correctAnswer = "3x^3-3x^2+3x-15"
        result = str(poly // poly2)
        self.assertEqual(result, correctAnswer) 

    def test17(self): # reszta z dzielenia jako wielomian wyższego rzędu
        poly = self.param("5x^5-4x^4+3x^3-2x^2+x+1")
        poly2 = self.param("x^3+x^2+x+2")
        correctAnswer = "-10x^2+12x-13"
        result = str(poly % poly2)
        self.assertEqual(result, correctAnswer) 

    def test18(self): # odejmowanie wielokrotne
        poly = self.param("x^3+8x^7-10x^10+x-23")
        poly2 = self.param("2x^7-x-45")
        correctAnswer = "-10x^10+2x^7+x^3+4x+112"
        result = str(poly-poly2-poly2-poly2)
        self.assertEqual(result, correctAnswer) 

    def test19(self): # odejmowanie - wynik to liczba, test usuwania nadmiarowych zer
        poly = self.param("x^2-x+1")
        poly2 = self.param("x^2-x-1")
        correctAnswer = "2"
        result = str(poly-poly2)
        self.assertEqual(result, correctAnswer) 

if __name__ == '__main__':
    suite = unittest.TestSuite()
    polyforms = [intpolylib.ListPolynomial, intpolylib.DictPolynomial, intpolylib.PointsPolynomial]
    suite.addTest(ParametrizedTestCase.parametrize(TestFindDivisors))
    for form in polyforms:
        suite.addTest(ParametrizedTestCase.parametrize(TestFactorization, param=form))
        suite.addTest(ParametrizedTestCase.parametrize(TestDerivative, param=form))
        suite.addTest(ParametrizedTestCase.parametrize(TestStr, param=form))
        suite.addTest(ParametrizedTestCase.parametrize(TestBasicOperations, param=form))
    unittest.TextTestRunner(verbosity=2).run(suite)