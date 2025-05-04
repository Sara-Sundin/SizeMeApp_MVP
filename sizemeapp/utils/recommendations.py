from sizemeapp.utils.stretch import STRETCH_FACTORS
from decimal import Decimal


def get_size_recommendations(user_chest, product, max_difference=Decimal("4.0")):
    """
    Generate size recommendations for a given user and product.

    Args:
        user_chest (Decimal or float or str): The user's chest measurement in cm.
        product (Product): The product instance, which must have a related category and size_fits.
        max_difference (Decimal): Maximum allowed difference between target and actual chest to consider a match.

    Returns:
        List[Dict]: A list of recommended sizes per fit (Slim, Regular, Loose),
                    each with 'fit' and 'size_label' keys.
    """

    category = product.category
    user_chest = Decimal(str(user_chest))  # Convert input to Decimal for precision

    # Retrieve stretch factors from the category or fall back to defaults
    stretch_fits = {
        "Slim": category.slim_factor if category else Decimal("1.00"),
        "Regular": category.regular_factor if category else Decimal("1.10"),
        "Loose": category.loose_factor if category else Decimal("1.20"),
    }

    # Get all garment sizes associated with the product
    garment_sizes = product.size_fits.all()
    recommendations = []

    # Loop through each fit type to find the best size match
    for fit_name, factor in stretch_fits.items():
        target_chest = user_chest * factor  # Expected garment chest for this fit

        # Find size with closest actual chest value
        closest = min(
            garment_sizes,
            key=lambda s: abs(s.chest - target_chest),
            default=None
        )

        # Only recommend size if it's within the max acceptable difference
        if closest:
            diff = abs(closest.chest - target_chest)
            if diff <= max_difference:
                recommendations.append({
                    "fit": fit_name,
                    "size_label": closest.size_label,
                })

    return recommendations
