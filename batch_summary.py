import os
import argparse
import subprocess


def process_all_audios(input_dir, output_dir):
    """
    Process all audio files in the input directory and save outputs to the output directory.
    """
    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)
    
    # Define supported audio file extensions (add more if needed)
    supported_exts = ['.mp3', '.wav', '.m4a', '.flac', '.aac']
    
    # Process each file in the input directory.
    for filename in os.listdir(input_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in supported_exts:
            audio_path = os.path.join(input_dir, filename)
            print(f"Resumindo arquivo {filename}")
            # summarize(audio_path, output_dir)
            subprocess.run(
                    ["python", "summarize.py", audio_path, output_dir],
                    check=True
                )
        else:
            print(f"Ignorando arquivo não suportado: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processa todos os arquivos de áudio em uma pasta, realizando transcrição, diarização e resumindo o conteúdo."
    )
    parser.add_argument("input_dir", help="Caminho para a pasta contendo arquivos de áudio.")
    parser.add_argument("output_dir", help="Caminho para a pasta onde serão salvos os resultados.")
    args = parser.parse_args()
    
    process_all_audios(args.input_dir, args.output_dir)