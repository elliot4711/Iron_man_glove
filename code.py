import time
import math
import board
import busio
import adafruit_lis3dh
import digitalio
import neopixel

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

pixel_pin = board.D5
num_pixels = 9
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=True, pixel_order=ORDER)


# Enable the speaker
#spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
#spkrenable.direction = digitalio.Direction.OUTPUT
#spkrenable.value = True

# Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
# otherwise check I2C pins.
i2c = board.I2C()
int1 = digitalio.DigitalInOut(board.D7)  # Set this to the correct pin for the interrupt
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)


# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_16_G
lis3dh.set_tap(2, 20)

wave_file = open("Iron-man-Repulsor-Sound-effect-littlelouder.wav", "rb")
wave = WaveFile(wave_file)
audio = AudioOut(board.A0)
wave_file1 = open("Iron-man-Repulsor-Sound-effect-glow-long.wav", "rb")
wave1 = WaveFile(wave_file1)

OFF = (0, 0, 0)
effects_mode = True

while True:
    time.sleep(0.05)
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs.
    x, y, z = [
        value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]
    print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
    # Small delay to keep things responsive but give time for interrupt processing.

    if lis3dh.tapped:
        print("Tapped")
        if effects_mode == True:
            effects_mode = False
            for i in range(200):
                r = i - 25
                if r < 0:
                    r = 0
                g = i - 25
                if g < 0:
                    g = 0
                b = i
                COLOR = (r, g, b)
                pixels.fill(COLOR)
                pixels.show()
                time.sleep(0.003)

            COLOR = (175, 175, 200)
            pixels.fill(COLOR)
            pixels.show()

        else:
            effects_mode = True
            for j in range(200, 0, -1):
                r = j - 25
                if r < 0:
                    r = 0
                g = j - 25
                if g < 0:
                    g = 0
                b = j
                COLOR = (r, g, b)
                pixels.fill(COLOR)
                pixels.show()
                time.sleep(0.004)

            pixels.fill(OFF)
            pixels.show()

    if effects_mode:
        if (y > 0 and y < 0.35):
            if (x < 0 and x > -0.6):
                if (z < -0.6 and z > -1):
                    time.sleep(1)
                    audio.play(wave1)
                    while audio.playing:
                        for i in range(200):
                            r = i - 25
                            if r < 0:
                                r = 0
                            g = i - 25
                            if g < 0:
                                g = 0
                            b = i
                            COLOR = (r, g, b)
                            pixels.fill(COLOR)
                            pixels.show()
                            time.sleep(0.003)

                        COLOR = (175, 175, 200)
                        pixels.fill(COLOR)
                        pixels.show()
                        time.sleep(2.05)

                        for j in range(200, 0, -1):
                            r = j - 25
                            if r < 0:
                                r = 0
                            g = j - 25
                            if g < 0:
                                g = 0
                            b = j
                            COLOR = (r, g, b)
                            pixels.fill(COLOR)
                            pixels.show()
                            time.sleep(0.0045)

                        pixels.fill(OFF)
                        pixels.show()
                        time.sleep(2)

    if effects_mode:
        if math.fabs(x) < 0.3:
            if math.fabs(z) < 0.45:
                if y >= 0.75:
                    audio.play(wave)
                    while audio.playing:
                        for i in range(150):
                            r = i - 25
                            if r < 0:
                                r = 0
                            g = i - 25
                            if g < 0:
                                g = 0
                            b = i
                            COLOR = (r, g, b)
                            pixels.fill(COLOR)
                            pixels.show()
                            time.sleep(0.004)

                        COLOR = (255, 255, 150)
                        pixels.fill(COLOR)
                        pixels.show()
                        time.sleep(1.3)

                        for j in range(200, 0, -1):
                            r = j - 25
                            if r < 0:
                                r = 0
                            g = j - 25
                            if g < 0:
                                g = 0
                            b = j
                            COLOR = (r, g, b)
                            pixels.fill(COLOR)
                            pixels.show()
                            time.sleep(0.004)

                        pixels.fill(OFF)
                        pixels.show()
                        time.sleep(0.5)

