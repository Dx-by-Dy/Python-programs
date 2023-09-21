class NotANumber(Exception):

	def __str__(self):
		return "The result is not defined."

class RatNum(object):
	"""docstring for RatNum"""
	numrt : int
	deno : int
	_DesimalPrint = False

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

	def __str__(self):
		if self.numrt == 0: return "0"
		if self.deno == 1: return str(self.numrt)
		if self._DesimalPrint: return str(self.numrt / self.deno)
		return f"{self.numrt}/{self.deno}"

	def __neg__(self):
		self.numrt *= -1
		return self

	def __add__(self, other):
		if isinstance(other, self.__class__):
			return RatNum(self.numrt * other.deno + other.numrt * self.deno, self.deno * other.deno)
		if isinstance(other, int):
			return self + RatNum(other)
		raise TypeError

	def __iadd__(self, other):
		result = self + other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __radd__(self, other):
		if isinstance(other, int):
			return self + RatNum(other)
		raise TypeError

	def __sub__(self, other):
		return self + (-other)

	def __isub__(self, other):
		self += -other
		return self

	def __rsub__(self, other):
		if isinstance(other, int):
			return RatNum(other) - self
		raise TypeError

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			return RatNum(self.numrt * other.numrt, self.deno * other.deno)
		if isinstance(other, int):
			return self * RatNum(other)
		raise TypeError

	def __imul__(self, other):
		result = self * other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __rmul__(self, other):
		if isinstance(other, int):
			return self * RatNum(other)
		raise TypeError

	def __truediv__(self, other):
		return self * RatNum(other.deno, other.numrt)

	def __itruediv__(self, other):
		result = self / other
		self.numrt, self.deno = result.numrt, result.deno
		return self

	def __rtruediv__(self, other):
		if isinstance(other, int):
			return RatNum(other) / self
		raise TypeError

	def setDesimalPrint(self, arg):
		if not isinstance(arg, bool): raise ValueError("The argument must be bool type.")
		self._DesimalPrint = arg

	def _reduction(self):
		if self.numrt == 0: return
		min_num = abs(min(self.numrt, self.deno))
		for i in range(2, int(min_num**0.5 + 1) + 1):
			while self.numrt % i == 0 and self.deno % i == 0:
				self.numrt //= i
				self.deno //= i
			if min_num < i: break
		if self.numrt % min_num == 0 and self.deno % min_num == 0: 
			self.numrt //= min_num
			self.deno //= min_num

RatNum.setDesimalPrint(RatNum, False)

X = RatNum(5, 16)
Y = RatNum(0, 3)
Z = RatNum(1, -6)
X /= Z
print(X)
		