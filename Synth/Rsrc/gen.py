#! /usr/bin/env python3

import sys

key_min = -40
keys = 5 * 12
frequences = keys + 2 * 12
f_max = 24000 / 2

def f (x):
	return 440.0 * (2**(x/12))

freqs = [ f(key) for key in range(key_min, key_min + frequences) ]
# print(freqs)

def gen_o ():
	res = []
	for key in range(key_min, key_min + frequences):
		i = key - key_min
		i_freq = freqs[i]
		if i < keys:
			l = [ f'K[{i}].A' ]
		else:
			l = []
		j = i - 1
		while j >= 0:
			j_freq = freqs[j]
			if abs(i_freq - j_freq * 2) < 1e-6:
				if j < keys:
					l.append(f'K[{j}].A DIV 2')
			elif abs(i_freq - j_freq * 4) < 1e-6:
				if j < keys:
					l.append(f'K[{j}].A DIV 8')
			j -= 1
		if (len(l) == 1) and (' ' not in l[0]):
			ls = l[0]
		else:
			ls = '(' + ' + '.join(l) + ')'
		s = f"{ls} * S[((M[{i}] * t) DIV D) MOD SN]"
		res.append(s)
	return '\n\t\t\t + '.join(res)

def gen_c ():
	res = []
	for key in range(key_min, key_min + frequences):
		i = key - key_min
		i_freq = freqs[i]
		if i < keys:
			l = [ f'K[{i}].A' ]
		else:
			l = []
		j = i - 1
		while j >= 0:
			j_freq = freqs[j]
			if abs(i_freq - j_freq * 2) < 1e-6:
				if j < keys:
					l.append(f'(K[{j}].A >> 1)')
			elif abs(i_freq - j_freq * 4) < 1e-6:
				if j < keys:
					l.append(f'(K[{j}].A >> 3)')
			j -= 1
		if len(l) == 1:
			ls = l[0]
		else:
			ls = '(' + ' + '.join(l) + ')'
		s = f"{ls} * S[((M[{i}] * t) >> DN) & (SN-1)]"
		res.append(s)
	return '\n\t\t + '.join(res)

def main ():
	if (len(sys.argv) == 2) and (sys.argv[1] in ('oberon', 'c')):
		if sys.argv[1] == 'oberon':
			print(gen_o())
		elif sys.argv[1] == 'c':
			print(gen_c())
		else:
			raise RuntimeError()
	else:
		print(f"usage: {sys.argv[0]} lang")
		print("    lang: oberon c")

if __name__ == '__main__':
	main()
