# sizemeapp/utils/recommendation.py
from sizemeapp.utils.stretch import STRETCH_FACTORS
from decimal import Decimal


def get_size_recommendations(user_chest, product, max_difference=Decimal("4.0")):
    category = product.category
    user_chest = Decimal(str(user_chest))  # Ensure it's Decimal

    stretch_fits = {
        "Slim": category.slim_factor if category else Decimal("1.00"),
        "Regular": category.regular_factor if category else Decimal("1.10"),
        "Loose": category.loose_factor if category else Decimal("1.20"),
    }

    garment_sizes = product.size_fits.all()
    recommendations = []

    for fit_name, factor in stretch_fits.items():
        target_chest = user_chest * factor

        closest = min(
            garment_sizes,
            key=lambda s: abs(s.chest - target_chest),
            default=None
        )

        if closest:
            diff = abs(closest.chest - target_chest)
            if diff <= max_difference:
                recommendations.append({
                    "fit": fit_name,
                    "size_label": closest.size_label,
                })

    return recommendations

