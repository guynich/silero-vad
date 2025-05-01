"""Test Silero VAD speech detection without and with "priming"."""
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from speech_detector import SpeechDetector


def process_audio_chunks(audio, speech_detector):
    chunk_size = speech_detector.chunk_size
    num_chunks = len(audio) // chunk_size
    return [
        speech_detector(audio[i * chunk_size : (i + 1) * chunk_size])
        for i in range(num_chunks)
    ]


def main():
    audio, rate = sf.read("./audio/jfk.wav")
    speech_detector = SpeechDetector(rate=rate)

    # Get speech probabilities without priming
    speech_detector.reset()
    speech_probs = process_audio_chunks(audio, speech_detector)

    # Get speech probabilities with one second of zero "priming"
    speech_detector.reset()
    for _ in range(rate // speech_detector.chunk_size):
        speech_detector(np.zeros(speech_detector.chunk_size))
    speech_probs_zero_primed = process_audio_chunks(audio, speech_detector)

    # Plotting
    time_step = speech_detector.chunk_size / rate
    x_ticks = np.linspace(0.0, len(speech_probs) * time_step, len(speech_probs))
    audio_x_ticks = np.linspace(0.0, len(audio) / rate, len(audio))

    plt.figure()
    plt.plot(x_ticks, speech_probs, "g-.", label="no priming")
    plt.plot(x_ticks, speech_probs_zero_primed, "r:", label="zero primed")
    plt.plot(audio_x_ticks, audio, "b", label="audio")
    plt.ylim([-1.1, 1.1])
    plt.grid()
    plt.legend(loc="lower right")
    plt.title("jfk.wav audio: speech detected probability.")
    plt.show()


if __name__ == "__main__":
    main()
