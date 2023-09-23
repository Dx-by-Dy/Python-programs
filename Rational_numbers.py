class NotANumber(Exception):

	def __str__(self):
		return "The result is not defined."

class RatNum(object):
	"""docstring for RatNum"""
	numrt : int
	deno : int
	_DesimalPrint = False

	#def __call__(self, numrt : int, deno : int = 1):
	#	pass

	def __init__(self, numrt : int, deno : int = 1):
		if not (isinstance(numrt, int) and isinstance(deno, int)): raise TypeError("The numerator and denominator must be int type.")
		if numrt == 0 and deno == 0: raise NotANumber
		if deno == 0: raise ZeroDivisionError("The denominator must be non-zero int number.")

		if deno < 0:
			self.numrt = -numrt
			self.deno = -deno
		else:
			self.numrt = numrt
			self.deno = deno

		self._reduction()

	def __repr__(self):
		return str(self)

	def __str__(self):
		if self.numrt == 0: return "0"
		if self.deno == 1: return str(self.numrt)
		if self._DesimalPrint: return str(self.inDes())
		return f"{self.numrt}/{self.deno}"

	def __neg__(self):
		self.numrt *= -1
		return self

	def __pos__(self):
		return self

	def __add__(self, other):
		if isinstance(other, self.__class__):
			return RatNum(self.numrt * other.deno + other.numrt * self.deno, self.deno * other.deno)
		if isinstance(other, int):
			return self + RatNum(other)
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __iadd__(self, other):
		result = self + other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __radd__(self, other):
		if isinstance(other, int):
			return self + RatNum(other)
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __sub__(self, other):
		return self + (-other)

	def __isub__(self, other):
		self += -other
		return self

	def __rsub__(self, other):
		if isinstance(other, int):
			return RatNum(other) - self
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			return RatNum(self.numrt * other.numrt, self.deno * other.deno)
		if isinstance(other, int):
			return self * RatNum(other)
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __imul__(self, other):
		result = self * other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __rmul__(self, other):
		if isinstance(other, int):
			return self * RatNum(other)
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __truediv__(self, other):
		if isinstance(other, self.__class__):
			return self * RatNum(other.deno, other.numrt)
		if isinstance(other, int):
			return self * RatNum(1, other)
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __itruediv__(self, other):
		result = self / other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __rtruediv__(self, other):
		if isinstance(other, int):
			return RatNum(other) / self
		raise TypeError("The addition, substraction, multiplication, division can be only with RatNum class or int numbers.")

	def __pow__(self, other):
		if isinstance(other, int):
			return RatNum(self.numrt ** other, self.deno ** other)
		raise TypeError("The exponentation can be only with int numbers.")

	def __ipow__(self, other):
		result = self ** other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __rpow__(self, other):
		if isinstance(other, (int, float)):
			return other ** self.inDes()
		raise TypeError("The exponentation can be only with int and float numbers.")

	def __abs__(self):
		self.numrt = abs(self.numrt)
		return self

	def __invert__(self):
		self.numrt, self.deno = self.deno, self.numrt
		return self

	def __int__(self):
		return int(self.inDes())

	def __float__(self):
		return self.inDes()

	def __round__(self):
		return round(self.inDes())

	def __lt__(self, other):
		if isinstance(other, self.__class__):
			return self.inDes() < other.inDes()
		if isinstance(other, int):
			return self < RatNum(other)
		raise TypeError("The comparison can be only with RatNum class or int numbers.")

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (self.numrt == other.numrt and self.deno == other.deno) or (self.numrt == 0 and other.numrt == 0)
		if isinstance(other, int):
			return self == RatNum(other)
		raise TypeError("The comparison can be only with RatNum class or int numbers.")

	def __le__(self, other):
		return (self < other or self == other)

	def __ne__(self, other):
		return not (self == other)

	def __gt__(self, other):
		if isinstance(other, self.__class__):
			return self.inDes() > other.inDes()
		if isinstance(other, int):
			return self > RatNum(other)
		raise TypeError("The comparison can be only with RatNum class or int numbers.")

	def __ge__(self, other):
		return (self > other or self == other)

	def inDes(self):
		return self.numrt / self.deno

	def setDesimalPrint(self, arg):
		if not isinstance(arg, bool): raise TypeError("The argument must be bool type.")
		self._DesimalPrint = arg

	def _reduction(self):
		if self.numrt == 0: return

		gcd_numrt = abs(self.numrt)
		gcd_deno = self.deno
		while gcd_numrt > 0 and gcd_deno > 0:
			if gcd_deno > gcd_numrt: gcd_deno %= gcd_numrt
			else: gcd_numrt %= gcd_deno
		self.numrt //= max(gcd_numrt, gcd_deno)
		self.deno //= max(gcd_numrt, gcd_deno)