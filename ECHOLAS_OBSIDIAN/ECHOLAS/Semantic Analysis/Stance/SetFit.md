
2 stage few shot text classification. 

- fine tunes a pre trained sentence transformer model on a couple examples using contrastive learning. 


at baseline, we're getting around 82% accuracy (2 epochs), which is pretty insane  with how little effort we put into it

so single epoch actually did silghtly better (83%) which is weird, but indicates that our model slightly overfit to the training data, although not by alot. 


okay fuck we changed the training data slightly and modified the iteration count (increased it) and now it's got an accuracy of 90%

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