import random



# reversemortgage.report
def build_report(data, TAEG_parameters=None):
    """
    Simule le vrai build_report.
    """

    maximum_quotity: float = random.randint(1_000,6_000)/10_000
    prix_5p: int = random.randint(500_000, 1_500_000)

    results = {
        "Base Case": {
            "Quantile_Prix_Immo": {
                "prix 5%": None
            },
            "maximum_quotity": None
        }
    }
    results["Base Case"]["maximum_quotity"] = maximum_quotity
    results["Base Case"]["Quantile_Prix_Immo"]["prix 5%"] = prix_5p

    return results


if __name__ == "__main__":
    data = {}
    response = build_report(data)
    print(response)