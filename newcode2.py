import os
import pickle
import streamlit as st
import pandas as pd
import math
import numpy as np
import pydeck as pdk
import json
from PIL import Image
from streamlit_folium import st_folium
import folium
st.set_page_config(layout="wide")
st.markdown("""
<style>
.big-font {
    padding: 10px;
    font-size:35px !important;
    background-color: #c1f5ef;
}
</style>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components
import geojson
import fiona
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon
import json
_RELEASE = False

import folium
import gdown

def download_model(file_id, output_path):
    # Check if the file already exists
    if not os.path.exists(output_path):
        # Create the gdown URL for the file ID
        url = f'https://drive.google.com/uc?id={file_id}'
        
        # Show a message that we're downloading the file
        with st.spinner('Downloading model... This may take a while! \nDo not close this page...'):
            gdown.download(url, output_path, quiet=False)
        st.success('Downloaded the model successfully!')
download_model('1JzLuMa1X2u3EgR4nWzC1WJnhniiUWOVc', 'finalized_mod.sav')
def my_component(key=None):
    # Create a Map centered around the coordinates (usually the tiles are in English)
    m = folium.Map(location=[24.44172333286647, 54.60779221637909],tiles="https://tile.openstreetmap.de/{z}/{x}/{y}.png", zoom_start=10, attr= '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
    
    # Add the interactive LatLngPopup to display coordinates when clicking on the map
    m.add_child(folium.LatLngPopup())
    
    # Use Streamlit's component for folium to render the map (replace with actual Streamlit component syntax)
    f_map = st_folium(m, width=800, height=400)
   
    # Default values for selected latitude and longitude
    selected_latitude = 24.44172333286647
    selected_longitude = 54.60779221637909

    # Check if a location has been clicked on the map and update the coordinates
    if f_map.get("last_clicked"):
        selected_latitude = f_map["last_clicked"]["lat"]
        selected_longitude = f_map["last_clicked"]["lng"]

    # Return the selected coordinates
    return {"lat": selected_latitude, "lng": selected_longitude}


def distance (lat1, lon1, lat2, lon2):
    R = 6373.0
    distance = []
    lat1 = lat1 * math.pi/180
    lat2 = lat2 * math.pi/180
    lon1 = lon1* math.pi/180
    lon2 = lon2 * math.pi/180;
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


if not _RELEASE:
#     st.markdown(f'''
#     <style>
#     section[data-testid="stSidebar"] .css-ng1t4o {{width: 2rem;}}
#     </style>
# ''',unsafe_allow_html=True)
    html_temp = """ 
       <div style ="background-color:#ffffff;padding:1px"> 
       <h1 style ="color:blue;text-align:center;">Housing Affordability in Abu Dhabi</h2> 
       </div> 
       """
    st.markdown(html_temp, unsafe_allow_html = True) 
    html_temp1 = """ 
       <div style ="background-color:white;padding:4px"> 
       <h4 style ="color:black;text-align:left;">Please select any location</h4> 
       </div> 
     """
    st.markdown(html_temp1, unsafe_allow_html = True)
    cols1,cols2 = st.columns([2,1]) 
    with cols1:
      clicked_coords = my_component()
    district_name = "None"

    if type(clicked_coords) != int:
       lat = clicked_coords["lat"]
       lng = clicked_coords["lng"]
       try:
         with fiona.open("Abudhabi_analytics_final_3.json","r",encoding="utf16le", errors="ignore") as layer:
            Alist = list(layer)
       except Exception as e:
           st.error(f"An error occurred: {e}")
       point = {"coordinates": (lng, lat), "type": "Point"}
       pt = shape(point)
       for i in Alist:
        try:
         if pt.within(shape(i["geometry"])):
            district_name = i["properties"]["DISTRICTNA"]
            district_details = i["properties"]
            district_geometry = i["geometry"]
            district_report = i
            break
        except Exception as e:
              st.text(f"An error occurred: {e}")


    df_busStops = pd.read_csv("BusStops.csv")
    list_busstops = []
    for index, row in df_busStops.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_busstops.append((row["latitude"], row["longitude"], row["NAME"], d))
    

    df_clinics = pd.read_csv("Clinics.csv")
    list_clinics = []
    for index, row in df_clinics.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_clinics.append((row["latitude"], row["longitude"], row["NAMEENG"],d))
    
    df_hospitals = pd.read_csv("Hospitals.csv")
    list_hospitals = []
    for index, row in df_hospitals.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_hospitals.append((row["latitude"], row["longitude"], row["NAMEENG"],d))
    
    
    df_pharmacy = pd.read_csv("Pharmacy.csv")
    list_pharmacy = []
    for index, row in df_pharmacy.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_pharmacy.append((row["latitude"], row["longitude"], row["NAMEENG"],d))

    df_hotels = pd.read_csv("Hotels.csv")
    list_hotels = []
    for index, row in df_hotels.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_hotels.append((row["latitude"], row["longitude"], row["NAME_ENG"],d))
    
    df_parks = pd.read_csv("Public_Parks.csv")
    list_parks = []
    for index, row in df_parks.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_parks.append((row["latitude"], row["longitude"], row["CF_NAMEENG"],d))

    df_quran = pd.read_csv("Quran_memorization_centres.csv") 
    list_quran = []
    for index, row in df_quran.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_quran.append((row["latitude"], row["longitude"], row["EN_NAME"],d))
    
    df_restaurent = pd.read_csv("Restaurents.csv")
    list_restaurent = []
    for index, row in df_restaurent.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_restaurent.append((row["latitude"], row["longitude"], row["CF_NAMEENG"],d))

    df_cafes = pd.read_csv("cafes.csv")
    list_cafes = []
    for index, row in df_restaurent.iterrows():
        point = {"coordinates": (row["longitude"], row["latitude"]), "type": "Point"}
        pt = shape(point)
        if pt.within(shape(district_geometry)):
            d = distance(row["latitude"],row["longitude"],lat, lng )
            if d<1:
                list_cafes.append((row["latitude"], row["longitude"], row["CF_NAMEENG"],d))
    st.markdown(str(len(list_cafes)) + ", " + str(len(list_restaurent)))

    district_nam = ["Delma"
          ,"Bad' Al Mutaw'ah"
          ,"Ghiyathi"
          ,"Al Marfa"
          ,"Western Mahadir"
          ,"Zayed City"
          ,"Mzeerʻah"
          ,"Al Selmiyyah"
          ,"Al Bateen"
          ,"Al Khalidiyah"
          ,"Al Hisn"
          ,"Al Danah"
          ,"Al Manhal"
          ,"Al Zahiyah"
          ,"Al Nahyan"
          ,"Al Mushrif"
          ,"Jazeerat Al Reem"
          ,"Hadbat Al Za'faranah"
          ,"Al Sa'adah"
          ,"Al Rawdah"
          ,"Al Maqta'"
          ,"Musaffah"
          ,"Khalifa City"
          ,"Mohamed Bin Zayed City"
          ,"Al Rahah"
          ,"Bani Yas"
          ,"Shakhbout City"
          ,"Al Shahamah"
          ,"Al Bahyah"
          ,"Al Khaznah"
          ,"Sweihan"
          ,"Rimah"
          ,"Al Qou'"
          ,"Nahil"
          ,"Al Wiqan"
          ,"Al Faqa'"
          ,"'Asharij"
          ,"Al Khibeesi"
          ,"Al Muwaij'i"
          ,"Al Jimi"
          ,"Al Mu'tarid"
          ,"Al Jahili"
          ,"Al Qattarah"
          ,"Central District"
          ,"Al Mutaw'ah"
          ,"Industrial Area"
          ,"Hili"
          ,"Al Sarouj"]
    pickle_in = open("finalized_mod.sav", "rb") 
    classifier = pickle.load(pickle_in)
    @st.cache_data()
  
# defining the function which will make the prediction using the data which the user inputs 
    def prediction(a1, a2, a3,a4,a5,a6,a7,a8,a9,a10,a11,a12):   
         # Making predictions 
         prediction = classifier.predict( 
             [[a1, a2, a3,a4,a5,a6,a7,a8,a9,a10,a11,a12]])
         return prediction
    def main():       
       if district_name != "None" and district_name in district_nam:
           c1 = district_name
       else: 
           c1 = "Delma"
    #    cols1, cols2= st.columns(2)
       with cols2:
         if district_name == "None" or district_name not in district_nam:
            html_temp2k = "District not available, please select it manually"
         else:
            html_temp2k = ""
         html_temp2 = """ 
       <div style ="background-color:white;padding:4px"> 
       <h6 style ="color:black;text-align:left;">""" + html_temp2k + """</h6> 
       </div> 
       """
         st.markdown(html_temp2, unsafe_allow_html = True )
         b1 = st.selectbox("District", ("Delma"
          ,"Bad' Al Mutaw'ah"
          ,"Ghiyathi"
          ,"Al Marfa"
          ,"Western Mahadir"
          ,"Zayed City"
          ,"Mzeerʻah"
          ,"Al Selmiyyah"
          ,"Al Bateen"
          ,"Al Khalidiyah"
          ,"Al Hisn"
          ,"Al Danah"
          ,"Al Manhal"
          ,"Al Zahiyah"
          ,"Al Nahyan"
          ,"Al Mushrif"
          ,"Jazeerat Al Reem"
          ,"Hadbat Al Za'faranah"
          ,"Al Sa'adah"
          ,"Al Rawdah"
          ,"Al Maqta'"
          ,"Musaffah"
          ,"Khalifa City"
          ,"Mohamed Bin Zayed City"
          ,"Al Rahah"
          ,"Bani Yas"
          ,"Shakhbout City"
          ,"Al Shahamah"
          ,"Al Bahyah"
          ,"Al Khaznah"
          ,"Sweihan"
          ,"Rimah"
          ,"Al Qou'"
          ,"Nahil"
          ,"Al Wiqan"
          ,"Al Faqa'"
          ,"'Asharij"
          ,"Al Khibeesi"
          ,"Al Muwaij'i"
          ,"Al Jimi"
          ,"Al Mu'tarid"
          ,"Al Jahili"
          ,"Al Qattarah"
          ,"Central District"
          ,"Al Mutaw'ah"
          ,"Industrial Area"
          ,"Hili"
          ,"Al Sarouj"),district_nam.index(c1))
       district_number = [32,29,33,13,46,47,41,25,2,8,5,3,11,28,18,15,37,34,23,22,12,40,38,39,21,30,44,26,1,9,45,43,20,42,27,4,0,10,17,7,14,6,19,31,16,36,35,24]
    
       district_dict = dict(zip(district_nam,district_number))
    #    if district_name != "None":
    #        c1 = district_name
       a1 = district_dict[b1]
    #    cols1, cols2, cols3 = st.columns(2)
       with cols2:
          b2 = st.selectbox("Unit type",("Flat", "Villa", "Studio"),0)
       if b2 == "Flat":
           a2 = 0
       if b2 == "Villa":
           a2 = 1
       if b2 == "Studio":
           a2 = 2
       with cols2:
           a3 = st.selectbox("Number of Rooms", (1,2,3,4,5,6), 0)
       with cols2:
               st.download_button("Download District Report", str(dict(district_report["properties"])), file_name = "District_report.json" )
               df_busStopsk = pd.DataFrame(list_busstops, columns=["lat", "lon", "Name","Distance (km)"])
               df_busStopsk["facility_type"] = "Bus_Stop"
               df_cafesk = pd.DataFrame(list_cafes, columns=["lat", "lon", "Name","Distance (km)"])
               df_cafesk ["facility_type"] = "Cafe"
               df_clinicsk = pd.DataFrame(list_clinics, columns=["lat", "lon", "Name","Distance (km)"])
               df_clinicsk["facility_type"] = "Clinic"
               df_hospitalsk = pd.DataFrame(list_hospitals, columns=["lat", "lon", "Name","Distance (km)"])
               df_hospitalsk["facility_type"] = "Hospital"
               df_hotelsk = pd.DataFrame(list_hotels, columns=["lat", "lon", "Name","Distance (km)"])
               df_hotelsk["facility_type"] = "Hotel"
               df_parksk = pd.DataFrame(list_parks, columns=["lat", "lon", "Name","Distance (km)"])
               df_parksk["facility_type"] = "Park"
               df_pharmacyk = pd.DataFrame(list_pharmacy, columns=["lat", "lon", "Name","Distance (km)"])
               df_pharmacyk["facility_type"] = "Pharmacy"
               df_qurank = pd.DataFrame(list_quran, columns=["lat", "lon", "Name","Distance (km)"])
               df_qurank["facility_type"] = "Quran_Memorization_Center"
               df_restaurentk = pd.DataFrame(list_restaurent, columns=["lat", "lon", "Name","Distance (km)"])
               df_restaurentk["facility_type"] = "Restaurent"
               final_df = pd.concat([df_busStopsk,df_cafesk,df_clinicsk,df_hospitalsk,df_hotelsk,df_parksk,df_pharmacyk,df_qurank,df_restaurentk])
               @st.cache_data
               def convert_df(df):
                   # IMPORTANT: Cache the conversion to prevent computation on every rerun
                   return df.to_csv().encode("utf-8")
    #            final_dfk = final_df.drop(final_df.columns[0], axis=1, inplace=True)
               csv = convert_df(final_df)
    #    final_df.to_csv("Facility_details.csv",final_df, delimeter = ",")
               st.download_button(
                  label="Download Facility Report ",
                  data=csv,
                  file_name="facility_details.csv",
                   mime="text/csv",
                   )
       col1, col2, col3 = st.columns(3)   

       with col1:  
                 a4 = st.slider("Number of Bus Stops (within 1 km)",0,60,len(list_busstops))
                 a5 = st.slider("Number of Hotels (within 1 km)",0,40,len(list_hotels))
                 a6 = st.slider("Number of Clinics (within 1 km)",0,30,len(list_clinics))
       with col2:  
                 a7 = st.slider("Number of Cafes (within 1 km)",0,70,len(list_cafes))
                #  a8 = st.slider("Number of Pharmacies (within 1 km)",0,50,len(list_pharmacy))
                 a11 = st.slider("Number of Quran Memorization Centres (within 1 km)",0,5,len(list_quran))
                 a9 = st.slider("Number of Restauranets (within 1 km)",0,200,len(list_restaurent))
       with col3:
                 a8 = st.slider("Number of Pharmacies (within 1 km)",0,50,len(list_pharmacy))
                 a10 = st.slider("Number of Hospitals (within 1 km)",0,5,len(list_hospitals))
                #  a11 = st.slider("Number of Quran Memorization Centres (within 1 km)",0,5,len(list_quran))
                 a12 = st.slider("Number of Public Parks (within 1 km)",0,5,len(list_parks))
       result =""
      
   

       layert2 = pdk.Layer(
        type="TextLayer",
        data=df_cafesk,
        pickable=False,
        get_position=["lon", "lat"],
        get_text="facility_type",
        get_size=30,
        sizeUnits="meters",
        get_color=[0, 0, 0],
        get_angle=0,
        getTextAnchor= '"middle"',
        get_alignment_baseline='"bottom"'
        )
    

       initial_view =pdk.ViewState(
           latitude=lat,
           longitude= lng,
           zoom=16,
           pitch=50,
          )

       bus_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/busstop.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
    #    df_busStopsk["bus_data"] = None
       df_busStopsk["bus_data"] = [bus_data] * len(df_busStopsk)
    #    for i in df_busStopsk.index:
    #      df_busStopsk["bus_data"][i] = bus_data
       bus_layer = pdk.Layer(
            type="IconLayer",
            data= df_busStopsk,
            get_icon="bus_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)


       clinic_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/clinics.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
    #    df_clinicsk["clinic_data"] = None
    #    for i in df_clinicsk.index:
       df_clinicsk["clinic_data"] = [clinic_data]*len(df_clinicsk)
       clinic_layer = pdk.Layer(
            type="IconLayer",
            data= df_clinicsk,
            get_icon="clinic_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)

       pharmacy_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/pharmacy.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_pharmacyk["pharmacy_data"] = [pharmacy_data]*len(df_pharmacyk)
       pharmacy_layer = pdk.Layer(
            type="IconLayer",
            data= df_pharmacyk,
            get_icon="pharmacy_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)
       hotel_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/hotel.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_hotelsk["hotel_data"] = [hotel_data]*len(df_hotelsk)
       hotel_layer = pdk.Layer(
            type="IconLayer",
            data= df_hotelsk,
            get_icon="hotel_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)
       restaurent_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/restaurant.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_restaurentk["restaurent_data"] = [restaurent_data]*len(df_restaurentk)
       restaurent_layer = pdk.Layer(
            type="IconLayer",
            data= df_restaurentk,
            get_icon="restaurent_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)

       cafe_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/cafe1.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_cafesk["cafe_data"] = [cafe_data]*len(df_cafesk)
       cafe_layer = pdk.Layer(
            type="IconLayer",
            data= df_cafesk,
            get_icon="cafe_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)

       hospital_data = {
           "url":"https://upload.wikimedia.org/wikipedia/commons/1/18/Hospital_pointer.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_hospitalsk["hospital_data"] = [hospital_data]*len(df_hospitalsk)
       hospital_layer = pdk.Layer(
            type="IconLayer",
            data= df_hospitalsk,
            get_icon="hospital_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)

       park_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/parks.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_parksk["park_data"] = [park_data]*len(df_parksk)
       park_layer = pdk.Layer(
            type="IconLayer",
            data= df_parksk,
            get_icon="park_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)

       QM_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/quran1.png",
           "width": 242,
           "height": 242,
           "anchorY": 242,
          }
       df_qurank["QM_data"] = [QM_data]*len(df_qurank)
       QM_layer = pdk.Layer(
            type="IconLayer",
            data= df_qurank,
            get_icon="QM_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True)
       home_data = {
           "url":"https://raw.githubusercontent.com/Analystharsh/PricePrediction/main/pin.png",
           "width": 1000,
           "height": 1000,
           "anchorY": 242,
          }
      
       cols = ["lat","lon","Name","home_data"]
       df_homek = pd.DataFrame([[lat,lng,"Home" ,home_data]], columns = cols)   
       home_layer = pdk.Layer(
            type="IconLayer",
            data= df_homek,
            get_icon="home_data",
            get_size=4,
            size_scale=50,
            get_position=["lon", "lat"],
            pickable=True)


       layer2 =  pdk.Layer(
             "ScatterplotLayer",
             data=df_cafesk,
             get_position="[lon, lat]",
             get_color="[200, 40, 0, 160]",
             get_radius=40,
              )
    
       layertlist = []
    
       if len(list_cafes) !=0:
           layert2 = pdk.Layer(
        type="TextLayer",
        data=df_cafesk,
        pickable=False,
        get_position=["lon", "lat"],
        get_text="facility_type",
        get_size=30,
        sizeUnits="meters",
        get_color=[0, 0, 0],
        get_angle=0,
        getTextAnchor= '"middle"',
        get_alignment_baseline='"bottom"'
        )
           layertlist.append(layert2)  
   
       layer_list =  [bus_layer, hotel_layer, hospital_layer,clinic_layer,QM_layer,pharmacy_layer,restaurent_layer,park_layer,cafe_layer,home_layer] 
       
       st.pydeck_chart( pdk.Deck(
         
          initial_view_state=initial_view
          
          ,layers = layer_list,tooltip={"text": "{Name}"}, map_style="mapbox://styles/mapbox/light-v10"
          
          ))
       if st.button("Predict"): 
           result = prediction(a1, a2, a3,a4,a5,a6,a7,a8,a9,a10,a11,a12) 
           st.markdown('<p class="big-font">'+ "The predicted house rent value is: " + "<b style={color:blue;}>" + str(round(result[0]*a3,2))  +  ' AED per year'  + '</b><br>' + "This house is affordable for someone with the monthly salary of " + '<b style={color:blue;}>' + str(np.round(result*a3*3.33/12,2)[0])  + " AED." +'</b></p>', unsafe_allow_html=True)  

     
    if __name__=='__main__': 
       main()
