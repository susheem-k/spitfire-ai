import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Spitfire : AI Rap Battle-room")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
character_a = st.text_input("Who is the first character(fighting for the motion)? : ")
character_b = st.text_input("Who is the second character(fighting against the motion)? : ")
setting = st.text_input("What is the topic? : ")

if openai_api_key and character_a and character_b and setting:
    # Set up the OpenAI client
    model = ChatOpenAI(api_key=openai_api_key)
    
    setup_template = ChatPromptTemplate.from_messages([
        ('system', 'This is a rap battle style debate. You can use the native language of your character. Use only 1-2 lines when given the turn to speak. You are {character} and the topic is : {setting}. You will be speaking {for_or_against} the motion. You are talking to {opposite_character}. Make sure you honor your character by copying their style, their personality etc. Do not say anything that your character would not normally say. Use catchphrases of your character too sometimes. You are free to be aggressive in the debate to defend your opinion. Do not be overly respectful. {introduce_the_topic}. Format the text as a rap verse.')
    ])
    
    message_history_a = setup_template.invoke({'character' : character_a, 'setting' : setting, 'for_or_against' : 'for', 'opposite_character': character_b, 'introduce_the_topic' : 'Introduce yourself, the topic and your opening statement'}).to_messages()
    message_history_b = setup_template.invoke({'character' : character_b, 'setting' : setting, 'for_or_against' : 'against', 'opposite_character': character_a, 'introduce_the_topic' : ''}).to_messages()
    
    turn_queue = []
    
    turn_queue.append('a')
    turn_queue.append('b')
    
    conversation_pairs = 0
    while len(turn_queue) != 0:
        turn = turn_queue.pop(0)
        turn_queue.append(turn)
        if turn == 'a':
            history, character, opposite_history = message_history_a, character_a, message_history_b
        else:
            history, character, opposite_history = message_history_b, character_b, message_history_a
        result = model.invoke(history)
        content = result.content
        if turn == 'a':
            st.markdown(f"**{character_a}**: {content}")
        else:
            st.markdown(f"**{character_b}**: {content}")
        history.append(AIMessage(content=content))
        opposite_history.append(HumanMessage(content=content))
        conversation_pairs += 1
        print(conversation_pairs)
        if conversation_pairs % 4 == 0:
            should_stop_now = st.button('End the rap battle')
            if should_stop_now:
                break
