#index
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

#question = 'What is the necessary documents to get the passport at morocco'


vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"), collection_name="rag-chroma")

store = {}

    
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

retriever = vectorstore.as_retriever(k=3)
#LLM---------------------------------------------------------------------------------------------------------------
url="https://apjhl54nu2w6tstq.us-east-1.aws.endpoints.huggingface.cloud/"

llm1 = ChatOllama(model="llama3")
llm2 = HuggingFaceEndpoint(
    endpoint_url = url,
    max_new_tokens=1024,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.8,
    repetition_penalty=1.03,
    huggingfacehub_api_token="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"
    
)


prompt0 = PromptTemplate(
    template="""You are an expert at routing user questions to the appropriate source: general chat, vectorstore, or web search. \n
    You can rewrite the question in arabic or frensh or english depending on what you see useful
    First, determine if the question is general, such as greetings or casual conversation like 'hi' or 'tell me a joke'. If so, route to general chat. \n
    If the question is not general, check if it relates to the context for routing to vectorstore. \n
    If the question does not fit the above categories, use web search for questions requiring current events, factual information, or specific knowledge not directly related to LLMs. \n
    Return a JSON object with a single key 'datasource' indicating 'general', 'vectorstore', or 'web_search' based on the question content. \n
    Question to route: {question}""",
    input_variables=["question"],
)

question_router = prompt0 | llm1 | JsonOutputParser()


#answer general questions------------------------------------------------------------------------------------
prompt1 = PromptTemplate(
    template="""You are a conversational expert designed to provide a concise and informative answer to general questions. \n
    Here is the question: {question} \n
    Please provide a clear and helpful response appropriate for a general audience.\n""",
    input_variables=["question"],
)

generalgenerator = prompt1 | llm2 | StrOutputParser()


### Retrieval Grader-----------------------------------------------------------------------------------------

prompt2 = PromptTemplate(
    template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
    Here is the retrieved document: \n\n {document} \n\n
    Here is the user question: {question} \n
    If the document contains keywords related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
    Provide the binary score as a JSON with a single key 'score' and no premable or explanation.""",
    input_variables=["question", "document"],
)

retrieval_grader = prompt2 | llm1 | JsonOutputParser()


### Generate---------------------------------------------------------------------------------
VAAA=[ "Passport", "CIN", "permis"]
# Prompt
prompt = PromptTemplate(
    template="""You are a administration assistant, and you qre given some tools to do a websearch.\
             Use the following pieces of retrieved context to answer the question.  \
             Use three sentences maximum and keep the answer concise.\
             if the user needs one of this documents : {VAAA}, at the last line say the name of this Document Say only the element of the list asked about.\
             If the question is in frensh answer it in frensh , if it is in arabic answer the user in arabic , if the answer is in english answer the user in english 
             Question: {question} 

             Context: {context} 

             Answer:
    """,
    input_variables=["context", "question", "VAAA"],
    
)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm2 | StrOutputParser()

# Run



### Hallucination Grader---------------------------------------------------------------------------------------

# Prompt
prompt3 = PromptTemplate(
    template="""You are a grader assessing whether an answer is grounded in / supported by a set of facts. \n 
    Here are the facts:
    \n ------- \n
    {documents} 
    \n ------- \n
    Here is the answer: {generation}
    Give a binary score 'yes' or 'no' score to indicate whether the answer is grounded in / supported by a set of facts. \n
    Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.""",
    input_variables=["generation", "documents"]
)

hallucination_grader = prompt3 | llm1 | JsonOutputParser()

### Answer  -------------------------------------------------------------------------------------------------

# Prompt
prompt4 = PromptTemplate(
    template="""You are a grader assessing whether an answer is useful to resolve a question. \n 
    Here is the answer:
    \n ------- \n
    {generation} 
    \n ------- \n
    Here is the question: {question}
    Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question. \n
    Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.""",
    input_variables=["generation", "question"],
)

answer_grader = prompt4 | llm1 | JsonOutputParser()


### Question Re-writer----------------------------------------------------------------------------------------

# Prompt
re_write_prompt = PromptTemplate(
    template="""You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the initial and formulate an improved question. \n
     Here is the initial question: \n\n {question}. Improved question with no preamble: \n """,
    input_variables=["generation", "question"],
)

question_rewriter = re_write_prompt | llm2 | StrOutputParser()

##WEB Search --------------------------------------------------------------------------------------
from tavily import TavilyClient
tavily = TavilyClient(api_key="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")

### Search--------------------------------------------------------------
import os

from langchain_community.tools.tavily_search import TavilySearchResults

os.environ['TAVILY_API_KEY'] = "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"

web_search_tool = TavilySearchResults(k=3)
###Graph --------------------------------------------------------------------------
from typing_extensions import TypedDict
from typing import List


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]

### Nodes

from langchain.schema import Document


def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]

    # Retrieval
    documents = retriever.get_relevant_documents(question)
    return {"documents": documents, "question": question}


def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    # RAG generation
    
    generation = rag_chain.invoke({"context": documents, "question": question, "VAAA":VAAA})
    return {"documents": documents, "question": question, "generation": generation}

def generategeneral(state):
    print("---generating a general answer---")
    question = state["question"]
    generalgeneration=generalgenerator.invoke({"question":question})
    return{"question":question,"generalgeneration":generalgeneration}

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score["score"]
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    return {"documents": filtered_docs, "question": question}


def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    # Re-write question
    better_question = question_rewriter.invoke({"question": question})
    return {"documents": documents, "question": better_question}


def web_search(state):
    """
    Web search based on the re-phrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with appended web results
    """

    print("---WEB SEARCH---")
    question = state["question"]

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)

    return {"documents": web_results, "question": question}


### Edges ###


def route_question(state):
    """
    Route question to general chat, web search, or RAG (vectorstore).

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    question = state["question"]
    print(f"Question: {question}")
    source = question_router.invoke({"question": question})
    print("Routing Information:", source)
    datasource = source["datasource"]
    print(f"Datasource: {datasource}")

    if datasource == "general":
        print("---ROUTE QUESTION TO GENERAL CHAT---")
        return "general_chat"
    elif datasource == "web_search":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "web_search"
    elif datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    filtered_documents = state["documents"]

    if not filtered_documents:
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print(
            "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
        )
        return "transform_query"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    grade = score["score"]

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score["score"]
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
    
##BUILD Graph ---------------------------------------------------------------------------------------------
from langgraph.graph import END, StateGraph

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("generategeneral",generategeneral)
workflow.add_node("web_search", web_search)  # web search
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)  # transform_query

# Build graph
workflow.set_conditional_entry_point(
    route_question,
    {
        "general":"generategeneral",
        "web_search": "web_search",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("generategeneral",END)
workflow.add_edge("web_search", "generate")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "transform_query",
    },
)

# Compile-----------------------------------------------------------------
app = workflow.compile()

from pprint import pprint

# Run----------------------------------------------------------------------------------
QUESTION = input("Enter your question:              ")
inputs = {"question":  QUESTION}


# Final generation---------------------------------------------------------------------

def final_gen(inputs):
    return app.invoke(inputs)['generation']

pprint(final_gen(inputs))

