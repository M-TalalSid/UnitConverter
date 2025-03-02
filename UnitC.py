import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="UniConvert Pro",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS without recursive definitions
def local_css():
    st.markdown("""
    <style>
    /* Base styles */
    .stApp {
        background-color: #f8f9fa;
        color: #333333;
    }
    
    /* Cards */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #6C63FF;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Result display */
    .result-display {
        background: linear-gradient(135deg, #6C63FF, #FF6584);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        margin: 20px 0;
    }
    
    /* History items */
    .history-item {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #6C63FF;
        color: #E0E0E0;
    }
    
    /* Formula display */
    .formula-display {
        background-color: white;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        margin: 15px 0;
    }
    
    /* Logo */
    .logo-text {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(45deg, #6C63FF, #FF6584);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    
    /* Unit icons */
    .unit-icon {
        font-size: 42px;
        text-align: center;
        margin: 20px 0;
    }
    
    .unit-icon h3 {
        color: #E0E0E0;
        font-size: 16px;
        font-weight: 600;
        margin-top: 8px;
        background: rgba(0, 0, 0, 0.2);
        padding: 6px 12px;
        border-radius: 16px;
        display: inline-block;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .card {
            padding: 15px;
        }
        
        .result-display {
            font-size: 20px;
            padding: 15px;
        }
        
        .logo-text {
            font-size: 24px;
        }
        
        .unit-icon {
            font-size: 36px;
        }
    }
    /* Enhanced Recent Conversions Header */
    .recent-conversions-header {
        background: linear-gradient(90deg, rgba(108, 99, 255, 0.2) 0%, rgba(108, 99, 255, 0.1) 100%);
        padding: 12px 16px;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #6C63FF;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .recent-conversions-header h3 {
        color: #FFFFFF;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .recent-conversions-header .icon {
        font-size: 1.2rem;
        color: #6C63FF;
        opacity: 0.9;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .recent-conversions-header {
            padding: 10px 14px;
        }
        
        .recent-conversions-header h3 {
            font-size: 1.1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Detect mobile devices (simplified version)
def is_mobile():
    try:
        return st.session_state.get('is_mobile', False)
    except:
        return False

# Define conversion functions and formulas
def convert_length(value, from_unit, to_unit):
    conversions = {
        'meter': 1,
        'kilometer': 0.001,
        'centimeter': 100,
        'millimeter': 1000,
        'inch': 39.3701,
        'foot': 3.28084,
        'yard': 1.09361,
        'mile': 0.000621371,
        'nautical mile': 0.000539957
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_weight(value, from_unit, to_unit):
    conversions = {
        'kilogram': 1,
        'gram': 1000,
        'milligram': 1e6,
        'pound': 2.20462,
        'ounce': 35.274,
        'ton': 0.001,
        'stone': 0.157473
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'celsius' and to_unit == 'fahrenheit':
        formula = f"({value} × 9/5) + 32"
        return (value * 9/5) + 32, formula
    elif from_unit == 'fahrenheit' and to_unit == 'celsius':
        formula = f"({value} - 32) × 5/9"
        return (value - 32) * 5/9, formula
    elif from_unit == 'celsius' and to_unit == 'kelvin':
        formula = f"{value} + 273.15"
        return value + 273.15, formula
    elif from_unit == 'kelvin' and to_unit == 'celsius':
        formula = f"{value} - 273.15"
        return value - 273.15, formula
    elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
        formula = f"({value} - 32) × 5/9 + 273.15"
        return (value - 32) * 5/9 + 273.15, formula
    elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
        formula = f"({value} - 273.15) × 9/5 + 32"
        return (value - 273.15) * 9/5 + 32, formula
    else:
        return value, "No conversion needed"

def convert_volume(value, from_unit, to_unit):
    conversions = {
        'liter': 1,
        'milliliter': 1000,
        'cubic meter': 0.001,
        'gallon (US)': 0.264172,
        'quart (US)': 1.05669,
        'pint (US)': 2.11338,
        'cup (US)': 4.22675,
        'fluid ounce (US)': 33.814,
        'tablespoon (US)': 67.628,
        'teaspoon (US)': 202.884
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_time(value, from_unit, to_unit):
    conversions = {
        'second': 1,
        'millisecond': 1000,
        'minute': 1/60,
        'hour': 1/3600,
        'day': 1/86400,
        'week': 1/604800,
        'month (30 days)': 1/2592000,
        'year (365 days)': 1/31536000,
        'decade': 1/315360000,
        'century': 1/3153600000,
        'millennium': 1/31536000000
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_data(value, from_unit, to_unit):
    conversions = {
        'byte': 1,
        'kilobyte': 1/1024,
        'megabyte': 1/(1024**2),
        'gigabyte': 1/(1024**3),
        'terabyte': 1/(1024**4),
        'petabyte': 1/(1024**5),
        'bit': 8,
        'kibibyte': 1/1024,
        'mebibyte': 1/(1024**2),
        'gibibyte': 1/(1024**3),
        'tebibyte': 1/(1024**4),
        'pebibyte': 1/(1024**5)
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[from_unit] / conversions[to_unit], formula

def convert_area(value, from_unit, to_unit):
    conversions = {
        'square meter': 1,
        'square kilometer': 0.000001,
        'square centimeter': 10000,
        'square millimeter': 1000000,
        'square inch': 1550.0031,
        'square foot': 10.76391,
        'square yard': 1.19599,
        'acre': 0.000247105,
        'hectare': 0.0001
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_speed(value, from_unit, to_unit):
    conversions = {
        'meter per second': 1,
        'kilometer per hour': 3.6,
        'mile per hour': 2.23694,
        'knot': 1.94384,
        'foot per second': 3.28084,
        'inch per second': 39.3701
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[to_unit] / conversions[from_unit], formula

def convert_energy(value, from_unit, to_unit):
    conversions = {
        'joule': 1,
        'kilojoule': 0.001,
        'calorie': 0.239006,
        'kilocalorie': 0.000239006,
        'watt hour': 0.000277778,
        'kilowatt hour': 0.000000277778,
        'electron volt': 6.242e+18,
        'british thermal unit': 0.000947817
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[from_unit] / conversions[to_unit], formula

def convert_pressure(value, from_unit, to_unit):
    conversions = {
        'pascal': 1,
        'kilopascal': 0.001,
        'megapascal': 0.000001,
        'bar': 0.00001,
        'atmosphere': 0.00000986923,
        'torr': 0.00750062,
        'psi': 0.000145038,
        'millimeter of mercury': 0.00750062
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[from_unit] / conversions[to_unit], formula

def convert_power(value, from_unit, to_unit):
    conversions = {
        'watt': 1,
        'kilowatt': 0.001,
        'megawatt': 0.000001,
        'horsepower': 0.00134102,
        'british thermal unit per hour': 3.41214,
        'calorie per second': 0.239006
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[from_unit] / conversions[to_unit], formula

def convert_frequency(value, from_unit, to_unit):
    conversions = {
        'hertz': 1,
        'kilohertz': 0.001,
        'megahertz': 0.000001,
        'gigahertz': 0.000000001,
        'cycle per second': 1,
        'revolution per minute': 60,
        'beat per minute': 60
    }
    formula = f"{value} {from_unit} × ({conversions[to_unit]}/{conversions[from_unit]})"
    return value * conversions[from_unit] / conversions[to_unit], formula

def swap_units():
    temp = st.session_state.from_unit
    st.session_state.from_unit = st.session_state.to_unit
    st.session_state.to_unit = temp

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []
if 'from_unit' not in st.session_state:
    st.session_state.from_unit = None
if 'to_unit' not in st.session_state:
    st.session_state.to_unit = None
if 'selected_unit' not in st.session_state:
    st.session_state.selected_unit = "Length"

# Sidebar
with st.sidebar:
    st.markdown('<div class="logo-text">🔄 UniConvert Pro</div>', unsafe_allow_html=True)
    
    # Unit type selection with icons
    st.markdown("""
        <h3 style="
            color: #E0E0E0;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            letter-spacing: 0.5px;
        ">Select Unit Type</h3>
    """, unsafe_allow_html=True)
    
    # Create tabs for category groups
    tabs = st.tabs(["Basic", "Science", "Digital"])
    
    with tabs[0]:  # Basic measurements
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📏 Length", use_container_width=True):
                st.session_state.selected_unit = "Length"
                st.rerun()
            if st.button("⚖️ Weight", use_container_width=True):
                st.session_state.selected_unit = "Weight"
                st.rerun()
            if st.button("🌡️ Temperature", use_container_width=True):
                st.session_state.selected_unit = "Temperature"
                st.rerun()
        with col2:
            if st.button("🧪 Volume", use_container_width=True):
                st.session_state.selected_unit = "Volume"
                st.rerun()
            if st.button("📐 Area", use_container_width=True):
                st.session_state.selected_unit = "Area"
                st.rerun()
            if st.button("⚡ Speed", use_container_width=True):
                st.session_state.selected_unit = "Speed"
                st.rerun()
    
    with tabs[1]:  # Science and time
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏱️ Time", use_container_width=True):
                st.session_state.selected_unit = "Time"
                st.rerun()
            if st.button("📊 Pressure", use_container_width=True):
                st.session_state.selected_unit = "Pressure"
                st.rerun()
        with col2:
            if st.button("⚗️ Energy", use_container_width=True):
                st.session_state.selected_unit = "Energy"
                st.rerun()
            if st.button("🔋 Power", use_container_width=True):
                st.session_state.selected_unit = "Power"
                st.rerun()
    
    with tabs[2]:  # Digital units
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Data", use_container_width=True):
                st.session_state.selected_unit = "Data"
                st.rerun()
            if st.button("📶 Frequency", use_container_width=True):
                st.session_state.selected_unit = "Frequency"
                st.rerun()
    
    # Display unit type icon
    unit_icons = {
        "Length": "📏",
        "Weight": "⚖️",
        "Temperature": "🌡️",
        "Volume": "🧪",
        "Time": "⏱️",
        "Data": "💾",
        "Area": "📐",
        "Speed": "⚡",
        "Pressure": "📊",
        "Energy": "⚗️",
        "Power": "🔋",
        "Frequency": "📶"
    }
    
    st.markdown(f"""
    <div class="unit-icon">
        <div style="font-size: 48px;">{unit_icons.get(st.session_state.selected_unit, "🔄")}</div>
        <h3>{st.session_state.selected_unit}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Update the Recent Conversions header HTML in the sidebar section
    st.markdown("""
        <div class="recent-conversions-header">
            <span class="icon">📋</span>
            <h3>Recent Conversions</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Display history with better styling
    if st.session_state.history:
        for i, conversion in enumerate(reversed(st.session_state.history)):
            st.markdown(f'<div class="history-item">{conversion}</div>', unsafe_allow_html=True)
    else:
        st.info("No recent conversions")

# Main content
st.markdown('<h1 class="animate-fade-in">Unit Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="animate-fade-in">Convert between different units with precision and ease</p>', unsafe_allow_html=True)

# Unit selection based on type
selected_unit = st.session_state.selected_unit

if selected_unit == "Length":
    units = ['meter', 'kilometer', 'centimeter', 'millimeter', 'inch', 'foot', 'yard', 'mile', 'nautical mile']
elif selected_unit == "Weight":
    units = ['kilogram', 'gram', 'milligram', 'pound', 'ounce', 'ton', 'stone']
elif selected_unit == "Temperature":
    units = ['celsius', 'fahrenheit', 'kelvin']
elif selected_unit == "Volume":
    units = ['liter', 'milliliter', 'cubic meter', 'gallon (US)', 'quart (US)', 'pint (US)', 'cup (US)', 
             'fluid ounce (US)', 'tablespoon (US)', 'teaspoon (US)']
elif selected_unit == "Time":
    units = ['second', 'millisecond', 'minute', 'hour', 'day', 'week', 'month (30 days)', 'year (365 days)',
             'decade', 'century', 'millennium']
elif selected_unit == "Data":
    units = ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte', 'petabyte',
             'bit', 'kibibyte', 'mebibyte', 'gibibyte', 'tebibyte', 'pebibyte']
elif selected_unit == "Area":
    units = ['square meter', 'square kilometer', 'square centimeter', 'square millimeter',
             'square inch', 'square foot', 'square yard', 'acre', 'hectare']
elif selected_unit == "Speed":
    units = ['meter per second', 'kilometer per hour', 'mile per hour', 'knot',
             'foot per second', 'inch per second']
elif selected_unit == "Energy":
    units = ['joule', 'kilojoule', 'calorie', 'kilocalorie', 'watt hour', 
             'kilowatt hour', 'electron volt', 'british thermal unit']
elif selected_unit == "Pressure":
    units = ['pascal', 'kilopascal', 'megapascal', 'bar', 'atmosphere', 
             'torr', 'psi', 'millimeter of mercury']
elif selected_unit == "Power":
    units = ['watt', 'kilowatt', 'megawatt', 'horsepower', 
             'british thermal unit per hour', 'calorie per second']
elif selected_unit == "Frequency":
    units = ['hertz', 'kilohertz', 'megahertz', 'gigahertz',
             'cycle per second', 'revolution per minute', 'beat per minute']

# Card for input
st.markdown('<div class="card animate-fade-in">', unsafe_allow_html=True)

# Optimize layout for mobile
if is_mobile():
    column_ratio = [1, 0.5, 1]  # Adjusted ratios for mobile
else:
    column_ratio = [2, 1, 2]  # Original ratios for desktop

# Update the main content layout
col1, col2, col3 = st.columns(column_ratio)

with col1:
    from_unit = st.selectbox("From", units, key="from_unit_select", index=units.index(st.session_state.from_unit) if st.session_state.from_unit in units else 0)
    st.session_state.from_unit = from_unit
    value = st.number_input("Value", value=1.0, step=0.01, format="%.4f")

with col2:
    st.markdown('''
        <div style="display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    height: 100%; 
                    padding: 1rem 0;">
    ''', unsafe_allow_html=True)
    if st.button("↔️ Swap", key="swap_button"):
        swap_units()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    to_unit = st.selectbox("To", units, key="to_unit_select", index=units.index(st.session_state.to_unit) if st.session_state.to_unit in units else min(1, len(units)-1))
    st.session_state.to_unit = to_unit
    st.markdown("<br>", unsafe_allow_html=True)
    convert_button = st.button("Convert", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Perform conversion
if value is not None and (convert_button or True):  # Auto-convert
    # Show a spinner during conversion
    with st.spinner("Converting..."):
        time.sleep(0.3)  # Small delay for effect
        
        if selected_unit == "Length":
            result, formula = convert_length(value, from_unit, to_unit)
        elif selected_unit == "Weight":
            result, formula = convert_weight(value, from_unit, to_unit)
        elif selected_unit == "Temperature":
            result, formula = convert_temperature(value, from_unit, to_unit)
        elif selected_unit == "Volume":
            result, formula = convert_volume(value, from_unit, to_unit)
        elif selected_unit == "Time":
            result, formula = convert_time(value, from_unit, to_unit)
        elif selected_unit == "Data":
            result, formula = convert_data(value, from_unit, to_unit)
        elif selected_unit == "Area":
            result, formula = convert_area(value, from_unit, to_unit)
        elif selected_unit == "Speed":
            result, formula = convert_speed(value, from_unit, to_unit)
        elif selected_unit == "Energy":
            result, formula = convert_energy(value, from_unit, to_unit)
        elif selected_unit == "Pressure":
            result, formula = convert_pressure(value, from_unit, to_unit)
        elif selected_unit == "Power":
            result, formula = convert_power(value, from_unit, to_unit)
        elif selected_unit == "Frequency":
            result, formula = convert_frequency(value, from_unit, to_unit)
    
    # Display result
    st.markdown(f"""
    <div class="result-display animate-fade-in">
        {value:.4f} {from_unit} = {result:.4f} {to_unit}
        <button class="copy-btn" onclick="navigator.clipboard.writeText('{result:.4f} {to_unit}')">📋</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Display formula
    st.markdown(f'<div class="formula-display">Formula: {formula} = {result:.4f}</div>', unsafe_allow_html=True)
    
    # Add to history
    if len(st.session_state.history) >= 5:
        st.session_state.history.pop(0)
    st.session_state.history.append(f"{value:.4f} {from_unit} → {result:.4f} {to_unit}")

# Additional features card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### Quick Reference")

if selected_unit == "Length":
    reference_data = {
        "Unit": ["meter", "kilometer", "inch", "foot", "mile"],        "Equivalent": ["1 meter", "1000 meters", "0.0254 meters", "0.3048 meters", "1609.34 meters"]
    }
elif selected_unit == "Weight":
    reference_data = {
        "Unit": ["kilogram", "gram", "pound", "ounce", "ton"],
        "Equivalent": ["1 kilogram", "0.001 kilograms", "0.453592 kilograms", "0.0283495 kilograms", "1000 kilograms"]
    }
elif selected_unit == "Temperature":
    reference_data = {
        "Unit": ["celsius", "fahrenheit", "kelvin"],
        "Freezing Point": ["0°C", "32°F", "273.15K"],
        "Boiling Point": ["100°C", "212°F", "373.15K"]
    }
elif selected_unit == "Volume":
    reference_data = {
        "Unit": ["liter", "milliliter", "gallon (US)", "cup (US)", "fluid ounce (US)"],
        "Equivalent": ["1 liter", "0.001 liters", "3.78541 liters", "0.236588 liters", "0.0295735 liters"]
    }
elif selected_unit == "Time":
    reference_data = {
        "Unit": ["second", "minute", "hour", "day", "year"],
        "Equivalent": ["1 second", "60 seconds", "3600 seconds", "86400 seconds", "31536000 seconds"]
    }
elif selected_unit == "Data":
    reference_data = {
        "Unit": ["byte", "kilobyte", "megabyte", "gigabyte", "terabyte"],
        "Equivalent": ["1 byte", "1024 bytes", "1048576 bytes", "1073741824 bytes", "1099511627776 bytes"]
    }
elif selected_unit == "Area":
    reference_data = {
        "Unit": ["square meter", "square kilometer", "acre", "hectare"],
        "Equivalent": ["1 m²", "1,000,000 m²", "4046.86 m²", "10,000 m²"]
    }
elif selected_unit == "Speed":
    reference_data = {
        "Unit": ["meter per second", "kilometer per hour", "mile per hour", "knot"],
        "Equivalent": ["1 m/s", "3.6 km/h", "2.237 mph", "1.944 knots"]
    }
elif selected_unit == "Energy":
    reference_data = {
        "Unit": ["joule", "kilojoule", "kilocalorie", "watt hour", "kilowatt hour"],
        "Equivalent": ["1 J", "1000 J", "4184 J", "3600 J", "3.6×10⁶ J"]
    }
elif selected_unit == "Pressure":
    reference_data = {
        "Unit": ["pascal", "kilopascal", "bar", "atmosphere", "psi"],
        "Equivalent": ["1 Pa", "1000 Pa", "100000 Pa", "101325 Pa", "6894.76 Pa"]
    }
elif selected_unit == "Power":
    reference_data = {
        "Unit": ["watt", "kilowatt", "horsepower", "british thermal unit per hour"],
        "Equivalent": ["1 W", "1000 W", "745.7 W", "0.293071 W"]
    }
elif selected_unit == "Frequency":
    reference_data = {
        "Unit": ["hertz", "kilohertz", "megahertz", "gigahertz"],
        "Equivalent": ["1 Hz", "1000 Hz", "1000000 Hz", "1000000000 Hz"]
    }

reference_df = pd.DataFrame(reference_data)
st.dataframe(reference_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("©2025 Made With Stremlit By Talal Shoaib | UniConvert Pro", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Easter egg - hidden feature
if st.session_state.history and len(st.session_state.history) > 3:
    st.markdown('<div style="text-align: center; margin-top: 20px; font-size: 12px; color: var(--text-light);">🎉 You\'ve unlocked dark mode pro! Keep converting!</div>', unsafe_allow_html=True)

# Add touch feedback for buttons
def add_touch_feedback():
    st.markdown("""
        <script>
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('touchstart', () => {
                button.style.transform = 'scale(0.98)';
            });
            button.addEventListener('touchend', () => {
                button.style.transform = 'scale(1)';
            });
        });
        </script>
    """, unsafe_allow_html=True)

# Call the touch feedback function
add_touch_feedback()

