class polynom:
	def __init__(self,pol):
		self.pol = self.reduce(pol)
		self.degre = len(pol)-1

	def __call__(self):
		return (self.pol, int(self.pol,2),hex(int(self.pol,2))[2:], self.degre)

	def __add__(self,pol2):
		return (self.badd(pol2()[0]).beucdiv(polynom("100011011")))[1]
	
	def __mul__(self,pol2):
		return (self.bmul(pol2()[0]).beucdiv(polynom("100011011")))[1]

	def new(self,pol):
		self.pol = (self.reduce(pol).beucdiv(polynom("100011011")))[1]
		self.degre = len(pol)-1

	def reduce(self,poly):
		return bin(int("".join([str(int(i)%2) for i in poly]),2))[2:]
		
	def eval(self,val):
		res = 0
		cur = 1
		for i in range(len(self.pol)-1,-1,-1):
			res += int(self.pol[i]) * cur
			cur *= val
		return res

	def badd(self,pol2):
		return polynom(bin(int(self.pol,2)^int(pol2,2))[2:])

	def bmul(self,pol2):
		tmp = {}	
		for i in range(1,len(self.pol)+1):
			for j in range(1,len(pol2)+1):
				if int(self.pol[-i])&int(pol2[-j]):
					if str(i+j-2) in tmp:
						tmp[str(i+j-2)] += 1
					else:
						tmp[str(i+j-2)] = 1
		return polynom(bin(sum([2**int(i) for i in tmp if tmp[i] % 2 == 1]))[2:])
	
	def beucdiv(self,pol2):
		pol1 = self
		div = []
		while pol1()[1] > pol2()[1]:		
			div += [pol1.degre-pol2.degre]
			pol1 += (pol2.bmul("1"+"0"*(pol1.degre-pol2.degre)))
		return polynom(bin(sum([2**int(i) for i in div]))[2:]),polynom(pol1()[0])				

