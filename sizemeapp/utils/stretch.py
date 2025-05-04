# Stretch factor presets used for size recommendation calculations.
# These define how much extra space (as a multiplier) is allowed for each fit type,
# depending on the garment category. For example, a "Regular" fit shirt may allow 10% extra space.

STRETCH_FACTORS = {
    "shirts": {
        "Slim": 1.00,    # No added ease — matches chest exactly
        "Regular": 1.10, # 10% additional room
        "Loose": 1.20,   # 20% additional room
    },
    "crew_necks": {
        "Slim": 0.90,    # Tighter than exact chest
        "Regular": 1.00, # True to size
        "Loose": 1.20,   # Loose fit with 20% ease
    },
    # Add more categories as needed (e.g., hoodies, jackets, tees)
}
