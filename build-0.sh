#!/bin/sh
#
# Build for some board
#

bbcb2-cli <<DATA
O7ARMv7MP.Compile MicroKernel0/s MicroARMv7M/s MicroARMv7MTraps/s MicroARMv7MMath/s MicroSTM32F4/s MicroSTM32F4Pins/s MicroSTM32F4System/s

O7ARMv7MP.Compile MobxARMv7MSTM32SysTick0/s

O7ARMv7MP.Compile SynthCommon/s SynthBoardSynth0/s SynthTables/s SynthSynth/s SynthSynthesizer

O7ARMv7MLinker.Link STM32F407VG SynthSynthesizer
DATA
