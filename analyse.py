import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("outputs", exist_ok=True)

#Load cleaned data
df= pd.read_csv("data/cleaned.csv")
print(f"Loaded{len(df):,}rows")

#extract hour of day

df["hour"]= (df["departure_sec"]// 3600)
df["hour"] = df["hour"].astype(int)

#Analysis 1
print("\nAnalysing busiest hours...")
hourly= (df.groupby("hour").size().reset_index(name="departures"))

print(hourly.to_string(index=False))
hourly.to_csv("outputs/hourly_summary.csv",index=False)

#Analysis 2
print("\nAnalysing top routes...." )
top_routes = (df.groupby("route_short_name")
              .size()
              .reset_index(name="total_stops")
              .sort_values("total_stops")
              .sort_values("total_stops", ascending=False)
              .head(10))
print(top_routes.to_string(index=False))
top_routes.to_string(index=False)

#Anslysis 3
print("\nAnalysing peak periods...")

def get_period(hour):
    if 6 <= hour <= 9:
        return "AM Peak"
    elif 16 <= hour <= 19:
        return "PM Peak"
    else:
        return "Off-Peak"

df["period"] = df["hour"].apply(get_period)
period_summary = (df.groupby("period")
                    .size()
                    .reset_index(name="departures"))
print(period_summary.to_string(index=False))
period_summary.to_csv("outputs/period_summary.csv", index=False)

# -------------------------------------------------------
# CHART 1 — DEPARTURES BY HOUR
# -------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.bar(hourly["hour"], hourly["departures"], color="steelblue")
plt.title("Brisbane Departures by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Scheduled Departures")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig("outputs/chart_hourly.png")
plt.close()
print("\nSaved: chart_hourly.png")

# -------------------------------------------------------
# CHART 2 — TOP 10 BUSIEST ROUTES
# -------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.barh(top_routes["route_short_name"].astype(str),
         top_routes["total_stops"],
         color="teal")
plt.title("Top 10 Busiest Brisbane Routes")
plt.xlabel("Total Scheduled Stops")
plt.ylabel("Route")
plt.tight_layout()
plt.savefig("outputs/chart_top_routes.png")
plt.close()
print("Saved: chart_top_routes.png")

# -------------------------------------------------------
# CHART 3 — PEAK VS OFF-PEAK
# -------------------------------------------------------
colours = {"AM Peak": "orange", "PM Peak": "steelblue", "Off-Peak": "grey"}
plt.figure(figsize=(6, 5))
plt.bar(period_summary["period"],
        period_summary["departures"],
        color=[colours[p] for p in period_summary["period"]])
plt.title("Brisbane Departures: Peak vs Off-Peak")
plt.xlabel("Period")
plt.ylabel("Scheduled Departures")
plt.tight_layout()
plt.savefig("outputs/chart_peak.png")
plt.close()
print("Saved: chart_peak.png")

print("\nAll done. Check your outputs/ folder.")