import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import pandas as pd
import matplotlib.pyplot as plt


location = Location (latitude = 51.21826587795989, longitude=6.779891694457053,
                     tz="Europe/Berlin", altitude = 30, name ="home")

sandia_modules=pvlib.pvsystem.retrieve_sam("SandiaMod")
cec_inverters=pvlib.pvsystem.retrieve_sam("CECInverter")

module=sandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter=cec_inverters['ABB__PVI_3_0_OUTD_S_US_A__208V_']

temperature_parameters=TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

system = PVSystem(surface_tilt=45, surface_azimuth=180,
                  module_parameters=module, inverter_parameters=inverter,
                  temperature_model_parameters=temperature_parameters,
                  modules_per_string=7, strings_per_inverter=2)

modelchain = ModelChain(system, location)


#----------------------------------------------------------------------------------------------
#preprocessing the TMY data
tmy = pd.read_csv(r"C:\Users\user\OneDrive\Desktop\Srinaath personal files\Personal projects\Project 6 Calculating solar pv output from irradiation data\TMY_data.csv", skiprows=16, nrows=8760,
                  usecols=["time(UTC)","T2m","G(h)", "Gb(n)", "Gd(h)","WS10m"],
                  index_col=0)

tmy.index = pd.date_range(start="2023-01-01 00:00", end="2023-12-31 23:00", freq= "h")
tmy.columns = ["temp_air", "ghi", "dni", "dhi", "wind_speed"]

# print(tmy)
# tmy.plot(figsize=(16,9))
# plt.show()

tmy.to_csv(r"C:\Users\user\OneDrive\Desktop\Srinaath personal files\Personal projects\Project 6 Calculating solar pv output from irradiation data\processed_data_Dusseldorf.csv")

#----------------------------------------------------------------------------------------------

tmy = pd.read_csv(r"C:\Users\user\OneDrive\Desktop\Srinaath personal files\Personal projects\Project 6 Calculating solar pv output from irradiation data\processed_data_Dusseldorf.csv",
                  index_col=0)

tmy.index=pd.to_datetime(tmy.index)
modelchain.run_model(tmy)
ax= modelchain.results.ac.plot(figsize=(16,9))
ax.set_title ("Hourly AC Power Output (in Watts")
#ax.set_xlabel("Time")
ax.set_ylabel("Power Output (W)")
plt.show()

axx=modelchain.results.ac.resample("M").sum().plot(figsize=(16,9))
axx.set_title ("Energy Output (in Watt-hours)")
axx.set_ylabel("Energy Output (Wh)")
plt.show()

# Resample the AC power output by month, and sum it up
monthly_total = modelchain.results.ac.resample("M").sum()

# Print the summed-up values for each month
print("Monthly Total Energy Output (Wh):")
for month, total in monthly_total.items():
    # Format and print the total for each month
    print(f"{month.strftime('%B %Y')}: {total:.2f} Wh")
    
yearly_total = monthly_total.sum()

# Print the total energy output for the entire year
print(f"\nTotal Energy Output for the Year: {yearly_total:.2f} Wh")
#----------------------------------------------------------------------------------------------








