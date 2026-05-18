import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from io import StringIO  # This was missing - critical fix!

# Set page configuration
st.set_page_config(
    page_title="Student Study Hours vs. Marks Predictor",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .stMetric {
        background-color: #e6f0fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📚 Student Study Hours vs. Marks Predictor")
st.markdown("Upload your study hours and scores data to predict student performance using linear regression")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file (with Hours and Scores columns)", type=["csv"])

# Sample data (if no file is uploaded)
sample_data = """Hours,Scores
2.5,21
5.1,47
3.2,27
8.5,75
3.5,30
1.5,20
9.2,88
5.5,60
8.3,81
2.7,25
7.7,85
5.9,62
4.5,41
3.3,42
1.1,17
8.9,95
2.5,30
1.9,24
6.1,67
7.4,69
2.7,30
4.8,54
3.8,35
6.9,76
7.8,86"""

# Determine which data to use
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded! ✅")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        df = pd.read_csv(StringIO(sample_data))
        st.info("Using sample data instead. Please upload a valid CSV file.")
else:
    df = pd.read_csv(StringIO(sample_data))
    st.info("Using sample data. Upload your own CSV file to analyze your data.")

# Data validation
if 'Hours' not in df.columns or 'Scores' not in df.columns:
    st.error("CSV must contain 'Hours' and 'Scores' columns. Using sample data instead.")
    df = pd.read_csv(StringIO(sample_data))

# Display data
st.subheader("📊 Data Preview")
st.dataframe(df.head(10), use_container_width=True)

# Show basic statistics
st.subheader("📈 Basic Statistics")
col1, col2 = st.columns(2)
with col1:
    st.metric("Number of Students", len(df))
    st.metric("Average Study Hours", f"{df['Hours'].mean():.2f} hours")
with col2:
    st.metric("Average Score", f"{df['Scores'].mean():.2f}")
    st.metric("Max Score", df['Scores'].max())

# Train model
st.subheader("🤖 Linear Regression Model")
X = df[['Hours']].values
y = df['Scores'].values

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Display model parameters
col1, col2 = st.columns(2)
with col1:
    st.metric("Slope (Coefficient)", f"{model.coef_[0]:.2f}")
with col2:
    st.metric("Intercept", f"{model.intercept_:.2f}")

st.markdown(f"**Regression Equation:** `Scores = {model.coef_[0]:.2f} * Hours + {model.intercept_:.2f}`")

# Evaluation metrics
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

st.subheader("🔍 Model Evaluation")
col1, col2 = st.columns(2)
with col1:
    st.metric("Mean Squared Error (MSE)", f"{mse:.2f}")
with col2:
    st.metric("R-squared (R²)", f"{r2:.4f}")

# Visualization
st.subheader("📈 Regression Analysis")
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data points
ax.scatter(X, y, color='blue', s=100, alpha=0.7, edgecolor='k', label='Actual Scores')
ax.plot(X, y_pred, color='red', linewidth=3, label='Regression Line')

# Customize plot
ax.set_title('Study Hours vs. Student Scores', fontsize=16, fontweight='bold')
ax.set_xlabel('Hours Studied', fontsize=14)
ax.set_ylabel('Scores', fontsize=14)
ax.grid(alpha=0.3)
ax.legend(fontsize=12)
plt.tight_layout()

st.pyplot(fig)

# Custom prediction
st.subheader("🔮 Predict Your Score")
hours = st.slider("Select hours studied", min_value=0.0, max_value=10.0, value=5.0, step=0.25)

# Make prediction
predicted_score = model.predict([[hours]])[0]
st.metric(f"Predicted score for {hours:.2f} hours", f"{predicted_score:.2f} points")

# Show confidence interval
confidence = 1.96 * np.sqrt(mse)
st.caption(f"95% Confidence Interval: {predicted_score - confidence:.1f} to {predicted_score + confidence:.1f}")

# Advanced options
with st.expander("See detailed predictions"):
    results = pd.DataFrame({
        'Hours': df['Hours'],
        'Actual Scores': df['Scores'],
        'Predicted Scores': y_pred,
        'Residuals': df['Scores'] - y_pred
    }).round(2)
    
    st.dataframe(results, use_container_width=True)
    
    # Download button for results
    csv = results.to_csv(index=False)
    st.download_button(
        label="Download predictions as CSV",
        data=csv,
        file_name="regression_predictions.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for students | Simple Linear Regression Model")
