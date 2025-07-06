import os
import json
import time
from langchain.memory import ConversationBufferMemory
from langchain.schema import message_to_dict, messages_from_dict

MEMORYFILE = "data/chat_memory.json"
MEMORY_EXPIRE = 24

def is_memory_expired() -> bool:
    """
    Check if the memory file is expired based on the last modified time.
    
    Returns:
        bool: True if the memory file is expired, False otherwise.
    """
    if not os.path.exists(MEMORYFILE):
        return True
    last_modified = os.path.getmtime(MEMORYFILE)
    current_time = os.path.getmtime(__file__)
    return (current_time - last_modified) > MEMORY_EXPIRE * 3600

# get memory fron ConversationBufferMemory
def get_memory() -> ConversationBufferMemory:
    """
    Get the conversation memory for the agent.
    
    Returns:
        ConversationBufferMemory: The conversation memory instance.
    """

    memory =  ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="input",
        output_key="output"
    )
    if not is_memory_expired():
        try:
            with open(MEMORYFILE, "r") as f:
                memory_data = json.load(f)
                memory.chat_memory.messages = messages_from_dict(memory_data["messages"])
        except (FileNotFoundError, json.JSONDecodeError):
            print("Memory file not found. Start Fresh.")
            pass  # If the file doesn't exist or is corrupted, start with an empty memory
    return memory

# Save memory with timestamp
def save_memory(memory: ConversationBufferMemory):
    """
    Save the conversation memory to a file.
    
    Args:
        memory (ConversationBufferMemory): The conversation memory to save.
    """
    memory_data = {
        "timestamp": time.time(),
        "messages": [message_to_dict(msg) for msg in memory.chat_memory.messages]
    }
    with open(MEMORYFILE, "w") as f:
        json.dump(memory_data, f, indent=4)
    print(f"Memory saved to {MEMORYFILE}")