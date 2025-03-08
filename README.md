<h1 align="center">EasySoccerData</h1>
<p align="center">
A simple python package for extracting real-time soccer data from diverse online sources, providing essential statistics and insights.
</p>


> [!IMPORTANT]  
> Currently in the early development phase. Please take this into consideration.

# Installation
```
pip install easysoccerdata
```

# Usage
Simple example using Sofascore
```py
import esd

# get live events
client = esd.SofascoreClient()
events = client.get_events(live=True)
for event in events:
    print(event)

# search matchs
matchs: list[esd.Event] = client.search(
    "Real Madrid", entity=esd.EntityType.EVENT
)
for match in matchs:
    print(f"Match ID: {match.id}, Status: {match.status.description}")
    print(f"{match.home_team.name} vs {match.away_team.name}")
```

And more! Check out [examples](https://github.com/manucabral/EasySoccerData/tree/main/examples)

# Supported modules

| Name | Implemented |
| :---  | :---: |
| Sofascore   | ✔️ |
| FBref    | ❌ |
| Understat | ❌ |
...

### Constributions
All constributions, bug reports or fixes and ideas are welcome.
