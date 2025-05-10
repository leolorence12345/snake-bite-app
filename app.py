# import streamlit as st
# import pandas as pd
# from PIL import Image
# import matplotlib.pyplot as plt
# import gspread
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from metadata import LOCATION_OPTIONS, TIME, SEASON, PLACE, LOCAL_SYMPTOMS, SYSTEMATIC_SYMPTOMS

# # ------------------ GOOGLE AUTH ------------------
# creds_dict = st.secrets["connections"]["gsheets"]
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
# gc = gspread.authorize(creds)
# drive_service = build('drive', 'v3', credentials=creds)
# spreadsheet = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
# worksheet = spreadsheet.worksheet("Snake")
# existing_data = pd.DataFrame(worksheet.get_all_records())

# # ------------------ STREAMLIT UI ------------------
# st.title("🐍 Snake Bite Management Portal")

# st.markdown("""
#     <style>
#     body, .stApp { background-color: #0b3d0b; color: #e0e0e0; }
#     .stApp h1 { color: #b0f2b4; font-family: 'Trebuchet MS', sans-serif; text-shadow: 1px 1px 4px #000; }
#     label, .css-1cpxqw2, .css-1aumxhk, .css-1p05t8e { color: #d4f0c0 !important; font-weight: bold; }
#     div.stButton > button, .upload-btn label { background-color: #3e5f47; color: white; padding: 0.5em 1em; border-radius: 12px; font-weight: bold; border: none; cursor: pointer; transition: 0.3s; width: 100%; }
#     div.stButton > button:hover, .upload-btn label:hover { background-color: #66bb6a; color: black; }
#     .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect { background-color: #184c18 !important; color: #ffffff !important; border-radius: 10px; border: 1px solid #4caf50; }
#     img { border: 4px solid #4caf50; border-radius: 10px; }
#     .stAlert-success { background-color: #4caf50; color: white; }
#     .stAlert-warning { background-color: #ff9800; color: white; }
#     .upload-btn input[type="file"] { display: none; }
#     .stFileUploader label { display: none; }
#     </style>
# """, unsafe_allow_html=True)

# def combine_symptom_values(selected_symptoms, symptom_dict):
#     if "No Symptoms" in selected_symptoms:
#         return [0, 0, 0, 0]
#     result = None
#     for symptom in selected_symptoms:
#         values = symptom_dict[symptom]
#         result = values if result is None else [sum(x) for x in zip(result, values)]
#     return result

# def upload_to_drive(temp_filename):
#     file_metadata = {'name': temp_filename}
#     media = MediaFileUpload(temp_filename, mimetype='image/jpeg')
#     uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     drive_service.permissions().create(fileId=uploaded_file['id'], body={'type': 'anyone', 'role': 'reader'}).execute()
#     return f"https://drive.google.com/uc?id={uploaded_file['id']}"


# action = st.selectbox("Choose an Action", ["Snake Bite Detection", "Admin"])

# # -----------------------------------------------------------------------------------------------------

# if action == "Admin":
#     st.markdown("## 🔐 Admin Access Required")

#     if "authenticated" not in st.session_state:
#         st.session_state.authenticated = False

#     if not st.session_state.authenticated:
#         password = st.text_input("Enter Password", type="password", placeholder="Password", help="Only authorized personnel")
#         if st.button("Unlock"):
#             if password == st.secrets["admin"]["password"]:

#                 st.session_state.authenticated = True
#                 st.rerun()
#             else:
#                 st.error("❌ Incorrect password.")
#         # Stop here so no other UI elements render
#         st.stop()

#     # Show data only if authenticated
#     st.success("✅ Access granted.")
#     st.dataframe(existing_data)

# # ------------------ STATE INIT ------------------
# if "submitted" not in st.session_state:
#     st.session_state.submitted = False
#     st.session_state.predicted_species = ""
#     st.session_state.image_url = ""
#     st.session_state.record = {}

