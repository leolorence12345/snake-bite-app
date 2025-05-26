# import streamlit as st
# import pandas as pd
# from PIL import Image
# import random
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

# # ------------------ STYLES ------------------
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
#     .upload-btn input[type="file"] { display: none; }
#     .stFileUploader label { display: none; }
#     </style>
# """, unsafe_allow_html=True)

# # ------------------ HELPERS ------------------
# def combine_symptom_values(selected, reference):
#     if not selected or "No Symptoms" in selected:
#         return [0, 0, 0, 0]
#     out = None
#     for sym in selected:
#         val = reference[sym]
#         out = val if out is None else [x + y for x, y in zip(out, val)]
#     return out

# def upload_to_drive(temp_filename):
#     file_metadata = {'name': temp_filename}
#     media = MediaFileUpload(temp_filename, mimetype='image/jpeg')
#     uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     drive_service.permissions().create(fileId=uploaded_file['id'], body={'type': 'anyone', 'role': 'reader'}).execute()
#     return f"https://drive.google.com/uc?id={uploaded_file['id']}"

# # ------------------ ACTION ------------------
# action = st.selectbox("Choose an Action", ["Snake Bite Detection", "Admin"])

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
#         st.stop()

#     st.success("✅ Access granted.")
#     st.dataframe(existing_data)

# # ------------------ STATE INIT ------------------
# if "submitted" not in st.session_state:
#     st.session_state.submitted = False
#     st.session_state.identity_filled = False
#     st.session_state.predicted_species = ""
#     st.session_state.image_url = ""
#     st.session_state.record = {}

# # ------------------ STEP 1: Victim Identity ------------------
# if not st.session_state.identity_filled:
#     with st.form("identity_form", clear_on_submit=False):
#         st.subheader("👤 Victim Details")

#         col1, col2 = st.columns(2)
#         with col1:
#             name = st.text_input("Full Name*")
#             dob = st.date_input("Date of Birth*")
#             sex = st.selectbox("Sex*", ["Male", "Female", "Other"], index=None)
#         with col2:
#             phone = st.text_input("Phone Number*", max_chars=10)
#             address = st.text_area("Address*")

#         identity_submit = st.form_submit_button("Continue to Bite Form")

#     if identity_submit:
#         if not all([name, dob, sex, phone, address]):
#             st.warning("Please fill all required personal details.")
#         else:
#             st.session_state.identity_info = {
#                 "Name": name,
#                 "Date of Birth": str(dob),
#                 "Sex": sex,
#                 "Phone": phone,
#                 "Address": address
#             }
#             st.session_state.identity_filled = True
#             st.rerun()

# # ------------------ STEP 2: Snake Bite Details ------------------
# elif not st.session_state.submitted:
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
#         district = st.selectbox("Location of the bite", list(LOCATION_OPTIONS.keys()), index=None)
#         time = st.selectbox("Time of the bite", list(TIME.keys()), index=None)
#         season = st.selectbox("Season during bite", list(SEASON.keys()), index=None)
#         place = st.selectbox("Where did the bite happen", list(PLACE.keys()), index=None)
#         local_symptoms = st.multiselect("Local symptoms", list(LOCAL_SYMPTOMS.keys()))
#         sys_symptoms = st.multiselect("Systematic symptoms", list(SYSTEMATIC_SYMPTOMS.keys()))
#         notes = st.text_area("Additional Notes")
#         submit = st.form_submit_button("Submit Snake Bite Details")

#     if submit:
#         weights = [0.8, 0.4, 0.4, 0.5, 0.6, 0.8]
#         vectors = []
#         if district: vectors.append(LOCATION_OPTIONS[district])
#         if time: vectors.append(TIME[time])
#         if season: vectors.append(SEASON[season])
#         if place: vectors.append(PLACE[place])
#         if local_symptoms: vectors.append(combine_symptom_values(local_symptoms, LOCAL_SYMPTOMS))
#         if sys_symptoms: vectors.append(combine_symptom_values(sys_symptoms, SYSTEMATIC_SYMPTOMS))

