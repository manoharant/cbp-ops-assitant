import chainlit as cl

suggestions = ["Suggestion 1", "Suggestion 2", "Suggestion 3"]


@cl.on_chat_start
async def start():
    actions = [
        cl.Action(
            name=f"suggestion_{i}",
            label=suggestion,
            payload={"value": suggestion}
        ) for i, suggestion in enumerate(suggestions)
    ]

    await cl.Message(content="Select a suggestion:", actions=actions).send()


@cl.action_callback(r"Suggestion_\d+")
async def on_suggestion(action: cl.Action):
    print(f"User selected: {action.payload['value']}")
    # You can also send a response back to the user here
    await cl.Message(content=f"You selected: {action.payload['value']}").send()
