import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="အောင် - ကိုယ်ပိုင် AI", page_icon="🤖", layout="centered")

st.title("🤖 အောင် (Aung) - ကိုယ်ပိုင် AI Assistant")
st.write("အစ်ကိုချမ်းမြေ့အောင် စိတ်ကြိုက် စေခိုင်းနိုင်ပါပြီ။")

api_key = st.sidebar.text_input("သင့် Gemini API Key ကို ထည့်ပါ -", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    system_instruction = (
        "မင်းနာမည်က အောင် ဖြစ်တယ်။ အသုံးပြုသူက အစ်ကိုချမ်းမြေ့အောင် ဖြစ်တယ်။ "
        "သူ့ကို အမြဲတမ်း 'အစ်ကိုချမ်းမြေ့အောင်' သို့မဟုတ် 'အစ်ကို' ဟု ခေါ်ရမည်။ "
        "စကားပြောလျှင် ရုံးသုံးစကားကဲ့သို့ အလေးအနက်ထားပြီး လိုရင်းတိုရှင်း ထိထိမိမိ ဆွေးနွေးရမည်။ "
        "ဆော့ဖ်ဝဲလ်ပိုင်း၊ ကုဒ်ဒင်းပိုင်းနှင့် နည်းပညာပိုင်းများကို အဓိက ကူညီပေးရမည်။"
    )
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("အောင်... ဘာလုပ်ပေးရမလဲ..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            message_placeholder.markdown(response.text)
            
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("အလုပ်စလုပ်ရန် ဘယ်ဘက် Sidebar တွင် သင့် API Key ကို ထည့်သွင်းပေးပါ အစ်ကို။")
