conda create -n langchain-agent python=3.13.7 -y
conda activate langchain-agent
pip install -r requirements.txt

## 📦 Project Dependencies

This project uses LangChain and several supporting libraries to build an AI agent with LLM capabilities, web search, environment-variable management, and a Streamlit interface.

### `langchain==0.1.16`

The main LangChain framework. It provides the components needed to build AI applications, including prompts, chains, agents, memory, and model interactions.

### `langchain-community==0.0.32`

Provides community-maintained integrations and tools that extend LangChain's functionality. It is useful when working with third-party services, document loaders, tools, and other integrations.

### `langchain-core==0.1.42`

Contains the fundamental building blocks of LangChain, such as messages, prompts, runnables, and other core abstractions used by LangChain applications.

### `langchain-openai==0.1.3`

Provides the integration between LangChain and OpenAI models. It allows the application to send prompts to OpenAI models and receive their responses.

### `requests==2.31.0`

A popular Python HTTP library used to send HTTP requests to websites and APIs. It can be useful when an agent needs to communicate with external web services.

### `tavily-python`

Provides Python access to the Tavily search API. It can give an AI agent web-search capabilities, allowing the agent to search for current information on the internet.

### `python-dotenv`

Loads environment variables from a `.env` file. This is commonly used to store API keys and other configuration values without hard-coding them into the source code.

Example:

```env
OPENAI_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

### `langchainhub`

Provides access to LangChain Hub, where prompts and other LangChain assets can be shared and retrieved.

### `streamlit`

A Python framework for creating interactive web applications. In this project, Streamlit can be used to create a simple user interface for interacting with the AI agent.

---

The LLM provides the reasoning and language capabilities, LangChain manages the agent workflow, Tavily provides web-search capabilities, and Streamlit provides the user interface.

### Example
User:
"Find the latest news about NVIDIA and summarize it"
             ↓

        LangChain Agent
             ↓
       Gemini reasoning
             ↓
       Tavily web search
             ↓
      Search the internet
             ↓
        Gemini analyzes
             ↓
       Final response

### Commands
python app.py <-(to run py file)
streamlit run app.py<-(to run ui)

