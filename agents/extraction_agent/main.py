import yaml
from extraction_agent import ExtractionAgent


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    config = load_config("config.yaml")
    agent = ExtractionAgent(config=config)
    agent.load()
    agent.run()
