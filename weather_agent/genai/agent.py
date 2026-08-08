import os
import json

from dotenv import load_dotenv
from google import genai

from prompts import SYSTEM_PROMPT
from tools import get_weather

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


TOOLS = {"get_weather": get_weather}


MODEL_NAME = os.getenv("MODEL_NAME")


def ask_model(messages):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.2,
        },
    )

    return response.text


def parse_response(response_text):

    if not response_text:
        raise ValueError("Gemini returned an empty response.")

    response_text = response_text.strip()

    print("\nRAW RESPONSE:")
    print(response_text)

    # Remove markdown JSON fences if Gemini adds them
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    return json.loads(response_text)


def run_agent(user_input):

    messages = [{"role": "user", "parts": [{"text": user_input}]}]

    while True:

        response_text = ask_model(messages)

        result = parse_response(response_text)

        print("\nAGENT:")
        print(json.dumps(result, indent=2))

        step = result.get("step")

        # ---------------------------------
        # PLAN
        # ---------------------------------

        if step == "PLAN":

            messages.append({"role": "model", "parts": [{"text": response_text}]})

            # Tell the model to continue
            messages.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "Continue to the next step. "
                                "Follow the workflow and return "
                                "exactly one valid JSON step."
                            )
                        }
                    ],
                }
            )

        # ---------------------------------
        # TOOL
        # ---------------------------------

        elif step == "TOOL":

            tool_name = result.get("tool")
            tool_input = result.get("input")

            print(f"\nTOOL CALL: {tool_name}")
            print(f"INPUT: {tool_input}")

            if tool_name not in TOOLS:
                raise ValueError(f"Unknown tool: {tool_name}")

            tool_function = TOOLS[tool_name]

            tool_result = tool_function(tool_input)

            print("\nOBSERVE:")
            print(tool_result)

            # Add model's tool request
            messages.append({"role": "model", "parts": [{"text": response_text}]})

            # Add tool result
            messages.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": json.dumps(
                                {
                                    "step": "OBSERVE",
                                    "tool": tool_name,
                                    "output": tool_result,
                                }
                            )
                        }
                    ],
                }
            )

        # ---------------------------------
        # OUTPUT
        # ---------------------------------

        elif step == "OUTPUT":

            return result.get("content", "")

        # ---------------------------------
        # UNKNOWN
        # ---------------------------------

        else:

            raise ValueError(f"Invalid step returned by Gemini: {step}")
