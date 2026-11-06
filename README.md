# tts-puno-quechua

Open-licensed text-to-speech (TTS) models for **Puno Quechua** (ISO 639-3: `qxp`), a Collao Quechua variety of Southern Quechua spoken in the Puno region of Peru.

Puno Quechua is mainly a spoken language. Most speakers went to school in Spanish, so many speak Quechua fluently but rarely read or write it. Speech synthesis gives these speakers a way to use digital tools and educational material without needing to read the language. Until now, no Quechua TTS system was available under a free licence. This repository provides a first one, trained with the [VITS](https://arxiv.org/abs/2106.06103) architecture as implemented in [Coqui TTS](https://github.com/coqui-ai/TTS).

## Contents

- [Training data](#training-data)
- [Models](#models)
- [Voice anonymisation](#voice-anonymisation)
- [Evaluation](#evaluation)
- [Usage](#usage)
- [Repository layout](#repository-layout)
- [Limitations and future work](#limitations-and-future-work)
- [Related resources](#related-resources)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Training data

The models are trained on **Common Voice Scripted Speech 26.0 – Puno Quechua (qxp)**: read-aloud recordings of community-written sentences. The dataset is released under CC0-1.0 on the [Mozilla Data Collective](https://mozilladatacollective.com). To download it, create an account there and accept the data usage agreement.

**Versions.** Common Voice publishes a new cumulative release every quarter. These models use **Scripted Speech 26.0**. The 15 evaluation sentences come from **Spontaneous Speech 4.0**. All releases are listed at **<https://commonvoice.mozilla.org/en/datasets>**.

The data comes from a community-led collection campaign that ran from January 2025 to March 2026. It was organised with the National University of Altiplano of Puno, the Puno Regional Government and the community organisation Illariy Ch'aska. Native speakers recorded sentences on a localised version of the Common Voice platform. Other community members then listened to each clip and voted on whether it was acceptable.

| | Value |
|---|---|
| Recorded audio | 34.88 h |
| Validated audio | 31.18 h |
| Clips | 25,423 |
| Speakers | 81 |
| Prompt sentences | 2,070 |
| Average clip duration | 4.94 s |

The data is **heavily imbalanced by gender**:

| Gender | Voices | Audio | Clips |
|---|---|---|---|
| Female | 62 | ~23 h | 17,547 |
| Male | 17 | ~7 h | 5,180 |

Among the male contributors, only five recorded more than 10 minutes of speech, and two speakers account for about 70% of all male recording time.

## Models

Two VITS models were trained: one on female voices and one on male voices.

| Model | Training data | Output voices | Status |
|---|---|---|---|
| Female | All female recordings (62 speakers, ~23 h) | 4 anonymised voices | **Released** ([`female_model/`](female_model/)) |
| Male | The 2 main male contributors (~5 h) | 1 | **Trained, not yet released.** Its voices could not be anonymised (see below). |

The female recordings are spread fairly evenly across speakers, so the whole female subset was used. The male recordings are concentrated in a few people, so the male model uses only the two main contributors.

Main settings of the released female model (see [`female_model/config.json`](female_model/config.json)):

| Setting | Value |
|---|---|
| Architecture | VITS (Coqui TTS), multi-speaker with speaker embeddings |
| Sample rate | 22,050 Hz |
| Text input | Graphemes (no phonemiser); Quechua alphabet including `'` for ejectives |
| Mel bands / FFT / hop | 80 / 1024 / 256 |
| Batch size | 32 |
| Epochs | 1000 |
| Learning rate (generator / discriminator) | 2e-4 / 2e-4 |

## Voice anonymisation

The voices of the people who recorded the training data must not be reproducible, to prevent misuse such as deepfakes. The models were therefore anonymised after training.

**Female model.** The speaker embeddings learned during training were clustered. A new synthetic speaker embedding was created from the centroid of each cluster. Any centroid that was too close to a real speaker's embedding was discarded. This left **four anonymised voices**, `anon_speaker_000` to `anon_speaker_003`. These are the only voices the released model can produce.

![Speaker embeddings of the female model](./visualisations/speaker_embeddings_female_model.png)

**Male model.** This method does not work for the male model. The two contributors it was trained on sound so similar that a centroid voice would stay too close to a real speaker. The male model will only be released once a different anonymisation method has been applied. The samples in [`demo/male/`](demo/male/) are included only to show what the model sounds like.

## Evaluation

### Method

Fifteen sentences were chosen from the Common Voice Spontaneous Speech 4.0 (qxp) dataset so that together they cover every phoneme of Puno Quechua. They are listed in [`evaluations/eval_sentences.tsv`](evaluations/eval_sentences.tsv). Each sentence was synthesised with every available voice. The audio was then scored with [NISQA v2](https://github.com/gabrielmittag/NISQA), which predicts an overall Mean Opinion Score (MOS, 1–5) and four quality dimensions: noisiness, coloration, discontinuity and loudness.

> **Caveat.** NISQA estimates *audio signal quality* without a reference recording. It does not measure how intelligible, natural or correctly pronounced the speech is, and it was not designed to evaluate TTS systems. Read the scores as a check on signal quality, not as a replacement for listening tests with native speakers.

### Results

Mean and median NISQA MOS per voice (15 sentences each):

| Model | Voice | Mean MOS | Median MOS |
|---|---|---|---|
| Female | `anon_speaker_000` | 2.99 | 2.99 |
| Female | `anon_speaker_001` | 3.85 | 3.91 |
| Female | `anon_speaker_002` | 4.30 | 4.41 |
| Female | `anon_speaker_003` | 4.07 | 4.07 |
| Female | *all voices* | 3.80 | 3.93 |
| Male (unreleased) | — | 4.56 | 4.55 |

The male model scores consistently high because it was trained on a small amount of clean, consistent audio from two people. The female voices vary more. `anon_speaker_002` and `anon_speaker_003` are the strongest, and `anon_speaker_000` is noticeably weaker. Scores per sentence and per dimension are in [`evaluations/`](evaluations/).

## Usage

### 1. Clone with Git LFS

The model weights are stored with [Git LFS](https://git-lfs.com/). Install it before cloning:

```bash
git lfs install
git clone https://github.com/QuechuaBase/tts-puno-quechua.git
cd tts-puno-quechua
```

### 2. Install dependencies

Tested with Python 3.11:

```bash
python -m venv tts-env
source tts-env/bin/activate
pip install -r requirements_tts.txt
```

### 3. Run inference

```bash
python run_inference.py female_model \
    --checkpoint female_model.pth \
    --speaker anon_speaker_002 \
    --text "Kunanqa nuqapis qichwata rimaniña." \
    --output demo.wav
```

| Argument | Description | Default |
|---|---|---|
| `dirname` | Model directory containing `config.json`, the checkpoint and `speakers.pth` | (required) |
| `--checkpoint`, `-c` | Checkpoint file name **inside** `dirname` | first `*.pth` found |
| `--speaker`, `-s` | `anon_speaker_000`, `anon_speaker_001`, `anon_speaker_002` or `anon_speaker_003` | `anon_speaker_001` |
| `--text`, `-t` | Sentence to synthesise, in Puno Quechua orthography | a sample sentence |
| `--output`, `-o` | Output `.wav` path | `demo.wav` |

The model reads characters directly (graphemes), so write the input in standard Quechua spelling, using `'` for ejectives (e.g. `p'unchay`, `hallp'a`).

## Repository layout

```
.
├── female_model/        Released female VITS model (config, LFS checkpoint, speaker embeddings)
├── demo/
│   ├── female/          One sample per anonymised female voice
│   └── male/            Evaluation sentences from the unreleased male model, with NISQA scores
├── evaluations/         Evaluation sentences and NISQA scores for both models
├── visualisations/      Speaker-embedding plot of the female model
├── run_inference.py     Command-line inference script
└── requirements_tts.txt Pinned dependencies (Coqui TTS)
```

See [`demo/README.md`](demo/README.md) for a description of each audio sample.

## Limitations and future work

- **Gender imbalance.** Male speech makes up less than a quarter of the training data, and most of it comes from two people. That is why the male model has only one voice and can't be released yet.
- **Evaluation scope.** NISQA measures signal quality only. Listening tests with Puno Quechua speakers, to judge intelligibility and naturalness, have not been done yet.
- **Crowd-sourced audio.** Recordings were made on varied phones and in varied environments, which shows up as differences in quality between voices.
- **Possible improvements:** pre-filtering the training data down to the cleanest clips, using the speaker-embedding clusters to pick the most consistent voices, and finding an anonymisation method that works for few-speaker models such as the male model.

## Related resources

- **Datasets (CC0-1.0):** Common Voice Scripted Speech 26.0 and Spontaneous Speech 4.0 – Puno Quechua (qxp), downloadable from the [Mozilla Data Collective](https://mozilladatacollective.com). All releases are listed at <https://commonvoice.mozilla.org/en/datasets>.
- **Speech recognition:** [QuechuaBase/asr-puno-quechua](https://github.com/QuechuaBase/asr-puno-quechua), with fine-tuned XLS-R models on Hugging Face ([xls-r-qxp-cv26-silver](https://huggingface.co/QuechuaBase/xls-r-qxp-cv26-silver), [xls-r-cpt-qxp-cv26-silver](https://huggingface.co/QuechuaBase/xls-r-cpt-qxp-cv26-silver))
- **Speech emotion recognition:** [QuechuaBase/SER-quechua-collao](https://github.com/QuechuaBase/SER-quechua-collao)
- **Common Voice Puno Quechua:** <https://commonvoice.mozilla.org/qxp>

## License

The contents of this repository are released under [CC0 1.0 Universal](LICENSE). The training data is also CC0-1.0. Its data usage agreement forbids attempting to identify individual contributors. Please respect that rule when using these models too.

## Acknowledgements

We thank the Puno Quechua speakers who recorded and validated the data, as well as the National University of Altiplano of Puno, the Puno Regional Government and the Illariy Ch'aska association for making the collection campaign possible.