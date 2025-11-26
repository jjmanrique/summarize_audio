import logging
import os


from dotenv import load_dotenv
import whisperx

load_dotenv()

hf_token = os.environ["HF_TOKEN"]


def transcribe(audio_path, device, compute_type, batch_size):
    # load model
    logging.info("Loading Transcription Model...")
    model = whisperx.load_model("large-v3", device, compute_type=compute_type)

    audio = whisperx.load_audio(audio_path)
    logging.info("transcribing...")
    result = model.transcribe(audio, batch_size=batch_size, language="pt")
    # del model

    return audio, result


def align(audio, transcription_result, device):
    logging.info("alining...")
    model_a, metadata = whisperx.load_align_model(
        language_code=transcription_result["language"], device=device
    )
    aligned_result = whisperx.align(
        transcription_result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )
    return aligned_result


def diarize(audio, aligned_result, device, min_speakers=1, max_speakers=2):
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)

    # add min/max number of speakers if known
    logging.info("diarizing...")
    diarize_segments = diarize_model(
        audio, min_speakers=min_speakers, max_speakers=max_speakers
    )

    result = whisperx.assign_word_speakers(diarize_segments, aligned_result)

    return result
