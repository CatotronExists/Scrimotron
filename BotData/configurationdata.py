# ValueIDs
# 1 // T/F | Hour(s) before start
# 2 // T/F | @RoleID
# 3 // Click to View/Edit
# 4 // #ChannelID

# Structure
# "Automation" <<-- Main View
#    "Setup" <<-- Sub View
#               <<-- Sub Sub View ()

ConfigData = {
    "Automation": { # <-- option
        "Setup": { # <-- sub_option
            "ValueID": 1,
            "Buttons": ["Enable", "Disable", "Change Timing"]
        },
        "Checkin" : { # <-- sub_option
            "ValueID": 1,
            "Buttons": ["Enable", "Disable", "Change Timing"]
        },

        "Poi" : { # <-- sub_option
            "ValueID": 1,
            "Buttons": ["Enable", "Disable", "Change Timing"]
        }
    },
    "Channels": { # <-- option
        "Announcement" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        },
        "Checkin" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        },
        "Rules" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        },
        "Format" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        },
        "Poi" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        },
        "Registration" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        },
        "Log" : { # <-- sub_option
            "ValueID": 4,
            "Buttons": ["Change Channel"]
        }
    },
    "Messages": { # <-- option
        "Announcement" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        },
        "Checkin" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        },
        "Rules" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        },
        "Format" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        },
        "Poi" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        },
        "Registration" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        },
        "Reserve" : { # <-- sub_option
            "ValueID": 3,
            "Buttons": ["Change Message"]
        }
    },
    "Scrims": { # <-- option
        "Caster" : { # <-- sub_option
            "ValueID": 2,
            "Buttons": ["Enable", "Disable", "Change Role"]
        }
    }
}