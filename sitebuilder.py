# Read YAML file
import yaml
import jinja2
from pathlib import Path
import sass

# This script path and directory
SCRIPT_PATH = Path(__file__)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Site Directories
SITE_DIR = SCRIPT_DIR / 'site'

# Data
DATA_FILE = SCRIPT_DIR / 'data.yaml'

# Templates
TEMPLATES_DIR = SITE_DIR / 'templates'

# Assets
ASSETS_DIR = SITE_DIR / 'assets'
IMG_DIR = ASSETS_DIR / 'img'  # Images
SCRIPTS_DIR = ASSETS_DIR / 'js'  # JavaScript
STYLES_DIR = ASSETS_DIR / 'styles'  # Styles

# Distribution
DIST_DIR = SCRIPT_DIR / 'dist'
DIST_ASSETS_DIR = DIST_DIR / 'assets'
DIST_IMG_DIR = DIST_ASSETS_DIR / 'img'
DIST_SCRIPTS_DIR = DIST_ASSETS_DIR / 'js'
DIST_STYLES_DIR = DIST_ASSETS_DIR / 'css'


def read_data(file_path) -> dict:
    with open(file_path, 'r') as file:
        return dict(yaml.safe_load(file))


def copy_assets(src_dir: Path, dst_dir: Path):
    if src_dir.exists():
        for item in src_dir.iterdir():
            if item.is_file():
                dest_file = dst_dir / item.name
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                with open(item, 'rb') as src, open(dest_file, 'wb') as dst:
                    dst.write(src.read())
            elif item.is_dir():
                copy_assets(item, dst_dir / item.name)


def main():

    # Ensure distribution directory exists
    Path(DIST_DIR).mkdir(parents=True, exist_ok=True)
    Path(DIST_STYLES_DIR).mkdir(parents=True, exist_ok=True)

    # Read data
    data: dict = read_data(DATA_FILE) if DATA_FILE.exists() else {}

    # Compile styles
    sass.compile(dirname=(str(STYLES_DIR), str(
        DIST_STYLES_DIR)), output_style='expanded')

    # Set up Jinja2 environment
    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
    template_env = jinja2.Environment(loader=template_loader)

    # Render template
    template = template_env.get_template("template.html")
    with open(Path(DIST_DIR) / "index.html", "w") as f:
        f.write(template.render(data=data))

    # Copy static assets
    copy_assets(IMG_DIR, DIST_IMG_DIR)  # Copy images
    copy_assets(SCRIPTS_DIR, DIST_SCRIPTS_DIR)  # Copy scripts
    


if __name__ == "__main__":

    main()
