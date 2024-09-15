import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize the expense and income dataframes
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

if 'income' not in st.session_state:
    st.session_state.income = pd.DataFrame(columns=['Date', 'Source', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def add_income(date, source, amount, description):
    new_income = pd.DataFrame([[date, source, amount, description]], columns=st.session_state.income.columns)
    st.session_state.income = pd.concat([st.session_state.income, new_income], ignore_index=True)

def load_expenses():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)
        st.success("Expenses loaded successfully!")
    else:
        st.warning("Please upload a CSV file to load expenses.")

def save_transactions():
    expenses_with_type = st.session_state.expenses.copy()
    income_with_type = st.session_state.income.copy()
    expenses_with_type['Type'] = 'Expense'
    income_with_type['Type'] = 'Income'
    
    transactions = pd.concat([expenses_with_type, income_with_type], ignore_index=True)
    transactions.to_csv('transactions.csv', index=False)
    st.success("Transactions saved successfully!")

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
        st.write("Total Expenses: ₹", st.session_state.expenses['Amount'].sum())
        st.write("Average Expense: ₹", st.session_state.expenses['Amount'].mean())
        st.write("Maximum Expense: ₹", st.session_state.expenses['Amount'].max())
        st.write("Minimum Expense: ₹", st.session_state.expenses['Amount'].min())
    else:
        st.warning("No expenses to summarize!")

def income_summary():
    if not st.session_state.income.empty:
        st.write("Total Income: ₹", st.session_state.income['Amount'].sum())
        st.write("Average Income: ₹", st.session_state.income['Amount'].mean())
    else:
        st.warning("No income to summarize!")

def budget_calculation():
    total_income = st.session_state.income['Amount'].sum()
    total_expenses = st.session_state.expenses['Amount'].sum()
    remaining_budget = total_income - total_expenses
    st.write(f"Remaining Budget: ₹{remaining_budget:.2f}")

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

# Application Title
st.title('Your Personal Expense & Income Tracker')

# Sidebar for adding expenses and income
with st.sidebar:
    st.header('Add Expense')
    date = st.date_input('Date')
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Shopping', 'Utilities', 'Medical', 'Other'])
    amount = st.number_input('Amount (₹)', min_value=0.0, format="%.2f")
    description = st.text_input('Description')
    
    if st.button('Add Expense'):
        add_expense(date, category, amount, description)
        st.success('Expense added!')

    st.header('Add Income')
    income_date = st.date_input('Income Date')
    source = st.text_input('Source')
    income_amount = st.number_input('Income Amount (₹)', min_value=0.0, format="%.2f")
    income_description = st.text_input('Income Description')

    if st.button('Add Income'):
        add_income(income_date, source, income_amount, income_description)
        st.success('Income added!')

    st.header('File Operations')
    if st.button('Save Transactions'):
        save_transactions()
        
    load_expenses()

# Expense and income display
st.header('Expenses')
st.write(st.session_state.expenses)

st.header('Income')
st.write(st.session_state.income)

# Filter expenses
st.header('Filter Expenses by Category')
category_filter = st.selectbox('Filter Expense Category', ['All', 'Food', 'Transport', 'Entertainment', 'Shopping', 'Utilities', 'Medical', 'Other'])
if st.button('Apply Filter'):
    if category_filter == 'All':
        st.write(st.session_state.expenses)
    else:
        filter_expenses(category_filter)

# Visualization
st.header('Visualization')
if st.button('Visualize Expense Bar Chart'):
    visualize_expenses()
if st.button('Visualize Expense Category Pie Chart'):
    pie_chart()



# Summary and Budget Calculation
st.header('Summary & Budget Calculation')
if st.button('Show Expense Summary'):
    expense_summary()

if st.button('Show Income Summary'):
    income_summary()

if st.button('Calculate Budget'):
    budget_calculation()



# Expense deletion
st.header('Delete Expense')
delete_index = st.number_input('Enter index to delete', min_value=0, step=1)
if st.button('Delete Expense'):
    delete_expense(delete_index)
