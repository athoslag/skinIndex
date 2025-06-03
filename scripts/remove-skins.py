import os
import sys

skinsToRemove = ["0989"]

for skin in skinsToRemove:
    skinPath = "skin/" + str(skin) + ".skin"
    hskinPath = "skin/" + str(skin) + ".hskin"
    imagePath = "image/" + str(skin) + ".jpg"
    
    try:
        os.remove(skinPath)
        print(f"Removed skin file {skin}.")
    except FileNotFoundError:
        print(f"{skin}.skin not found. Trying to remove .hskin")
        try:
            os.remove(hskinPath)
            print(f"Removed hskin file {skin}.")
        except FileNotFoundError:
            print(f"{skin}.hskin not found.")
            sys.exit()
        except Exception as exc:
            print(f"{skin}.hskin could not be removed: {exc}")
            sys.exit()
    except Exception as exc:
        print(f"Could not remove skin file {skin}: {exc}")
    try:
        os.remove(imagePath)
        print(f"Removed image {skin}.")
    except Exception as exc:
        print(f"{skin}.jpg could not be removed. {exc}")
