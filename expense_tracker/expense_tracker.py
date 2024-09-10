import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize the expense dataframe
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def load_expenses():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)

def save_expenses():
    st.session_state.expenses.to_csv('expenses.csv', index=False)
    st.success("Expenses saved successfully!")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

def filter_expenses(category):
    if not st.session_state.expenses.empty:
        filtered = st.session_state.expenses[st.session_state.expenses['Category'] == category]
        st.write(filtered)
    else:
        st.warning("No expenses available!")

def expense_summary():
    if not st.session_state.expenses.empty:
        st.write("Total Expenses: $", st.session_state.expenses['Amount'].sum())
        st.write("Average Expense: $", st.session_state.expenses['Amount'].mean())
        st.write("Maximum Expense: $", st.session_state.expenses['Amount'].max())
        st.write("Minimum Expense: $", st.session_state.expenses['Amount'].min())
    else:
        st.warning("No expenses to summarize!")

def pie_chart():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        category_sum = st.session_state.expenses.groupby('Category')['Amount'].sum()
        ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

def delete_expense(index):
    if not st.session_state.expenses.empty and index < len(st.session_state.expenses):
        st.session_state.expenses.drop(index, inplace=True)
        st.session_state.expenses.reset_index(drop=True, inplace=True)
        st.success(f"Expense {index} deleted!")
    else:
        st.warning("Invalid index!")

st.title('Your Personal Expense Tracker')

# Sidebar for adding expenses
with st.sidebar:
    st.header('Add Expense')
    date = st.date_input('Date')
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Shopping','Utilities', 'Medical','Other'])
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    description = st.text_input('Description')
    if st.button('Add'):
        add_expense(date, category, amount, description)
        st.success('Expense added!')

    st.header('File Operations')
    if st.button('Save Expenses'):
        save_expenses()
    if st.button('Load Expenses'):
        load_expenses()

st.header('Expenses')
st.write(st.session_state.expenses)


# Visualization
st.header('Visualization')
if st.button('Visualize Bar Chart'):
    visualize_expenses()
if st.button('Visualize Category Pie Chart'):
    pie_chart()

# Adding filters and summary statistics
st.header('Expense Summary')
if st.button('Show Summary'):
    expense_summary()

st.header('Filter by Category')
category_filter = st.selectbox('Filter Category', ['All', 'Food', 'Transport', 'Entertainment', 'Shopping', 'Utilities', 'Medical', 'Other'])
if st.button('Apply Filter'):
    if category_filter == 'All':
        st.write(st.session_state.expenses)
    else:
        filter_expenses(category_filter)



# Expense deletion
st.header('Delete Expense')
delete_index = st.number_input('Enter index to delete', min_value=0, step=1)
if st.button('Delete Expense'):
    delete_expense(delete_index)
