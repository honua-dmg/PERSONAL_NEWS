
# Proper review:
## core sentiment
1. polarity (1, filtering)
	direction expressed in sentiment (pos neg neutral)
	works by capturing patterns between words
	DistilBert (low compute) 
	should be sentence or paragraph. document level is bad in news #question why
	helps cuz it creates a cheap emotional baseline
	note that alot of polarity models struggle with irony sarcasm and institutional phrasing. 
2. sentiment intensity (1, mapping + filtering)
	how strong a sentiment is
	(mild or strong)
	(continuous score)
	usually implemented via a regression based transformer or a confidence weighted polarity
	same as polarity - run it with sentiment level and then scale up to paragraph level- document level is a big no no.
	hard to detect passive agressiveness tho
	note:
		different sources have different emotional baselines
		
## Aspect sentiment
1. targeted sentiment(2, filtering+Mapping)
	what emotion is being expressed towards who?
	yeah this isn't a single library we can import, it's a pipeline.
		1. entity detction {NER, entity linking, noun phrase extraction}
		2. sentiment attribution
			1. Joint models (clean but harder to implement)
			2. Heuristic + classifier 
		3. Aggregation (time based analysis)
	note: start with NER + noun phrases, entities are usually half the topics covered
	
2. Aspect-based sentiment (2.1,filtering+mapping)
	targeted sentiment, but we're also trying to figure out what specific aspect of the entity we're trying to gauge sentiment on.
	It has 2 subproblems 
	1. aspect detection
	2. sentiment attribution to aspect. 
	look into controlled vocab, embedding similarity, and clustering 
	be careful about 
	- aspect explosion (too many categories, fragmented, )
	LLMs work- but we can fine tune and choose specific smaller models to do this more efficiently
	
## stance
1. stance detection(2.2,filtering+mapping)
	author's position towards a target (for, against, neutral) (aim for a gradient (-1,1))
	it's target conditioned classification, we have to teach a model
		- evaluative language
		- causal structure
		- implied endorsement/ rejection.
	again should be sentence level or paragraph level.
	alot of openly available datasets are simple and pretty retarded, we're gonna have to fine-tune, augment, and semi-supervise with LLMS

## Emotion 
1. emotion labels (3,filtering+mapping) {secondary tho}
	what emotional lever is the article pulling?
	usually multi label
	Approach: Multi-label transformer (Long term, more learning)or LLM-based tagging (good for prototyping)
	stick to 6-8 core emotions, fear is prolly the biggest one to look out for, second is anger.
	
	ideal is is entity based emotion mapping

## Framing and narrative
1. Framing type (2, filtering+mapping)
	from what lens is the news being potrayed ex: Economical, moral, security, humanitarian, legal etc
	it's a form of context classification, start with single dominant frame labeling
	Approach:
	supervised frame classifier (fine tuned transformer+fixed frame taxonomy)
	LLM based frame tagging (good for prototyping)
	
2. Agency assignment (2.1,Mapping (blame graphs, victim agressor maps #question how))
	 agent/actor, victim, enabler/blocker tagging
	 missing agents could be a sign of passive voice- important to think about
	 shows how different actors are being portrayed.
	 look for proxy agents
	 Approach:
	 event selection, entity extraction, dependency parsing?, 
	 blame vs credit heuristic 
	 more of a temporal analysis role.
	 risk of being over engineered- 
	 1. Filter for agency sentences
	2. Use dependency parsing for agent/affected
	3. Detect missing agents (passive voice)
	4. Classify blame vs credit
	5. Aggregate patterns, not sentences
	

## Bias & objectivity 
1. subjectivity Score (2 filtering)
	balanced, selective, persuasive, or agenda driven?
	a composite signal:
	1. subjectivity score
	2. loaded language detection
	3. source balance
	4. certainty vs hedging
	5. agency suppression
	6. selection bias (advanced apparently)
2. source bias fingerprinting (temporal analysis)

## Claims & evidence ()
1. claim extraction (2/3, filter,)
	what kind of claim?
	what kind of evidence
		- explicit
		- authority reference 
		- implicit or missing evidence
	guddabal difficult, but forces accountability, and give weight.
2. claim Sentiment
## Entity & narrative Graphs
1. entity sentiment graph(3)
	entity normalization, #todo look more into this, 
	outlet 
	
2. narrative drift over time

   