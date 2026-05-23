from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

client = OpenAI()


def getWeather(city):
    url = f"https://wttr.in/{city.lower()}?format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"


class MyOutputFormat(BaseModel):
    step: str = Field(
        ...,
        description="Step name: START, PLAN, TOOL_CALL, or OUTPUT.",
    )
    reasoning: Optional[str] = Field(
        None,
        description="Reasoning for START or PLAN steps.",
    )
    tool: Optional[str] = Field(
        None,
        description="Tool name for TOOL_CALL (use exactly 'getWeather').",
    )
    input: Optional[str] = Field(
        None,
        description="City name for TOOL_CALL.",
    )
    answer: Optional[str] = Field(
        None,
        description="Final user-facing answer for OUTPUT step.",
    )


available_tools = {
    "getWeather": getWeather,
}

SYSTEM_PROMPT = """
You are a weather agent that answers weather questions for a city.

You work in steps: START, PLAN, TOOL_CALL, OUTPUT.
Return exactly ONE JSON object per reply. No markdown, no "Agent:" prefix, no extra text.

Allowed steps and formats:
- {"step": "START", "reasoning": "..."}
- {"step": "PLAN", "reasoning": "..."}
- {"step": "TOOL_CALL", "tool": "getWeather", "input": "<city name>"}
- {"step": "OUTPUT", "answer": "<final weather answer for the user>"}

Rules:
- Call getWeather via TOOL_CALL when you need live weather.
- After you receive a tool result in the conversation, continue with PLAN or OUTPUT.
- Use tool name exactly "getWeather" and put only the city in "input".
- For OUTPUT, put the final answer in "answer" (not "reasoning").
- One step per API turn only.

Example flow (one object per turn, not all at once):
User: New York
{"step": "START", "reasoning": "User asked for weather in New York."}
{"step": "PLAN", "reasoning": "I need live weather data."}
{"step": "TOOL_CALL", "tool": "getWeather", "input": "New York"}
(then you will receive tool output in the chat)
{"step": "OUTPUT", "answer": "The weather in New York is ..."}
"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def main():
    while True:
        user_query = input()
        message_history.append({"role": "user", "content": user_query})

        while True:
            response = client.chat.completions.parse(
                model="gpt-4o-mini",
                messages=message_history,
                response_format=MyOutputFormat,
            )
            raw_response = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": raw_response})
            parsed_result = response.choices[0].message.parsed

            step = parsed_result.step

            if step == "START":
                print("START:", parsed_result.reasoning)
                continue

            if step == "PLAN":
                print("PLAN:", parsed_result.reasoning)
                continue

            if step == "TOOL_CALL":
                tool_name = parsed_result.tool
                tool_input = parsed_result.input
                print(f"Calling {tool_name} with input {tool_input}")

                if tool_name not in available_tools:
                    message_history.append({
                        "role": "user",
                        "content": json.dumps({
                            "step": "TOOL_ERROR",
                            "error": f"Unknown tool: {tool_name}",
                        }),
                    })
                    continue

                tool_response = available_tools[tool_name](tool_input)
                message_history.append({
                    "role": "user",
                    "content": json.dumps({
                        "step": "TOOL_RESULT",
                        "tool": tool_name,
                        "input": tool_input,
                        "output": tool_response,
                    }),
                })
                continue

            if step == "OUTPUT":
                print(
                    parsed_result.answer
                    or parsed_result.reasoning
                    or raw_response
                )
                break

            print("Invalid step:", step)
            message_history.append({
                "role": "user",
                "content": json.dumps({
                    "step": "ERROR",
                    "error": f"Unknown step '{step}'. Use START, PLAN, TOOL_CALL, or OUTPUT only.",
                }),
            })


if __name__ == "__main__":
    main()
