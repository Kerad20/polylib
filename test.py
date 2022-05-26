import unittest
import intpolylib

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

    def test1(self): # sprawdzanie wybranej dużej liczby wiekszej od 2^16
        data = 1048576
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)
    
    def test2(self): # sprawdzanie działania dla liczby 2^32
        data = 4294967296
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 
        2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)

    def test3(self): # duża liczba zawierająca dzielnik będący liczbą pierwszą większą niż 2^16
        data = 5247145
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 5, 1049429, 5247145]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)

    def test4(self): # liczba mniejsza niż 2^16
        data = 25000
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500, 625, 1000, 1250, 2500, 3125, 5000, 6250, 12500, 25000]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)
    
    def test5(self): # liczba > 2^16 zawierająca małe dzielniki jak i duże dzielniki pierwsze
        data = 20988580
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 2, 4, 5, 10, 20, 1049429, 2098858, 4197716, 5247145, 10494290, 20988580]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)

    def test6(self): # faktoryzacja liczby pierwszej > 2^16
        data = 9064457
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 9064457]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)

    def test7(self): # faktoryzacja 1
        data = 1
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
        self.assertEqual(result, correctAnswer)

    def test8(self): # faktoryzacja 0
        data = 0
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = []
        self.assertEqual(result, correctAnswer)

    def test9(self): # liczba z dużą ilością dzielników
        data = 2183462912
        base = intpolylib.BasePolynomial()
        result = base.findDivisors(data)
        correctAnswer = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 33317, 65536, 66634, 133268, 
        266536, 533072, 1066144, 2132288, 4264576, 8529152, 17058304, 34116608, 68233216, 136466432, 272932864, 545865728, 1091731456, 2183462912]
        minus = [-i for i in correctAnswer]
        correctAnswer = sorted(correctAnswer + minus)
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
    
    def test1(self): # testy faktoryzacji bez pierwiastków
        poly = self.param("x^5-x^4-2x^3-8x^2+6x-1")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x^2-3x+1", "x^3+2x^2+3x-1"]
        self.assertEqual(result, correctAnswer)

    def test2(self): # testy faktoryzacji z pierwiastkami oraz jednyn nierozkładalnym czynnikiem
        poly = self.param("x^4+x^2-20")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x-2", "x+2", "x^2+5"]
        self.assertEqual(result, correctAnswer)

    def test3(self): # testy faktoryzacji z dużą nierozkładalną częścią w dziedzinie liczb całkowitych i jednym pierwiastkiem
        poly = self.param("14x^4-46x^3-82x^2+138x+120")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['7x+5', 'x-4', '2x^2-6']
        self.assertEqual(result, correctAnswer)

    def test4(self): # faktoryzacja wielomianu wyższego rzędu, zawierjącego pierwiastek jak i części nierozkładalne
        poly = self.param("x^6+3x^3-4")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x-1", "x^2+x+1", "x^3+4"]
        self.assertEqual(result, correctAnswer)

    def test5(self): # faktoryzacja wielomianu wysokiego rzędu z wyrazem wolnym 0
        poly = self.param("2x^14-512x^6")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x", "x", "x", "x", "x", "x", "x-2", "x+2", "x^2+4", "2x^4+32"]
        self.assertEqual(result, correctAnswer)

    def test6(self): # wielomian nierozkładalny
        poly = self.param("-7x^8-x^5+x^3-x^2-8x-1")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["-7x^8-x^5+x^3-x^2-8x-1"]
        self.assertEqual(result, correctAnswer)

    def test7(self): # wielokrotny pierwiastek
        poly = self.param("x+4")
        poly = poly * poly * poly * poly
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x+4", "x+4", "x+4", "x+4"]
        self.assertEqual(result, correctAnswer)

    def test8(self): # pierwiastek zero wielokrotny i jeden zwykły pierwiastek
        poly = self.param("6x^7+3x^4-9x^3")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ["x", "x", "x","x-1", "6x^3+6x^2+6x+9"]
        self.assertEqual(result, correctAnswer)

    def test9(self):
        poly = self.param("7x+7x^3+x^4+x^6")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['x', 'x^2+1', 'x^3+7']
        self.assertEqual(result, correctAnswer)

    def test10(self): # pierwiastek wielokrotny
        poly = self.param("x^2-20x+100")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['x-10', 'x-10']
        self.assertEqual(result, correctAnswer)

    def test11(self):
        poly = self.param("x^4-25")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['-x^2+5', '-x^2-5']
        self.assertEqual(result, correctAnswer)

    def test12(self):
        poly = self.param("3x^4-3x^3-36x^2")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['x', 'x', 'x-4','x+3', '3']
        self.assertEqual(result, correctAnswer)

    def test13(self):
        poly = self.param("x^4+x^2-20")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['x-2', 'x+2', 'x^2+5']
        self.assertEqual(result, correctAnswer)

    def test14(self):
        poly = self.param("6x^6+x^3-2")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['-2x^3+1', '-3x^3-2']
        self.assertEqual(result, correctAnswer)     

    def test15(self):
        poly = self.param("2x^8-14x^4+20")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['-x^4+2', '-2x^4+10']
        self.assertEqual(result, correctAnswer)     

    def test16(self):
        poly = self.param("3x^5-17x^4-28x^3")
        factors = poly.factorization()
        result = [str(factor) for factor in factors]
        correctAnswer = ['x', 'x', 'x', 'x-7', '3x+4']
        self.assertEqual(result, correctAnswer)        
    

