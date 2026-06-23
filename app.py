import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

st.set_page_config(page_title="Image Captioner", page_icon="🖼️", layout="centered")
st.title("Standard AI Image Description Generator")
st.write("Upload an image to get a standard descriptive caption.")

# 1. Load the BLIP model
@st.cache_resource
def load_model():
    model_id = "Salesforce/blip-image-captioning-base"
    processor = BlipProcessor.from_pretrained(model_id)
    
    model = BlipForConditionalGeneration.from_pretrained(
        model_id, 
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    return processor, model

with st.spinner("Initializing model..."):
    processor, model = load_model()

# 2. Upload Interface
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    # Display the uploaded image
    st.image(image, width=450, caption="Uploaded Image")
    
    if st.button("Generate Caption", type="primary"):
        with st.spinner("Analyzing image..."):
            try:
                # Preprocess image structure
                inputs = processor(images=image, return_tensors="pt")
                
                # Generate a normal description using standard generation settings
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs, 
                        max_length=200,       # Increased to allow full, normal sentences
                        min_length=15,       # Prevents the model from cutting off too early
                        num_beams=3,         # Searches for better word combinations for higher quality
                        early_stopping=True  # Safely stops when the full sentence is naturally finished
                    )
                
                # Decode output back into text
                caption = processor.decode(outputs[0], skip_special_tokens=True)
                
                st.success(f"**Result:** {caption.capitalize()}")
                
            except Exception as e:
                st.error(f"Error: {e}")