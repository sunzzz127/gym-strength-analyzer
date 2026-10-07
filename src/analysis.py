import pandas as pd
import matplotlib.pyplot as plt

# Load workout data.
workouts = pd.read_csv("data/workouts.csv")

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------

# Training volume = weight x reps.
workouts["volume"] = workouts["weight_lbs"] * workouts["reps"]

# Estimate one-rep max using the Epley formula.
workouts["estimated_1rm"] = (
    workouts["weight_lbs"] * (1 + workouts["reps"] / 30)
)

# Combine sets from the same exercise and workout.
progress = (
    workouts.groupby(["exercise", "workout_number"])
    .agg(
        weight=("weight_lbs", "max"),
        total_reps=("reps", "sum"),
        total_volume=("volume", "sum"),
        estimated_1rm=("estimated_1rm", "max")
    )
    .reset_index()
)

# -----------------------------
# EXERCISE SELECTION
# -----------------------------

print("\nAvailable exercises:")

for exercise in sorted(workouts["exercise"].unique()):
    print("-", exercise)

exercise_name = input("\nEnter an exercise: ").strip()

exercise_data = progress[
    progress["exercise"].str.lower() == exercise_name.lower()
].copy()

if exercise_data.empty:
    print("\nExercise not found.")

else:
    exercise_data = exercise_data.sort_values("workout_number")

    print(f"\n{exercise_name} Progress:")
    print(exercise_data.to_string(index=False))

    # -----------------------------
    # SUMMARY STATISTICS
    # -----------------------------

    first_workout = exercise_data.iloc[0]
    latest_workout = exercise_data.iloc[-1]

    volume_change = (
        (latest_workout["total_volume"] - first_workout["total_volume"])
        / first_workout["total_volume"]
    ) * 100

    strength_change = (
        (latest_workout["estimated_1rm"] - first_workout["estimated_1rm"])
        / first_workout["estimated_1rm"]
    ) * 100

    print("\nSummary")
    print("----------------------------")
    print(f"Starting weight: {first_workout['weight']:.1f} lb")
    print(f"Latest weight: {latest_workout['weight']:.1f} lb")
    print(f"Volume change: {volume_change:.1f}%")
    print(f"Estimated strength change: {strength_change:.1f}%")
    print(f"Best estimated 1RM: {exercise_data['estimated_1rm'].max():.1f} lb")

    # -----------------------------
    # VISUALIZATION 1
    # TRAINING VOLUME
    # -----------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        exercise_data["workout_number"],
        exercise_data["total_volume"],
        marker="o"
    )

    plt.title(f"{exercise_name} - Training Volume")
    plt.xlabel("Workout Number")
    plt.ylabel("Volume (lb x reps)")
    plt.xticks(exercise_data["workout_number"])
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "images/training_volume.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    # -----------------------------
    # VISUALIZATION 2
    # ESTIMATED STRENGTH
    # -----------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        exercise_data["workout_number"],
        exercise_data["estimated_1rm"],
        marker="o"
    )

    plt.title(f"{exercise_name} - Estimated Strength Progression")
    plt.xlabel("Workout Number")
    plt.ylabel("Estimated 1RM (lb)")
    plt.xticks(exercise_data["workout_number"])
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "images/estimated_strength.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()