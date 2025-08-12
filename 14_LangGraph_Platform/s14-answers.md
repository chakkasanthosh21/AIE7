# Session 14 Assignment Answers

## Question 1: Chunk Overlap Parameter
The `chunk_overlap` parameter in RecursiveCharacterTextSplitter creates overlapping text segments between adjacent chunks to maintain context continuity across boundaries. Increasing overlap improves context preservation and reduces information loss at chunk edges, but also increases storage requirements and computational overhead due to duplicate content processing. Decreasing overlap reduces redundancy and storage costs but may fragment important information that spans chunk boundaries, potentially degrading retrieval quality.

## Question 2: Search k Parameter Impact
Adjusting the `k` value in search_kwargs affects RAGAS metrics by controlling how many relevant documents are retrieved for context generation. Increasing `k` from 5 to a higher value typically improves Context Recall by capturing more relevant information, but may decrease Context Precision due to including less relevant documents that dilute the context quality. Conversely, decreasing `k` improves precision by focusing on top-ranked documents but risks missing relevant information, reducing recall.

## Question 3: Agent vs Agent_Helpful Comparison
The `agent` assistant uses a simple tool-using graph while `agent_helpful` incorporates a separate helpfulness evaluation node that assesses response quality before completion. The helpfulness evaluator fits between the agent's response generation and final output, routing execution back to the agent if the response fails helpfulness criteria (allowing refinement) or terminating if the response meets quality standards, creating a feedback loop for improved responses.
