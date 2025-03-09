import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.offsetbox as offsetbox
import numpy as np
import os

# -----------------------------
# Rocket Height Function
# -----------------------------
def rocket_height(baking_soda):
    """
    Simulate rocket height (in feet) as a function of baking soda (tsp),
    assuming 2 cups of vinegar is fixed.

    We use a parabolic model:
      height = -a * (baking_soda - k)^2 + max_height
    And clamp the minimum at 0 (no negative height).
    """
    a = 0.5         # Steepness factor
    k = 6           # 'Optimal' baking soda amount (tsp)
    max_height = 20 # Max height at the optimal ratio

    height = -a * (baking_soda - k)**2 + max_height
    return max(0, height)


# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.title("Baking Soda + Vinegar Rocket!")
    st.write("""
    Adjust the slider to change how many teaspoons of baking soda you mix with 2 cups of vinegar.
    Watch how the rocket's height changes. There's an 'optimal' amount around 6 tsp!
    """)

    # Slider for baking soda amount
    baking_soda_tsp = st.slider(
        label="Baking Soda (tsp)",
        min_value=0,
        max_value=12,
        value=6,
        step=1
    )

    # Calculate rocket height in feet
    height_feet = rocket_height(baking_soda_tsp)

    # -----------------------------
    # Plot with Matplotlib
    # -----------------------------
    fig, ax = plt.subplots()
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 25)
    ax.set_xlabel("Baking Soda (tsp)")
    ax.set_ylabel("Rocket Height (feet)")
    ax.set_title("Rocket Launch Simulation")

    # Add a simple horizontal line for ground reference
    ax.axhline(y=0, color='gray', linewidth=2)

    # Place the rocket image or marker at (x=baking_soda_tsp, y=height_feet)
    rocket_plotted = False

    # Attempt to load rocket image if present
    rocket_image_path = "rocket.png"  # <-- Make sure rocket.png is in the same folder.
    if os.path.exists(rocket_image_path):
        try:
            rocket_img = mpimg.imread(rocket_image_path)
            imagebox = offsetbox.OffsetImage(rocket_img, zoom=0.1)
            ab = offsetbox.AnnotationBbox(
                imagebox,
                (baking_soda_tsp, height_feet),
                frameon=False
            )
            ax.add_artist(ab)
            rocket_plotted = True
        except Exception as e:
            st.warning(f"Could not load rocket image: {e}")

    if not rocket_plotted:
        # Fallback: just plot a marker if image is missing
        ax.plot(baking_soda_tsp, height_feet, marker="^", markersize=15, color="red")

    # Annotate the rocket's exact height
    ax.text(
        baking_soda_tsp + 0.3,
        height_feet,
        f"{height_feet:.1f} ft",
        fontsize=9,
        va='bottom'
    )

    st.pyplot(fig)

    # -----------------------------
    # Explanation or Additional Info
    # -----------------------------
    st.write(f"You've added **{baking_soda_tsp} tsp** of baking soda. The rocket reached about **{height_feet:.1f} ft**!")

if __name__ == "__main__":
    main()