# # ------------------ PAGE 1: Snake Bite Detection ------------------
# if not st.session_state.submitted:
#     st.markdown("Upload or capture an image of the bite area:")
#     if "show_camera" not in st.session_state:
#         st.session_state.show_camera = False

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Open Camera"):
#             st.session_state.show_camera = True
#     with col1:
#         if st.session_state.show_camera:
#             captured_image = st.camera_input("Take a photo using camera")
#         else:
#             captured_image = None
#     with col2:
#         uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
#         st.markdown('<label class="upload-btn" for="file_uploader"></label>', unsafe_allow_html=True)

#     with st.form("snakebite_form"):
#         district = st.selectbox("Location of the bite*", list(LOCATION_OPTIONS), index=None)
#         time = st.selectbox("Time of the bite*", list(TIME), index=None)
#         season = st.selectbox("Season during bite*", list(SEASON), index=None)
#         place = st.selectbox("Where did the bite happen*", list(PLACE), index=None)
#         local_symptoms = st.multiselect("Local symptoms*", list(LOCAL_SYMPTOMS))
#         sys_symptoms = st.multiselect("Systematic symptoms", list(SYSTEMATIC_SYMPTOMS))
#         notes = st.text_area("Additional Notes")
#         submit = st.form_submit_button("Submit Snake Bite Details")

#     if submit:
#         if None in [district, time, season, place] or not local_symptoms:
#             st.warning("Fill all required fields.")
#         else:
#             # Calculate probabilities
#             weights = [0.8, 0.4, 0.4, 0.5, 0.6, 0.8]
#             vals = [
#                 LOCATION_OPTIONS[district],
#                 TIME[time],
#                 SEASON[season],
#                 PLACE[place],
#                 combine_symptom_values(local_symptoms, LOCAL_SYMPTOMS),
#                 combine_symptom_values(sys_symptoms, SYSTEMATIC_SYMPTOMS),
#             ]
#             scores = [sum(x * w for x, w in zip(v, weights)) for v in zip(*vals)]
#             total = sum(scores)
#             probs = [(v / total) * 100 for v in scores]
#             labels = ["Monocled Cobra", "Spectacled Cobra", "Russell's Viper", "Krait Species"]
#             idx = probs.index(max(probs))
#             prediction = labels[idx]

#             # Save image
#             image_to_save = captured_image or uploaded_image
#             image_url = ""
#             if image_to_save:
#                 img = Image.open(image_to_save).convert("RGB")
#                 file = f"bite_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.jpg"
#                 img.save(file)
#                 image_url = upload_to_drive(file)

#             st.session_state.predicted_species = prediction
#             st.session_state.image_url = image_url
#             st.session_state.record = {
#                 "District": district,
#                 "Time": time,
#                 "Season": season,
#                 "Place": place,
#                 "Local symptoms": ", ".join(local_symptoms),
#                 "Systematic symptoms": ", ".join(sys_symptoms),
#                 "Prediction": prediction,
#                 "Image URL": image_url,
#                 "Notes": notes
#             }
#             st.session_state.submitted = True
#             st.rerun()

# # ------------------ PAGE 2: Clinical Review ------------------
# else:
#     species = st.session_state.predicted_species
#     image_url = st.session_state.image_url
#     record = st.session_state.record

#     st.header(f"Predicted Snake: 🐍 {species}")
#     # safe_species = species.lower().replace("'", "").replace(" ", "_")
#     img_path = f"images/{species.lower().replace(' ', '_')}.jpg"

#     try:
#         st.image(img_path, caption=species, use_container_width=True)
#     except:
#         st.warning("No reference image available.")

#     st.markdown("### Enter Clinical Diagnosis:")
#     clinical_name = st.text_input("🩺 Clinical Snake Identification*", placeholder="Enter confirmed species")
#     clinical_notes = st.text_area("Additional Clinical Notes (optional)")

