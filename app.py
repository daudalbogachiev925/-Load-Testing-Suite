import streamlit as st
import pandas as pd
import plotly.express as px
from src.scenarios import load_scenarios
from src.runner import LoadRunner
from src.metrics import compute_metrics, throughput_by_second, metrics_by_step
from src.analysis import find_bottlenecks, sla_check, recommend_scaling

st.set_page_config(page_title="Load Testing", layout="wide")
st.title("Load Testing Suite — 1C")

scenarios = load_scenarios()
names = [s.name for s in scenarios]
selected = st.selectbox("Scenario", names)
scenario = next(s for s in scenarios if s.name == selected)

duration = st.slider("Duration (sec)", 5, 120, 30)
scenario.duration_sec = duration

if st.button("Run load test"):
    with st.spinner("Running..."):
        runner = LoadRunner(scenario)
        results = runner.run()
    st.session_state["results"] = results
    st.session_state["summary"] = runner.summary()

if "results" in st.session_state:
    results = st.session_state["results"]
    m = compute_metrics(results)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Requests", m["requests"])
    c2.metric("Errors %", m["error_rate_pct"])
    c3.metric("p95 ms", m["p95_ms"])
    c4.metric("Avg ms", m["avg_ms"])

    st.subheader("Throughput (req/sec)")
    tp = pd.Series(throughput_by_second(results)).sort_index()
    st.line_chart(tp)

    st.subheader("By step")
    st.dataframe(pd.DataFrame(metrics_by_step(results)).T)

    st.subheader("Bottlenecks")
    st.dataframe(pd.DataFrame(find_bottlenecks(results)))

    st.subheader("SLA check")
    st.json(sla_check(results))

    st.subheader("Recommendation")
    st.info(recommend_scaling(results))
