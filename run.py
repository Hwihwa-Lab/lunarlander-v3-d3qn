"""
Quick Launcher for Lunar Lander Mission Control Dashboard
"""

from server import run_server

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("🚀 [Lunar Lander] Mission Control Web Dashboard")
    print("🛸 Cyberpunk DQN Flight Deck & Real-time Reinforcement Learning")
    print("🌐 Open URL: http://localhost:8000")
    print("=" * 65 + "\n")
    run_server(host="0.0.0.0", port=8000)
