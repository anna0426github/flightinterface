import streamlit as st
import datetime
import requests
import streamlit as st
import base64


st.title("Sia Airline Flight Booking")
#st.image(r"C:\Users\prasa\Downloads\wp2025608.jpg")
api_url = "http://3.90.26.147:8080/predict-flight-fare"
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("wp2025608.jpg")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image:url("https://th.bing.com/th/id/R.985b75077b30a11798fab99ed5aab390?rik=wmB%2fxhQHchgaGQ&pid=ImgRaw&r=0");
background-size: 100%;
background-position: top left;
background-repeat: repeat;
background-attachment: fixed;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://th.bing.com/th/id/R.985b75077b30a11798fab99ed5aab390?rik=wmB%2fxhQHchgaGQ&pid=ImgRaw&r=0");
background-position: top left; 
background-repeat: no-repeat;
background-attachment: fixed;
#background-color:#;
}}
[data-testid="stHeader"] {{
background: rgba(1,1,0,0);
background-color: #f0f0f0;
font: monospace;
font-size: 24;
}}
[data-testid="stToolbar"] {{
right: 10rem;
}}
[data-testid="stTextArea"] {{
font: monospace;
color: #333333;
font-style: bold;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)



airlines = ["air_india" ,
        "goair" ,
        "indigo" ,
        "spicejet" ,
        "trujet",
        "vistara"]
airline_times = {
                 "Air_India":{"time":[["07:30 am - 09:05 am","Non"],["15:30 pm - 19:50 pm","  1"],["18:45 pm - 20:05 pm","Non"]]},
                "goair":{"time":[["09:30 am - 11:05 am","Non"],["14:30 pm - 15:50 pm","Non"]]},
                "indigo":{"time":[["12:30 pm - 14:05 pm","Non"],["15:40 pm - 19:00 pm","  1"]]},
                "spicejet":{"time":[["17:30 pm - 19:05 pm","Non"],["20:30 pm - 21:50 pm","Non"]]},
                "trujet":{"time":[["07:45 am - 09:20 am","Non"],["13:30 pm - 16:50 pm","  1"]]},
                "vistara":{"time":[["21:30 pm - 23:05 pm","Non"],["06:30 am - 09:50 am","  1"]]}
                 }

airline = ""
widget_id = (id for id in range(1, 100_00))
with st.sidebar as sb :

    st.title("Search Flight",help="Search required flights")

   
    source = st.selectbox(
    "Origin",
    ("Chennai", "Delhi", "Kolkata","Mumbai"),placeholder = "Choose an option")
    st.write("You selected:", source)
    dest = st.selectbox(
    "Destination",
    ("Cochin", "Delhi", "Hyderabad","DELHI"))

    st.write("You selected:", dest)
    

    dep = st.date_input("Departure", datetime.datetime.today(),min_value=datetime.datetime.today())
    arval = st.date_input("Return", datetime.datetime.today(),min_value=datetime.datetime.today())
    
    
    st.title('Passenger')

    adults = st.number_input('Adults (12+)', min_value=0, step=1, value=1)
    children = st.number_input('Children (2-11)', min_value=0, step=1, value=0)
    infants = st.sidebar.number_input('Infants (-2)', min_value=0, step=1, value=0)
    
    search_btn = st.button("SEARCH")


if search_btn:
    st.markdown("Membership Status: Gold")
    for i,j in airline_times.items():
     with st.container(border=True):
        

        #print(i)
       # st.write(i)
        st.header(i.replace("_", " ").capitalize(),divider=True)
        for k in j["time"]:
            time_var = k[0].split(" - ")
            #duration = time_var[1] - time_var[0]
            duration = ((datetime.datetime.strptime(time_var[1], '%H:%M %p') - datetime.datetime.strptime( time_var[0], '%H:%M %p')))
            time_obj = datetime.datetime.strptime(str(duration), "%H:%M:%S")#.strftime("%-H:%M")



           
            
            if k[1].lower() =="non":
               Number_Of_Stops = "0"
            else:
               Number_Of_Stops = str(k[1])
            journey_date = dep.strftime("%d-%b-%Y")
            Dept_Time = str(datetime.datetime.strptime(time_var[0], '%H:%M %p').strftime("%H:%M"))
            arrval_time = str(datetime.datetime.strptime(time_var[1], '%H:%M %p').strftime("%H:%M"))
            
            data = {
                 "Airline_Name":i,
    "Number_Of_Stops":int(Number_Of_Stops.strip()),
    "Journey_Date":str(journey_date),
    "Dept_Time":Dept_Time,
    "Arrival_Time":arrval_time,
    "Source": source,
    "Destination":dest,
    "Membership_status":"Gold"
            }
           
            response = requests.post(api_url,json=data)
            api_result = response.json()
            display_text = k[0] + "   "+ source + " - " + dest + "    " + k[1]+ "-Stop" + "    " + str(time_obj.strftime("%H:%M")).split(":")[0]+"h " + str(time_obj.strftime("%H:%M")).split(":")[1]+"m"

            
            
            #st.text_area(label="",value= display_text ) 
            #with st.text_area(label="") :
            st.subheader("  "+ display_text ) 
            col1, col2, col3,col4 = st.columns(4)
            #("Our Best offered Price" + "\n" +"Rs." + str(api_result["Best_offered_price"]))
            col1.text_area("Membership Status: Gold",label_visibility= 'hidden',disabled=True,value="Our Best offered Price" + "\n" +"Rs." + str(api_result["Best_offered_price"]))
            col2.text_area(label="abv",disabled=True,value="GoIbibo" + "\n" +"Rs. " + str(api_result["Goibibo"]),label_visibility='hidden')
            col3.text_area(label="abv",disabled=True,value="MakeMyTrip" + "\n"+"Rs. "  + str(api_result["Makemytrip"]),label_visibility='hidden')
            col4.text_area(label="abv",disabled=True,value="IRCTC" + "\n" +"Rs." + str(api_result["IRCTC"]),label_visibility='hidden')
            book =st.button("Book Flight",key=next(widget_id))
            
               
            
            

               