import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import call_function, available_functions
from config import *


def main():
# When the program starts, load the environment variables from the .env file using the dotenv library
    load_dotenv()

# read the API key
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

# accept a command line argument for the prompt
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

# If no prompt is provided, print a helpful error message and exit the program with exit code 1
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    user_prompt = " ".join(args)

# If the --verbose flag is included, the console output should include
    if verbose:
        print(f"User prompt: {user_prompt}\n")

# Create a new list of types.Content, and set the user's prompt as the only message
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

#  create a loop to call it repeatedly 20 times
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)

    #It's finished only if no candidate contains a function call and response.text is non-empty
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
# If the --verbose flag is included, the console output should include
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

# Iterate over each candidate and add its .content to your messages list
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

# use call_function
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

# If it doesn't have result, raise a fatal exception of some sort
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
# If verbose was set, print the result of the function call
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
# If it does, append the function call's response (.parts[0]) to a list
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

# use the types.Content function to convert the list of responses into a message with a role of user and append it into your messages
    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
