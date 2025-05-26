import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Password Protection
def check_password():
    def password_entered():
        if st.session_state["password"] == "SPI2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("## 🔐 SPI ROI Calculator - Zugang")
        st.text_input("Passwort eingeben:", type="password", 
                     on_change=password_entered, key="password")
        st.info("💡 Passwort erforderlich für Zugang zum ROI Calculator")
        st.markdown("---")
        st.markdown("**SPI GmbH** - Automatisierungslösungen für die Blechbearbeitung")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("## 🔐 SPI ROI Calculator - Zugang")
        st.text_input("Passwort eingeben:", type="password", 
                     on_change=password_entered, key="password")
        st.error("❌ Falsches Passwort - Bitte erneut versuchen")
        st.info("💡 Kontaktieren Sie Ihr SPI Team für das Passwort")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Seitenkonfiguration
st.set_page_config(
    page_title="SPI ROI Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .roi-highlight {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏭 SPI ROI Calculator</h1>
    <p>Berechnen Sie den Return on Investment Ihrer Automatisierungslösung für die Blechbearbeitung</p>
</div>
""", unsafe_allow_html=True)

# Sidebar für Eingaben
st.sidebar.header("📝 Parameter eingeben")

# Unternehmensdaten
st.sidebar.subheader("🏢 Unternehmensdaten")
mitarbeiter_anzahl = st.sidebar.number_input("Anzahl Mitarbeiter", value=50, min_value=1)
jahresumsatz = st.sidebar.number_input("Jahresumsatz (€)", value=5000000, min_value=100000, step=100000)
teile_pro_jahr = st.sidebar.number_input("Teile pro Jahr", value=2000, min_value=100, step=100)

# Aktuelle Situation
st.sidebar.subheader("⏱️ Aktuelle Situation")
manuelle_zeit = st.sidebar.number_input("Programmierzeit pro Teil (Min)", value=120, min_value=1)
fehlerquote_aktuell = st.sidebar.slider("Aktuelle Fehlerquote (%)", 0.0, 15.0, 5.0, 0.1)
durchlaufzeit_aktuell = st.sidebar.number_input("Durchlaufzeit (Tage)", value=14, min_value=1)
personalkosten = st.sidebar.number_input("Personalkosten (€/Stunde)", value=65, min_value=20)

# SPI Lösung
st.sidebar.subheader("🚀 SPI Verbesserungen")
zeitersparnis = st.sidebar.slider("Zeitersparnis Programmierung (%)", 0, 90, 75)
fehlerreduktion = st.sidebar.slider("Fehlerreduktion (%)", 0, 95, 80)
durchlaufzeit_reduktion = st.sidebar.slider("Durchlaufzeit-Reduktion (%)", 0, 70, 40)

# Investitionskosten
st.sidebar.subheader("💰 Investition")
software_kosten = st.sidebar.number_input("Software-Lizenzen (€)", value=85000, min_value=10000, step=5000)
implementierung_kosten = st.sidebar.number_input("Implementierung (€)", value=25000, min_value=5000, step=2500)
schulung_kosten = st.sidebar.number_input("Schulungen (€)", value=15000, min_value=2000, step=1000)

# Berechnungen
def calculate_roi():
    # Zeitersparnis
    aktuelle_zeit_pro_teil = manuelle_zeit / 60  # in Stunden
    neue_zeit_pro_teil = aktuelle_zeit_pro_teil * (1 - zeitersparnis / 100)
    zeitersparnis_pro_teil = aktuelle_zeit_pro_teil - neue_zeit_pro_teil
    gesamt_zeitersparnis = zeitersparnis_pro_teil * teile_pro_jahr
    kosteneinsparung_zeit = gesamt_zeitersparnis * personalkosten
    
    # Fehlerreduktion
    aktuelle_fehlkosten = jahresumsatz * (fehlerquote_aktuell / 100) * 0.3
    neue_fehlkosten = aktuelle_fehlkosten * (1 - fehlerreduktion / 100)
    kosteneinsparung_fehler = aktuelle_fehlkosten - neue_fehlkosten
    
    # Durchlaufzeit
    durchlaufzeit_vorher = durchlaufzeit_aktuell
    durchlaufzeit_nachher = durchlaufzeit_vorher * (1 - durchlaufzeit_reduktion / 100)
    kapitalbindung_reduktion = (jahresumsatz * 0.4) * ((durchlaufzeit_vorher - durchlaufzeit_nachher) / 365) * 0.05
    
    # Zusätzliche Aufträge
    mehr_auftraege = teile_pro_jahr * (durchlaufzeit_reduktion / 100) * 0.5
    zusatz_umsatz = mehr_auftraege * (jahresumsatz / teile_pro_jahr) * 0.15
    
    # Gesamtkosten und ROI
    gesamt_investition = software_kosten + implementierung_kosten + schulung_kosten
    jahres_einsparungen = kosteneinsparung_zeit + kosteneinsparung_fehler + kapitalbindung_reduktion + zusatz_umsatz
    
    payback_period = gesamt_investition / jahres_einsparungen if jahres_einsparungen > 0 else 0
    roi_3_jahre = ((jahres_einsparungen * 3 - gesamt_investition) / gesamt_investition) * 100 if gesamt_investition > 0 else 0
    npv_3_jahre = jahres_einsparungen * 2.72 - gesamt_investition
    
    return {
        'zeitersparnis_pro_teil': zeitersparnis_pro_teil,
        'kosteneinsparung_zeit': kosteneinsparung_zeit,
        'kosteneinsparung_fehler': kosteneinsparung_fehler,
        'kapitalbindung_reduktion': kapitalbindung_reduktion,
        'zusatz_umsatz': zusatz_umsatz,
        'jahres_einsparungen': jahres_einsparungen,
        'gesamt_investition': gesamt_investition,
        'payback_period': payback_period,
        'roi_3_jahre': roi_3_jahre,
        'npv_3_jahre': npv_3_jahre,
        'durchlaufzeit_vorher': durchlaufzeit_vorher,
        'durchlaufzeit_nachher': durchlaufzeit_nachher
    }

# Berechnungen durchführen
results = calculate_roi()

# Hauptbereich mit Ergebnissen
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 ROI Ergebnisse")
    
    # Key Metrics
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    
    with col_metric1:
        st.metric(
            "Amortisation", 
            f"{results['payback_period']:.1f} Jahre",
            delta=f"{'Sehr gut' if results['payback_period'] < 2 else 'Gut' if results['payback_period'] < 3 else 'Akzeptabel'}"
        )
    
    with col_metric2:
        st.metric(
            "ROI (3 Jahre)", 
            f"{results['roi_3_jahre']:.0f}%",
            delta=f"{'Exzellent' if results['roi_3_jahre'] > 200 else 'Sehr gut' if results['roi_3_jahre'] > 100 else 'Gut'}"
        )
    
    with col_metric3:
        st.metric(
            "Jährliche Einsparung", 
            f"{results['jahres_einsparungen']:,.0f} €",
            delta=f"{results['jahres_einsparungen']/results['gesamt_investition']:.1f}x Investition"
        )

with col2:
    # ROI Highlight Box
    st.markdown(f"""
    <div class="roi-highlight">
        <h3>💰 Nettogewinn (3 Jahre)</h3>
        <h2>{results['npv_3_jahre']:,.0f} €</h2>
        <p>Nach Abzug aller Investitionskosten</p>
    </div>
    """, unsafe_allow_html=True)

# Detaillierte Einsparungen
st.header("💡 Einsparungen im Detail")

einsparungen_data = {
    'Bereich': ['Zeitersparnis\nProgrammierung', 'Fehler-\nreduktion', 'Kapitalbindung\nreduziert', 'Zusätzliche\nAufträge'],
    'Einsparung': [
        results['kosteneinsparung_zeit'],
        results['kosteneinsparung_fehler'], 
        results['kapitalbindung_reduktion'],
        results['zusatz_umsatz']
    ],
    'Farben': ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b']
}

fig_einsparungen = px.bar(
    einsparungen_data, 
    x='Bereich', 
    y='Einsparung',
    color='Bereich',
    color_discrete_sequence=einsparungen_data['Farben'],
    title="Jährliche Einsparungen nach Bereichen"
)
fig_einsparungen.update_layout(showlegend=False, xaxis_title="", yaxis_title="Einsparung (€)")
fig_einsparungen.update_traces(texttemplate='%{y:,.0f}€', textposition='outside')

st.plotly_chart(fig_einsparungen, use_container_width=True)

# Operative Verbesserungen
st.header("⚡ Operative Verbesserungen")

col_op1, col_op2, col_op3 = st.columns(3)

with col_op1:
    st.info(f"""
    **Programmierzeit pro Teil**
    
    Vorher: {manuelle_zeit} Min
    
    Nachher: {manuelle_zeit * (1-zeitersparnis/100):.0f} Min
    
    ✅ **-{results['zeitersparnis_pro_teil']*60:.0f} Min gespart**
    """)

with col_op2:
    st.success(f"""
    **Durchlaufzeit**
    
    Vorher: {results['durchlaufzeit_vorher']} Tage
    
    Nachher: {results['durchlaufzeit_nachher']:.1f} Tage
    
    ✅ **-{results['durchlaufzeit_vorher']-results['durchlaufzeit_nachher']:.1f} Tage schneller**
    """)

with col_op3:
    st.warning(f"""
    **Fehlerquote**
    
    Vorher: {fehlerquote_aktuell}%
    
    Nachher: {fehlerquote_aktuell*(1-fehlerreduktion/100):.1f}%
    
    ✅ **-{fehlerquote_aktuell*fehlerreduktion/100:.1f}% weniger Fehler**
    """)

# 3-Jahres Cashflow
st.header("📈 3-Jahres Cashflow")

jahre = ['Jahr 0', 'Jahr 1', 'Jahr 2', 'Jahr 3']
cashflow = [
    -results['gesamt_investition'],
    results['jahres_einsparungen'] - results['gesamt_investition'],
    results['jahres_einsparungen'] * 2 - results['gesamt_investition'],
    results['jahres_einsparungen'] * 3 - results['gesamt_investition']
]

fig_cashflow = go.Figure()
fig_cashflow.add_trace(go.Scatter(
    x=jahre, 
    y=cashflow,
    mode='lines+markers',
    line=dict(color='#10b981', width=3),
    marker=dict(size=8)
))

fig_cashflow.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
fig_cashflow.update_layout(
    title="Kumulativer Cashflow über 3 Jahre",
    xaxis_title="Jahr",
    yaxis_title="Kumulativer Cashflow (€)",
    yaxis_tickformat=',.'
)

st.plotly_chart(fig_cashflow, use_container_width=True)

# Investment Summary
st.header("📋 Investment Summary")

col_inv1, col_inv2 = st.columns(2)

with col_inv1:
    st.subheader("💸 Investitionskosten")
    investment_df = pd.DataFrame({
        'Bereich': ['Software-Lizenzen', 'Implementierung', 'Schulungen', 'GESAMT'],
        'Kosten': [software_kosten, implementierung_kosten, schulung_kosten, results['gesamt_investition']],
        'Anteil': [
            f"{software_kosten/results['gesamt_investition']*100:.0f}%",
            f"{implementierung_kosten/results['gesamt_investition']*100:.0f}%", 
            f"{schulung_kosten/results['gesamt_investition']*100:.0f}%",
            "100%"
        ]
    })
    st.dataframe(investment_df, hide_index=True)

with col_inv2:
    st.subheader("💰 Nutzen-Kosten-Verhältnis")
    
    bcr_3_jahre = (results['jahres_einsparungen'] * 3) / results['gesamt_investition']
    
    if bcr_3_jahre > 3:
        bcr_bewertung = "🚀 Hervorragend"
        bcr_color = "green"
    elif bcr_3_jahre > 2:
        bcr_bewertung = "✅ Sehr gut"
        bcr_color = "green" 
    elif bcr_3_jahre > 1.5:
        bcr_bewertung = "👍 Gut"
        bcr_color = "orange"
    else:
        bcr_bewertung = "⚠️ Kritisch"
        bcr_color = "red"
    
    st.markdown(f"""
    **Nutzen-Kosten-Verhältnis:** {bcr_3_jahre:.1f}:1
    
    **Bewertung:** :{bcr_color}[{bcr_bewertung}]
    
    Für jeden investierten Euro erhalten Sie {bcr_3_jahre:.1f}€ zurück.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>SPI GmbH ROI Calculator</strong> - Ihre Investition in die Zukunft der Blechbearbeitung</p>
    <p><em>Alle Berechnungen basieren auf Ihren Eingaben und typischen Branchenwerten.</em></p>
</div>
""", unsafe_allow_html=True)