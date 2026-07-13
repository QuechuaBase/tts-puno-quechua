import argparse
import os
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument("dirname")
parser.add_argument(
    "--checkpoint", "-c", help="Model name (.pth)")
parser.add_argument(
    "--text", "-t", default="Chay rumiyuq hallp'aqa manan tarpunapaq allinchu.", help="Sentence to generate")
parser.add_argument(
    "--speaker", "-s", default="anon_speaker_001", help="Speaker name")
parser.add_argument(
    "--output", "-o", default="demo.wav", help="Name of generated wav")

args = parser.parse_args()

if not args.checkpoint:
    detected = glob(os.path.join(args.dirname, "*.pth"))
    print(f"Checkpoints detected in the directory: {detected}. Using detected[0]")
    ckpt = detected[0]

model_path = os.path.join(args.dirname, ckpt)
text = args.text
file_path = args.output

tts = TTS(
    model_path=model_path,
    config_path=os.path.join(args.dirname, "config.json")
)

print(f"Voices available in the model: {tts.speakers}")

tts.tts_to_file(
    text=text,
    file_path=file_path,
    speaker=args.speaker
)
