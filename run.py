import os
import subprocess
import sys

# Project root (directory containing this run.py)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_step(title, command):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,   # Always execute from project root
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed during: {title}")
        sys.exit(e.returncode)


def main():

    env_file = os.path.join(PROJECT_ROOT, ".env")

    if not os.path.exists(env_file):
        print("❌ .env file not found.")
        sys.exit(1)

    run_step(
        "Step 1: Building Dataset",
        [sys.executable, "-m", "data.generate_dataset"]
    )

    run_step(
        "Step 2: Generating Replies",
        [sys.executable, "-m", "generator.generate_replies"]
    )

    run_step(
        "Step 3: Evaluating Replies",
        [sys.executable, "-m", "evaluator.evaluate_replies"]
    )

    print("\n" + "=" * 60)
    print("🎉 Pipeline completed successfully!")
    print("=" * 60)

    print("\nGenerated files:")
    print("✓ data/emails.json")
    print("✓ data/replies.json")
    print("✓ data/scores.json")


if __name__ == "__main__":
    main()