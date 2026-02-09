
2 stage few shot text classification. 

- fine tunes a pre trained sentence transformer model on a couple examples using contrastive learning. 


at baseline, we're getting around 82% accuracy (2 epochs), which is pretty insane  with how little effort we put into it

so single epoch actually did silghtly better (83%) which is weird, but indicates that our model slightly overfit to the training data, although not by alot. 


okay  we changed the training data slightly and modified the iteration count (increased it) and now it's got an accuracy of 90%

I fear it's slightly overfit to the test data, let's change that. 

oh hell nah we're steady at around 88% we balling for now. 

so we are not balling for now, chat jus gave me a pretty solid smack back to reality. 

heres the jist of it:
- news is never this straightforward
- I'm not segmenting my errors into buckets to see where this is actually failing. 
- this labeling system is nice but eventually we'll need to move to a gradient system (-1,1)


we'll move to a continuous labling system and confidence score implementation. 

- this'll be our next task.


we understand why setfit works
- the contrastive learning part nudges similarly labeled objects closer together- clear clusters, easier to regress on. 


- figure out a decent training set that teaches stance not sentiment.

- measure how the latent space moved
- figure out how to tune contrastive learning for labels that aren't all that contrastive (neutral vs neg or neutral vs pos)

## Continuous labeling 

### Things to consider
-  how to _measure_ how much the space moved
-  how to visualize stance axes explicitly
- how to tune contrastive loss for asymmetric labels (For vs Against > Neutral)


holy shit this thing is insane
test data
![[Pasted image 20260208201912.png]]
diverse data test set 1![[Pasted image 20260208203108.png]]
financial data set 1![[Pasted image 20260208204151.png]]

okay so this introduces a new problem, if the wrong examples are tightly clustered around the wrong label's centroid, how are we gonna figure out the confidence score- the model seems super confident that it has the right answer. 


When you observe where the model screws up, you tend to see patterns. 

Our stance alignment is really a composition of 4 types of alignment:
1. linguistic 
	this looks objectively at whether the text provided supports a specific stance explicitly
	ex: hey this is great!
2. moral
	this looks at moral values that underpin what's being said
	ex: ceos don't work 300 times a normal wage worker, this is insane.
3. necessity 
	looks at how mandatory an entity/event is to a given structure
	ex: allaudin was an evil man but he saved india from mongol invasion. 
4. policy
	looks at if the speaker supports the policy being talked about
	ex: swach barath is an important policy that has yet to show real impact. 