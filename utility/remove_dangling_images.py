import subprocess

def remove_dangling_images():
    try:
        print("Checking for dangling images...")
        # Get IDs of dangling images (those with <none> as repo/tag)
        result = subprocess.run(
            ["docker", "images", "--filter=dangling=true", "--quiet"],
            check=True,
            capture_output=True,
            text=True
        )

        image_ids = result.stdout.strip().splitlines()

        if not image_ids:
            print("No dangling images found.")
            return

        print(f"Dangling images found:\n{image_ids}")
        print("Removing images...")
        subprocess.run(["docker", "rmi"] + image_ids, check=True)
        print("Successfully removed all dangling images.")

    except subprocess.CalledProcessError as e:
        print(f"Error during Docker command execution: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    remove_dangling_images()
