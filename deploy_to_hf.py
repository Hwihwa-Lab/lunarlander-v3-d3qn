"""
One-Click Hugging Face Deployment Pipeline for Lunar Lander D3QN.
Deploys Model Hub (Weights, Config, Docs) and Interactive Static Space (60FPS Web Deck).
100% Free Forever, Zero-Server Cost, Zero Subscription Required.

Usage:
    # 1. Deploy Live Interactive Space (Public Default)
    python deploy_to_hf.py --target space

    # 2. Deploy Model Hub (Weights & Config)
    python deploy_to_hf.py --target model

    # 3. Deploy All (Both Model Hub and Spaces)
    python deploy_to_hf.py --target all
"""

import os
import sys
import json
import argparse
from pathlib import Path
from huggingface_hub import HfApi, create_repo


def deploy_model(repo_name: str = "lunarlander-v3-d3qn", private: bool = False, model_path: str = "models/best_model.pth") -> bool:
    api = HfApi()
    
    # 1. Verify authentication
    try:
        user_info = api.whoami()
        username = user_info["name"]
        print(f"🔑 Authenticated as: {username}")
    except Exception as e:
        print(f"❌ Authentication failed. Please run 'hf auth login' first. Error: {e}")
        return False

    repo_id = f"{username}/{repo_name}"
    
    # 2. Check model file existence
    if not os.path.exists(model_path):
        print(f"❌ Model weight file not found at: {model_path}")
        print("💡 Please ensure training has created 'models/best_model.pth'.")
        return False
        
    print(f"📦 Model weight found: {model_path} ({os.path.getsize(model_path) / 1024:.1f} KB)")

    # 3. Create or verify repository on Hugging Face
    print(f"\n🌐 Creating / checking Model Hub repository: {repo_id} (Private={private})...")
    try:
        create_repo(repo_id=repo_id, repo_type="model", private=private, exist_ok=True)
        print(f"✅ Model Hub ready: https://huggingface.co/{repo_id}")
    except Exception as e:
        print(f"❌ Failed to create repo {repo_id}: {e}")
        return False

    # 4. Generate & upload config.json
    config_data = {
        "algorithm": "Dueling Double DQN (D3QN)",
        "environment": "LunarLander-v3",
        "state_dim": 8,
        "action_dim": 4,
        "hidden_dim": 128,
        "gamma": 0.99,
        "lr": 0.0005,
        "batch_size": 64,
        "tau": 0.001,
        "framework": "PyTorch",
        "library": "Gymnasium"
    }
    
    temp_dir = Path("scratch")
    temp_dir.mkdir(exist_ok=True)
    
    config_file = temp_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    # 5. Upload files to Hugging Face Model Hub
    print("📤 Uploading files to Hugging Face Model Hub...")
    try:
        # Upload model weight
        api.upload_file(
            path_or_fileobj=model_path,
            path_in_repo="best_model.pth",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Upload LunarLander D3QN best model weights"
        )
        print("  - [1/5] Uploaded best_model.pth ✅")
        
        # Upload config.json
        api.upload_file(
            path_or_fileobj=str(config_file),
            path_in_repo="config.json",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Upload model configuration and metadata"
        )
        print("  - [2/5] Uploaded config.json ✅")
        
        # Upload dqn_agent.py
        if os.path.exists("dqn_agent.py"):
            api.upload_file(
                path_or_fileobj="dqn_agent.py",
                path_in_repo="dqn_agent.py",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Upload DQNAgent and DuelingQNetwork PyTorch architecture source"
            )
            print("  - [3/5] Uploaded dqn_agent.py (Architecture Source) ✅")
        
        # Upload README.md
        if os.path.exists("README.md"):
            api.upload_file(
                path_or_fileobj="README.md",
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Upload comprehensive Global English Model Card README"
            )
            print("  - [4/5] Uploaded README.md (Global English Model Card) ✅")

        # Upload README_KR.md
        if os.path.exists("README_KR.md"):
            api.upload_file(
                path_or_fileobj="README_KR.md",
                path_in_repo="README_KR.md",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Upload comprehensive Korean manual README_KR.md"
            )
            print("  - [5/5] Uploaded README_KR.md (Korean Manual) ✅")

        # Upload LICENSE
        if os.path.exists("LICENSE"):
            api.upload_file(
                path_or_fileobj="LICENSE",
                path_in_repo="LICENSE",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Upload MIT License"
            )
            print("  - [Bonus] Uploaded LICENSE ✅")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 MODEL HUB DEPLOYMENT COMPLETE!")
    print(f"👉 Model Hub URL: https://huggingface.co/{repo_id}")
    print("=" * 60 + "\n")
    return True


