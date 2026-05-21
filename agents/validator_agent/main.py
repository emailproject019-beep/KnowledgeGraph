import yaml
from validator_agent import ValidatorAgent


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    config = load_config("config.yaml")
    agent = ValidatorAgent(config=config)
    agent.load()
    agent.run()
