#! /usr/bin/env python3
#
# Alexander Shiryaev, 2019.11, 2022.09
#
# objdump output to Oberon code converter (ARM Thumb)
#

import sys

def process (srcFName, dstFName):
	fh = open(srcFName, 'rb')
	src = fh.read()
	fh.close()
	src = src.decode('ascii')[:-1].split('\n\n')
	dst = []
	cLenTotal = 0
	d = {}
	for x in src:
		if x.startswith('0'):
			y = x.split('\n')
			symName = y[0].split('<')[1].split('>')[0]
			z0 = []
			zc = []
			yc = []
			z = []
			z.append("	%s := SYSTEM.VAL(Proc," % (symName,))
			cLen = 0
			isPc = False
			aligned = None
			for l in y[1:]:
				offset, s = l.split(':	')
				offset = int(offset.lstrip(), 16)
				assert offset % 2 == 0
				if aligned is None:
					aligned = offset % 4 == 0
				code, asm = s.split(' 	')
				asm = asm.replace('\t', ' ')
				asm = asm.replace('[ip]', '[r12]')
				if '[pc,' in asm:
					isPc = True
				code = code.strip()
				codeWords = code.split(' ')
				c = []
				for word in codeWords:
					if len(word) == 4:
						x1 = word[0:2]
						x0 = word[2:4]
						c.append(x0.upper())
						c.append(x1.upper())
						yc.append(int(x1 + x0, 16))
					elif len(word) == 8:
						x3 = word[0:2]
						x2 = word[2:4]
						x1 = word[4:6]
						x0 = word[6:8]
						c.append(x0.upper())
						c.append(x1.upper())
						c.append(x2.upper())
						c.append(x3.upper())
						yc.append(int(x1 + x0, 16))
						yc.append(int(x3 + x2, 16))
					else:
						assert False
				cLen = cLen + len(c)
				c = ' '.join(c)
				# z.append('		%s	(* %s *)' % (c, asm))
				z0.append("			%s	%s" % (code, asm))
				zc.append('			%s' % (c,))
			if isPc and (not aligned):
				z0.insert(0, "			bf00	nop (align)")
				zc.insert(0, "			00 BF")
			z.append("		(*")
			z.append('\n'.join(z0))
			z.append("		*)")
			z.append("		SYSTEM.ADR($")
			z.append("%s$) + 1 (* Thumb *)); (* %s B *)" % ('\n'.join(zc), cLen,))
			cLenTotal = cLenTotal + cLen
			dst.append('\n'.join(z))
			assert symName not in d
			d[symName] = [yc, isPc, aligned]
			# print("%s: %s: %d B" % (srcFName, symName, cLen))
	if dstFName is not None:
		dst = '\n\n'.join(dst) + '\n'
		dst = dst.encode('ascii')
		fh = open(dstFName, 'wb')
		fh.write(dst)
		fh.close()
	print("%s: total code len: %s" % (srcFName, cLenTotal))
	return d

def main ():
	if len(sys.argv) == 3:
		d = process(sys.argv[1], sys.argv[2])
	else:
		print(f"usage: {sys.argv[0]} src dst")

if __name__ == '__main__':
	main()
