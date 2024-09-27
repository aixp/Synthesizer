.PHONY: all clean

all: Synthesizer-0.bin Synthesizer-Nucleo-F446RE.bin

# for some board
Synthesizer-0.bin:
	rm -f Synth/Files/Synthesizer.bin Synth/Files/Synthesizer.hex
	./build-0.sh
	cp Synth/Files/Synthesizer.bin Synthesizer-0.bin

# for Nucleo-F446RE board
Synthesizer-Nucleo-F446RE.bin:
	rm -f Synth/Files/Synthesizer.bin Synth/Files/Synthesizer.hex
	./build-Nucleo-F446RE.sh
	cp Synth/Files/Synthesizer.bin Synthesizer-Nucleo-F446RE.bin

clean:
	rm -f Synth/Files/*.bin Synth/Files/*.hex \
		Synth/Files/BoardSynth.smb Synth/Files/Common.smb Synth/Files/Synth.smb Synth/Files/Synthesizer.smb Synth/Files/Tables.smb \
		Synth/Files/BoardSynth.a7m Synth/Files/Common.a7m Synth/Files/Synth.a7m Synth/Files/Synthesizer.a7m Synth/Files/Tables.a7m \
		Synthesizer-0.bin Synthesizer-Nucleo-F446RE.bin
