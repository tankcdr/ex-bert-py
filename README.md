# BERT experiments

Experiments with hugging face transformers library.

Some of the more interesting experiments are....

| Python script                             | Description                                                                                                                                                                                          |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| qa/telegram_wikipedia_qa_bot.py           | Simple telegram bot that uses the wikipedia api for Q&A. Uses HuggingFace `question_answering` transform to answer questions based on the wikipedia context. Accuracy can be improved significantly. |
| nlp/telegram_nlp_toxicity_bot.py          | Telegram bot that detects toxicity and intent. Uses Hugginface `zero-shot-classifier` for intent classification and `unitary/toxic-bert` for toxicity classificaiton.                                |
| summary/telegram_wikipedia_summary_bot.py | Uses the T5 transformer to summary information from a wikiepedia query                                                                                                                               |
| translation/telegram_translation_bot.py   | Leverages the `zero-shot-classification` transformer to detect the src langague and uses the TranslationModel (dl-translate) to transalate src into a user selected target language.                 |
| ner/telegram_ner_bot.py                   | Simple named entity recognition Telegram bot                                                                                                                                                         |
| ner/telgram_medical_ner_bot.py            | Simple named entity recognition Telegram bot                                                                                                                                                         |

## Dependencies

Virtual environment: `python -venv venv`

```
pip install transformers datasets dl-translate
pip install --pre torch  --index-url https://download.pytorch.org/whl/nightly/cpu
pip install jupyterlab
pip install pytelegrambotapi python-dotenv
```
