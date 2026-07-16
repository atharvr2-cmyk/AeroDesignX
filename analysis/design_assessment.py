"""
Aircraft Design Assessment

Evaluates conceptual aircraft performance using a weighted scoring system.
"""


def evaluate_design(
    required_cl,
    lift_to_drag,
    stall_margin,
    wing_loading,
):
    """
    Evaluate the aircraft design and print recommendations.

    Parameters
    ----------
    required_cl : float
        Lift coefficient required during cruise.

    lift_to_drag : float
        Aircraft lift-to-drag ratio.

    stall_margin : float
        Cruise speed divided by stall speed.

    wing_loading : float
        Aircraft wing loading in N/m^2.

    Returns
    -------
    dict
        Assessment score, grade, status, and recommendations.
    """

    score = 0.0
    recommendations = []

    # --------------------------------------------------
    # Required lift coefficient: 30 points
    # --------------------------------------------------

    if required_cl <= 0.8:
        cl_score = 30
        cl_status = "Excellent"
    elif required_cl <= 1.2:
        cl_score = 24
        cl_status = "Acceptable"
    elif required_cl <= 1.5:
        cl_score = 15
        cl_status = "High"
        recommendations.append(
            "Increase wing area or cruise speed to reduce required CL."
        )
    else:
        cl_score = 5
        cl_status = "Critical"
        recommendations.append(
            "Required CL is unrealistically high. Increase wing area "
            "or cruise speed."
        )

    score += cl_score

    # --------------------------------------------------
    # Lift-to-drag ratio: 30 points
    # --------------------------------------------------

    if lift_to_drag >= 15:
        ld_score = 30
        ld_status = "Excellent"
    elif lift_to_drag >= 10:
        ld_score = 24
        ld_status = "Good"
    elif lift_to_drag >= 7:
        ld_score = 15
        ld_status = "Fair"
        recommendations.append(
            "Improve aerodynamic efficiency by reducing drag."
        )
    else:
        ld_score = 5
        ld_status = "Poor"
        recommendations.append(
            "Lift-to-drag ratio is low. Review wing geometry and drag assumptions."
        )

    score += ld_score

    # --------------------------------------------------
    # Stall margin: 25 points
    # --------------------------------------------------

    if stall_margin >= 1.5:
        stall_score = 25
        stall_status = "Safe"
    elif stall_margin >= 1.3:
        stall_score = 18
        stall_status = "Limited"
        recommendations.append(
            "Increase cruise speed or reduce stall speed."
        )
    else:
        stall_score = 5
        stall_status = "Unsafe"
        recommendations.append(
            "Cruise speed is too close to stall speed."
        )

    score += stall_score

    # --------------------------------------------------
    # Wing loading: 15 points
    # --------------------------------------------------

    if wing_loading <= 120:
        wing_loading_score = 15
        wing_loading_status = "Appropriate"
    elif wing_loading <= 180:
        wing_loading_score = 10
        wing_loading_status = "Moderate"
    else:
        wing_loading_score = 4
        wing_loading_status = "High"
        recommendations.append(
            "Reduce aircraft mass or increase wing area."
        )

    score += wing_loading_score

    # --------------------------------------------------
    # Overall grade
    # --------------------------------------------------

    if score >= 90:
        grade = "A"
        overall_status = "Excellent conceptual design"
    elif score >= 80:
        grade = "B"
        overall_status = "Good conceptual design"
    elif score >= 70:
        grade = "C"
        overall_status = "Acceptable but requires improvement"
    elif score >= 60:
        grade = "D"
        overall_status = "Marginal design"
    else:
        grade = "F"
        overall_status = "Design is not currently feasible"

    # --------------------------------------------------
    # Report
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("DESIGN ASSESSMENT")
    print("=" * 60)

    print(
        f"Required CL:             {required_cl:.3f} "
        f"({cl_status}, {cl_score}/30)"
    )
    print(
        f"Lift-to-Drag Ratio:      {lift_to_drag:.2f} "
        f"({ld_status}, {ld_score}/30)"
    )
    print(
        f"Cruise/Stall Ratio:      {stall_margin:.2f} "
        f"({stall_status}, {stall_score}/25)"
    )
    print(
        f"Wing Loading:            {wing_loading:.2f} N/m^2 "
        f"({wing_loading_status}, {wing_loading_score}/15)"
    )

    print("-" * 60)
    print(f"Overall Score:           {score:.0f}/100")
    print(f"Design Grade:            {grade}")
    print(f"Assessment:              {overall_status}")

    print("\nRecommendations")

    if recommendations:
        for number, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            print(f"{number}. {recommendation}")
    else:
        print("No major design changes are currently recommended.")

    print("=" * 60)

    return {
        "score": score,
        "grade": grade,
        "status": overall_status,
        "recommendations": recommendations,
    }