import glob


def list_files(source_path):
    extensions = ["png", "jpg", "jpeg", "gif"]
    files = []
    for extension in extensions:
        files += (glob.glob(f"{source_path}/*.{extension}"))
    #files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    return files
