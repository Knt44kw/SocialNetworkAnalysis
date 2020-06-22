import os

def extract_dataset_name(filename) -> str:
    target = os.path.basename(filename)
    if "karate" in target:
        karate, _ = target.split(".")
        return karate
    
    elif "facebook" in target:
        facebook, _ = target.split("_")
        return facebook

    elif "twitter" in target:
        twitter, _ = target.split("_")    
        return twitter
    
