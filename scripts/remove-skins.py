import os
import sys

skinsToRemove = [1149, 1143, 1487, 1628, 1641, 1709, 1790, 1807, 2322, 2325, 2341, 2342, 2347, 2366, 2374, 2551, 2895, 2896]

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
