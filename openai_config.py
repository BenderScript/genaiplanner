import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI



class OpenAIConfig:
    """
    A class to configure and initialize an OpenAI or Azure OpenAI chat model based on environment variables.

    This class reads environment variables to determine whether to configure an OpenAI or Azure OpenAI model.
    It supports both standard OpenAI API and Azure OpenAI services. It attempts to load configuration from
    `.env` or `.env.azure` files, if available.

    Attributes:
        chat_model (ChatOpenAI | AzureChatOpenAI | None): The initialized chat model instance, either
            from OpenAI or Azure OpenAI, or None if initialization fails.

    Methods:
        load_env_file():
            Loads environment variables from `.env` or `.env.azure` files. Raises a FileNotFoundError
            if neither file is found.
        
        create():
            Initializes the chat model based on the environment variables. Supports both OpenAI and Azure
            OpenAI configurations. Raises ValueError if required environment variables are missing.

    Raises:
        FileNotFoundError: If neither `.env` nor `.env.azure` files are found.
        ValueError: If required environment variables for either OpenAI or Azure OpenAI are missing.

    Example:
        config = OpenAIConfig()
        # This will automatically load environment variables and initialize the chat_model based on the environment.
        # If the OPENAI_API_KEY is set, an instance of ChatOpenAI will be created.
        # If the AZURE_OPENAI_API_KEY is set, an instance of AzureChatOpenAI will be created.
    """

    def __init__(self,  *args, **kwargs):
        super().__init__(**kwargs)
        self.chat_model = None
        self.load_env_file()
        self.create()

    @staticmethod
    def load_env_file():
        # Try to find and load the default .env file first
        env_path = find_dotenv()
        if env_path != "":
            load_dotenv(dotenv_path=env_path, override=True)
        else:
            # If the default .env file is not found, try to find and load .env.azure
            env_azure_path = find_dotenv(".env.azure")
            if env_azure_path:
                load_dotenv(dotenv_path=env_azure_path, override=True)
            else:
                raise FileNotFoundError("Neither .env nor .env.azure files were found")

    def create(self, *args, **kwargs):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")

        if openai_api_key:
            required_env_vars = [
                "OPENAI_API_KEY",
                "OPENAI_MODEL_NAME"
            ]

            missing_vars = [var for var in required_env_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"The following environment variables are missing: {', '.join(missing_vars)}")
            self.chat_model = ChatOpenAI(api_key=openai_api_key, model=os.getenv("OPENAI_MODEL_NAME"), temperature=0)
        elif azure_openai_api_key:
            required_env_vars = [
                "AZURE_OPENAI_ENDPOINT",
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_DEPLOYMENT",
                "AZURE_OPENAI_API_VERSION"
            ]

            missing_vars = [var for var in required_env_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"The following environment variables are missing: {', '.join(missing_vars)}")

            # Handle Azure-specific initialization here
            self.chat_model = AzureChatOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                              api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                              deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                                              openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                                              max_tokens=4096)
        else:
            raise ValueError("Neither OPENAI_API_KEY nor AZURE_OPENAI_API_KEY is set in the environment variables")
