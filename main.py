from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_LLM, contextForLlm
from note import note_engine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from pdf import startup_engine

load_dotenv()

myAPIkey = os.environ["OPENAI_API_KEY"]

startupDataPATH = os.path.join("data","population.csv" )

# Data directoruy and file polulation.csv
startup_df = pd.read_csv("/Users/pragalvhasharma/Downloads/Prag GO to Documents/Comp Sci/MY Projects/LLamaIndexRag Agent/env/Data/startupData.csv")

#Creating Query Engine
startup_query_engine = PandasQueryEngine(
    df=startup_df, verbose = True, instruction_str = instruction_LLM )

startup_query_engine.update_prompts({"pandas_prompt": new_prompt})
##population_query_engine.query("What is the population of Canada?")

#List of Tools LLM has acess to 
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=startup_query_engine,
        metadata=ToolMetadata(
            name="startup_data",
            description="this gives important information about startups such as (Company,Valuation ($B),Date Joined,Country,City,Industry,Select Investors)",
        ),
    ),
    QueryEngineTool(
        query_engine=startup_engine,
        metadata=ToolMetadata(
            name="lecture_data",
            description="this gives advice based on lecture.pdf about startups",
        ),
    ),
]

llm = OpenAI(model = "gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context= contextForLlm) #Context tells agent before hand what its supposed to be doing


try:
    prompt = input("Enter a prompt (q to quit):")
    while prompt != "q":
        result = agent.query(prompt)
        print(result)
        prompt = input("Enter a prompt (q to quit):")
except ValueError as e:
    response = str(e)
    if not response.startswith("Could not parse LLM output: `"):
        raise e
    response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
    prompt = input("Enter a prompt (q to quit):")
    while prompt != "q":
        result = agent.query(prompt)
        print(result)
        prompt = input("Enter a prompt (q to quit):")





