import os
from subprocess import run, CalledProcessError


def get_env():
    env = os.environ.copy()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env["PYTHONPATH"] = f'{root_dir}:{os.path.join(root_dir, "src")}'
    return env


async def run_model(model: str, track_no: int, env=None):
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", f"{model.value}_model.py")
    try:
        env = env if env is not None else get_env()
        result = run(
            ["python", model_path, str(track_no)],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
    except CalledProcessError as e:
        print(e.output, e.stderr, e.stdout)
        raise CalledProcessError(f"Model execution failed: {e.output}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Invalid model. {model} not found.")
    return result
