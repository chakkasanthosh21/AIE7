
###### ? Question 1:

1) Is there any way to modify the embedding dimension of text-embedding-3-small?**
2) What technique does OpenAI use to achieve this?**


####### ANSWERS:

**A1:** No, you cannot directly modify the embedding dimension of OpenAI's text-embedding-3-small model. The output dimension (1536) is fixed by the model architecture. If you need a different dimension, you can apply dimensionality reduction (e.g., PCA) to the output embeddings, but the model itself always returns 1536-dimensional vectors.

**A2:** OpenAI uses a transformer-based neural network architecture, trained to produce dense vector representations of text. The embedding size is set by the model's final layer. The model is trained using objectives like contrastive learning to ensure semantically similar texts have similar embeddings. The exact details are proprietary, but the approach is similar to other transformer-based embedding models.

-------------------------------------------------------------------------------------

###### ? Question 2:

1) What are the benifits of using ASYNC approach to collecting our embeddings 

###### ANSWER:
***A1:** Using an async approach to collect embeddings allows you to send multiple requests to the API at the same time, making the process much faster and more efficient. It reduces waiting time, improves resource usage, and helps your program handle large batches of data or stay responsive if it has a user interface. Async is especially beneficial when working with slow or rate-limited APIs.

--------------------------------------------------------------------------------------

##### ? QUestion 3:

1) When Calling the OpenAI API - are there any other ways we can achieve more reproducible outputs? 

##### ANSWER:
***A1:** To achieve more reproducible outputs with the OpenAI API, set a fixed seed (if supported), use the same prompt and parameters (like temperature=0), and specify the exact model version.

--------------------------------------------------------------------------------------

##### ? Question 4:

1) What prompting strategies could you use to make the LLM have a more thoughtful, detailed responses ? 
what is that strategy called ?

##### ANSWER:
***A1:** To get more thoughtful, detailed responses from an LLM, use chain-of-thought prompting by asking the model to explain its reasoning step by step.