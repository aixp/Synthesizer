#! /usr/bin/env python3
#
# Alexander Shiryaev, 2019.11, 2022.09
#
# replace Oberon obj code with objdump outputs code
#

import sys, struct

import dasm2ob, o

def process1 (srcObjFName, dstObjFName, symNames, d):
	symNames = symNames.split(' ')

	fhS = open(srcObjFName, 'rb')
	obj = o.ReadObj(fhS)
	fhS.close()

	if obj is not None:
		# print("obj.code:", obj.code)
		# print("obj.entires: %d" % (len(obj.entries),))
		# for entry in obj.entries:
		# 	print("entry:", entry)
		# print("entry point:", obj.entry)

		pc = 0
		newCode = []

		newCode.append(0xbf00) # nop
		pc = pc + 1
		# newCode.append(0xbf00) # nop
		# pc = pc + 1

		entIdx = len(obj.entries) - len(symNames)
		assert obj.entries[entIdx] in (4, 8)
		for symName in symNames:
			symCode, isPc, aligned = d[symName]
			if isPc and ((pc % 2 == 0) != aligned): # align start of procedure, for "LDR x, [pc, ...]"
				newCode.append(0xbf00) # nop
				pc = pc + 1
				print("aligned: %s: %d" % (symName, pc * 2))
			newEntry = pc * 4
			i = 0
			for name, adr in obj.commands:
				if adr == obj.entries[entIdx]:
					print("fixing command %s -> %s: %s -> %s" % (name.decode('ascii'), symName, adr, newEntry))
					obj.commands[i] = [name, newEntry]
				i = i + 1
			obj.entries[entIdx] = newEntry
			entIdx += 1
			newCode.extend(symCode)
			pc = pc + len(symCode)
		# INIT
		obj.entries[0] = pc * 4
		obj.entry = pc * 4
		symCode = d.get('INIT', [0x4770,]) # bx lr
		newCode.extend(symCode)
		obj.code = newCode

		# print("obj.code:", obj.code)
		# print("obj.entires: %d" % (len(obj.entries),))
		# for entry in obj.entries:
		# 	print("entry:", entry)
		# print("entry point:", obj.entry)

		if obj.fixP != 0:
			print("obj.fixP: %s -> 0" % (obj.fixP,))
			obj.fixP = 0
		if obj.fixD != 0:
			print("obj.fixD: %s -> 0" % (obj.fixD,))
			obj.fixD = 0
		assert obj.fixT == 0

		fhD = open(dstObjFName, 'wb')
		o.WriteObj(fhD, obj)
		fhD.close()

def main ():
	if (len(sys.argv) >= 7) and ((len(sys.argv) - 1) % 3 == 0):
		nInputs = (len(sys.argv) - 1) // 3 - 1
		assert nInputs >= 0
		i = 1
		d = {}
		for j in range(nInputs):
			d0 = dasm2ob.process(sys.argv[i], sys.argv[i+1])
			impSymbols = sys.argv[i+2]
			if impSymbols == '*':
				for k, v in d0.items():
					assert k not in d
					d[k] = v
			else:
				impSymbols = impSymbols.split(' ')
				for k, v in d0.items():
					if k in impSymbols:
						assert k not in d
						d[k] = v
			i = i + 3
		process1(sys.argv[i], sys.argv[i+1], sys.argv[i+2], d)
	else:
		print(f"usage: {sys.argv[0]} {{ inp.objdump inpRepr inpSymbols }} objSrc objDst symbols")
		print("	inpSymbols: * | symbol { ' ' symbol }")
		print("	symbols: symbol { ' ' symbol }")

if __name__ == '__main__':
	main()
