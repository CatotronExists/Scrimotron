import nextcord
import traceback
from nextcord.ext import commands
from Main import formatOutput, guildID, errorResponse, channel_poi
from Config import db_team_data, db_bot_data

### POIS (as of season 19)
pois = {
    "Map": {
        "Worlds Edge": {
            "Big Maude": {
                "ID": "Big Maude",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Stacks"],
                    "Secondary": [None] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a" },
                "Vechical": False }, 

            "Climatizer":
                {"ID": "Climatizer",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Epicenter", "Survey Camp"],
                    "Secondary": ["Fissure Crossing"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West" },
                "Vechical": False },

            "Countdown":
                {"ID": "Countdown",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Lava Fissure", "Trials"],
                    "Secondary": ["Hill Valley", "The Bridge"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South" },
                "Vechical": True },

            "Fragment East":
                {"ID": "Fragment East",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Monument"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West" },
                "Vechical": True },

            "Harvester":
                {"ID": "Harvester",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Staging"],
                    "Secondary": ["Mining Pass", "The Ridge"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South" },
                "Vechical": True },

            "Landslide":
                {"ID": "Landslide",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Outlook", "Staging"],
                    "Secondary": ["Hill Valley", "The Bridge", "Mining Pass"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a" },
                "Vechical": True },

            "Launch Site":
                {"ID": "Launch Site",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["The Tree", "The Dome"],
                    "Secondary": ["Lava Fields"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South" },
                "Vechical": True },

            "Lava Fissure":
                {"ID": "Lava Fissure",
                "Type": "MAIN",
                "Neighbours": {
                    "Main": ["Mirage à Trois", "Countdown"],
                    "Secondary": ["The Bridge"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South" },
                "Vechical": False },

            "Lava Siphon":
                {"ID": "Lava Siphon",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["The Tree", "Launch Site"],
                    "Secondary": ["The Ridge"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West" },
                "Vechical": False },

            "Mirage à Trois":
                {"ID": "Mirage à Trois",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Staging", "Lava Fissure"],
                    "Secondary": ["The Bridge"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },

            "Monument":
                {"ID": "Monument",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Fragment East", "Epicenter"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Overlook":
                {"ID": "Overlook",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Fragment East"],
                    "Secondary": ["Tunnel", "Fissure Crossing"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Skyhook":
                {"ID": "Skyhook",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Trials"],
                    "Secondary": ["Storage Room", "Rain Tunnel", "Sniper's Ridge"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },

            "Stacks":
                {"ID": "Stacks",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Big Maude", "The Dome"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },

            "Staging":
                {"ID": "Staging",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Mirage à Trois", "Harvester", "Landslide"],
                    "Secondary": ["The Bridge", "Mining Pass"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "Top/Bottom"},
                "Vechical": True },

            "Survey Camp":
                {"ID": "Survey Camp",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Epicenter", "Climatizer"],
                    "Secondary": ["Rain Tunnel", "Fissure Crossing"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },

            "The Dome":
                {"ID": "The Dome",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Launch Site", "Stacks"],
                    "Secondary": ["Lava Fields"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },

            "The Epicenter":
                {"ID": "The Epicenter",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Climatizer", "Survey Camp", "Monument"],
                    "Secondary": ["Fissure Crossing"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },
                
            "The Geyser":
                {"ID": "The Geyser",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Big Maude"],
                    "Secondary": ["Tunnel", "The Ridge"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "The Tree":
                {"ID": "The Tree",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Lava Siphon", "Launch Site"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "Center/Outer"},
                "Vechical": False },

            "Thermal Station":
                {"ID": "Thermal Station",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Staging", "The Tree"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },

            "Trials":
                {"ID": "Trials",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Countdown", "Skyhook", "Lava Siphon"],
                    "Secondary": ["Uncharted Territories", "Sniper's Ridge"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },

        }, "Olympus":
            {"Bonsai Plaza":
                {"ID": "Bonsai Plaza",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Icarus", "Phase Driver"],
                    "Secondary": ["Bonsai Hillside"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },

            "Clinc":
                {"ID": "Clinic",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Gardens", "Grow Towers"],
                    "Secondary": ["Power Station East", "Energy Depot"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Docks":
                {"ID": "Docks",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Fight Night", "Supercarrier"],
                    "Secondary": ["Landing Pier", "Secondary Power Grid"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Elysium":
                {"ID": "Elysium",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Hydroponics"],
                    "Secondary": ["Farmstead"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Energy Depot":
                {"ID": "Energy Depot",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Hammond Labs", "Gardens"],
                    "Secondary": ["Underpass"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Estates":
                {"ID": "Estates",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Wildflower Meadow", "Phase Gateway West"] },
                "Split": {  
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },

            "Fight Night":
                {"ID": "Fight Night",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Supercarrier", "Turbine", "Power Grid"],
                    "Secondary": ["Landing Pier", "Secondary Power Grid"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Gardens":
                {"ID": "Gardens",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Energy Depot", "Clinc"],
                    "Secondary": ["Underpass", "Power Station East"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Grow Towers":
                {"ID": "Grow Towers",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Clinc", "Gardens"],
                    "Secondary": ["Ivory Pass"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Hammond Labs":
                {"ID": "Hammond Labs",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Energy Depot", "Terminal"],
                    "Secondary": ["Phase Gateway Center", "Lab Annex", "Research Basin"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Hydroponics":
                {"ID": "Hydroponics",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Elysium"],
                    "Secondary": ["Farmstead", "Backlot", "Agriculture Entry"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Icarus":
                {"ID": "Icarus",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Bonsai Plaza", "Solar Array"],
                    "Secondary": ["Defense Perimeter", "Power Station South"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Oasis":
                {"ID": "Oasis",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Icarus"],
                    "Secondary": ["Shipyard", "Irrigation Platform", "Oasis Villa"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Orbital Cannon":
                {"ID": "Orbital Cannon",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Icarus"],
                    "Secondary": ["Defense Perimeter", "Power Station South"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Phase Driver":
                {"ID": "Phase Driver",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Bonsai Plaza"],
                    "Secondary": ["Backlot", "Shifted Grounds"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Power Grid":
                {"ID": "Power Grid",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Fight Night", "Turbine"],
                    "Secondary": ["Secondary Power Grid", "Supply Track"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Rift":
                {"ID": "Rift",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Power Grid"],
                    "Secondary": ["Secondary Power Grid", "Supply Track"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Solar Array":
                {"ID": "Solar Array",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Icarus"],
                    "Secondary": ["Defense Perimeter", "Bonsai Hillside"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Supercarrier":
                {"ID": "Supercarrier",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Docks", "Fight Night"],
                    "Secondary": ["Shipyard"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
            "Terminal":
                {"ID": "Terminal",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Hammond Labs"],
                    "Secondary": ["Lab Annex", "Shifted Grounds"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Turbine":
                {"ID": "Turbine",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Fight Night"],
                    "Secondary": ["Antechamber", "Maintenance"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
        }, "Kings Canyon":
            {"Airbase":
                {"ID": "Airbase",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Bunker", "Gauntlet"],
                    "Secondary": ["High Desert"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
            "Artillery":
                {"ID": "Artillery",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Destroyed Artillery Tunnel", "Watchtower North"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Basin":
                {"ID": "Basin",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Rig"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
            "Bunker":
                {"ID": "Bunker",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["River Center", "High Desert", "The Cage"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Containment":
                {"ID": "Containment",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Destroyed Cascades", "Lagoon Crossing", "Watchtower North"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },
            
            "Gauntlet":
                {"ID": "Gauntlet",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Relic", "Airbase"],
                    "Secondary": ["Broken Coast Overlook"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"}, 
                "Vechical": False },
            
            "Hydro Dam":
                {"ID": "Hydro Dam",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Repulsor", "Cage"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"}, 
                "Vechical": False },
            
            "Map Room":
                {"ID": "Map Room",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Repulsor"],
                    "Secondary": ["Watchtower South"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },
            
            "Market":
                {"ID": "Market",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Relic"],
                    "Secondary": ["Caves", "River Center"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Relic":
                {"ID": "Relic",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Gauntlet", "Market"],
                    "Secondary": ["Broken Coast Overlook"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Repulsor":
                {"ID": "Repulsor",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Hydro Dam", "Map Room"],
                    "Secondary": ["Watchtower South"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Rig":
                {"ID": "Rig",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Basin"],
                    "Secondary": ["Broken Coast Overlook"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Runoff":
                {"ID": "Runoff",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["The Pit"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
            "Singh Labs":
                {"ID": "Singh Labs",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Swamps", "Capacitor"],
                    "Secondary": ["Capacitor Tunnel"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "Top/Bottom"},
                "Vechical": False },
            
            "Spotted Lakes":
                {"ID": "Spotted Lakes",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["The Pit"],
                    "Secondary": ["Uncovered Bone"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
            
            "Swamps":
                {"ID": "Swamps",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Singh Labs", "Repulsor"],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },

            "The Cage":
                {"ID": "The Cage",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Repulsor"],
                    "Secondary": ["Reclaimed Forest"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "Top/Bottom"},
                "Vechical": False },

            "The Pit":
                {"ID": "The Pit",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["Runoff", "Spotted Lakes"],
                    "Secondary": ["Uncovered Bone"] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },

        }, "Broken Moon": 
            {"Alpha Base":
                {"ID": "Alpha Base",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Moon's End", "Lunar Cave"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Backup Atmo":
                {"ID": "Backup Atmo",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Lunar Cave", "Garden Pass"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Breaker Wharf":
                {"ID": "Breaker Wharf",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Black Sands", "North Road"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Dry Gulch":
                {"ID": "Dry Gulch",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Haven"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Eternal Gardens": 
                {"ID": "Eternal Gardens",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Misty Hill"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Stasis Array":
                {"ID": "Stasis Array",
                "Type": "Main",
                "Neighbours": {
                    "Main": ["North Promenade"],
                    "Secondary": ["Misty Hill"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "The Core":
                {"ID": "The Core",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Production Yard":
                {"ID": "Production Yard",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Brakken Cliffs"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "North Promenade":
                {"ID": "North Promenade",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Intersection", "Water Works"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "The Foundry":
                {"ID": "The Foundry",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Research Corridor"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "Cultivation": 
                {"ID": "Cultivation",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Windy Hill"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Atmostation":
                {"ID": "Atmostation",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Windy Hill", "Retreat"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Terraformer":
                {"ID": "Terraformer",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Intersection"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "The Divide":
                {"ID": "The Divide",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Bionomics":
                {"ID": "Bionomics",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": ["Retreat"] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

        }, "Storm Point":
            {"Barometer":
                {"ID": "Barometer",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
            "Cascade Falls":
                {"ID": "Cascade Falls",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
            
            "Cenote Cave":
                {"ID": "Cenote Cave",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Ceto Station":
                {"ID": "Ceto Station",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Checkpoint":
                {"ID": "Checkpoint",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Command Center":
                {"ID": "Command Center",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": False,
                    "SplitType": "n/a"},
                "Vechical": False },

            "Devastaded Coast":
                {"ID": "Devastaded Coast",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },
                
            "Downed Beast":
                {"ID": "Downed Beast",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Echo HQ":
                {"ID": "Echo HQ",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": True },
            
            "Jurassic":
                {"ID": "Jurassic",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Launch Pad":
                {"ID": "Launch Pad",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Lighting Rod":
                {"ID": "Lighting Rod",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },
            
            "North Pad":
                {"ID": "North Pad",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "East/West"},
                "Vechical": False },

            "Storm Catcher":
                {"ID": "Storm Catcher",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },

            "The Mill":
                {"ID": "The Mill",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "The Pylon":
                {"ID": "The Pylon",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },

            "The Wall":
                {"ID": "The Wall",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": True },

            "Zeus Station":
                {"ID": "Zeus Station",
                "Type": "Main",
                "Neighbours": {
                    "Main": [],
                    "Secondary": [] },
                "Split": {
                    "CanSplit": True,
                    "SplitType": "North/South"},
                "Vechical": False },
        }
    }
}

class Command_select_poi_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class select_poi_map2_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name

            data = list(db_team_data.find())
            picked_pois = []
            contests = 0
            for i in data:
                if i["pois"]["map2"] != "None": # if team has picked a poi
                    if i["team_name"] != self.team_name: # if team is not the current team
                        picked_pois.append(i["pois"]["map2"])

            for i in picked_pois:
                if picked_pois.count(i) > 1:
                    contests = contests + 1

            for i in pois["Map"][map2]:
                if i not in picked_pois: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                else:
                    if contests > 2: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red, disabled=True)
                    else: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red)

                button.callback = self.create_callback(i)    
                self.add_item(button)

        def create_callback(self, i):
            async def callback(interaction: nextcord.Interaction):
                try:
                    poi = i
                    if selection_mode == "Simple": # Simple Selection
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": poi}})
                        data = db_team_data.find_one({"team_name": self.team_name})
                        channel = interaction.guild.get_channel(channel_poi)
                        try: # check if team is repicking pois
                            messages = await channel.history(limit=30).flatten()
                            for msg in messages:
                                if msg.author.bot:
                                    if msg.embeds[0].title == f"POIs Picked for {self.team_name}":
                                        await msg.delete()
                        except: pass
                        finally: # send poi selection
                            embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=f"{map1} - {data['pois']['map1']}\n{map2} - {data['pois']['map2']}", color=0x000)
                            channel = interaction.guild.get_channel(channel_poi)
                            await channel.send(embed=embed)
                            embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=0x000)
                            await interaction.send(embed=embed, ephemeral=True)
                            formatOutput(output=f"   /select_poi | {self.team_name} has selected {map1} - {data['pois']['map1']} & {map2} - {data['pois']['map2']}", status="Good")
                            formatOutput(output=f"   /select_poi was successful!", status="Good")

                    if selection_mode == "Advanced": # Advanced Selection
                        if pois["Map"][map2][poi]["Split"]["CanSplit"] == True:
                            split_type = pois["Map"][map2][poi]["Split"]["SplitType"]
                            embed = nextcord.Embed(title="POI Split", description=f"{poi} Can be split {split_type}, Select a part of {poi}\nYou cant pick the same half as another team (Shown by a Red button).\nIf no other team picks your POI your team gets the whole POI.", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_split_view(interaction, self.team_name, poi), ephemeral=True)
                        else: 
                            if pois["Map"][map2][poi]["Vechical"] == True: # has vechical
                                embed = nextcord.Embed(title="POI Split", description=f"{poi} has a Trident\nYou can choose to have prioity over the Trident\nOtherwise any other team that chooses this POI can take the Trident", color=0x000)
                                await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_trident_view(interaction, self.team_name, poi), ephemeral=True)
                            else:
                                if pois["Map"][map2][poi]["Neighbours"]["Main"] != None: # has main poi
                                    embed = nextcord.Embed(title="POI Split", description=f"{poi} has a Main POI close by\nYou can choose to add another POI to your landing spot", color=0x000)
                                    await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_secondary_view(interaction, self.team_name, poi), ephemeral=True)
                                elif pois["Map"][map2][poi]["Neighbours"]["Secondary"] != None: # has secondary poi
                                    embed = nextcord.Embed(title="POI Split", description=f"{poi} has a Secondary POI close by\nYou can choose to add a Secondary POI to your landing spot\nOtherwise any other team that chooses this POI can take the Secondary POI\nReminder: Secondary POIs are small POIs that dont appear on the map", color=0x000)
                                    await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_secondary_view(interaction, self.team_name, poi), ephemeral=True)
                                else: 
                                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": poi, "pois.map2_split": "None"}})
                                    data = db_team_data.find_one({"team_name": self.team_name})
                                    channel = interaction.guild.get_channel(channel_poi)
                                    try: # check if team is repicking pois
                                        messages = await channel.history(limit=30).flatten()
                                        for msg in messages:
                                            if msg.author.bot:
                                                if msg.embeds[0].title == f"POIs Picked for {self.team_name}":
                                                    await msg.delete()
                                    except: pass # nothing found
                                    finally: # send poi selection
                                        message = [f"{map1} - {data['pois']['map1']}\n{map2} - {data['pois']['map2']}"]
                                        if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                                            message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                                        elif data["pois"]["map1_secondary"] != None:
                                            message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                                        elif data["pois"]["map2_secondary"] != None:
                                            message.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                                        elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                                            message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                                        elif data["pois"]["map1_trident"] != None:
                                            message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                                        elif data["pois"]["map2_trident"] != None:
                                            message.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")

                                        message = "".join(message)
                                        embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=message, color=0x000)
                                        channel = interaction.guild.get_channel(channel_poi)
                                        await channel.send(embed=embed)
                                        embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=0x000)
                                        await interaction.send(embed=embed, ephemeral=True)

                                        output = [f"   /select_poi | {self.team_name} has selected {map1} - {data['pois']['map1']} ({data['pois']['map1_split']}) & {map2} - {data['pois']['map2']} ({data['pois']['map2_split']})"]
                                        if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                                            output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                                        elif data["pois"]["map1_secondary"] != None:
                                            output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                                        elif data["pois"]["map2_secondary"] != None:
                                            output.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                                        elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                                            output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                                        elif data["pois"]["map1_trident"] != None:
                                            output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                                        elif data["pois"]["map2_trident"] != None:
                                            output.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")
                                        output = "".join(output)
                                        formatOutput(output=output, status="Good")

                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback
    
    class select_poi_map2_split_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi
            
            data = list(db_team_data.find())
            picked_splits = []

            for i in data:
                if i["pois"]["map2"] == self.poi:
                    if i["pois"]["map2_split"] != "None":
                        if i["team_name"] != self.team_name:
                            picked_splits.append(i["pois"]["map2_split"])

            if pois["Map"][map2][poi]["Split"]["SplitType"] == "North/South":
                if "North" not in picked_splits: button = nextcord.ui.Button(label="North", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="North", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("North")
                self.add_item(button)

                if "South" not in picked_splits: button = nextcord.ui.Button(label="South", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="South", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("South")
                self.add_item(button)

            elif pois["Map"][map2][poi]["Split"]["SplitType"] == "East/West":
                if "East" not in picked_splits: button = nextcord.ui.Button(label="East", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="East", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("East")
                self.add_item(button)

                if "West" not in picked_splits: button = nextcord.ui.Button(label="West", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="West", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("West")
                self.add_item(button)

            elif pois["Map"][map2][poi]["Split"]["SplitType"] == "Top/Bottom":
                if "Top" not in picked_splits: button = nextcord.ui.Button(label="Top", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Top", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Top")
                self.add_item(button)

                if "Bottom" not in picked_splits: button = nextcord.ui.Button(label="Bottom", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Bottom", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Bottom")
                self.add_item(button)

            elif pois["Map"][map2][poi]["Split"]["SplitType"] == "Center/Outer":
                if "Center" not in picked_splits: button = nextcord.ui.Button(label="Center", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Center", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Center")
                self.add_item(button)

                if "Outer" not in picked_splits: button = nextcord.ui.Button(label="Outer", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Outer", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Outer")
                self.add_item(button)

        def create_callback(self, split):
            async def callback(interaction: nextcord.Interaction):
                try:
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": self.poi, "pois.map1_split": split}})
                    if pois["Map"][map2][self.poi]["Vechical"] == True:
                        embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Trident\nYou can choose to have prioity over the Trident\nOtherwise any other team that chooses this POI can take the Trident", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_trident_view(interaction, self.team_name, self.poi), ephemeral=True)
                    else:
                        if pois["Map"][map2][self.poi]["Neighbours"]["Main"] != None:
                            embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Main POI close by\nYou can choose to add another POI to your landing spot", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                        elif pois["Map"][map2][self.poi]["Neighbours"]["Secondary"] != None:
                            embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Secondary POI close by\nYou can choose to add a Secondary POI to your landing spot\nOtherwise any other team that chooses this POI can take the Secondary POI\nReminder: Secondary POIs are small POIs that dont appear on the map", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                        else:
                            db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": self.poi, "pois.map2_split": split}})
                            data = db_team_data.find_one({"team_name": self.team_name})
                            channel = interaction.guild.get_channel(channel_poi)
                            try: # check if team is repicking pois
                                messages = await channel.history(limit=30).flatten()
                                for msg in messages:
                                    if msg.author.bot:
                                        if msg.embeds[0].title == f"POIs Picked for {self.team_name}":
                                            await msg.delete()
                            except: pass
                            finally: # send poi selection
                                message = [f"{map1} - {data['pois']['map1']}\n{map2} - {data['pois']['map2']}"]
                                if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                                    message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                                elif data["pois"]["map1_secondary"] != None:
                                    message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                                elif data["pois"]["map2_secondary"] != None:
                                    message.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                                elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                                    message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                                elif data["pois"]["map1_trident"] != None:
                                    message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                                elif data["pois"]["map2_trident"] != None:
                                    message.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")

                                message = "".join(message)
                                embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=message, color=0x000)
                                channel = interaction.guild.get_channel(channel_poi)
                                await channel.send(embed=embed)
                                embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=0x000)
                                await interaction.send(embed=embed, ephemeral=True)

                                output = [f"   /select_poi | {self.team_name} has selected {map1} - {data['pois']['map1']} ({data['pois']['map1_split']}) & {map2} - {data['pois']['map2']} ({data['pois']['map2_split']})"]
                                if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                                    output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                                elif data["pois"]["map1_secondary"] != None:
                                    output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                                elif data["pois"]["map2_secondary"] != None:
                                    output.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                                elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                                    output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                                elif data["pois"]["map1_trident"] != None:
                                    output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                                elif data["pois"]["map2_trident"] != None:
                                    output.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")
                                output = "".join(output)
                                formatOutput(output=output, status="Good")
                                
                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback
        
    class select_poi_map2_trident_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi

            data = list(db_team_data.find())
            picked_tridents = []

            for i in data:
                if i["pois"]["map2"] == self.poi:
                    if i["pois"]["map2_trident"] != "None" or i["pois"]["map2_trident"] != "No Trident":
                        if i["team_name"] != self.team_name:
                            picked_tridents.append(i["pois"]["map2_trident"])

            if "Trident" not in picked_tridents: 
                button = nextcord.ui.Button(label="Take Trident", style=nextcord.ButtonStyle.gray)
                button.callback = self.create_callback("Take Trident")
                self.add_item(button)
            else: # picked already
                button = nextcord.ui.Button(label="Take Trident", style=nextcord.ButtonStyle.red, disabled=True) 
                button.callback = self.create_callback("Take Trident")
                self.add_item(button)

            button = nextcord.ui.Button(label="No Trident", style=nextcord.ButtonStyle.gray)
            button.callback = self.create_callback("No Trident")
            self.add_item(button)
    
        def create_callback(self, trident):
            async def callback(interaction: nextcord.Interaction):
                try:
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": self.poi, "pois.map2_trident": trident}})
                    if pois["Map"][map2][self.poi]["Neighbours"]["Main"] != None:
                        embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Main POI close by\nYou can choose to add another POI to your landing spot", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                    elif pois["Map"][map2][self.poi]["Neighbours"]["Secondary"] != None:
                        embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Secondary POI close by\nYou can choose to add a Secondary POI to your landing spot\nOtherwise any other team that chooses this POI can take the Secondary POI\nReminder: Secondary POIs are small POIs that dont appear on the map", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                    else:
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map2": self.poi, "pois.map2_trident": trident}})
                        data = db_team_data.find_one({"team_name": self.team_name})
                        channel = interaction.guild.get_channel(channel_poi)
                        try: # check if team is repicking pois
                            messages = await channel.history(limit=30).flatten()
                            for msg in messages:
                                if msg.author.bot:
                                    if msg.embeds[0].title == f"POIs Picked for {self.team_name}":
                                        await msg.delete()
                        except: pass
                        finally:
                            message = [f"{map1} - {data['pois']['map1']}\n{map2} - {data['pois']['map2']}"]
                            if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                                message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                            elif data["pois"]["map1_secondary"] != None:
                                message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                            elif data["pois"]["map2_secondary"] != None:
                                message.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                            elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                                message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                            elif data["pois"]["map1_trident"] != None:
                                message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                            elif data["pois"]["map2_trident"] != None:
                                message.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")

                            message = "".join(message)
                            embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=message, color=0x000)
                            channel = interaction.guild.get_channel(channel_poi)
                            await channel.send(embed=embed)
                            embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=0x000)
                            await interaction.send(embed=embed, ephemeral=True)

                            output = [f"   /select_poi | {self.team_name} has selected {map1} - {data['pois']['map1']} ({data['pois']['map1_split']}) & {map2} - {data['pois']['map2']} ({data['pois']['map2_split']})"]
                            if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                                output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                            elif data["pois"]["map1_secondary"] != None:
                                output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                            elif data["pois"]["map2_secondary"] != None:
                                output.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                            elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                                output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                            elif data["pois"]["map1_trident"] != None:
                                output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                            elif data["pois"]["map2_trident"] != None:
                                output.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")
                            output = "".join(output)
                            formatOutput(output=output, status="Good")
                        
                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback

    class select_poi_map2_secondary_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi
            
            data = list(db_team_data.find())
            picked_secondaries = []

            for i in data:
                if i["pois"]["map2"] == self.poi:
                    if i["pois"]["map2_secondary"] != "None":
                        if i["team_name"] != self.team_name:
                            picked_secondaries.append(i["pois"]["map2_secondary"])

            for i in pois["Map"][map2]:
                if i not in picked_secondaries:
                    button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                else:
                    button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red, disabled=True) # picked already

                button.callback = self.create_callback(i)
                self.add_item(button)
        
        def create_callback(self, secondary):
            async def callback(interaction: nextcord.Interaction):
                try:
                    data = db_team_data.find_one({"team_name": self.team_name})
                    channel = interaction.guild.get_channel(channel_poi)
                    try: # check if team is repicking pois
                        messages = await channel.history(limit=30).flatten()
                        for msg in messages:
                            if msg.author.bot:
                                if msg.embeds[0].title == f"POIs Picked for {self.team_name}":
                                    await msg.delete()
                    except: pass
                    finally: # send poi selection
                        message = [f"{map1} - {data['pois']['map1']}\n{map2} - {data['pois']['map2']}"]
                        if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                            message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                        elif data["pois"]["map1_secondary"] != None:
                            message.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                        elif data["pois"]["map2_secondary"] != None:
                            message.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                        elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                            message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                        elif data["pois"]["map1_trident"] != None:
                            message.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                        elif data["pois"]["map2_trident"] != None:
                            message.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")
                        message = "".join(message)
                        embed = nextcord.Embed(title=f"POIs Picked for {self.team_name}", description=message, color=0x000)
                        channel = interaction.guild.get_channel(channel_poi)
                        await channel.send(embed=embed)
                        embed = nextcord.Embed(description=f"✅ POI Selection Confirmed", color=0x000)
                        await interaction.send(embed=embed, ephemeral=True)

                        output = [f"   /select_poi | {self.team_name} has selected {map1} - {data['pois']['map1']} ({data['pois']['map1_split']}) & {map2} - {data['pois']['map2']} ({data['pois']['map2_split']})"]
                        if data["pois"]["map1_secondary"] or data["pois"]["map2_secondary"] != "None":
                            output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}\n{map2} - {data['pois']['map2_secondary']}")
                        elif data["pois"]["map1_secondary"] != None:
                            output.append(f"\nSecondaries: {map1} - {data['pois']['map1_secondary']}")
                        elif data["pois"]["map2_secondary"] != None:
                            output.append(f"\nSecondaries: {map2} - {data['pois']['map2_secondary']}")
                        elif data["pois"]["map1_trident"] or data["pois"]["map2_trident"] != "None":
                            output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}\n{map2} - {data['pois']['map2_trident']}")
                        elif data["pois"]["map1_trident"] != None:
                            output.append(f"\nTridents: {map1} - {data['pois']['map1_trident']}")
                        elif data["pois"]["map2_trident"] != None:
                            output.append(f"\nTridents: {map2} - {data['pois']['map2_trident']}")
                        output = "".join(output)
                        formatOutput(output=output, status="Good")
                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback
    
    class select_poi_map1_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name

            data = list(db_team_data.find())
            picked_pois = []
            contests = 0
            for i in data:
                if i["pois"]["map1"] != "None": # if team has picked a poi
                    if i["team_name"] != self.team_name: # if team is not the current team
                        picked_pois.append(i["pois"]["map1"])
            
            for i in picked_pois:
                if picked_pois.count(i) > 1:
                    contests = contests + 1

            for i in pois["Map"][map1]:
                if i not in picked_pois: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                else:
                    if contests > 2: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red, disabled=True)
                    else: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red)

                button.callback = self.create_callback(i)    
                self.add_item(button)

        def create_callback(self, label):
            async def callback(interaction: nextcord.Interaction):
                poi = label
                try: 
                    if selection_mode == "Simple": # Simple Selection
                        db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": poi}})
                        embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)
                    elif selection_mode == "Advanced": # Advanced Selection
                        if pois["Map"][map1][poi]["Split"]["CanSplit"] == True:
                            split_type = pois["Map"][map1][poi]["Split"]["SplitType"]
                            embed = nextcord.Embed(title="POI Split", description=f"{poi} Can be split {split_type}, Select a part of {poi}\nYou cant pick the same half as another team (Shown by a Red button).\nIf no other team picks your POI your team gets the whole POI.", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_split_view(interaction, self.team_name, poi), ephemeral=True)
                        else: 
                            if pois["Map"][map1][poi]["Vechical"] == True: # has vechical
                                embed = nextcord.Embed(title="POI Split", description=f"{poi} has a Trident\nYou can choose to have prioity over the Trident\nOtherwise any other team that chooses this POI can take the Trident", color=0x000)
                                await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_trident_view(interaction, self.team_name, poi), ephemeral=True)
                            else:
                                if pois["Map"][map1][poi]["Neighbours"]["Main"] != None: # has main poi
                                    embed = nextcord.Embed(title="POI Split", description=f"{poi} has a Main POI close by\nYou can choose to add another POI to your landing spot", color=0x000)
                                    await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_secondary_view(interaction, self.team_name, poi), ephemeral=True)
                                elif pois["Map"][map1][poi]["Neighbours"]["Secondary"] != None: # has secondary poi
                                    embed = nextcord.Embed(title="POI Split", description=f"{poi} has a Secondary POI close by\nYou can choose to add a Secondary POI to your landing spot\nOtherwise any other team that chooses this POI can take the Secondary POI\nReminder: Secondary POIs are small POIs that dont appear on the map", color=0x000)
                                    await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_secondary_view(interaction, self.team_name, poi), ephemeral=True)
                                else: 
                                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": poi, "pois.map1_split": "None"}})
                                    embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI", color=0x000)
                                    await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)

                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback
    
    class select_poi_map1_split_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi
            
            data = list(db_team_data.find())
            picked_splits = []

            for i in data:
                if i["pois"]["map1"] == self.poi:
                    if i["pois"]["map1_split"] != "None":
                        if i["team_name"] != self.team_name:
                            picked_splits.append(i["pois"]["map1_split"])

            if pois["Map"][map1][poi]["Split"]["SplitType"] == "North/South":
                if "North" not in picked_splits: button = nextcord.ui.Button(label="North", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="North", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("North")
                self.add_item(button)

                if "South" not in picked_splits: button = nextcord.ui.Button(label="South", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="South", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("South")
                self.add_item(button)

            elif pois["Map"][map1][poi]["Split"]["SplitType"] == "East/West":
                if "East" not in picked_splits: button = nextcord.ui.Button(label="East", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="East", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("East")
                self.add_item(button)

                if "West" not in picked_splits: button = nextcord.ui.Button(label="West", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="West", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("West")
                self.add_item(button)

            elif pois["Map"][map1][poi]["Split"]["SplitType"] == "Top/Bottom":
                if "Top" not in picked_splits: button = nextcord.ui.Button(label="Top", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Top", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Top")
                self.add_item(button)

                if "Bottom" not in picked_splits: button = nextcord.ui.Button(label="Bottom", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Bottom", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Bottom")
                self.add_item(button)

            elif pois["Map"][map1][poi]["Split"]["SplitType"] == "Center/Outer":
                if "Center" not in picked_splits: button = nextcord.ui.Button(label="Center", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Center", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Center")
                self.add_item(button)

                if "Outer" not in picked_splits: button = nextcord.ui.Button(label="Outer", style=nextcord.ButtonStyle.gray)
                else: button = nextcord.ui.Button(label="Outer", style=nextcord.ButtonStyle.red, disabled=True) # picked already
                button.callback = self.create_callback("Outer")
                self.add_item(button)

        def create_callback(self, split):
            async def callback(interaction: nextcord.Interaction):
                try:
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": self.poi, "pois.map1_split": split}})
                    if pois["Map"][map1][self.poi]["Vechical"] == True:
                        embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Trident\nYou can choose to have prioity over the Trident\nOtherwise any other team that chooses this POI can take the Trident", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_trident_view(interaction, self.team_name, self.poi), ephemeral=True)
                    else:
                        if pois["Map"][map1][self.poi]["Neighbours"]["Main"] != None:
                            embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Main POI close by\nYou can choose to add another POI to your landing spot", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                        elif pois["Map"][map1][self.poi]["Neighbours"]["Secondary"] != None:
                            embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Secondary POI close by\nYou can choose to add a Secondary POI to your landing spot\nOtherwise any other team that chooses this POI can take the Secondary POI\nReminder: Secondary POIs are small POIs that dont appear on the map", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                        else:
                            embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI", color=0x000)
                            await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)

                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback
    
    class select_poi_map1_trident_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi

            data = list(db_team_data.find())
            picked_tridents = []

            for i in data:
                if i["pois"]["map1"] == self.poi:
                    if i["pois"]["map1_trident"] != "None" or i["pois"]["map1_trident"] != "No Trident":
                        if i["team_name"] != self.team_name:
                            picked_tridents.append(i["pois"]["map1_trident"])

            if "Trident" not in picked_tridents: 
                button = nextcord.ui.Button(label="Take Trident", style=nextcord.ButtonStyle.gray)
                button.callback = self.create_callback("Take Trident")
                self.add_item(button)
            else: # picked already
                button = nextcord.ui.Button(label="Take Trident", style=nextcord.ButtonStyle.red, disabled=True) 
                button.callback = self.create_callback("Take Trident")
                self.add_item(button)

            button = nextcord.ui.Button(label="No Trident", style=nextcord.ButtonStyle.gray)
            button.callback = self.create_callback("No Trident")
            self.add_item(button)
    
        def create_callback(self, trident):
            async def callback(interaction: nextcord.Interaction):
                try:
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": self.poi, "pois.map1_trident": trident}})
                    if pois["Map"][map1][self.poi]["Neighbours"]["Main"] != None:
                        embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Main POI close by\nYou can choose to add another POI to your landing spot", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                    elif pois["Map"][map1][self.poi]["Neighbours"]["Secondary"] != None:
                        embed = nextcord.Embed(title="POI Split", description=f"{self.poi} has a Secondary POI close by\nYou can choose to add a Secondary POI to your landing spot\nOtherwise any other team that chooses this POI can take the Secondary POI\nReminder: Secondary POIs are small POIs that dont appear on the map", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map1_secondary_view(interaction, self.team_name, self.poi), ephemeral=True)
                    else:
                        embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI", color=0x000)
                        await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)

                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback

    class select_poi_map1_secondary_view(nextcord.ui.View):
        def __init__(self, interaction: nextcord.Interaction, team_name, poi):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.team_name = team_name
            self.poi = poi

            data = list(db_team_data.find())
            picked_secondaries = []

            for i in data:
                if i["pois"]["map1"] == self.poi:
                    if i["pois"]["map1_secondary"] != "None":
                        if i["team_name"] != self.team_name:
                            picked_secondaries.append(i["pois"]["map1_secondary"])

            if pois["Map"][map1][self.poi]["Neighbours"]["Main"] != None:
                for i in pois["Map"][map1][self.poi]["Neighbours"]["Main"]:
                    if i not in picked_secondaries: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red, disabled=True) # picked already

                    button.callback = self.create_callback(i)
                    self.add_item(button)
                
                for i in pois["Map"][map1][self.poi]["Neighbours"]["Secondary"]:
                    if i not in picked_secondaries: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.gray)
                    else: button = nextcord.ui.Button(label=i, style=nextcord.ButtonStyle.red, disabled=True)
                
                button = nextcord.ui.Button(label="No Secondary", style=nextcord.ButtonStyle.gray)
                button.callback = self.create_callback("No Secondary")
                self.add_item(button)

        def create_callback(self, secondary):
            async def callback(interaction: nextcord.Interaction):
                try:
                    db_team_data.update_one({"team_name": self.team_name}, {"$set": {"pois.map1": self.poi, "pois.map1_secondary": secondary}})
                    embed = nextcord.Embed(title="Select POI", description=f"Select a POI for {map2}\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI", color=0x000)
                    await interaction.send(embed=embed, view=Command_select_poi_Cog.select_poi_map2_view(interaction, self.team_name), ephemeral=True)

                except Exception as e:
                    error_traceback = traceback.format_exc()
                    await errorResponse(error=f"{e}\n{error_traceback}", command="select_poi", interaction=interaction)
            return callback

    @nextcord.slash_command(guild_ids=[guildID], name="select_poi", description="Select POIs")
    async def select_poi(self, interaction: nextcord.Interaction, team_name = nextcord.SlashOption(name="team_name", description="Select your team", required=True, choices={i["team_name"]:i["team_name"] for i in list(db_team_data.find())})):
        command = 'select_poi'
        userID = interaction.user.id
        formatOutput(output=f"/{command} Used by {userID} | @{interaction.user.name}", status="Normal")
        try: await interaction.response.defer(ephemeral=True)
        except: pass

        try:
            if db_bot_data.find_one({"poi": {"$exists": True}}) == None: # checking if poi selection is open
                await interaction.edit_original_message(content="POI Selections are not open yet!")
                formatOutput(output=f"   /{command} | POI Selections are not open yet!", status="Warning") 
            else: # -> yes
                if db_team_data.find_one({"team_name": team_name}) != None: # team exists
                    data = db_team_data.find_one({"team_name": team_name})
                    if interaction.user.id == data["captain"] or interaction.user.guild_permissions.administrator: # user is captain or admin
                        map_data = db_bot_data.find_one({"maps": {"$exists": True}})
                        maps = [None, map_data["maps"]["map1"], map_data["maps"]["map2"], map_data["maps"]["selection_mode"]]
                        global map1, map2, selection_mode
                        map1 = maps[1]
                        map2 = maps[2]
                        selection_mode = maps[3]

                        if selection_mode == "Simple": description = f"Select a POI for {map1}\nSelection Mode: {selection_mode} - Pick one POI per map\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI\nSelection Mode: {selection_mode}"
                        elif selection_mode == "Advanced": description = f"Select a POI for {map1}\nSelection Mode: {selection_mode} - Option to pick Secondary POIs and Tridents\nGray Buttons indicate no team has chosen that POI yet,\nRed Buttons indicate that a team has picked that POI\nSelection Mode: {selection_mode}"
                        embed = nextcord.Embed(title="POI Selection", description=description, color=0x000)
                        await interaction.edit_original_message(embed=embed, view=Command_select_poi_Cog.select_poi_map1_view(interaction, team_name))

                    else: # not captain or admin
                        await interaction.edit_original_message(content=f"You are not the captain of {team_name}!")
                        formatOutput(output=f"   /{command} | {userID} is not captain of {team_name}!", status="Warning")
                else: # team doesnt exist
                    await interaction.edit_original_message(content=f"Team {team_name} not found!")
                    formatOutput(output=f"   /{command} | {team_name} not found!", status="Warning")
        except Exception as e:
            error_traceback = traceback.format_exc()
            await errorResponse(error=f"{e}\n{error_traceback}", command=command, interaction=interaction)

def setup(bot):
    bot.add_cog(Command_select_poi_Cog(bot))