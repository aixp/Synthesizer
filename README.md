# Synthesizer

This repository contains the source code for a synthesizer (currently resembling an electronic piano) designed for the STM32F4-family microcontroller,
mostly written in the [Oberon](https://en.wikipedia.org/wiki/Oberon_(programming_language)) programming language.

## Features

- **Key Detection**: Supports detection of individual synthesizer keys

- **ADSR Envelope**: Features an Attack-Decay-Sustain-Release ([ADSR](https://en.wikipedia.org/wiki/Envelope_(music))) envelope

- **Audio Synthesis**: Implements audio wave generation (sine wave, with harmonics) for producing sounds

## Getting Started

### Prerequisites

To build and run this firmware, you'll need the following:

- Some keyboard

- STM32F4 microcontroller

- [O7](https://github.com/aixp/O7) compiler

- [Micro](https://github.com/aixp/O7/blob/master/BlackBox/Micro) framework

- A tool to upload firmware to microcontroller

### Installation

1. Install the [BlackBox Component Builder](https://github.com/bbcb/bbcp)

2. Clone the [O7](https://github.com/aixp/O7) repository:

```shell
git clone https://github.com/aixp/O7.git
```

3. Build the [O7](https://github.com/aixp/O7) compiler

```shell
cd O7/BlackBox
make
```

4. Clone this repository:

```shell
git clone https://github.com/aixp/Synthesizer.git
```

5. Adopt for your hardware

6. Build the firmware

```shell
cd Synthesizer
make
```

7. Upload the compiled firmware onto the microcontroller

## Usage

Once the firmware is uploaded to the microcontroller, the synthesizer will be ready for use.
Connect microcontroller [DAC](https://en.wikipedia.org/wiki/Digital-to-analog_converter) output to an audio line input (through a 1–10 µF capacitor), turn on the power, press the keys, and you will hear sounds.

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

## License

This project is licensed under the GPL-3.0 License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to [iadenisov@](https://github.com/iadenisov) for their continued support and ideas.
