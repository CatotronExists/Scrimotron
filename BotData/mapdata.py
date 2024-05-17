### POIS (as of season 19 start) [UPDATE TO MID SEASON 19] + [SEASON 20?]
MapData = {
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
            "Vechical": True },

        "Cascade Falls":
            {"ID": "Cascade Falls",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["Oasis", "Water Hole"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "North/South"},
            "Vechical": False },

        "Cenote Cave":
            {"ID": "Cenote Cave",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["Medina Island"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "East/West"},
            "Vechical": True },

        "Ceto Station":
            {"ID": "Ceto Station",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["Oasis", "Siren Isle"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "East/West"},
            "Vechical": True },

        "Checkpoint":
            {"ID": "Checkpoint",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["Forest"] },
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

        "Devastated Coast":
            {"ID": "Devastated Coast",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["The Ridge"] },
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
                "Secondary": ["The Caves"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "East/West"},
            "Vechical": False },

        "Launch Pad":
            {"ID": "Launch Pad",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["The Ridge"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "East/West"},
            "Vechical": False },

        "Lighting Rod":
            {"ID": "Lighting Rod",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["Mountain Top"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "North/South"},
            "Vechical": True },

        "North Pad":
            {"ID": "North Pad",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["Trenches", "Black Sand Islands"] },
            "Split": {
                "CanSplit": True,
                "SplitType": "East/West"},
            "Vechical": False },

        "Storm Catcher":
            {"ID": "Storm Catcher",
            "Type": "Main",
            "Neighbours": {
                "Main": [],
                "Secondary": ["East Lift", "East Trail"] },
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
                "Secondary": ["Black Diamond", "Bunny Slope"] },
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