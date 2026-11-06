# Audio samples

Speech synthesised by the Puno Quechua TTS models. All files are 22,050 Hz mono WAV.

## `female/` – released female model

One sample for each of the four anonymised voices the released model can produce. These are synthetic voices built from clusters of speaker embeddings; none of them belongs to a real contributor. See [Voice anonymisation](../README.md#voice-anonymisation).

| File | Voice | NISQA mean MOS (evaluation set) |
|---|---|---|
| `anon_speaker_000.wav` | `anon_speaker_000` | 2.99 |
| `anon_speaker_001.wav` | `anon_speaker_001` | 3.85 |
| `anon_speaker_002.wav` | `anon_speaker_002` | 4.30 |
| `anon_speaker_003.wav` | `anon_speaker_003` | 4.07 |

To make your own sample with any of these voices:

```bash
python run_inference.py female_model -c female_model.pth -s anon_speaker_002 -t "Kunanqa nuqapis qichwata rimaniña." -o sample.wav
```

## `male/` – male model (trained, not yet released)

The 15 evaluation sentences synthesised by the male model. That model was trained on the two main male contributors. It can't be anonymised with the method used for the female model, so it has **not been released**. These samples are provided only to illustrate its quality.

[`eval_nisqa_male_model.csv`](male/eval_nisqa_male_model.csv) lists each file with its transcription and NISQA scores (overall MOS, noisiness, discontinuity, coloration, loudness).

| File | Sentence |
|---|---|
| `sent_0.wav` | Imapaqtaq ashwanta celularniykita apanaqanki? |
| `sent_1.wav` | Mana yachakunchu imatachá musuq watapi ruwasaq. |
| `sent_2.wav` | T'ikakunaqta manan nishuta qhichwa simipi sutinkunata riqsinichu. |
| `sent_3.wav` | Kusisqa runallan kani, ch'in purikuq utaq kusisqa purikuq. |
| `sent_4.wav` | Chayllatapuniyá ruwasharqani. |
| `sent_5.wav` | Qhali warmi kani, saphiymantapacha yachayniyuq. |
| `sent_6.wav` | Turay ama llakisqa puriychu, kusikuspalla purikunaqa. |
| `sent_7.wav` | Nuqa hatarispa uyayta, kiruyta maqchikuni, hinaspa wayk'uni mikhunayta. |
| `sent_8.wav` | Nuqa phishqa watapi nuqa llank'asaq yachachiqhina. |
| `sent_9.wav` | Kayta ruwanayta tukuspa nuqa mikhuq purinay karqan. |
| `sent_10.wav` | Wawa kaspayki, imaynatan taytamamaykita yanaparqanki? |
| `sent_11.wav` | Kay killaqa mana maytapis karu llaqtamanqa risaqchu. |
| `sent_12.wav` | Wasiq rakinkunaqa kashan: wayk'una wasi, mikhuna wasi, puñuna wasi, hinaspapis hisp'ana wasi. |
| `sent_13.wav` | Aylluypaq p'achankunaqa munay pullirayuq, muntirayuq, chamarayuq hinallataq warak'ayuq. |
| `sent_14.wav` | Qhatuqa llaqtaypi hunt'a llipin muyuq llaqtakunamanta hamunku, qhatukuqpis rantikuqpis. |

The same sentences are listed in [`../evaluations/eval_sentences.tsv`](../evaluations/eval_sentences.tsv).
