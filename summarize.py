import argparse
import logging
import os

import google.generativeai as genai
import torch

from src.audio_handler import align, diarize, transcribe
from src.doc_write import write_docx
from src.prompts import get_summarization_prompt

if os.environ.get("LD_LIBRARY_PATH") is None:
    import nvidia.cublas.lib
    import nvidia.cudnn.lib

    os.environ["LD_LIBRARY_PATH"] = (
        os.path.dirname(nvidia.cublas.lib.__file__)
        + ":"
        + os.path.dirname(nvidia.cudnn.lib.__file__)
    )
    print("loaded nvida env vars")


logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)


genai.configure(api_key=os.environ["GEMINI_KEY"])

device = "cuda"
batch_size = 16  # reduce if low on GPU mem
compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True


llm = genai.GenerativeModel("gemini-2.0-flash")


def write_transcription(result):
    output_text = ""
    logging.info("writing transcription...")
    for segment in result["segments"]:
        speaker = segment.get("speaker")
        text = segment["text"].strip()
        output_text += f"[{speaker}]: {text}\n"

    return output_text


def summarize(audio_path, output_dir="./"):
    # Extract filename without extension for output file naming.
    base_filename = os.path.splitext(os.path.basename(audio_path))[0]
    # Define file paths for outputs.
    transcription_path = os.path.join(output_dir, f"transcription_{base_filename}.docx")
    summary_path = os.path.join(output_dir, f"summary_{base_filename}.docx")

    audio, result = transcribe(audio_path, device, compute_type, batch_size)
    aligned_result = align(audio, result, device)
    diarized_result = diarize(audio, aligned_result, device)
    output_text = write_transcription(diarized_result)

    write_docx(transcription_path, output_text, use_markdown=False)

    prompt = get_summarization_prompt(output_text)
    response = llm.generate_content(prompt)

    print("writing summary...")
    write_docx(summary_path, response.text, use_markdown=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    summarize(args.audio_file, args.output_dir)
