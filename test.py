import streamlit as st
from st_supabase_connection import SupabaseConnection
from utils import get_or_create_anon_id

MAX_CHARACTERS = 200

st.set_page_config(page_title="End of the year messages", page_icon="🎫")
st.title("🎫 End of the year messages")

st.write(
    """
    🎉 One New Year’s resolution. Totally anonymous.
    Let’s see what everyone is aiming for this year!
    """
)

st.session_state.anon_id, st.session_state.new_user = get_or_create_anon_id()
st.session_state.sb_conn = st.connection("supabase",type=SupabaseConnection)

# messages_tb = st.session_state.sb_conn.table(table_name='messages')
# messages = messages_tb.select("*").execute()

#TODO se l'utente é nuovo dai la possibilitá di scrivere un messaggio,
st.header("Write a new message")

txt = st.text_area(label="Message", max_chars=200)#, disabled=not(st.session_state.new_user))

st.write(f"{len(txt)}/{MAX_CHARACTERS} characters.")
#TODO #DEBUG
# print(messages)

# st.header("Existing messages")
# for row in messages.data:
#     st.write(f"Message: {row['message']} - At: {row['created_at']}")

# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st

# # Show app title and description.


# # Show a section to add a new ticket.
# st.header("Add a ticket")

# # We're adding tickets via an `st.form` and some input widgets. If widgets are used
# # in a form, the app will only rerun once the submit button is pressed.
# with st.form("add_ticket_form"):
#     issue = st.text_area("Describe the issue")
#     priority = st.selectbox("Priority", ["High", "Medium", "Low"])
#     submitted = st.form_submit_button("Submit")

# if submitted:
#     # Make a dataframe for the new ticket and append it to the dataframe in session
#     # state.
#     recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
#     today = datetime.datetime.now().strftime("%m-%d-%Y")
#     df_new = pd.DataFrame(
#         [
#             {
#                 "ID": f"TICKET-{recent_ticket_number+1}",
#                 "Issue": issue,
#                 "Status": "Open",
#                 "Priority": priority,
#                 "Date Submitted": today,
#             }
#         ]
#     )

#     # Show a little success message.
#     st.write("Ticket submitted! Here are the ticket details:")
#     st.dataframe(df_new, use_container_width=True, hide_index=True)
#    

# # Show section to view and edit existing tickets in a table.
# st.header("Existing tickets")
# st.write(f"Number of tickets: `{len(st.session_state.df)}`")

# st.info(
#     "You can edit the tickets by double clicking on a cell. Note how the plots below "
#     "update automatically! You can also sort the table by clicking on the column headers.",
#     icon="✍️",
# )

# # Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# # cells. The edited data is returned as a new dataframe.
# edited_df = st.data_editor(
#     st.session_state.df,
#     use_container_width=True,
#     hide_index=True,
#     column_config={
#         "Status": st.column_config.SelectboxColumn(
#             "Status",
#             help="Ticket status",
#             options=["Open", "In Progress", "Closed"],
#             required=True,
#         ),
#         "Priority": st.column_config.SelectboxColumn(
#             "Priority",
#             help="Priority",
#             options=["High", "Medium", "Low"],
#             required=True,
#         ),
#     },
#     # Disable editing the ID and Date Submitted columns.
#     disabled=["ID", "Date Submitted"],
# )

# # Show some metrics and charts about the ticket.
# st.header("Statistics")

# # Show metrics side by side using `st.columns` and `st.metric`.
# col1, col2, col3 = st.columns(3)
# num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
# col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
# col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
# col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# # Show two Altair charts using `st.altair_chart`.
# st.write("")
# st.write("##### Ticket status per month")
# status_plot = (
#     alt.Chart(edited_df)
#     .mark_bar()
#     .encode(
#         x="month(Date Submitted):O",
#         y="count():Q",
#         xOffset="Status:N",
#         color="Status:N",
#     )
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

# st.write("##### Current ticket priorities")
# priority_plot = (
#     alt.Chart(edited_df)
#     .mark_arc()
#     .encode(theta="count():Q", color="Priority:N")
#     .properties(height=300)
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
