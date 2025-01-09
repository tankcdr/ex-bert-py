from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# initialize the pipeline with a DistilBERT model
# tokenizer = AutoTokenizer.from_pretrained(
#   "ktrapeznikov/biobert_v1.1_pubmed_squad_v2")
# model = AutoModelForQuestionAnswering.from_pretrained(
#   "ktrapeznikov/biobert_v1.1_pubmed_squad_v2")


def main():
    try:
        bio_bert_classifier = pipeline("question-answering",
                                       model='ktrapeznikov/biobert_v1.1_pubmed_squad_v2',
                                       tokenizer='ktrapeznikov/biobert_v1.1_pubmed_squad_v2')
        print("Model and tokenizer loaded successfully.")

        basic_classifier = pipeline("question-answering")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # ask a question
    context = "“Symptoms of COVID-19 are variable, but often include fever, cough, fatigue, breathing difficulties, and loss of smell and taste. Symptoms may begin one to fourteen days after exposure to the virus. At least a third of people who are infected do not develop noticeable symptoms.[9] Of those people who develop noticeable symptoms enough to be classed as patients, most (81%) develop mild to moderate symptoms (up to mild pneumonia), while 14% develop severe symptoms (dyspnea, hypoxia, or more than 50% lung involvement on imaging), and 5% suffer critical symptoms (respiratory failure, shock, or multiorgan dysfunction).[10] Older people are more likely to have severe symptoms. Some people continue to experience a range of effects—known as long COVID—for months after recovery, and damage to organs has been observed.[11] Multi-year studies are underway to further investigate the long-term effects of the disease.”"
    question = "What are the symptoms of COVID-19 ?"

    try:
        # Perform question-answering
        result = bio_bert_classifier(question=question, context=context)
        print(result)

        result = basic_classifier(question=question, context=context)
        print(result)
    except Exception as e:
        print(f"Error during question answering: {e}")


if __name__ == "__main__":
    main()
