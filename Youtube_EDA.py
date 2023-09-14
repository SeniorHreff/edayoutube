# Import necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = 'https://raw.githubusercontent.com/SeniorHreff/edayoutube/main/global_youtube_data_2023.csv'
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    # Pick the columns we want and remove the columns that contain NAs
    df = df.drop(columns = ['video views', 'Title', 'uploads', 'video_views_rank', 'country_rank', 'channel_type_rank','video_views_for_the_last_30_days', 'lowest_monthly_earnings', 'highest_monthly_earnings', 'lowest_yearly_earnings', 'highest_yearly_earnings', 'subscribers_for_last_30_days', 'created_month', 'created_date'])
    df = df.dropna()
    
    return df

# Load the data using the defined function
df = load_data()

st.title(":rainbow[Super cool dataset about Youtubers from around the world]")

st.header("Expand to get some cool information about the dataset 😎", divider = 'rainbow')

with st.expander("General information from the dataset"):
                 st.markdown("""
- Subscribers vary widely from 12.3 million to 245 million, with an average of approximately 23.07 million.
- The channels were created between 2005 and 2022, with an average creation year of 2012. (It says in the data that Youtubes own channel was created, which would have been 13 years before the invention of the internet 🤯)
- Gross tertiary education enrollment percentages vary from 7.6% to 113.1%, with an average of 63.4%.
- The population spans from 202,506 to 1.4 billion, with an average population of approximately 432.8 million. (There are some smart people in Australia 👨‍🎓👩‍🎓)
- Unemployment rates range from 0.8% to 14.7%, with an average of 9.2%.
- Urban populations vary widely, with an average of approximately 224.6 million.
"""
)

def my_function():
        st.write(df.describe().T.round(1))

if st.button("Press for cool table description 📈"):
                my_function()

st.header("Now that you have gotten some information about the data and have become smarter, let's look at some graphs 📈", divider = 'rainbow')

visualization_option = st.selectbox(
    "Select Visualization", 
    ["Top five countries with most top YouTubers",
     "Average amount of subs for each country",
     "Most popular categories",
     "Density plot over creation of top Youtube Channels"
    ]
)

if visualization_option == "Top five countries with most top YouTubers":
    count_data = df['Country'].value_counts().nlargest(5).reset_index()
    count_data.columns = ['Country', 'Count']
    count_chart = alt.Chart(count_data).mark_bar().encode(
        alt.X('Country:N', title = 'Countries', axis=alt.Axis(labelAngle=45)),
        alt.Y('Count', title = 'Amount of Youtube channels'),
        tooltip = [alt.Tooltip('Country:N', title = 'Country'), alt.Tooltip('Count:N', title = 'Amount of Youtubers')]
    ).properties(
        width = 1000,
        height = 500,
        title = 'Top five countries with most Youtubers'
    )
    st.markdown("""***You can hover over the bars to get the precise amount of channels***""")
    st.altair_chart(count_chart, use_container_width=True)
    st.markdown("""- We can see that the USA has the most amount of top Youtubers followed by India""")
    if st.button("The Number 1 YouTuber in USA"):
        st.image("https://media.tenor.com/IIXy6CqR5l8AAAAC/mrbeast-ytpmv.gif")


elif visualization_option == "Average amount of subs for each country":
        plt.figure(figsize=(22, 10))
        
        # Group the DataFrame by 'Abbreviation' and calculation of the mean for each Country
        mean_subscribers_by_country = df.groupby('Abbreviation')['subscribers'].mean().reset_index()
        
        sns.barplot(data=df, x='Abbreviation', y= 'subscribers')
        plt.xlabel("Countries (abbreviations)")
        plt.ylabel("Subscribers in millions")
        plt.title('Average subscribers for each country')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        st.markdown("The two countries that have the highest average subscribers are Cuba and El Salvador")

elif visualization_option == "Most popular categories":
    # Aggregate data by summing subscribers for each category
    category_counts = df.groupby('category')['subscribers'].sum()
        
    # Find the index of the row with the maximum subscribers
    most_popular_index = category_counts.idxmax()
        
    # Get the most popular category using the found index
    most_popular_category = most_popular_index
        
    # Create the pie chart
    plt.figure(figsize=(30, 15))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, labeldistance = None)
    plt.title("Pie chart of all the categories on YouTube")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(title="técnica")
    st.pyplot(plt)
    st.markdown("The most popular YouTube Category is: " + most_popular_category)

elif visualization_option == "Density plot over creation of top Youtube Channels":
    sns.displot(data=df[df['created_year'] > 1970], x='created_year', kind='kde')
    # Adding titles and labels
    plt.title("Year for Creation of YouTube Channel")
    plt.xlabel("Created Year")
    plt.ylabel("Density")
    st.pyplot(plt)
    st.markdown("""
    - YouTube was founded the 14th of February 2005 and we can see from the plot that a great amount of people signs up within the first year of YouTube.
    - Most people created a YouTube channel around 2010 and after."""
    )


st.header("All of this information is really cool! Let us have a look at some more geopolitical charts as well 🌍", divider = 'rainbow')

visualization_option2 = st.selectbox(
    "Select Correlation figure", 
    ['Correlation between Education and Unemployment rate',
     'Correlation between Urban Population and Unemployment rate'
    ]
)

if visualization_option2 == 'Correlation between Education and Unemployment rate':
    def generate_plot(df):
        fig, ax = plt.subplots()
        ax.scatter(df['Gross tertiary education enrollment (%)'], df['Unemployment rate'], s = df['Population']/1000000 )
        ax.set_xlabel('Education Enrollment Rate')
        ax.set_ylabel('Unemployment Rate')
        ax.set_title('Correlation between Education and Unemployment rate')
        return fig
    st.pyplot(generate_plot(df))
    st.markdown("""
    - It does not seem that there is a clear correlation between the Tertiary education enrollment rate and the Unemployment rate.
    - It is correct that there is a country with over 100 pct. enrollment rate, that is Australia, pretty wild!!
    """
    )



elif visualization_option2 == 'Correlation between Urban Population and Unemployment rate':
    def generate_plot(df):
        fig, ax = plt.subplots()
        ax.scatter(df['Unemployment rate'], df['Urban_population'], s = df['Population']/1000000 )
        ax.set_xlabel('Unemployment Rate [in %]')
        ax.set_ylabel('Urban Population [in millions]')
        ax.set_title('Correlation between Urban Population and Unemployment rate')
        return fig
    st.pyplot(generate_plot(df))
    st.markdown("""
    - There seems to be no clear correlation between the Urban Population in a coutry and its Unemployment rate.
    """
    )

with st.expander('Closing remarks'):
       st.markdown("""
Thank you so much for using time exploring our webapp and we hoped you learned something while exploring ❤.
""")
       st.image("https://media.tenor.com/IqbjPDIMCLIAAAAM/yakuza.gif")


on = st.toggle('Activate Friday mode')

if on:
        st.image('https://media.tenor.com/pLORkeju1bAAAAAC/yakuzadiscord-yakuza0.gif')