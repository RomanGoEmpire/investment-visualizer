from enum import StrEnum, auto

import plotly.graph_objects as go
import streamlit as st


class InvestmentType(StrEnum):
    MONTH = auto()
    YEAR = auto()


def invested_for_years() -> list[float]:
    return [start_capital + income_per_year * y for y in range(duration)]


def add_yearly_gains(capital) -> float:
    return capital * (1 + total_percentage / 100)


st.set_page_config(page_title="Investment Vizualizer", page_icon="💸")
st.title(":material_payments: Investment Visualizer")

with st.sidebar:
    start_capital = st.number_input("Start Capital", 0)
    investment_type = st.segmented_control(
        "Investment per",
        options=list(InvestmentType),
        default=InvestmentType.MONTH.value,
        selection_mode="single"
    )
    investment = st.number_input("Investment", 0, value=1000)
    duration = st.number_input("Duration in Years", 2, 1000, 10)

    increase_percentage = st.number_input("Increase in Percent", 0.0, 50.0, 4.0)
    inflation_percentage = st.number_input("Inflation in Percent", 0.0, 10.0)
    total_percentage = increase_percentage - inflation_percentage
    st.write(f"Total increase percentage `{total_percentage}%`")

    st.divider()
    start_year_takeout = st.slider("Start year takeout", 1, duration, duration)
    takeout = st.number_input("Takeout per Year", 0)
    adjust_takeout = st.checkbox("Adjust takeout to inflation")

    income_per_year = investment * 12 if investment_type == InvestmentType.MONTH.value else investment

data = {
    "years": [y for y in range(duration + 1)],
    "invested": [start_capital],
    "capital": [start_capital],
    "takeout": [0]
}

for year in range(1, duration + 1):
    new_invested = start_capital + income_per_year * year

    if year >= start_year_takeout and takeout > 0:
        new_takeout = data["takeout"][-1] if data["takeout"][-1] > 0 else takeout
        if adjust_takeout:
            new_takeout *= 1 + inflation_percentage / 100

        data["takeout"].append(new_takeout)
        new_capital = add_yearly_gains(data["capital"][-1] - new_takeout)
        new_invested = data["invested"][-1]
    else:
        data["takeout"].append(0)
        new_capital = add_yearly_gains(data["capital"][-1]) + income_per_year

    data["invested"].append(new_invested)
    data["capital"].append(new_capital)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data["years"],
    y=data["invested"],
    mode='lines',
    name='Invested'
))

fig.add_trace(go.Scatter(
    x=data["years"],
    y=data["capital"],
    mode='lines',
    name='Capital'
))

if start_year_takeout != duration:
    fig.add_trace(go.Scatter(
        x=data["years"],
        y=data["takeout"],
        mode='lines',
        name='Takeout'
    ))

# Update layout

st.plotly_chart(fig)
