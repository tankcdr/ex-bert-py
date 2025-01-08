from transformers import pipeline

# proofing environment

# initialize the pipeline with a DistilBERT model
classifier = pipeline("question-answering")

# ask a question
question = "What is the capital of France?"
context = "The capital of France is Paris."

print(classifier(question=question, context=context))

# ask another quesiton
question = "When was Pink Floyd formed?"
context = "Pink Floyd was an English rock band formed in London in 1965."

print(classifier(question=question, context=context))
