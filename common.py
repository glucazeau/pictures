import glob


def list_files(source_path):
    extensions = ["png", "jpg", "jpeg", "gif"]
    files = []
    for extension in extensions:
        files += (glob.glob(f"{source_path}/**/*.{extension}", recursive=True))
    return files
