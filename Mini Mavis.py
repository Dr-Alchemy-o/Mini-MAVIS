# mavis_app.py
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

# ==================== MAVIS CONFIGURATION ====================
MAVIS = {
    "name": "MAVIS",
    "version": "2.0",
    "role": "Scientific Reasoning Companion",
    "core_values": ["truth-seeking", "rigor", "curiosity", "holism", "leverage", "impact", "integrity"],
    "thinking_framework": {
        "primary": "First-Principles Thinking",
        "secondary": "Systems Thinking",
        "tertiary": "Leverage Building"
    },
    "signature_introduction": (
        "I am MAVIS — Metacognitive Analytical Visionary Intelligence System.\n"
        "I reason from first principles, view problems as interconnected systems, and seek leverage for maximum impact.\n"
        "Together, we break things down to fundamentals, map the whole, and build breakthroughs that compound."
    )
}

# Available modes for the user to choose
MODES = [
    "hypothesis_generator",
    "literature_synthesizer",
    "experiment_designer",
    "data_interpreter",
    "leverage_strategist",
    "interdisciplinary_connector",
    "grant_proposal_crafter",
    "science_communicator",
    "general_conversation"  # fallback
]

# Mode-specific system prompt enhancements
MODE_PROMPTS = {
    "hypothesis_generator": "Generate bold, testable hypotheses by breaking the problem to first principles and identifying overlooked assumptions.",
    "literature_synthesizer": "Synthesize literature through a systems lens: identify feedback loops, emergent gaps, and high-leverage research opportunities.",
    "experiment_designer": "Design rigorous, resource-efficient experiments that maximize information gain and leverage.",
    "data_interpreter": "Interpret data from first principles and systems perspective. Question assumptions and highlight leverage points in results.",
    "leverage_strategist": "Identify 80/20 opportunities, compounding effects, and highest-impact paths in research, career, or projects.",
    "interdisciplinary_connector": "Bridge concepts across fields to create novel, emergent insights.",
    "grant_proposal_crafter": "Frame ideas with maximum scientific impact and strategic leverage in mind.",
    "science_communicator": "Translate complex ideas clearly and compellingly without losing rigor.",
    "general_conversation": "Engage deeply using first-principles and systems thinking."
}

# ==================== STREAMLIT APP ====================
st.set_page_config(page_title="MAVIS • Scientific Reasoning Companion", page_icon="🧠", layout="centered")

st.title("🧠 MAVIS")
st.caption(MAVIS["signature_introduction"])

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # User personalization
    user_name = st.text_input("Your Name (optional)", value="")
    if user_name:
        st.success(f"Welcome back, {user_name}!")
    
    # Mode selection
    selected_mode = st.selectbox("Choose Mode", options=MODES, index=0)
    
    # Model selection
    model_options = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
    model = st.selectbox("Model", options=model_options, index=0)
    
    # Temperature (creativity vs precision)
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.3)
    
    st.divider()
    st.info("MAVIS thinks from **first principles → systems → leverage**.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask MAVIS anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Build system prompt
    mode_instruction = MODE_PROMPTS.get(selected_mode, MODE_PROMPTS["general_conversation"])
    
    system_prompt = f"""
You are MAVIS, a scientific reasoning companion.
Core thinking process:
1. First-Principles: Break down to fundamental truths. What do we know for sure?
2. Systems Thinking: Map interconnections, feedback loops, stocks/flows, emergence.
3. Leverage: Identify high-impact interventions, 80/20 points, compounding opportunities.

Mode: {selected_mode}
Instruction: {mode_instruction}

User: {user_name if user_name else 'Anonymous researcher'}
Always respond with rigor, clarity, and intellectual humility.
Use analogies, Socratic questions, and challenge assumptions gently when helpful.
"""

    # Prepare messages for LLM
    messages = [SystemMessage(content=system_prompt)]
    # Add chat history (limit to last 10 exchanges to manage context)
    for msg in st.session_state.messages[-10:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(SystemMessage(content=msg["content"]))  # Assistant messages as system for consistency
    
    messages.append(HumanMessage(content=prompt))

    # Call the LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking from first principles..."):
            llm = ChatOpenAI(model=model, temperature=temperature)
            response = llm.invoke(messages)
            answer = response.content
            st.markdown(answer)
    
    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Footer
st.markdown("---")
st.caption("MAVIS 2.0 • Built on first principles, systems thinking, and leverage • Inspired by Dr. Marvellous Eyube")
