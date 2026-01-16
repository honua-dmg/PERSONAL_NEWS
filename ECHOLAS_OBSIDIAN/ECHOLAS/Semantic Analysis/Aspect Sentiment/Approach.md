
the way I understand it now. 
if we can figure out which entity is being spoken about in which sentence/ sub sentence, we can effectively run a SetFit (sentence transformer fine tuning)


There's also natural language entailment (NLI- something that could be worth looking into)


siamese networks (contrastive learning)




# NER +SetFit 

### NER
Named entity recognition, we can use SpaCy to begin with, but looking libraries that offer less broad range and more news oriented entity recognition could be useful

### setFit
sentence transformer fine tuning - we give a few shot examples (annotated), and it uses the embedding distance to mark works. 
runs of a form of contrastive learning

Example usage:
```from setfit import SetFitModel, SetFitTrainer
from datasets import Dataset

# 1. Create a tiny dataset
data = {
    "text": ["Rates must rise to curb inflation", "We should pause hikes for now", ...],
    "label": [1, 0, ...] # 1 = Hawkish, 0 = Dovish
}
dataset = Dataset.from_dict(data)

# 2. Load a sentence transformer
model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")

# 3. Train (takes seconds)
trainer = SetFitTrainer(model=model, train_dataset=dataset)
trainer.train()

# 4. Inference
preds = model(["The central bank signals tightening."])
# Output: Hawkish
```

# SLM training
few shot training + CoT on a model like lamma 3 8B model. 


### Manifold learning
- unsupervised, take the embeddings, normalize and scale them down to lower dimensions, and run the consensus as a Gaussian Distribution.
