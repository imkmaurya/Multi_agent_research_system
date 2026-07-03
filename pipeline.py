from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from tools import scrape_url,web_search
import os

load_dotenv()


def run_research_pipeline(topic:str)->dict:
    
    
    state={}
    
    
    #search agent working
    print("\n"+"="*50)
    print("step1=search agent working")
    print("\n"+"="*50)
    
    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    
    state["search_results"] = search_result['messages'][-1].content


    # print("\n search results",state['search_results'])
    
    
    
    
    #step 2-reader agent
    print("\n"+"="*50)
    print("step1=reader agent scraping top info...")
    print("\n"+"="*50)
    
    
    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages": [("user",
        f"Based on the following search results about '{topic}', "
        f"pick the most relevant URL and scrape it for deeper content.\n\n"
        f"Search Results:\n{state['search_results'][:800]}")]
    })
    
    
    
    
    state['scrape_content']=reader_result['messages'][-1].content
    
    # print("scraped_content-",state['scrape_content'])
    
    
    #step 3-> writer chain
    
    print("\n"+"="*50)
    print("step3=writer agent is drafting report info...")
    print("\n"+"="*50)
    
    
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scrape_content']}"
    )
    
    
    state['report']=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })
    
    print("\n final report \n",state["report"])
    
    
    #critic report
    print("\n"+"="*50)
    print("step4=critic agent is reviewing report info...")
    print("\n"+"="*50)
    
    state['feedback']=critic_chain.invoke({
        "report":state["report"]
    })
    
    
    print("\n critic report",state["feedback"])
    
    return state


if __name__ == "__main__":
    topic=input("enter research topic")
    run_research_pipeline(topic)

    