from seg7 import Seg7
import pigpio

pi = pigpio.pi()

seg7 = Seg7(pi, 1, 0x71)

seg7.display("HELO", True, 5)