def deploy_space(space_name: str = "lunarlander-v3-d3qn", private: bool = False) -> bool:
    api = HfApi()
    
    # 1. Verify authentication
    try:
        user_info = api.whoami()
        username = user_info["name"]
        print(f"🔑 Authenticated as: {username}")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

    space_id = f"{username}/{space_name}"
    print("\n" + "=" * 60)
    print(f"🛸 Deploying to Hugging Face Static Spaces: {space_id} (Public={not private})")
    print("=" * 60)

    try:
        create_repo(
            repo_id=space_id,
            repo_type="space",
            space_sdk="static",
            private=private,
            exist_ok=True
        )
        print(f"✅ Space repository ready: https://huggingface.co/spaces/{space_id}")
    except Exception as e:
        print(f"❌ Failed to create Space repo {space_id}: {e}")
        return False

    # 2. Upload Space README.md with Static frontmatter
    space_readme = f"""---
title: LunarLander-v3 D3QN Mission Control
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
license: mit
tags:
- reinforcement-learning
- gymnasium
- d3qn
- pytorch
- aerospace
- box2d
---

# 🚀 LunarLander-v3 D3QN // Mission Control Deck

High-precision Dueling Double Deep Q-Network (D3QN) Reinforcement Learning Flight Simulator & Aerospace Telemetry Control Deck.

Developed by **[Hwihwa Lab](https://github.com/Hwihwa-Lab)** · *AI × Automation × Aesthetics ✨*

- **Model Hub**: [https://huggingface.co/{username}/lunarlander-v3-d3qn](https://huggingface.co/{username}/lunarlander-v3-d3qn)
- **GitHub Repository**: [https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn](https://github.com/Hwihwa-Lab/lunarlander-v3-d3qn)
- **Twin Evolution (Phase 2)**: [Tesla Roadster 180° Inversion Landing](https://huggingface.co/spaces/{username}/tesla-roadster-flip-landing)

---

*Trained and deployed with [LunarLander Mission Control](https://huggingface.co/spaces/{space_id}) by **HWIHWALAB**.*
"""

    print("📤 Uploading static application assets to Hugging Face Spaces...")
    try:
        # 1. README.md
        api.upload_file(
            path_or_fileobj=space_readme.encode("utf-8"),
            path_in_repo="README.md",
            repo_id=space_id,
            repo_type="space",
            commit_message="Update Space README with Static SDK metadata"
        )
        print("  - [1/4] Uploaded README.md (Space Metadata) ✅")

        # 2. index.html at root of Space
        if os.path.exists("static/index.html"):
            api.upload_file(
                path_or_fileobj="static/index.html",
                path_in_repo="index.html",
                repo_id=space_id,
                repo_type="space",
                commit_message="Upload index.html to Space root"
            )
            print("  - [2/4] Uploaded index.html (Cockpit UI) ✅")

        # 3. static/ folder (css, js)
        if os.path.exists("static"):
            api.upload_folder(
                folder_path="static",
                path_in_repo="static",
                repo_id=space_id,
                repo_type="space",
                commit_message="Upload static CSS and JS telemetry assets"
            )
            print("  - [3/4] Uploaded static/ assets folder ✅")

        # 4. LICENSE
        if os.path.exists("LICENSE"):
            api.upload_file(
                path_or_fileobj="LICENSE",
                path_in_repo="LICENSE",
                repo_id=space_id,
                repo_type="space",
                commit_message="Add MIT License"
            )
            print("  - [4/4] Uploaded LICENSE ✅")

    except Exception as e:
        print(f"❌ Space upload failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 SPACE DEPLOYMENT COMPLETE! YOUR APP IS 100% LIVE ON HUGGING FACE! 🚀")
    print(f"👉 Live Space URL: https://huggingface.co/spaces/{space_id}")
    print("=" * 60 + "\n")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy LunarLander DQN to Hugging Face")
    parser.add_argument(
        "--target",
        type=str,
        default="space",
        choices=["all", "model", "space"],
        help="Deployment target: 'space' (interactive web deck), 'model' (weights), or 'all'"
    )
    parser.add_argument("--repo-name", type=str, default="lunarlander-v3-d3qn", help="Name of the repository")
    parser.add_argument("--private", action="store_true", help="Set repository to private (default: public)")
    parser.add_argument("--model-path", type=str, default="models/best_model.pth", help="Path to model weights")
    args = parser.parse_args()

    if args.target in ["all", "model"]:
        deploy_model(repo_name=args.repo_name, private=args.private, model_path=args.model_path)

    if args.target in ["all", "space"]:
        deploy_space(space_name=args.repo_name, private=args.private)
