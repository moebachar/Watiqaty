# Watiqaty Platform

## Overview

Watiqaty is an AI-powered platform designed to assist Moroccans with their administrative paperwork. The platform leverages an advanced chatbot equipped with ADAPTIVE Retrieval-Augmented Generation (RAG) to guide users through the process of obtaining necessary documents and filling out forms.

<p align="center">
  <img src="https://github.com/moebachar/Watiqaty/blob/main/assets/logo.png?raw=true" alt="LangGraph Nodes Pipeline">
</p>

## Walkthrough of the ADAPTIVE RAG Pipeline

The ADAPTIVE RAG pipeline in the Watiqaty platform integrates complex decision-making processes to handle user queries efficiently. Here’s a detailed step-by-step explanation based on the provided flowchart:

![LangGraph Nodes Pipeline](https://github.com/moebachar/Watiqaty/blob/main/assets/diag.png?raw=true)


1. **Query Reception and Initial Processing**: When a query is received, it is first classified to determine if it is related to the existing index or requires a web search for gathering information.
   
2. **Document Retrieval**: Depending on the classification:
   - If related to the index, relevant documents are retrieved and graded for relevance.
   - If not related, a web search is initiated to find relevant information.

3. **Content Generation**:
   - **Check for Relevance**: The relevance of the retrieved information is verified.
   - **Generation**: Based on the relevance check, the system may generate a preliminary response.
   - **Check for Hallucination**: Ensures the generated content is accurate and not misleading.
   - **Question Rewriting**: If needed, the question is rewritten for clarity or to better match the available information.

4. **Answer Formulation**:
   - **Specific Answer Generation**: If the query is specific, a tailored answer is generated based on the retrieved documents.
   - **General Needs**: For more general queries, the system generates a broader response.
   - **Further Analysis**: Some queries may undergo additional analysis for better accuracy.

5. **Delivery through Interfaces**: 
   - **Flask Backend**: Processes and sends the response back to the user interface.
   - **React Frontend**: Displays the response dynamically to the user through the web interface.

This detailed pipeline ensures that every query is handled with precise logic and thorough analysis, providing users with reliable and accurate responses.

## Benchmarking

Here is a comparative table of ADAPTIVE RAG with other models based on several criteria:

| Model          | Accuracy | Speed | Scalability | Cost-Efficiency |
|----------------|:--------:|:-----:|:-----------:|:---------------:|
| ADAPTIVE RAG   |    ✔️    |   ✔️   |      ✔️     |       ✔️       |
| Model 2        |    ✔️    |   ❌   |      ✔️     |       ❌       |
| Model 3        |    ❌    |   ✔️   |      ❌     |       ✔️       |

## Demo

![Watiqaty Demo](https://github.com/moebachar/Watiqaty/blob/main/assets/Design%20sans%20titre.gif?raw=true)


## References to Data Sources

- Démarches Maroc: [Link](https://www.demarchesmaroc.com)
- Wecasablanca : [Link](https://www.casablancacity.ma/ar/demarche/41/autorisation-de-dresser-lacte-de-mariage)
- Royaume du Maroc, Ministère de l'Intérieur: [Link](https://www.passeport.ma/)
- Idarati: [Link](https://idarati.ma/)
  



