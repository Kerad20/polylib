# intpolylib
Library wchich contains operations on polynomials with integer coefficients. It includes basic operations like addition, subtraction, multiplication, division with the rest, derivative, but also factorization and finding rational roots. There are 3 represantations of polynomials: list of coefficients, dictionary of non-zero coefficients and list of points (ListPolynomial, DictPolynomial, PointsPolynomial).
# Installing
```
pip install intpolylib
```
# Usage
#### Addition
```python
>>> from intpolylib import ListPolynomial
>>> poly = ListPolynomial(x^2+x+1)
>>> poly2 = ListPolynomial(x+1)
>>> print(poly+poly2)
x^2+2x+2

```
