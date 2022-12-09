"""Stepper motor driver class."""

import rp2


@rp2.asm_pio(
    out_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW,
              rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    set_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW,
              rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW),
    out_shiftdir=rp2.PIO.SHIFT_RIGHT
)
def pioprog():
    """Drive stepper motor phases with input nibble at 80 % duty cycle
    for the step period, then interrupt to request next step nibble."""
    irq(rel(0))
    pull()
    out(pins, 4)[26]
    set(pins, 0)[4]


class Stepper():
    """Stepper motor driver class."""
    steptable = (0x5, 0x6, 0xa, 0x9)
    idxmask = len(steptable) - 1

    def __init__(self, pin_base, f_step):
        self.index, self.delta, self.incdec = 0, 0, 0
        self.sm = rp2.StateMachine(
            0, pioprog, freq=32*f_step, out_base=pin_base, set_base=pin_base)
        self.sm.irq(self._irq)
        self.sm.active(True)

    def _irq(self, pio):
        if self.delta != 0:
            self.index = (self.index + self.incdec) & self.idxmask
            self.delta -= self.incdec
        self.sm.put(self.steptable[self.index])

    def move(self, delta):
        self.incdec = 1 if delta > 0 else -1
        self.delta = delta
