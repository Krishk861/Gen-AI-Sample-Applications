import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

## Streamlit app
st.set_page_config(page_title="Langchain : Summarize text from youtube or website",page_icon="🦜")
st.title("🦜 Langchain: Summarize text from yt or website")
st.subheader('Summarize URL')

## Get the Groq API Key and url to be summarized
with st.sidebar:
    groq_api_key=st.text_input("Groq API Key",value=" ",type="password")

generic_url=st.text_input("URL",label_visibility="collapsed")

##Gemma model
llm=ChatGroq(model="Gemma-7b-It",groq_api_key=groq_api_key)
prompt_template="""Provide a summary of the following content in 300 words
content:{text}"""
prompt=PromptTemplate(template=prompt_template,input_variables=['Text'])
if st.button("Summarize the content from YT or website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the info")
    elif not validators.url(generic_url):
        st.error("Please enter a valid url. It can be a YT video or website url")

    else:
        try:
            with st.spinner("waiting...."):
                ## Loading yt video or website
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,headers={"User-Agent": "Moxilla/5.0 (Macintosh; Intel Mac OS X 13_5_1))"})
                docs=loader.load()

                ## Chain fro summarization
                chain=load_summarize_chain(llm,mchain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.Exception(f"Exceptiom:{e}")