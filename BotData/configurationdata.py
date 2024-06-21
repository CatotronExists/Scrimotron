# Structure
# "Automation" <<-- Main View
#    "Setup" <<-- Sub View
#               <<-- Sub Sub View ()

Data = {
    "Automation": {
        "Setup": {
            "Type": "Automation",
            "Options": ["Enable", "Disable", "Change Timing"],
        },
        "Checkin" : {
            "Type": "Automation",            
            "Options": ["Enable", "Disable", "Change Timing"],
        },
        "Poi" : {
            "Type": "Automation",
            "Options": ["Enable", "Disable", "Change Timing"],
        }
    },
    "Channels": {
        "Announcement" : {
            "Type": "Channel",
            "Options": ["Change Channel"],
        },
        "Rules": {
            "Type": "Channel",
            "Options": ["Change Channel"],
        },
        "Format": {
            "Type": "Channel",
            "Options": ["Change Channel"],
        },
        "Poi": {
            "Type": "Channel",
            "Options": ["Change Channel"],
        },
        "Log": {
            "Type": "Channel",
            "Options": ["Change Channel"],
        }
    },
    "Messages": {
        "Announcement": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        },
        "Checkin": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        },
        "Rules": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        },
        "Format": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        },
        "Poi": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        },
        "Registration": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        },
        "Reserve": {
            "Type": "Message",
            "Options": ["Change Message"], # [Change Message, Edit Type]
        }
    },
    "Scrims": {
        "Caster": {
            "Type": "Role",
            "Options": ["Enable", "Disable", "Change Role"],
        }
    }
}