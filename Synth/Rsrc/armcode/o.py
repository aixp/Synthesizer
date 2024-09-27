#! /usr/bin/emv python3
#
# Alexander Shiryaev, 2019.11
#
# Oberon-V5 obj file reader/writer
#

import struct

def ReadString (fh):
	x = fh.read(1)
	res = []
	while x != b'\x00':
		res.append(x)
		x = fh.read(1)
	return b''.join(res)

def ReadInt (fh):
	return struct.unpack("<i", fh.read(4))[0]

def ReadByte (fh):
	return struct.unpack("<B", fh.read(1))[0]

def Read (fh):
	return struct.unpack("<b", fh.read(1))[0]

def WriteString (fh, s):
	fh.write(s + b'\x00')

def WriteInt (fh, x):
	fh.write(struct.pack("<i", x))

def WriteByte (fh, x):
	fh.write(struct.pack("<B", x))

def Write (fh, x):
	fh.write(struct.pack("<b", x))

class Obj:

	pass

def ReadObj (fh):
	obj = Obj()

	obj.name = ReadString(fh)

	obj.key = ReadInt(fh)

	# version
	obj.version = Read(fh)

	obj.size = ReadInt(fh)

	# imports
	obj.imports = []
	name = ReadString(fh)
	while name != b'':
		key = ReadInt(fh)
		obj.imports.append((name, key))
		name = ReadString(fh)

	# type descriptors
	obj.tds = []
	n = ReadInt(fh)
	assert n % 4 == 0
	n = n // 4
	i = 0
	while i < n:
		data = ReadInt(fh)
		obj.tds.append(data)
		i = i + 1

	# data
	obj.data = ReadInt(fh)

	# strings
	n = ReadInt(fh)
	obj.strings = fh.read(n)

	# code
	obj.code = []
	n = ReadInt(fh)
	i = 0
	while i < n:
		data = ReadInt(fh)
		obj.code.append(data)
		i = i + 1

	# commands
	obj.commands = []
	name = ReadString(fh)
	while name != b'':
		adr = ReadInt(fh)
		obj.commands.append([name, adr])
		name = ReadString(fh)

	# entries
	obj.entries = []
	n = ReadInt(fh)
	i = 0
	while i < n:
		adr = ReadInt(fh)
		obj.entries.append(adr)
		i = i + 1

	# pointer refs
	obj.pointerRefs = []
	adr = ReadInt(fh)
	while adr != -1:
		obj.pointerRefs.append(adr)
		adr = ReadInt(fh)

	obj.fixP = ReadInt(fh)

	obj.fixD = ReadInt(fh)

	obj.fixT = ReadInt(fh)

	obj.entry = ReadInt(fh)

	ch = ReadByte(fh)
	if ch != ord('O'):
		print("source object file format error")
		obj = None

	return obj

def WriteObj (fh, obj):
	WriteString(fh, obj.name)

	WriteInt(fh, obj.key)

	Write(fh, obj.version)

	comsize = 4
	for name, adr in obj.commands:
		comsize = comsize + ((len(name) + 4) // 4) * 4 + 4
	size = obj.data + len(obj.tds) * 4 + len(obj.strings) + comsize + (len(obj.code) + len(obj.imports) + len(obj.entries) + len(obj.pointerRefs) + 1)*4
	if obj.size != size:
		print("obj.size: %s -> %s" % (obj.size, size))
	WriteInt(fh, size)

	# imports
	for name, key in obj.imports:
		WriteString(fh, name)
		WriteInt(fh, key)
	WriteString(fh, b'')

	# type descriptors
	WriteInt(fh, len(obj.tds) * 4)
	for td in obj.tds:
		WriteInt(fh, td)

	# data
	WriteInt(fh, obj.data)

	# strings
	WriteInt(fh, len(obj.strings))
	fh.write(obj.strings)

	# code
	WriteInt(fh, len(obj.code))
	for data in obj.code:
		WriteInt(fh, data)

	# commands
	for name, adr in obj.commands:
		WriteString(fh, name)
		WriteInt(fh, adr)
	WriteString(fh, b'')

	# entries
	WriteInt(fh, len(obj.entries))
	for adr in obj.entries:
		WriteInt(fh, adr)

	# pointer refs
	for adr in obj.pointerRefs:
		WriteInt(fh, adr)
	WriteInt(fh, -1)

	WriteInt(fh, obj.fixP)

	WriteInt(fh, obj.fixD)

	WriteInt(fh, obj.fixT)

	WriteInt(fh, obj.entry)

	fh.write(b'O')
