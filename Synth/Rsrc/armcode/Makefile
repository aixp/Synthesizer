# this is GNU Makefile, use gmake command in *BSD environment

# MFLOAT_ABI=hard
MFLOAT_ABI=softfp

AS ?= arm-none-eabi-as
ASMOPTS = -mcpu=cortex-m4 -march=armv7e-m -mfpu=fpv4-sp-d16 -mfloat-abi=${MFLOAT_ABI} -mthumb
OBJDUMP = arm-none-eabi-objdump

# NOTE: -falign-functions=n required for "[V]LDR x, [pc, imm]" instructions, offsets should be multiple of 4

GCC ?= arm-none-eabi-gcc
GCC_CFLAGS = -march=armv7e-m -mcpu=cortex-m4 -mtune=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=${MFLOAT_ABI} -fPIC -fno-builtin -ffreestanding -fno-math-errno -fomit-frame-pointer -ffast-math -fsingle-precision-constant -falign-functions=4 -ffixed-r6

CLANG = clang
CLANG_CFLAGS_BASE = -target thumbv7me-arm-none-eabi -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=${MFLOAT_ABI} -fPIC -fno-builtin -ffreestanding -fno-math-errno -fomit-frame-pointer -ffast-math -ffp-contract=fast -falign-functions=4
CLANG_CFLAGS_M4 = -mcpu=cortex-m4 -mtune=cortex-m4 ${CLANG_CFLAGS_BASE}
CLANG_CFLAGS_M7 = -mcpu=cortex-m7 -mtune=cortex-m7 ${CLANG_CFLAGS_BASE}
# -fsingle-precision-constant

PY3 = python3

all: Synth0.a7m.new

code_asm.o: code_asm.s
	${AS} ${ASMOPTS} code_asm.s -o code_asm.o

%_gcc_Os.o: %.c
	${GCC} ${GCC_CFLAGS} -Os -c $< -o $@

%_gcc_O3.o: %.c
	${GCC} ${GCC_CFLAGS} -O3 -c $< -o $@

%_clang_Os.o: %.c
	${CLANG} ${CLANG_CFLAGS_M7} -Os -c $< -o $@

%_clang_O3.o: %.c
	${CLANG} ${CLANG_CFLAGS_M7} -O3 -c $< -o $@

%.objdump: %.o
	${OBJDUMP} -d $< > $@

%.txt: %.objdump
	${PY3} dasm2ob.py $< $@

Synth0.a7m.new: Synth0.a7m code_adsr_clang_Os.objdump code_adsr_clang_Os.txt code_gen_gcc_O3.objdump code_gen_gcc_O3.txt
	${PY3} replaceCode.py \
		code_adsr_clang_Os.objdump code_adsr_clang_Os.txt "UpdateKey" \
		code_gen_gcc_O3.objdump code_gen_gcc_O3.txt "Gen" \
		Synth0.a7m Synth0.a7m.new \
		"UpdateKey Gen"

clean:
	rm -f *.o *.objdump *.txt code_gcc*.s code_clang*.s *.a7m.new