#         labels = ["Monocled Cobra", "Spectacled Cobra", "Russell's Viper", "Krait Species"]
#         prediction = ""

#         if vectors:
#             scores = [sum(x * w for x, w in zip(v, weights[:len(v)])) for v in zip(*vectors)]
#             total = sum(scores)
#             probs = [(v / total) * 100 for v in scores] if total else [0] * len(labels)
#             prediction = labels[probs.index(max(probs))] if total else random.choice(labels)
#         else:
#             prediction = random.choice(labels) if (captured_image or uploaded_image) else "Insufficient Input"

#         image_to_save = captured_image or uploaded_image
#         image_url = ""
#         if image_to_save:
#             img = Image.open(image_to_save).convert("RGB")
#             filename = f"bite_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.jpg"
#             img.save(filename)
#             image_url = upload_to_drive(filename)

#         st.session_state.predicted_species = prediction
#         st.session_state.image_url = image_url
#         st.session_state.record = {
#             **st.session_state.identity_info,
#             "District": district or "",
#             "Time": time or "",
#             "Season": season or "",
#             "Place": place or "",
#             "Local symptoms": ", ".join(local_symptoms),
#             "Systematic symptoms": ", ".join(sys_symptoms),
#             "Prediction": prediction,
#             "Image URL": image_url,
#             "Notes": notes
#         }
#         st.session_state.submitted = True
#         st.rerun()

# # ------------------ STEP 3: Clinical Confirmation ------------------
# else:
#     species = st.session_state.predicted_species
#     image_url = st.session_state.image_url
#     record = st.session_state.record

#     st.header(f"Predicted Snake: 🐍 {species}")
#     img_path = f"images/{species.lower().replace(' ', '_')}.jpg"

#     try:
#         st.image(img_path, caption=species, use_container_width=True)
#     except:
#         st.warning("Image not available.")

#     clinical = st.text_input("🩺 Clinical Snake Identification*", placeholder="Enter confirmed species")
#     clinical_notes = st.text_area("Additional Clinical Notes (optional)")

#     if st.button("Save Final Record"):
#         if not clinical.strip():
#             st.error("Please enter clinical identification.")
#         else:
#             final_data = {**record, "Clinical Snake": clinical, "Clinical Notes": clinical_notes}
#             updated_df = pd.concat([existing_data, pd.DataFrame([final_data])], ignore_index=True)
#             updated_df.replace([pd.NA, None, float("inf"), float("-inf")], "", inplace=True)
#             worksheet.clear()
#             worksheet.update([updated_df.columns.tolist()] + updated_df.values.tolist())
#             st.success("✅ Record saved successfully.")
#             st.session_state.submitted = False
#             st.session_state.identity_filled = False
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
from streamlit_javascript import st_javascript
from geopy.geocoders import Nominatim
import pgeocode

