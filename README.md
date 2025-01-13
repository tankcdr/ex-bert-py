# BERT experiments

Experiments with hugging face transformers library.

Some of the more interesting experiments are....

| Python script                   | Description                                                                                                                                                                                          |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| qa/telegram_wikipedia_qa_bot.py | Simple telegram bot that uses the wikipedia api for Q&A. Uses HuggingFace `question_answering` transform to answer questions based on the wikipedia context. Accuracy can be improved significantly. |

## Dependencies

Virtual environment: `python -venv venv`

```
pip install transformers datasets
pip install --pre torch  --index-url https://download.pytorch.org/whl/nightly/cpu
pip install jupyterlab
pip install pytelegrambotapi python-dotenv
```