class TestDerivative(ParametrizedTestCase): # testy pochodnej

    def test1(self):
        poly = self.param("x^3+x^2-10x+8")
        result = str(poly.derivative())
        correctAnswer = "3x^2+2x-10"
        self.assertEqual(result, correctAnswer)
    
    def test2(self):
        poly = self.param("x^4+2x^3-13x^2+4x-30")
        result = str(poly.derivative())
        correctAnswer = "4x^3+6x^2-26x+4"
        self.assertEqual(result, correctAnswer)

    def test3(self):
        poly = self.param("x^8+2x^7+x^6")
        result = str(poly.derivative())
        correctAnswer = "8x^7+14x^6+6x^5"
        self.assertEqual(result, correctAnswer)

    def test4(self): # pochodna małego wyrażenia
        poly = self.param("x-1")
        result = str(poly.derivative())
        correctAnswer = "1"
        self.assertEqual(result, correctAnswer)

    def test5(self):
        poly = self.param("2x^3-5x^2+4x+1")
        result = str(poly.derivative())
        correctAnswer = "6x^2-10x+4"
        self.assertEqual(result, correctAnswer)   

    def test6(self): # pochodna stałej
        poly = self.param("5")
        result = str(poly.derivative())
        correctAnswer = "0"
        self.assertEqual(result, correctAnswer)   

class TestStr(ParametrizedTestCase): # testy zamiany wielomianu z str na listę i z listy na str
    def test1(self):
        poly = self.param("x-2")
        result = str(poly)
        correctAnswer = "x-2"
        self.assertEqual(result, correctAnswer)

    def test2(self):
        poly = self.param("x^10-12457x^4-3x^3+2")
        result = str(poly)
        correctAnswer = "x^10-12457x^4-3x^3+2"
        self.assertEqual(result, correctAnswer)

    def test3(self):
        poly = self.param("-x^99-1")
        result = str(poly)
        correctAnswer = "-x^99-1"
        self.assertEqual(result, correctAnswer)

    # def test4(self):
    #     poly = self.param("-500000x^1000+345x^500-45x^45+12x^10-76x^8+x^3-1")
    #     result = str(poly)
    #     correctAnswer = "-500000x^1000+345x^500-45x^45+12x^10-76x^8+x^3-1"
    #     self.assertEqual(result, correctAnswer)     

    def test5(self):
        poly = self.param("0")
        result = str(poly)
        correctAnswer = "0"
        self.assertEqual(result, correctAnswer)    

    def test6(self):
        poly = self.param("12345779")
        result = str(poly)
        correctAnswer = "12345779"
        self.assertEqual(result, correctAnswer)   

    def test7(self):
        poly = self.param("-88x")
        result = str(poly)
        correctAnswer = "-88x"
        self.assertEqual(result, correctAnswer)   

    def test8(self):
        poly = self.param("-88x")
        result = str(poly)
        correctAnswer = "-88x"
        self.assertEqual(result, correctAnswer)  

    def test9(self):
        poly = self.param("-x^105")
        result = str(poly)
        correctAnswer = "-x^105"
        self.assertEqual(result, correctAnswer) 

    def test10(self): # jednomiany w różnej kolejności
        poly = self.param("x+x^100-7-x^2+80x^3")
        result = str(poly)
        correctAnswer = "x^100+80x^3-x^2+x-7" # na wyjściu posortowane jednomiany
        self.assertEqual(result, correctAnswer) 

    def test11(self): # wielomiany muszą mieć różne potęgi jednomianów
        with self.assertRaises(ValueError):
            self.param("x^10+2x^10")

    def test12(self): # wielomiany muszą mieć różne potęgi jednomianów
        with self.assertRaises(ValueError):
            self.param("x-5x")

    def test13(self): # wielomiany muszą mieć różne potęgi jednomianów
        with self.assertRaises(ValueError):
            self.param("3+5")

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