#     if st.button("Save Final Record"):
#         if not clinical_name.strip():
#             st.error("Please enter the clinical snake identification.")
#         else:
#             final_entry = {
#                 **record,
#                 "Clinical Snake": clinical_name.strip(),
#                 "Clinical Notes": clinical_notes.strip(),
#             }
#             updated_df = pd.concat([existing_data, pd.DataFrame([final_entry])], ignore_index=True)
#             updated_df = updated_df.replace([pd.NA, None, float('inf'), float('-inf')], "").fillna("")
#             worksheet.clear()
#             worksheet.update([updated_df.columns.tolist()] + updated_df.values.tolist())
#             st.success("✅ Final record saved successfully!")
#             st.balloons()

#             # Reset session
#             st.session_state.submitted = False
#             st.rerun()

import streamlit as st
import pandas as pd
from PIL import Image
import random
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from metadata import LOCATION_OPTIONS, TIME, SEASON, PLACE, LOCAL_SYMPTOMS, SYSTEMATIC_SYMPTOMS

# ------------------ GOOGLE AUTH ------------------
creds_dict = st.secrets["connections"]["gsheets"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
gc = gspread.authorize(creds)
drive_service = build('drive', 'v3', credentials=creds)
spreadsheet = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
worksheet = spreadsheet.worksheet("Snake")
existing_data = pd.DataFrame(worksheet.get_all_records())

# ------------------ STYLES ------------------
st.title("🐍 Snake Bite Management Portal")

st.markdown("""
    <style>
    body, .stApp { background-color: #0b3d0b; color: #e0e0e0; }
    .stApp h1 { color: #b0f2b4; font-family: 'Trebuchet MS', sans-serif; text-shadow: 1px 1px 4px #000; }
    label, .css-1cpxqw2, .css-1aumxhk, .css-1p05t8e { color: #d4f0c0 !important; font-weight: bold; }
    div.stButton > button, .upload-btn label { background-color: #3e5f47; color: white; padding: 0.5em 1em; border-radius: 12px; font-weight: bold; border: none; cursor: pointer; transition: 0.3s; width: 100%; }
    div.stButton > button:hover, .upload-btn label:hover { background-color: #66bb6a; color: black; }
    .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect { background-color: #184c18 !important; color: #ffffff !important; border-radius: 10px; border: 1px solid #4caf50; }
    img { border: 4px solid #4caf50; border-radius: 10px; }
    .upload-btn input[type="file"] { display: none; }
    .stFileUploader label { display: none; }
    </style>
""", unsafe_allow_html=True)

# ------------------ HELPERS ------------------
def combine_symptom_values(selected, reference):
    if not selected or "No Symptoms" in selected:
        return [0, 0, 0, 0]
    out = None
    for sym in selected:
        val = reference[sym]
        out = val if out is None else [x + y for x, y in zip(out, val)]
    return out

def upload_to_drive(temp_filename):
    file_metadata = {'name': temp_filename}
    media = MediaFileUpload(temp_filename, mimetype='image/jpeg')
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    drive_service.permissions().create(fileId=uploaded_file['id'], body={'type': 'anyone', 'role': 'reader'}).execute()
    return f"https://drive.google.com/uc?id={uploaded_file['id']}"




action = st.selectbox("Choose an Action", ["Snake Bite Detection", "Admin"])

# -----------------------------------------------------------------------------------------------------

if action == "Admin":
    st.markdown("## 🔐 Admin Access Required")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Enter Password", type="password", placeholder="Password", help="Only authorized personnel")
        if st.button("Unlock"):
            if password == st.secrets["admin"]["password"]:

                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password.")
        # Stop here so no other UI elements render
        st.stop()

    # Show data only if authenticated
    st.success("✅ Access granted.")
    st.dataframe(existing_data)



# ------------------ SESSION INIT ------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.predicted_species = ""
    st.session_state.image_url = ""
    st.session_state.record = {}

# ------------------ MAIN APP ------------------
if not st.session_state.submitted:
    st.markdown("Upload or capture an image of the bite area:")
    if "show_camera" not in st.session_state:
        st.session_state.show_camera = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Open Camera"):
            st.session_state.show_camera = True
    with col1:
        if st.session_state.show_camera:
            captured_image = st.camera_input("Take a photo using camera")
        else:
            captured_image = None
    with col2:
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        st.markdown('<label class="upload-btn" for="file_uploader"></label>', unsafe_allow_html=True)

    with st.form("snakebite_form"):
        district = st.selectbox("Location of the bite", list(LOCATION_OPTIONS.keys()), index=None)
        time = st.selectbox("Time of the bite", list(TIME.keys()), index=None)
        season = st.selectbox("Season during bite", list(SEASON.keys()), index=None)
        place = st.selectbox("Where did the bite happen", list(PLACE.keys()), index=None)
        local_symptoms = st.multiselect("Local symptoms", list(LOCAL_SYMPTOMS.keys()))
        sys_symptoms = st.multiselect("Systematic symptoms", list(SYSTEMATIC_SYMPTOMS.keys()))
        notes = st.text_area("Additional Notes")
        submit = st.form_submit_button("Submit Snake Bite Details")

    if submit:
        weights = [0.8, 0.4, 0.4, 0.5, 0.6, 0.8]
        vectors = []
        if district: vectors.append(LOCATION_OPTIONS[district])
        if time: vectors.append(TIME[time])
        if season: vectors.append(SEASON[season])
        if place: vectors.append(PLACE[place])
        if local_symptoms: vectors.append(combine_symptom_values(local_symptoms, LOCAL_SYMPTOMS))
        if sys_symptoms: vectors.append(combine_symptom_values(sys_symptoms, SYSTEMATIC_SYMPTOMS))

        labels = ["Monocled Cobra", "Spectacled Cobra", "Russell's Viper", "Krait Species"]
        prediction = ""

        if vectors:
            scores = [sum(x * w for x, w in zip(v, weights[:len(v)])) for v in zip(*vectors)]
            total = sum(scores)
            probs = [(v / total) * 100 for v in scores] if total else [0] * len(labels)
            prediction = labels[probs.index(max(probs))] if total else random.choice(labels)
        else:
            prediction = random.choice(labels) if (captured_image or uploaded_image) else "Insufficient Input"

        image_to_save = captured_image or uploaded_image
        image_url = ""
        if image_to_save:
            img = Image.open(image_to_save).convert("RGB")
            filename = f"bite_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.jpg"
            img.save(filename)
            image_url = upload_to_drive(filename)

        st.session_state.predicted_species = prediction
        st.session_state.image_url = image_url
        st.session_state.record = {
            "District": district or "",
            "Time": time or "",
            "Season": season or "",
            "Place": place or "",
            "Local symptoms": ", ".join(local_symptoms),
            "Systematic symptoms": ", ".join(sys_symptoms),
            "Prediction": prediction,
            "Image URL": image_url,
            "Notes": notes
        }
        st.session_state.submitted = True
        st.rerun()

# ------------------ PAGE 2: CLINICAL CONFIRMATION ------------------
else:
    species = st.session_state.predicted_species
    image_url = st.session_state.image_url
    record = st.session_state.record

    st.header(f"Predicted Snake: 🐍 {species}")
    img_path = f"images/{species.lower().replace(' ', '_')}.jpg"

    try:
        st.image(img_path, caption=species, use_container_width=True)
    except:
        st.warning("Image not available.")

    clinical = st.text_input("🩺 Clinical Snake Identification*", placeholder="Enter confirmed species")
    clinical_notes = st.text_area("Additional Clinical Notes (optional)")

    if st.button("Save Final Record"):
        if not clinical.strip():
            st.error("Please enter clinical identification.")
        else:
            final_data = {**record, "Clinical Snake": clinical, "Clinical Notes": clinical_notes}
            updated_df = pd.concat([existing_data, pd.DataFrame([final_data])], ignore_index=True)
            updated_df.replace([pd.NA, None, float("inf"), float("-inf")], "", inplace=True)
            worksheet.clear()
            worksheet.update([updated_df.columns.tolist()] + updated_df.values.tolist())
            st.success("✅ Record saved successfully.")
            st.session_state.submitted = False
            st.rerun()
