import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

### Set up the Strealit app
st.set_page_config(page_title="Text to math problem Solver and Data Search Assistant",page_icon="🔎")
st.title("Text to Math Problem Solver Using Google Gemma 2")

groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")

if not groq_api_key:
    st.info("Please add your groq api key")
    st.stop()

llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

### Initialize the tools
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find the various information on the topics mentioned ")

## Initialize the math tool'

math_chain=LLMMathChain.from_llm(llm=llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answer math related questions. Inly input mathematical expression"

)

prompt="""
You're a agent for solving users mathematical question.Locgically arrive at the solution and dispaly it point wise for the question below
Question:{question}
Answer:"""

prompt_template=PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combining all the tools into chain
chain=LLMChain(llm=llm,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning",
    func=chain.run,
    description="A tool for answerig logic-based and reasoning questions"
)

##Initialize the agents

assistant_agent=initialize_agent(
    tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state['messages']=[{"role":"assistant","content":"Hi, I'm a chatbot who can answer all your mathematical questions"}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

    ## Function to generate the response
    def generatea_response(question):
        response=assistant_agent.invoke({'input':question})
        return response
    

## Lets start the interaction
question=st.text_area("Enter your question:","I have 5 bananas and 7 grapes. I ate 3 bananas and 2 grapes. How many fruits am i left with?")


if st.button("find my answer"):
    if question:
        with st.spinner("Generate response..."):
            st.session_state.messages.append({"roleS":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])

            st.session_state.messages.append({"role":"assistant","content":response})
            st.write('## Response:')
            st.success(response)

    else:
        st.warning("Please enter the question")