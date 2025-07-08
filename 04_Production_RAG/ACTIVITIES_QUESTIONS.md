**####** Question 1
What is the embedding dimension, given that we're using `text-embedding-3-small`?
**####** Answer 1 
    embedding_dim =  1536

**####** Question 2
    
    **####** Question 2.a
    What if the retriever finds no relevant context? 
    
    **####** Answer 2.a 
    🧩 Approach:
	•	After retrieve(), check if state["context"] is empty or too short.
	•	If empty, return a fallback response like:
    “I don’t know. There’s no relevant information in the provided context.”

    **####** question 2.b
    What if the response needs fact-checking?

    **####** Answer 2.b
    Add a fact-checking node after the generate() step in the graph.
    🧩 Approach:
	•	Create a new LLM prompt that takes both the context and the generated response.
	•	Ask something like:
    “Based on the provided context, is the answer factually supported? Yes or No.”
	•	If the answer is No, return a warning:
    “⚠️ This answer may not be fully supported by the documents retrieved. Please verify independently.”