# ------------------ GOOGLE AUTH ------------------
creds_dict = st.secrets["connections"]["gsheets"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
gc = gspread.authorize(creds)
drive_service = build("drive", "v3", credentials=creds)
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
    .stCheckbox { background-color: white !important; color: #ffffff !important; }
    .upload-btn input[type="file"] { display: none; }
    .stFileUploader label { display: none; }
    </style>
""", unsafe_allow_html=True)

# ------------------ INITIALIZE SESSION STATE VARIABLES ------------------
for key in ["submitted", "identity_filled", "predicted_species", "image_url", "record", 
            "final_district", "final_pincode", "show_camera",
            "custom_place", "custom_local_symptoms", "custom_sys_symptoms"]:
    if key not in st.session_state:
        if key in ["submitted", "identity_filled", "show_camera"]:
            st.session_state[key] = False
        elif key in ["record"]:
            st.session_state[key] = {}
        else:
            st.session_state[key] = ""

# ------------------ HELPERS ------------------
def combine_symptom_values(selected, reference):
    if not selected or "No Symptoms" in selected:
        return [0, 0, 0, 0]
    out = None
    for sym in selected:
        val = reference.get(sym, [0, 0, 0, 0])
        out = val if out is None else [x + y for x, y in zip(out, val)]
    return out

def upload_to_drive(temp_filename):
    file_metadata = {"name": temp_filename}
    media = MediaFileUpload(temp_filename, mimetype="image/jpeg")
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    drive_service.permissions().create(fileId=uploaded_file["id"], body={"type": "anyone", "role": "reader"}).execute()
    return f"https://drive.google.com/uc?id={uploaded_file['id']}"

def map_hour_to_time_category(hour):
    if 4 <= hour < 9:
        return "Early Morning"
    elif 9 <= hour < 16:
        return "During the day"
    elif 16 <= hour < 20:
        return "Evening"
    else:
        return "Night"

def map_month_to_season(month):
    if month in [12, 1, 2]: return "Winter"
    elif month in [3, 4, 5]: return "Summer"
    elif month in [6, 7, 8]: return "Monsoon"
    elif month in [9, 10]: return "Autumn"
    else: return "Spring"

# ------------------ STATE INIT ------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.identity_filled = False
    st.session_state.predicted_species = ""
    st.session_state.image_url = ""
    st.session_state.record = {}

if "final_district" not in st.session_state:
    st.session_state.final_district = ""

if "final_pincode" not in st.session_state:
    st.session_state.final_pincode = ""


# ------------------ STEP 1: Victim Identity ------------------
if not st.session_state.identity_filled:
    with st.form("identity_form", clear_on_submit=False):
        st.subheader("👤 Victim Details")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth")
            sex = st.selectbox("Sex", ["Male", "Female", "Other"], index=None)
        with col2:
            phone = st.text_input("Phone Number", max_chars=10)
            address = st.text_area("Address")
        identity_submit = st.form_submit_button("Continue to Bite Form")
    if identity_submit:
        st.session_state.identity_info = {
            "Name": name,
            "Date of Birth": str(dob),
            "Sex": sex,
            "Phone": phone,
            "Address": address
        }
        st.session_state.identity_filled = True
        st.rerun()
# ------------------ STEP 2: Snake Bite Details ------------------
elif not st.session_state.submitted:
    st.markdown("Upload or capture an image of the bite area:")
    if "show_camera" not in st.session_state:
        st.session_state.show_camera = False
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Open Camera"):
            st.session_state.show_camera = True
    with col1:
        captured_image = st.camera_input("Take a photo using camera") if st.session_state.show_camera else None
    with col2:
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        st.markdown('<label class="upload-btn" for="file_uploader"></label>', unsafe_allow_html=True)

    location = st_javascript("""await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                resolve({ latitude: pos.coords.latitude, longitude: pos.coords.longitude });
            },
            (err) => {
                resolve({error: err.message});
            }
        );
    });""")

    if isinstance(location, dict) and "error" not in location:
        lat, lon = location["latitude"], location["longitude"]
        geolocator = Nominatim(user_agent="geoapi", timeout=10)
        try:
            loc = geolocator.reverse((lat, lon), language="en")
            address = loc.raw.get("address", {})
            st.session_state.final_district = address.get("state_district", "").upper()
            st.session_state.final_pincode = address.get("postcode", "")
            st.success(f"📍 Auto Detected District: {st.session_state.final_district} | Pincode: {st.session_state.final_pincode}")
        except:
            st.warning("Could not reverse geocode location.")
    else:
        st.warning("Location access not granted or unavailable.")

    override = st.checkbox("Provide location manually if not accurate")
    if override:
        manual_pin = st.text_input("Enter Pincode")
        if manual_pin:
            nomi = pgeocode.Nominatim("in")
            details = nomi.query_postal_code(manual_pin)
            if details is not None and pd.notna(details.place_name):
                st.session_state.final_pincode = manual_pin
                st.session_state.final_district = details.place_name.upper()
                st.success(f"📌 Manual Pincode matched district: {st.session_state.final_district}")
            else:
                st.error("Invalid pincode entered.")

    matched_district = None
    for district_key in LOCATION_OPTIONS:
        if st.session_state.final_district in district_key:
            matched_district = district_key
            break

    if matched_district:
        st.session_state.final_district = matched_district

    district = st.text_input("District", value=st.session_state.final_district)
    pincode = st.text_input("Pincode", value=st.session_state.final_pincode)

    # Dynamic Others
    place_options = list(PLACE.keys()) + ["Others"]
    selected_place = st.selectbox("Where did the bite happen", place_options, index=None, key="place_selection")
    custom_place = st.text_input("Please specify the place of bite", key="custom_place") if selected_place == "Others" else ""
    final_place = custom_place if selected_place == "Others" else selected_place

    local_options = list(LOCAL_SYMPTOMS.keys()) + ["Others"]
    selected_local = st.multiselect("Local symptoms", local_options, key="local_symptoms")
    custom_local = st.text_input("Specify other local symptoms", key="custom_local_symptoms") if "Others" in selected_local else ""
    final_local_symptoms = [s for s in selected_local if s != "Others"]
    if custom_local:
        final_local_symptoms.append(custom_local)

    sys_options = list(SYSTEMATIC_SYMPTOMS.keys()) + ["Others"]
    selected_sys = st.multiselect("Systematic symptoms", sys_options, key="systemic_symptoms")
    custom_sys = st.text_input("Specify other systemic symptoms", key="custom_sys_symptoms") if "Others" in selected_sys else ""
    final_sys_symptoms = [s for s in selected_sys if s != "Others"]
    if custom_sys:
        final_sys_symptoms.append(custom_sys)

    with st.form("snakebite_form"):
        st.markdown("### 🕓 Bite Time")
        col1, col2, col3 = st.columns(3)
        with col1:
            hour_12 = st.selectbox("Hour", list(range(1, 13)), index=11)
        with col2:
            minute = st.selectbox("Minute", list(range(0, 60)), format_func=lambda x: f"{x:02}", index=0)
        with col3:
            meridian = st.selectbox("AM/PM", ["AM", "PM"], index=0)

        hour_24 = hour_12 % 12 + (12 if meridian == "PM" else 0)
        time_key = map_hour_to_time_category(hour_24)

        st.markdown("### 🗓 Month of Bite")
        month_name = st.selectbox("Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        month_num = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ].index(month_name) + 1
        season_key = map_month_to_season(month_num)

        notes = st.text_area("Additional Notes")
        submit = st.form_submit_button("Submit Snake Bite Details")

    if submit:
        weights = [0.8, 0.4, 0.4, 0.5, 0.6, 0.8]
        vectors = []
        if district: vectors.append(LOCATION_OPTIONS.get(district.upper(), [0, 0, 0, 0]))
        if time_key: vectors.append(TIME[time_key])
        if season_key: vectors.append(SEASON[season_key])
        if final_place: vectors.append(PLACE.get(final_place, [0, 0, 0, 0]))
        if final_local_symptoms: vectors.append(combine_symptom_values(final_local_symptoms, LOCAL_SYMPTOMS))
        if final_sys_symptoms: vectors.append(combine_symptom_values(final_sys_symptoms, SYSTEMATIC_SYMPTOMS))

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
            **st.session_state.identity_info,
            "District": district or "",
            "Time": time_key or "",
            "Season": season_key or "",
            "Place": final_place or "",
            "Local symptoms": ", ".join(final_local_symptoms),
            "Systematic symptoms": ", ".join(final_sys_symptoms),
            "Prediction": prediction,
            "Image URL": image_url,
            "Notes": notes
        }
        st.session_state.submitted = True
        st.rerun()

# ------------------ STEP 3: Clinical Confirmation ------------------
else:
    species = st.session_state.predicted_species
    image_url = st.session_state.image_url
    record = st.session_state.record

    st.header(f"Predicted Snake: 🐍 {species}")
    try:
        image_url = f"images/{species.lower().replace(' ', '_')}.jpg"
        st.image(image_url, caption=species, use_container_width=True)
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
            st.session_state.identity_filled = False
            st.rerun()
