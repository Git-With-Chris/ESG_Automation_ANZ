
# Query Engineering

- [Query Engineering](#query-engineering)
  - [Why?](#why)
  - [Components of a Good Query](#components-of-a-good-query)
  - [How?](#how)
  - [Examples](#examples)

## Why? 

Query engineering, also known as prompt engineering, is crucial for several reasons, particularly in the context of utilising transformer/language models. Here are some key points highlighting its importance:

1. <font color="#fac08f">Optimising Output Quality</font>:
    
    - **Precision and Clarity**: Well-engineered queries result in more accurate, relevant, and clear responses. 
    - **Minimising Ambiguity**: Good query construction helps reduce ambiguity, ensuring the model understands the context and intent.
      
2. <font color="#fac08f">Efficiency in Information Retrieval:</font>
    
    - **Time-Saving**: Effective queries can quickly extract the required information, saving time and effort compared to broad or poorly structured queries.
    - **Relevance**: Focused queries help in retrieving information that is directly relevant to the user's needs, filtering out unnecessary or unrelated data.

## Components of a Good Query

A good query is composed of several key components that collectively ensure it is clear, specific, and contextually appropriate. These components include:

1. **Clarity**: The query should be clearly articulated, avoiding ambiguity and confusion. 
   
2. **Specificity**: Specific queries are more likely to yield relevant results.
   
4. **Relevance**: The query should focus on relevant aspects of the task at hand, ensuring that the retrieved sentences align with the desired criteria.
   
5. **Length**: Ensuring the query is sufficiently detailed without being overly verbose is crucial. 

## How? 

Here are practical guidelines for creating good queries:

- <font color="#4bacc6">Define the Objective</font>: Clearly state what you aim to achieve with the query. 
  
- <font color="#4bacc6">Use Descriptive Keywords</font>: Include keywords that are highly descriptive and relevant to the topic or information you seek.
  
- <font color="#4bacc6">Avoid Ambiguity</font>: Ensure that the query is free from ambiguous terms or phrases that could confuse the model.
  
- <font color="#4bacc6">Iterate and Refine</font>: Query engineering is often an iterative process. Start with a preliminary query, analyse the results, and refine the query as needed to improve relevance and accuracy.

## Examples

> **Product Packaging**
> 
> <font color="#fac08f">Task</font>: Sentences expressing details on product packaging.
> 
> <font color="#fac08f">Key Words</font>: Product packaging, Sustainable and relation/similarity.
> 
> <font color="#4bacc6">Query:</font> "This sentence is closely related to sustainable product packaging" 
  
<br>

> **Modern Slavery**
> 
> <font color="#fac08f">Task</font>: Sentences expressing details on modern slavery.
> 
> <font color="#fac08f">Key Words</font>: Modern slavery
>  
> <font color="#fac08f">Removing Ambiguity</font>:  Forced labor, Human trafficking, Exploitation
> 
> 
> <font color="#4bacc6">Query:</font> "Does this sentence relate to modern slavery, including forced labor, human trafficking, or exploitation?" 

The above examples are just to illustrate the best practices while building a query and not perfect templates to be used. We expect users to use this frame work to devise independent querying strategies. 



