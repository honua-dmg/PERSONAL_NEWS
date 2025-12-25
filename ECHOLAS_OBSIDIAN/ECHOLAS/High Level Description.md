The goal:
create a news summarizer that gives 2 views for a topics: for and against. 

People have complex stances on various topics events and people that cannot be simply represented as left wing or right wing. For the ideal intake of news, we believe that news should presented in a radically new format:
	```
	show people what was written in favour of their unique perspective,
	show people what was written againt their unique perspective.
	```
#### Why you may ask?
The purpose of news is to spread information, and the purpose of providers to ensure it is provided in a format that maximizes absorption. the compilation of snippets that directly support ones own view points will help give moral ground for a event for the viewer, while the compilation of snippets that directly conflict with one's own view points (arguably the more important of the two halves) will proceed to challenge the values that a person holds. We aim to create a framework that maximizes the pollination of critical thinking, leading people to become more well rounded on a topic on a dimension that goes above just remembering simple facts. 
#### How are we doing this?
From a birds eye view, what we are building is a perspective mapper  and an LLM pipeline that summarizes articles from a wide range of sources in a polar fashion, with the line of distinction being the users own view points.

Let's break that down byte by byte. 
We first look at **a wide range of sources**, which brings us to the first step of our pipeline
##### News aggregation
For v1, we are utilizing the powerful GDELT database (which is regularly updated with current events with articles from a wide range of sources) to source at a upwards of 250 articles for individual events (eg. Messi visited India for a practice match)

these articles are then scraped and stored in a local database for further processing

##### News sentiment analysis
We now pass each article through the **Sentimental analysis engine** (we can change the name), after which the article becomes a set of unique features, ranging from it's stance on events, to it's overall polarity and aggression. 

##### Perspective mapper
Now we get to the heart of the entire process. this engine's job is to take the set of features received from each individual article, and map them on a multi dimensional graph, whose axes will reflect different events/actors referenced in and are relevant to the topic being covered. The user's entity vector (a collection of their stance on various events/topics) will be mapped in this graph, and using eulerian distance, we will aim to create a gradient of agreeability. with articles mapped closer to the user will represent ideas more in frequency with the users perspective, and those further away will represent abstractions or contrastive features. 

after this mapping, the articles will be sent to the final stage of the pipeline.

##### Summariser
A LLM that will take all the articles ordered with respect to closeness to the user's worldview, and proceed to build a summary (not more than 10 lines) that will have a gradient shift, starting with ideas that closely represent the user's stance, and then diverging. It should be noted that throughout the summary- various links will be scattered to encourage a deep dives.
we will end the snippet with 2 open ended questions, framed to help the user reflect and engage critically. A sort of epistemic stress test if you will. Our goal is to nudge reflections, not opinions.

##### User vector
Perhaps the most important piece of data we will ever collect and utilize. It is an understatement to say that if our mapping of the user's worldview is skewed, the entire premise of this application will go bust. (This is something we have to focus heavily on)



##### Looking forward
we could look into temporal changes in the user's stance. things like, 
Your perspective of event X changed over the past couple weeks after being exposed to topic Y


surya:
- senti 
- work on user feedback, onboarding 

8 values - tracking political spectrum 
[https://8values.github.io/](https://8values.github.io/)
substack 
conversation or just views and read time metrics 
present 
highlight points of conflict - expand to see differences - LOOK INTO THIS. 




