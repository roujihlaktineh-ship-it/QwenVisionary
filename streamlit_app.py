import streamlit as st
import os
from pathlib import Path
from huggingface_hub import InferenceClient
from PIL import Image
import io
import base64
import requests

# Load HF_TOKEN from .env
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Initialize Hugging Face client
hf_token = os.environ.get("HF_TOKEN")
client = InferenceClient(api_key=hf_token)

# Page config
st.set_page_config(page_title="Qwen Vision Chatbot", layout="wide")
st.title("🎨 Qwen Vision Chatbot")
st.markdown("Convert between text and images using Qwen AI Model")

# Sidebar for mode selection
mode = st.sidebar.radio(
    "Select Task:",
    ["📝 Image to Text", "🎨 Text to Image"],
    help="Choose what you want to do"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.subheader("Chat History")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.write(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message.get("caption", ""))

# Main content area
st.subheader(mode)

if mode == "📝 Image to Text":
    st.write("Upload an image and I'll describe it for you!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "gif", "webp"])
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("🔍 Analyze Image", key="analyze_btn"):
            with st.spinner("Analyzing image..."):
                try:
                    # Convert image to base64 for API
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
                    
                    # Call Qwen model for image analysis
                    stream = client.chat.completions.create(
                        model="Qwen/Qwen3.5-9B:together",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Describe this image in detail. What do you see?"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_base64}"
                                        }
                                    }
                                ]
                            }
                        ],
                        stream=True,
                    )
                    
                    # Stream response
                    response_text = ""
                    response_placeholder = st.empty()
                    
                    for chunk in stream:
                        if chunk.choices and len(chunk.choices) > 0:
                            if chunk.choices[0].delta.content:
                                response_text += chunk.choices[0].delta.content
                                response_placeholder.write(response_text)
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "user",
                        "type": "image",
                        "content": image,
                        "caption": "Uploaded Image"
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "text",
                        "content": response_text
                    })
                    
                except Exception as e:
                    st.error(f"Error analyzing image: {str(e)}")

elif mode == "🎨 Text to Image":
    st.write("Describe an image and I'll generate it or create a detailed visual concept for you!")
    
    prompt = st.text_area("Enter your image description:", placeholder="Describe the image you want to generate...", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        generation_mode = st.radio(
            "Generation Mode:",
            ["Text-to-Image (via AI)", "Visual Concept (via Qwen)"]
        )
    
    if st.button("🎨 Generate", key="generate_btn"):
        if prompt.strip():
            if generation_mode == "Text-to-Image (via AI)":
                with st.spinner("Generating image from your description..."):
                    try:
                        # Try text-to-image generation
                        model_name = "stabilityai/stable-diffusion-2-1"
                        st.info("⏳ Generating image, this may take 30-60 seconds...")
                        
                        image_bytes = client.text_to_image(
                            prompt=prompt,
                            model=model_name
                        )
                        
                        # Display generated image
                        generated_image = Image.open(io.BytesIO(image_bytes))
                        st.image(generated_image, caption=f"Generated: {prompt}")
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "user",
                            "type": "text",
                            "content": f"Generate: {prompt}"
                        })
                        st.session_state.messages.append({
                            "role": "assistant",
                            "type": "image",
                            "content": generated_image,
                            "caption": f"Generated image for: {prompt}"
                        })
                        
                        st.success("✅ Image generated successfully!")
                        
                    except Exception as e:
                        error_msg = str(e)
                        st.warning("⚠️ Image generation temporarily unavailable. Generating visual concept instead...")
                        
                        # Fallback to text-based visual concept
                        try:
                            stream = client.chat.completions.create(
                                model="Qwen/Qwen3.5-9B:together",
                                messages=[
                                    {
                                        "role": "user",
                                        "content": f"Create a detailed visual concept description for this image: {prompt}\n\nProvide:\n1. Overall composition\n2. Color palette\n3. Objects and elements\n4. Style and mood\n5. Suggested photographic details"
                                    }
                                ],
                                stream=True,
                            )
                            
                            response_text = ""
                            response_placeholder = st.empty()
                            
                            for chunk in stream:
                                if chunk.choices and len(chunk.choices) > 0:
                                    if chunk.choices[0].delta.content:
                                        response_text += chunk.choices[0].delta.content
                                        response_placeholder.write(response_text)
                            
                            # Add to chat history
                            st.session_state.messages.append({
                                "role": "user",
                                "type": "text",
                                "content": f"Generate: {prompt}"
                            })
                            st.session_state.messages.append({
                                "role": "assistant",
                                "type": "text",
                                "content": response_text
                            })
                            
                            st.info("💡 Generated a detailed visual concept instead. Use this as inspiration for your own image generation.")
                            
                        except Exception as concept_error:
                            st.error(f"❌ Could not generate concept: {str(concept_error)}")
            
            else:  # Visual Concept mode
                with st.spinner("Creating detailed visual concept..."):
                    try:
                        stream = client.chat.completions.create(
                            model="Qwen/Qwen3.5-9B:together",
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"Create a detailed visual concept description for this image: {prompt}\n\nProvide:\n1. Overall composition\n2. Color palette\n3. Objects and elements\n4. Style and mood\n5. Suggested photographic details\n6. Lighting and atmosphere"
                                }
                            ],
                            stream=True,
                        )
                        
                        response_text = ""
                        response_placeholder = st.empty()
                        
                        for chunk in stream:
                            if chunk.choices and len(chunk.choices) > 0:
                                if chunk.choices[0].delta.content:
                                    response_text += chunk.choices[0].delta.content
                                    response_placeholder.write(response_text)
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "user",
                            "type": "text",
                            "content": f"Visual Concept: {prompt}"
                        })
                        st.session_state.messages.append({
                            "role": "assistant",
                            "type": "text",
                            "content": response_text
                        })
                        
                        st.success("✅ Visual concept created!")
                        
                    except Exception as e:
                        st.error(f"❌ Error creating concept: {str(e)}")
        else:
            st.warning("Please enter a description first!")

# Sidebar with options
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings")
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.markdown("""
**Qwen Vision Chatbot** uses:
- **Qwen/Qwen3.5-9B** model for text and image analysis
- **Streamlit** for the UI
- **Hugging Face Hub** for API access
""")
