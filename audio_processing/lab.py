"""
6.101 Lab 0:
Audio Processing
"""

import wave
import struct
# No Additional Imports Allowed!


def backwards(sound):
    return {'rate':sound['rate'], 'samples':list(reversed(sound['samples']))}


def mix(sound1, sound2, p):
    if sound1['rate'] != sound2['rate']:
        return None
    sound1_mult_p=[i*p for i in sound1['samples']]
    sound2_mult_p=[i*(1-p) for i in sound2['samples']]
    sound1_len = len(sound1['samples'])
    sound2_len = len(sound2['samples'])
    max_len = max(sound1_len, sound2_len)

    # Add zeros to the shortest list to get lists witht he same length
    sound1_mult_p += [0]*(sound2_len - sound1_len)
    sound2_mult_p += [0]*(sound1_len - sound2_len)

    # Then loop through both lists by adding numbers at the same positions
    mixed_sound=[(sound1_mult_p[i] + sound2_mult_p[i]) for i in range(max_len)]
    return {'rate':sound1['rate'], 'samples':mixed_sound}


def convolve(sound, kernel):
    convolve_len = len(sound['samples']) + len(kernel) - 1
    convolve_sound=[0] * convolve_len
    for i in range(len(kernel)):
        # Create a temporary sound sample with leading and ending zeros depending on i and length of sound['samples]
        temp_sound=([0] * i) + [(sound['samples'][k]*kernel[i]) for k in range(len(sound['samples']))] + ([0] * (len(kernel) - i - 1))
        for j in range(convolve_len):
            convolve_sound[j] += temp_sound[j] # Add the corrsponding value immediately
    return {'rate': sound['rate'], 'samples': convolve_sound}

def echo(sound, num_echoes, delay, scale):
    sample_delay = round(delay * sound['rate'])
    echo_sound= sound['samples'] + ([0] * num_echoes*sample_delay)
    for i in range(num_echoes):

        # Add zeros first, the original sample, and the leading zeros to have the same lemgth as echo_sound
        temp_echo = ([0]*(i+1)*sample_delay) + [j*(scale**(i+1)) for j in sound['samples']] + [0]*(sample_delay*(num_echoes -i-1))
        for k in range(len(echo_sound)):
            echo_sound[k] += temp_echo[k] # Similar to convolve computations
    return {'rate': sound['rate'], 'samples': echo_sound}


def pan(sound):
    sound_left=sound['left'][:]
    sound_right=sound['right'][:]
    sound_len=len(sound['left'])
    for i in range(sound_len):
        right_scale = i / (sound_len - 1) # Right scale to multiply to each integer in the sound['right']
        left_scale = 1 - (i / (sound_len - 1)) # Left scale to multiply to each integer in the sound['left']
        sound_left[i] *= left_scale
        sound_right[i] *= right_scale
    return {'rate':sound['rate'], 'left':sound_left, 'right':sound_right}


def remove_vocals(sound):
    # left-right at the corresponding locations
    sounds_vocaless = [(sound['left'][i] - sound['right'][i]) for i in range(len(sound['left']))]
    return {'rate':sound['rate'], 'samples':sounds_vocaless}


def bass_boost_kernel(n_val, scale=0):
    """
    Construct a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ n_val

    Then we scale that piece up and add a copy of the original signal back in.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    kernel = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    for i in range(n_val):
        kernel = convolve(kernel, base["samples"])
    kernel = kernel["samples"]

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel) // 2] += 1

    return kernel


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for left, right in zip(sound["left"], sound["right"]):
            left = int(max(-1, min(1, left)) * (2**15 - 1))
            right = int(max(-1, min(1, right)) * (2**15 - 1))
            out.append(left)
            out.append(right)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    pass
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)

    # hello = load_wav("sounds/hello.wav")
    # write_wav(backwards(hello), 'hello_reversed.wav')

    # mystery = load_wav("sounds/mystery.wav")
    # write_wav(backwards(mystery), 'sounds/mystery_reversed.wav')

    # synth = load_wav("sounds/synth.wav")
    # water = load_wav("sounds/water.wav")
    # write_wav(mix(synth, water, 0.2), 'sounds/synth_water_mix.wav')

    # ice_and_chilli = load_wav('sounds/ice_and_chilli.wav')
    # write_wav(convolve(ice_and_chilli, bass_boost_kernel(1000, 1.5)), 'sounds/ice_and_chilli_convolve.wav')

    # chord = load_wav('sounds/chord.wav')
    # write_wav(echo(chord, 5, 0.3, 0.6), 'sounds/chord_echo.wav')

    # car = load_wav('sounds/car.wav', stereo=True)
    # write_wav(pan(car), 'sounds/car_pan.wav')

    # lookout_mountain = load_wav('sounds/lookout_mountain.wav', stereo=True)
    # write_wav(remove_vocals(lookout_mountain), 'sounds/lookout_mountain_vocaless.wav')
