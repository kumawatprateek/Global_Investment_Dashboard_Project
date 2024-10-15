import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# Load your data from a CSV file
df = pd.read_csv('dummy_sample.csv')  # Replace with your CSV file path
df = df.drop(columns=['Company ID'])  # Remove unnecessary 'Company ID' column

# Create a horizontal option menu for navigation
selected = option_menu(
    menu_title=None,  # No title for the menu
    options=["Home", "Global", "Thematic"],  # Navigation options
    icons=["house", "globe2", "binoculars"],  # Corresponding icons for each option
    default_index=0,  # Default selected option is "Home"
    orientation="horizontal",  # Horizontal orientation of the menu
)

# Function to add a footer with social links
def add_footer():
    footer = """
    <style>
    .footer {
        width: 100%;
        background-color: #464746;
        color: #FFFFFF;
        text-align: center;
        padding: 10px;
        font-size: 15px;
        margin-top: 20px;  /* Adds space between content and footer */
    }
    .footer-icons {
        margin-top: 10px;
    }
    .footer-icons a {
        color: #FFFFFF;
        margin: 0 15px;
        font-size: 20px;
        text-decoration: none;
    }
    </style>
    <div class="footer">
        <p>© 2024 Created By Prateek Given By Persist Ventures</p>
        <div class="footer-icons">
            <a href="https://www.linkedin.com/in/kumawatprateek/" target="_blank">
                <i class="fa fa-linkedin"></i>
            </a>
            <a href="https://github.com/kumawatprateek" target="_blank">
                <i class="fa fa-github"></i>
            </a>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# Adding font-awesome for icons in the footer
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Handling the Home option
if selected == "Home":
    # Sidebar for selecting a company from the dataset
    with st.sidebar:
        selected_company1 = option_menu(
            menu_title="Companies",  # Title for sidebar
            options=["All"] + df['Company Name'].unique().tolist(),  # Dropdown options for companies
            menu_icon="buildings-fill",
            icons=["building"] * (len(df['Company Name'].unique()) + 1)  # Same icon for all options
        )

    # Title of the app
    st.title("Company Hierarchy Visualization")

    # Filter data based on selected company
    if selected_company1 == "All":
        company_data = df  # Show all data if "All" is selected
    else:
        company_data = df[df['Company Name'] == selected_company1]  # Filter by selected company

    # Calculate and display metrics (replace with relevant columns)
    total_capital = company_data['Total Capital Committed ($B)'].sum() if 'Total Capital Committed ($B)' in company_data.columns else 0
    total_fund_investments = company_data['Fund Investments'].sum() if 'Fund Investments' in company_data.columns else 0
    underlying_portfolio_companies = company_data['Country'].nunique() if 'Country' in company_data.columns else 0

    # Display metrics for the selected company
    st.header(f"{selected_company1} - Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Capital Catalyzed ($B)", f"{total_capital:.2f}")
    col2.metric("Total Fund Investments", f"{total_fund_investments}")
    col3.metric("Total Countries Funded", f"{underlying_portfolio_companies}")

    # Select relevant columns to display in the table
    selectedcolumn = ['Company Name', 'Fund','Investment ($M)','Total Capital Committed ($B)','Country', 'Country Capital Catalyzed ($M)','Global South Deals Funded']
    PrintData = company_data[selectedcolumn]

    # Display the filtered data
    st.subheader("Data Overview")
    st.dataframe(PrintData)

    # Create two pie charts for visualizing the data
    col1, col2 = st.columns(2)

    # Pie chart for 'Investments by Fund'
    with col1:
        if 'Investment ($M)' in company_data.columns and 'Fund' in company_data.columns:
            total_Fund1 = company_data['Investment ($M)'].sum()
            fig1 = px.pie(company_data, names='Fund', values='Investment ($M)', title=f'Investments by Fund($M) : {total_Fund1}')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.write("Data for 'Investment' or 'Fund' is missing.")

    # Pie chart for 'Committed Capital by Fund'
    with col2:
        if 'Total Capital Committed ($B)' in company_data.columns and 'Fund' in company_data.columns:
            total_Fund2 = company_data['Total Capital Committed ($B)'].sum()
            fig2 = px.pie(company_data, names='Fund', values='Total Capital Committed ($B)', title=f'Committed Capital by Fund($B) : {total_Fund2:.2f}')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("Data for 'Committed Capital' or 'Fund' is missing.")

    # Add footer at the bottom
    add_footer()

# Handling the Global option
if selected == "Global":
    # Sidebar for selecting a company
    with st.sidebar:
        selected_company2 = option_menu(
            menu_title="Companies",
            options=["All"] + df['Company Name'].unique().tolist(),
            menu_icon="buildings-fill",
            icons=["building"] * (len(df['Company Name'].unique()) + 1)
        )

    # Title of the page
    st.title("Global Investments - Overview")

    # Filter data based on selected company
    if selected_company2 == "All":
        company_data = df
    else:
        company_data = df[df['Company Name'] == selected_company2]

    # Display map with company data using equirectangular projection
    if 'Country' in company_data.columns:
        fig = px.scatter_geo(company_data,
                             locations='Country',
                             locationmode='country names',
                             hover_name='Country',
                             color_discrete_sequence=['#FF4500', '#FF6347', '#FF7F50'])  # Custom color palette

        fig.update_geos(projection_type="equirectangular",
                        showcoastlines=True,
                        coastlinecolor="Black",
                        showland=True,
                        landcolor="#f0e68c",
                        showocean=True,
                        oceancolor="#87CEFA",
                        showcountries=True,
                        countrycolor="Black")

        fig.update_layout(
            height=500,
            width=1400,
        )

        st.plotly_chart(fig, use_container_width=False)  # Fixed size for larger map
    else:
        st.write("Country data is missing.")

    # Display data overview in a table
    selectedcolumns = ['Company Name', 'Country', 'Country Capital Catalyzed ($M)', 'Investment ($M)']
    PrintDf = company_data[selectedcolumns]

    st.subheader("Data Overview")
    st.dataframe(PrintDf)

    # Pie chart for 'Capital by Theme'
    if 'Theme Capital Catalyzed ($M)' in company_data.columns and 'Theme' in company_data.columns:
        total_Theme = company_data['Theme Capital Catalyzed ($M)'].sum()
        fig1 = px.pie(company_data, names='Theme', values='Theme Capital Catalyzed ($M)', title=f'Capital Catalyzed by Theme($M) : {total_Theme}')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.write("Data for 'Theme' or 'Theme Capital' is missing.")

    # Add footer at the bottom
    add_footer()

# Handling the Thematic option
if selected == "Thematic":
    # Sidebar for selecting a company
    with st.sidebar:
        selected_company3 = option_menu(
            menu_title="Companies",
            options=["All"] + df['Company Name'].unique().tolist(),
            menu_icon="buildings-fill",
            icons=["building"] * (len(df['Company Name'].unique()) + 1)
        )

    # Filter data based on selected company
    if selected_company3 == "All":
        company_data = df
    else:
        company_data = df[df['Company Name'] == selected_company3]

    # Title of the page
    st.title("Thematic Overview")

    # Bar chart for 'Theme Capital Catalyzed'
    if 'Theme' in company_data.columns and 'Theme Capital Catalyzed ($M)' in company_data.columns:
        bar_fig = px.bar(company_data, x='Theme', y='Theme Capital Catalyzed ($M)', title='Number of Deals by Theme')
        st.plotly_chart(bar_fig, use_container_width=True)
    else:
        st.write("Data for 'Theme' or 'Theme Capital' is missing.")

    # Display data overview in a table
    selectedcolumns = ['Company Name', 'Fund', 'Investment ($M)', 'Country', 'Country Capital Catalyzed ($M)', 'Global South Deals Funded']
    PrintDf = company_data[selectedcolumns]

    st.subheader("Data Overview")
    st.dataframe(PrintDf)


    # Create two columns for horizontal display of the pie charts
    col1, col2 = st.columns(2)

    # First pie chart for 'Capital by Fund'
    # Second pie chart for 'Investments by Fund'
    with col1:
        if 'Investment ($M)' in company_data.columns and 'Fund' in company_data.columns:
            total_Fund1 = company_data['Investment ($M)'].sum() if 'Investment ($M)' in company_data.columns else 0
            fig1 = px.pie(company_data, names='Fund', values='Investment ($M)', title=f'Investments by Fund($M) : {total_Fund1}')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.write("Data for 'Deals Completed' or 'Fund Name' is missing.")

    with col2:
        if 'Total Capital Committed ($B)' in company_data.columns and 'Fund' in company_data.columns:
            total_Fund2 = company_data['Total Capital Committed ($B)'].sum() if 'Total Capital Committed ($B)' in company_data.columns else 0
            fig2 = px.pie(company_data, names='Fund', values='Total Capital Committed ($B)', title=f'Committed Capital by Fund($B) : {total_Fund2:.2f}')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("Data for 'Committed Capital' or 'Fund Name' is missing.")

    # Add footer at the bottom
    add_footer()
