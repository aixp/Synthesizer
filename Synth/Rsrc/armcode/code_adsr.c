// register int *SB asm ("r3"); // SB
register int *MT asm ("r6"); // MT

#define SN 2048
#define SA 2047

#define DN 10
#define D (1 << DN)

/* ADSR */
#define maxA 256 // 2^n
#define sustainA 103 // 0.4 * maxA

#define DACFreq 16000
#define attack (DACFreq / 100) // 10 ms
#define decay (DACFreq / 10) // 100 ms
#define release (DACFreq / 5) // 200 ms

enum {
	STATE_NONE,
	STATE_ATTACK,
	STATE_DECAY,
	STATE_SUSTAIN,
	STATE_RELEASE
};

struct Key {
	int A;

	int* IDR;
	int pinN;

	int state;
	int counter;
	int pressed;
};


/* ADSR */
__attribute__((always_inline))
static inline void update_key (struct Key *key) {
	// asm volatile ("" : : "r" (0) : "r6");

	int pressed = ((*(key->IDR)) & (1 << key->pinN)) == 0;

	switch (key->state) {
	case STATE_NONE:
		if (pressed && !key->pressed) {
			key->state = STATE_ATTACK;
			key->counter = 0;
		}
		break;
	case STATE_SUSTAIN:
		if (pressed && !key->pressed) {
			key->counter = (sustainA * attack) / maxA;
			key->state = STATE_ATTACK;
		} else if (!pressed) {
			key->state = STATE_RELEASE;
			key->counter = 0;
		}
		break;
	case STATE_RELEASE:
		++key->counter;
		key->A = sustainA - (key->counter * sustainA) / release;
		if (key->A <= 0) {
			key->A = 0;
			key->state = STATE_NONE;
		}
		if (pressed && !key->pressed) {
			key->counter = (key->A * attack) / maxA;
			key->state = STATE_ATTACK;
		}
		break;
	case STATE_DECAY:
		++key->counter;
		key->A = maxA - (key->counter * (maxA - sustainA)) / decay;
		if (key->A <= sustainA) {
			key->A = sustainA;
			key->state = STATE_SUSTAIN;
		}
		if (pressed && !key->pressed) {
			key->counter = (key->A * attack) / maxA;
			key->state = STATE_ATTACK;
		}
		break;
	default: // STATE_ATTACK
		++key->counter;
		key->A = (key->counter * maxA) / attack;
		if (key->A >= maxA) {
			key->A = maxA;
			key->state = STATE_DECAY;;
			key->counter = 0;
		}
	}

	key->pressed = pressed;
}

void UpdateKey (struct Key *key) {
	update_key(key);
}

/* can not use it: R6 usage generated
void UpdateKeys (int n, struct Key **keys) {
	// asm volatile ("" : : "r" (0) : "r6"); // prevent R6 usage

	for (int i = 0; i < n; ++i) {
		update_key(keys[i]);
	}
}
*/
