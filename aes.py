from polynom import *
import binascii
class AES_perso:
	def __init__(self,key,rounds):		
		self.subbytes_dict={	'00':'63','01':'7c','02':'77','03':'7b','04':'f2','05':'6b','06':'6f','07':'c5','08':'30','09':'01','0a':'67',
					'0b':'2b','0c':'fe','0d':'d7','0e':'ab','0f':'76','10':'ca','11':'82','12':'c9','13':'7d','14':'fa','15':'59',
					'16':'47','17':'f0','18':'ad','19':'d4','1a':'a2','1b':'af','1c':'9c','1d':'a4','1e':'72','1f':'c0','20':'b7',
					'21':'fd','22':'93','23':'26','24':'36','25':'3f','26':'f7','27':'cc','28':'34','29':'a5','2a':'e5','2b':'f1',
					'2c':'71','2d':'d8','2e':'31','2f':'15','30':'04','31':'c7','32':'23','33':'c3','34':'18','35':'96','36':'05',
					'37':'9a','38':'07','39':'12','3a':'80','3b':'e2','3c':'eb','3d':'27','3e':'b2','3f':'75','40':'09','41':'83',
					'42':'2c','43':'1a','44':'1b','45':'6e','46':'5a','47':'a0','48':'52','49':'3b','4a':'d6','4b':'b3','4c':'29',
					'4d':'e3','4e':'2f','4f':'84','50':'53','51':'d1','52':'00','53':'ed','54':'20','55':'fc','56':'b1','57':'5b',
					'58':'6a','59':'cb','5a':'be','5b':'39','5c':'4a','5d':'4c','5e':'58','5f':'cf','60':'d0','61':'ef','62':'aa',
					'63':'fb','64':'43','65':'4d','66':'33','67':'85','68':'45','69':'f9','6a':'02','6b':'7f','6c':'50','6d':'3c',
					'6e':'9f','6f':'a8','70':'51','71':'a3','72':'40','73':'8f','74':'92','75':'9d','76':'38','77':'f5','78':'bc',
					'79':'b6','7a':'da','7b':'21','7c':'10','7d':'ff','7e':'f3','7f':'d2','80':'cd','81':'0c','82':'13','83':'ec',
					'84':'5f','85':'97','86':'44','87':'17','88':'c4','89':'a7','8a':'7e','8b':'3d','8c':'64','8d':'5d','8e':'19',
					'8f':'73','90':'60','91':'81','92':'4f','93':'dc','94':'22','95':'2a','96':'90','97':'88','98':'46','99':'ee',
					'9a':'b8','9b':'14','9c':'de','9d':'5e','9e':'0b','9f':'db','a0':'e0','a1':'32','a2':'3a','a3':'0a','a4':'49',
					'a5':'06','a6':'24','a7':'5c','a8':'c2','a9':'d3','aa':'ac','ab':'62','ac':'91','ad':'95','ae':'e4','af':'79',
					'b0':'e7','b1':'c8','b2':'37','b3':'6d','b4':'8d','b5':'d5','b6':'4e','b7':'a9','b8':'6c','b9':'56','ba':'f4',
					'bb':'ea','bc':'65','bd':'7a','be':'ae','bf':'08','c0':'ba','c1':'78','c2':'25','c3':'2e','c4':'1c','c5':'a6',
					'c6':'b4','c7':'c6','c8':'e8','c9':'dd','ca':'74','cb':'1f','cc':'4b','cd':'bd','ce':'8b','cf':'8a','d0':'70',
					'd1':'3e','d2':'b5','d3':'66','d4':'48','d5':'03','d6':'f6','d7':'0e','d8':'61','d9':'35','da':'57','db':'b9',
					'dc':'86','dd':'c1','de':'1d','df':'9e','e0':'e1','e1':'f8','e2':'98','e3':'11','e4':'69','e5':'d9','e6':'8e',
					'e7':'94','e8':'9b','e9':'1e','ea':'87','eb':'e9','ec':'ce','ed':'55','ee':'28','ef':'df','f0':'8c','f1':'a1',
					'f2':'89','f3':'0d','f4':'bf','f5':'e6','f6':'42','f7':'68','f8':'41','f9':'99','fa':'2d','fb':'0f','fc':'b0',
					'fd':'54','fe':'bb','ff':'16'}	
		self.Rcon = False
		self.message = False
		self.rounds = rounds
		self.keys = [self.ArrayToMat([key[2*i:2*(i+1)] for i in range(len(key)//2)],4)]
		self.primaryKey = self.keys

	def digest(self,line):
		if len(line) % 32 == 0 and len(line) > 0:
			res = ""
			for block in [line[32*i:32*(i+1)] for i in range(len(line)//32)]:
				self.Rcon = False
				self.keys = self.primaryKey
				data = self.TransposeMat(self.ArrayToMat([block[2*i:2*(i+1)] for i in range(len(block)//2)],4))
				for i in range(self.rounds):
					data = self.AddRoundKey(data)
					data = self.SubBytes(data)
					data = self.ShiftRows(data)
					data = self.MixColumns(data)
				data = self.AddRoundKey(data)
				data = self.SubBytes(data)
				data = self.ShiftRows(data)
				data = self.AddRoundKey(data)
				data = "".join(["".join(i) for i in self.TransposeMat(data)])
				res += data		
			return(res)
		else:	
			print("La longueur doit être un multiple de 32")
			return False

	def ArrayToMat(self,line,w):
		if len(line)%w != 0:
			return False
		result = []
		tmp = []
		for i in line:
			tmp += [i]
			if len(tmp) == w:
				result += [tmp]
				tmp = []
		return result

	def MatToArray(self,mat):
		result = []
		for i in mat:
			for j in i:
				result += [j]
		return result

	def TransposeMat(self,mat):
		result = []
		tmp = []
		for i in range(len(mat[0])):
			for j in range(len(mat)):
				tmp += [mat[j][i]]
			result += [tmp]
			tmp = []
		return result

	def shift(self,line,i):
		return line[i:] + line[:i]
	
	def mix(self,line):
		if len(line) != 4:
			return False
		result = []
		mat = [['02','03','01','01'],['01','02','03','01'],['01','01','02','03'],['03','01','01','02']]
		for i in range(4):
			tmp = polynom('0')
			for j in range(4):
				tmp += polynom(bin(int(mat[i][j]))[2:])*polynom(bin(int(line[j],16))[2:])
			result += ["0"*((2-len(tmp()[2]))%2) + tmp()[2]]
		return result 

	def ShiftRows(self,mat):
		result = []
		for i in range(len(mat)):
			result += [self.shift(mat[i],i)]
		return result
	
	def SubBytes(self,mat):		
		w = len(mat[0])
		result = [self.subbytes_dict[i] for i in self.MatToArray(mat)]
		return self.ArrayToMat(result,w)

	def MixColumns(self,mat):
		tmp = []
		for i in self.TransposeMat(mat):	
			tmp += self.mix(i)
		return self.TransposeMat(self.ArrayToMat(tmp,4))

	def AddRoundKey(self,mat):
		result = mat[:]
		key = self.TransposeMat(self.keys[0])
		for i in range(len(mat)):
			for j in range(len(mat[i])):
				tmp = (polynom(bin(int(result[i][j],16))[2:]) + polynom(bin(int(key[i][j],16))[2:]))()[2]
				result[i][j] = "0"*((2-len(tmp))%2) + tmp
		self.keys = self.ExpandKey()
		self.keys = self.keys[1:]
		return mat	

	def ExpandKey(self):
		result = self.keys[0]
		temp = result[-1]			
		for i in range(4):
			if i%4 == 0:
				temp = self.ShiftRows(['',temp])[1]	
				temp = self.SubBytes([temp])[0]
				if self.Rcon == False:
					self.Rcon = polynom('1')
				else:
					self.Rcon *= polynom('10')
				if self.Rcon()[1] >= 0x80:
					self.Rcon += polynom(bin(0x11b)[2:])
				tmp = int(self.Rcon()[2],16)^int(temp[0],16)
				temp = [hex(tmp)[2:]]+temp[1:]
			tmp1 = []
			for j in range(4):
				tmp2 = hex(int(temp[j],16)^int(result[i][j],16))[2:]
				tmp1 += ["0"*((2-len(tmp2))%2) + tmp2]
			result += [tmp1]
			temp = tmp1
		keys = []
		for i in range(len(result)//4):
			keys += [result[4*i:4*(i+1)]]
		return keys

