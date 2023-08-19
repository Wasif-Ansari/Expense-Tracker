import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import calendar
import csv
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt

file_name = f'./{calendar.month_name[datetime.today().month]}_{datetime.today().year}.csv'
path = os.path.isfile(file_name)
if path==False:
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Spent on", "Amount", "location", "comment", "time"]) 

df = pd.read_csv(file_name)


data_file = f"./{calendar.month_name[datetime.today().month]}_data.csv"
path2 = os.path.isfile(data_file)
if path2==False:
    with open(data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "TIME", "Rupees", "Total", "foodtotal","colddrinktotal", "bakchoditotal", "groceriestotal", "savingstotal", "otherstotal" ]) 

df2 = pd.read_csv(data_file)




expenses = ["Food", "Cold-Drink", "bakchodi", "groceries", "savings", "others"]
location = ["College", "Home"]
currency = "INR"
page_title = "Expense Tracker"
page_icon = ":money_with_wings:"
layout = "centered"

# with open(data_file) as fin:
#     next(fin)
#     Total = sum(int(r[1]) for r in csv.reader(fin))

Total = 0
foodtotal = 0
colddrinktotal = 0
bakchoditotal = 0
groceriestotal = 0
savingstotal = 0
otherstotal = 0


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)





menu = option_menu(menu_title = None,
                   options = ["Data Entry", "Data Visualization"],
                   icons=["pencil-fill", "bar-chart-fill"],
                   orientation="horizontal",
                   )

if menu == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("Entry form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Spent on: ", expenses, key="spent_on")
        col2.selectbox("Location : ", location, key="location")

        st.number_input(f"Amount: ", min_value=0, format="%i", step=10, key="amount")
        
        with st.expander("Comment"):
            st.text_area("", placeholder="Enter a comment here ....", value=":", key="comments")


        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        spenton = str(st.session_state["spent_on"])
        amount = str(st.session_state["amount"])
        loc = str(st.session_state["location"])
        comm = str(st.session_state["comments"])
        add_data = st.form_submit_button("Save data")

        if add_data:
            new_data = {"Date":date, "Spent on":spenton, "Amount":amount, "location":loc, "comment":comm, "time":time}
            amount = int(amount)
            # Total+=amount
            # "Food", "Cold-Drink", "bakchodi", "groceries", "savings", "others"
            foodtotal = 0
            colddrinktotal = 0
            bakchoditotal = 0
            groceriestotal = 0
            savingstotal = 0
            otherstotal = 0
            if spenton=="Food":
                foodtotal = df2['foodtotal'].sum() + amount
            elif spenton=="Cold-Drink":
                colddrinktotal = df2['colddrinktotal'].sum() + amount
            elif spenton=="bakchodi":
                bakchoditotal = df2['bakchoditotal'].sum() + amount
            elif spenton=="groceries":
                groceriestotal = df2['groceriestotal'].sum() + amount
            elif spenton=="savings":
                savingstotal = df2['savingstotal'].sum() + amount
            else:
                otherstotal = df2['otherstotal'].sum() + amount

            Total = df2['Rupees'].sum() + amount
            # print(df2['Total'].sum())
            addeddata = {"Date":date, "TIME":time, "Rupees":amount, "Total":Total, "foodtotal":foodtotal, "colddrinktotal":colddrinktotal, "bakchoditotal":bakchoditotal, "groceriestotal":groceriestotal, "savingstotal":savingstotal, "otherstotal":savingstotal}
            df2 = df2._append(addeddata, ignore_index = True)
            df2.to_csv(f"{calendar.month_name[datetime.today().month]}_data.csv", index=False)
            df = df._append(new_data, ignore_index = True)
            df.to_csv(file_name, index = False)

            st.success("Data Saved! ")

else:
    pass
    #data visualization
    
    # st.dataframe(df)

    st.title("Graphs")

    contact_options = ["Rupees", "Amount", "Spent on", "time"]
    contact_selected = st.selectbox("Select a Students value", contact_options)
    # contact_options = ["Amount", "Spent on", "time"]
    # contact_selected = st.selectbox("Select a Students value", contact_options)

    inform = f"Students {contact_selected} Chart:"
    fig1 = px.line(df2, x="TIME", y=contact_selected, title=inform)
    # inform = f"Students {contact_selected} Chart:"
    # fig1 = px.line(df, x="time", y=contact_selected, title=inform)

    st.plotly_chart(fig1, use_container_width=True)
    
    # fig2 = px.line(df2, x="time", y=, title=inform)

    # st.plotly_chart(fig2, use_container_width=True)



    # data = pd.read_csv(data_file, nrows=100)
    # st.bar_chart(data["Total"], columns = ["TIME"] )










    # st.bar_chart(df2["Total"]) #IMPORTSNT












    # fig3 = px.line(df2, x="TIME", y="Total", title=inform)
    # st.plotly_chart(fig3, use_container_width=True)



    # chart_data = pd.DataFrame(df2["TIME"],
    # columns=[df2["Total"]])

    # st.bar_chart(chart_data)

    data  = pd.DataFrame(df2)
    bar_chart = alt.Chart(data).mark_bar().encode(
        y='Total:Q',
        x='TIME:O',
    )
 
    st.altair_chart(bar_chart, use_container_width=True)

    x1 = df2["Rupees"]
    y = df2["Total"]
    
    fig11, ax1 = plt.subplots()
    chr = ax1.pie(y, labels=x1, radius=1.2, autopct="%0.01f%%", shadow=True)

    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig11)
