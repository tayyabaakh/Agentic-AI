# import os
# import certifi
# import requests
# from dotenv import load_dotenv

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.tools import tool
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain.agents import create_agent


# # LOAD ENVIRONMENT VARIABLES

# os.environ["SSL_CERT_FILE"] = certifi.where()

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# # CHECK API KEYS

# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY is missing from .env")

# if not TAVILY_API_KEY:
#     raise ValueError("TAVILY_API_KEY is missing from .env")

# if not WEATHER_API_KEY:
#     raise ValueError("WEATHER_API_KEY is missing from .env")


# # TAVILY SEARCH TOOL

# search_tool = TavilySearchResults(
#     max_results=2
# )


# # CUSTOM WEATHER TOOL

# @tool
# def get_weather_data(city: str) -> str:
#     """Fetch current weather information for a city."""

# # url = (
# #     f"https://api.weatherstack.com/current?"
# #     f"access_key={WEATHER_API_KEY}&query={city}"
# # )

#     url = "https://api.weatherstack.com/current"

#     params = {
#         "access_key": WEATHER_API_KEY,
#         "query": city
#     }

#     response = requests.get(url, params=params)

#     data = response.json()

#     if "current" not in data:
#         return (
#             f"Could not fetch weather data for {city}. "
#             f"Error: {data.get('error', {}).get('info', 'Unknown error')}"
#         )

#     return (
#         f"City: {city}\n"
#         f"Temperature: {data['current']['temperature']}°C\n"
#         f"Weather: {data['current']['weather_descriptions'][0]}\n"
#         f"Humidity: {data['current']['humidity']}%"
#     )


# # GEMINI LLM

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.1-flash-lite",
#     google_api_key=GOOGLE_API_KEY
# )


# # TOOLS

# tools = [
#     search_tool,
#     get_weather_data
# ]


# # CREATE AGENT

# agent = create_agent(
#     model=llm,
#     tools=tools,
#     system_prompt="""You are a helpful AI agent.

# When answering a question:

# 1. Determine what information is needed.
# 2. Decide which available tool is appropriate.
# 3. Use the tool when necessary.
# 4. Examine the tool result.
# 5. If additional information is needed, use another tool.
# 6. Once you have enough information, provide the final answer.

# Always use the available tools when they are necessary to answer the question accurately.""",

#     debug=True
# )


# # RUN AGENT

# response = agent.invoke(
#     {
#         "messages": [
#             (
#                 "user",
#                 "Find the capital of India and then find its current weather."
#             )
#         ]
#     }
# )


# #  FINAL RESPONSE

# content = response["messages"][-1].content

# if isinstance(content, list):
#     print(content[0]["text"])
# else:
#     print(content)



# ----------------------
# Agent with Streamlit UI
#-----------------------

import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #172554 100%
        );
    }

    /* Main content */
    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .hero {
        padding: 2rem;
        border-radius: 20px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }

    .hero h1 {
        font-size: 2.7rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 1.05rem;
    }

    /* Cards */
    .card {
        padding: 1.2rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .status {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(34,197,94,0.15);
        color: #86efac;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        margin-bottom: 0.8rem;
    }

    /* Input */
    [data-testid="stChatInput"] {
        border-radius: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# ============================================================
# CHECK API KEYS
# ============================================================

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY is missing from your .env file.")
    st.stop()

if not TAVILY_API_KEY:
    st.error("❌ TAVILY_API_KEY is missing from your .env file.")
    st.stop()

if not WEATHER_API_KEY:
    st.error("❌ WEATHER_API_KEY is missing from your .env file.")
    st.stop()


# ============================================================
# WEATHER TOOL
# ============================================================

@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a city."""

    url = "https://api.weatherstack.com/current"

    params = {
        "access_key": WEATHER_API_KEY,
        "query": city,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        data = response.json()

        if "current" not in data:
            return (
                f"Could not fetch weather data for {city}. "
                f"Error: {data.get('error', {}).get('info', 'Unknown error')}"
            )

        return (
            f"City: {city}\n"
            f"Temperature: {data['current']['temperature']}°C\n"
            f"Weather: {data['current']['weather_descriptions'][0]}\n"
            f"Humidity: {data['current']['humidity']}%"
        )

    except Exception as e:
        return f"Weather service error: {str(e)}"


# ============================================================
# CREATE AGENT
# ============================================================

@st.cache_resource
def create_research_agent():

    search_tool = TavilySearchResults(
        max_results=3
    )

    llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY
    )


    tools = [
        search_tool,
        get_weather_data,
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
You are an intelligent AI research assistant.

You have access to web search and weather tools.

When answering a question:

1. Understand what the user is asking.
2. Determine whether external information is required.
3. Use the appropriate tool when necessary.
4. Carefully examine the tool result.
5. If multiple pieces of information are required, perform the necessary tools in sequence.
6. Do not invent information.
7. Use the latest available information when the user asks for current information.
8. Provide a concise and clear final answer.

Always use the available tools when they are necessary.
""",
    )

    return agent


agent = create_research_agent()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 AI Research Agent")

    st.markdown(
        """
        <div class="card">
            <div class="card-title">Agent Status</div>
            <span class="status">● Online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🧰 Available Tools")

    st.markdown(
        """
        **🔎 Tavily Search**

        Search the web for current information.

        **🌤️ Weatherstack**

        Get current weather information.

        **🧠 Gemini**

        Reason over the information and produce the final answer.
        """
    )

    st.divider()

    st.markdown("### 💡 Try asking")

    examples = [
        "What is the capital of India and what is its current weather?",
        "What are the latest AI developments?",
        "Who is the current president of India?",
        "What is the weather in Karachi?",
    ]

    for example in examples:
        if st.button(
            example,
            use_container_width=True,
        ):
            st.session_state.pending_prompt = example

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.caption("Built with LangChain + Gemini + Tavily + Streamlit")


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <h1>🤖 AI Research Agent</h1>

        <p>
        Ask questions and let the agent research, reason,
        search the web and retrieve live weather information.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# HANDLE SIDEBAR EXAMPLE
# ============================================================

prompt = st.chat_input(
    "Ask your AI research agent anything..."
)

if "pending_prompt" in st.session_state:

    if not prompt:
        prompt = st.session_state.pending_prompt

    del st.session_state.pending_prompt


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):

        with st.spinner("🧠 Agent is thinking..."):

            try:

                response = agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                prompt,
                            )
                        ]
                    }
                )

                content = response["messages"][-1].content

                if isinstance(content, list):

                    text_parts = []

                    for block in content:

                        if (
                            isinstance(block, dict)
                            and block.get("type") == "text"
                        ):
                            text_parts.append(
                                block.get("text", "")
                            )

                    final_answer = "\n".join(text_parts)

                else:
                    final_answer = content

            except Exception as e:

                final_answer = (
                    f"❌ **Agent Error**\n\n"
                    f"`{str(e)}`"
                )

        st.markdown(final_answer)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer,
        }
    )