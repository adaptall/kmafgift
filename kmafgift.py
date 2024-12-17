import streamlit as st
import pandas as pd

# Satsdata for vejafgift
sats_data_2025_2027 = {
    "CO2-emissionsklasse": ["Klasse 1", "Klasse 2", "Klasse 3", "Klasse 4", "Klasse 5"],
    "12-17,9 ton": [1.29, 1.19, 1.04, 0.69, 0.20],
    "18-32 ton": [1.50, 1.38, 1.23, 0.80, 0.20],
    "Over 32 ton": [1.65, 1.52, 1.37, 0.87, 0.20],
    "Øvrige veje": [0.86, 0.79, 0.69, 0.46, 0.13],
    "Ikke-afgiftsbelagte veje": [0.00, 0.00, 0.00, 0.00, 0.00]
}

sats_data_2028 = {
    "CO2-emissionsklasse": ["Klasse 1", "Klasse 2", "Klasse 3", "Klasse 4", "Klasse 5"],
    "12-17,9 ton": [1.72, 1.57, 1.36, 0.92, 0.29],
    "18-32 ton": [1.78, 1.62, 1.40, 1.04, 0.29],
    "Over 32 ton": [1.96, 1.78, 1.57, 1.11, 0.29],
    "Øvrige veje": [1.14, 1.05, 0.90, 0.62, 0.19],
    "Ikke-afgiftsbelagte veje": [0.00, 0.00, 0.00, 0.00, 0.00]
}

sats_data_2029 = {
    "CO2-emissionsklasse": ["Klasse 1", "Klasse 2", "Klasse 3", "Klasse 4", "Klasse 5"],
    "12-17,9 ton": [1.94, 1.70, 1.46, 1.00, 0.39],
    "18-32 ton": [2.02, 1.83, 1.57, 1.19, 0.39],
    "Over 32 ton": [2.27, 2.02, 1.76, 1.25, 0.39],
    "Øvrige veje": [1.29, 1.13, 0.97, 0.66, 0.26],
    "Ikke-afgiftsbelagte veje": [0.00, 0.00, 0.00, 0.00, 0.00]
}

sats_data = {
    "2025-2027": pd.DataFrame(sats_data_2025_2027),
    "2028": pd.DataFrame(sats_data_2028),
    "2029": pd.DataFrame(sats_data_2029)
}

# Streamlit layout
st.title("Kilometerbaseret Vejafgiftsberegner")
st.write("Beregn din vejafgift baseret på emissionsklasse, vægtklasse, vejtype og antal kilometer kørt.")

# Inputparametre
co2_klasse = st.selectbox("Vælg CO2-emissionsklasse:", sats_data_2025_2027["CO2-emissionsklasse"])
vægt_klasse = st.selectbox("Vælg vægtklasse:", ["12-17,9 ton", "18-32 ton", "Over 32 ton"])
procent_miljoezone = st.slider("Procentdel af kørsel i miljøzone (%)", 0, 100, 1)
procent_ikke_afgiftsbelagte = st.slider("Procentdel af kørsel på ikke-afgiftsbelagte veje (%)", 0, 100 - procent_miljoezone, 1)
antal_kilometer = st.number_input("Indtast det samlede antal kilometer kørt:", min_value=1, value=1000)
årstal = st.selectbox("Vælg år for beregning:", ["2025-2027", "2028", "2029"])

# Beregninger
sats_df = sats_data[årstal]

miljoezone_sats = sats_df.loc[sats_df["CO2-emissionsklasse"] == co2_klasse, vægt_klasse].values[0]
ovrige_veje_sats = sats_df.loc[sats_df["CO2-emissionsklasse"] == co2_klasse, "Øvrige veje"].values[0]
ikke_afgiftsbelagte_sats = sats_df.loc[sats_df["CO2-emissionsklasse"] == co2_klasse, "Ikke-afgiftsbelagte veje"].values[0]

km_miljoezone = (procent_miljoezone / 100) * antal_kilometer
km_ikke_afgiftsbelagte = (procent_ikke_afgiftsbelagte / 100) * antal_kilometer
km_ovrige_veje = antal_kilometer - km_miljoezone - km_ikke_afgiftsbelagte

af_gift_total = (km_miljoezone * miljoezone_sats) + (km_ovrige_veje * ovrige_veje_sats) + (km_ikke_afgiftsbelagte * ikke_afgiftsbelagte_sats)

# Vis resultater
st.subheader("Resultat")
st.write(f"Samlet vejafgift for {antal_kilometer} km i {årstal}: {af_gift_total:.2f} kr.")
