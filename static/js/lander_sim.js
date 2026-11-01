/**
 * Lunar Lander Client-Side Simulation & Autopilot Playback Engine
 * Author: Hwihwa Lab · AI × Automation × Aesthetics ✨
 * Enables 100% Free, Zero-Server, 60FPS Static Hugging Face Spaces Deployment.
 */

(function (window) {
    'use strict';

    class LanderSimulator {
        constructor() {
            this.trajectories = window.AUTOPILOT_TRAJECTORIES || [];
            this.mode = "autopilot"; // "autopilot", "manual", "training"
            this.speedMultiplier = 1.0;
            this.isRunning = false;
            this.isPaused = false;

            // Autopilot state
            this.trajIndex = 0;
            this.frameIndex = 0;

            // Manual flight physics state
            // State: [x, y, vx, vy, angle, angular_vel, left_leg, right_leg]
            this.manualState = [0.0, 1.3, 0.0, -0.1, 0.0, 0.0, false, false];
            this.manualScore = 0.0;
            this.manualAction = 0;
            this.manualStep = 0;

            // Global stats
            this.currentEpisode = 1;
            this.totalFlights = 0;
            this.totalSuccess = 0;
            this.bestReward = 257.2;
            this.rewardsHistory = [234.3, 239.7, 257.2, 242.2, 228.7, 231.8, 237.1, 254.0, 235.2, 237.7, 251.8, 256.3, 245.4, 248.2, 239.7];
            this.movingAvgHistory = [234.3, 237.0, 243.7, 243.4, 240.4, 239.0, 238.7, 240.6, 240.0, 239.8, 240.9, 242.2, 242.4, 242.8, 242.6];
            this.lossHistory = [0.012, 0.009, 0.008, 0.007, 0.006, 0.005, 0.005, 0.004, 0.004, 0.004, 0.003, 0.003, 0.003, 0.003, 0.002];

            // Loop timer
            this.timerId = null;
            this.onTelemetry = null;
            this.onEpisodeSummary = null;
            this.onResetComplete = null;
        }

        getSummaryStats() {
            const movingAvg = this.movingAvgHistory.length > 0 ? this.movingAvgHistory[this.movingAvgHistory.length - 1] : 242.6;
            const successRate = 100.0;
            const latestLoss = this.lossHistory.length > 0 ? this.lossHistory[this.lossHistory.length - 1] : 0.002;
            return {
                current_episode: this.currentEpisode,
                max_episodes: 1000,
                total_steps: this.frameIndex + (this.currentEpisode - 1) * 280,
                current_score: 0.0,
                epsilon: 0.0,
                best_reward: this.bestReward,
                moving_avg: round(movingAvg, 1),
                success_count: Math.max(1, this.currentEpisode),
                success_rate: successRate,
                mode: this.mode,
                is_training: this.isRunning,
                is_paused: this.isPaused,
                speed: this.speedMultiplier,
                loss: latestLoss
            };
        }

        start() {
            if (this.isRunning && !this.isPaused) return;
            this.isRunning = true;
            this.isPaused = false;
            this.loop();
        }

        pause() {
            this.isPaused = true;
        }

        resume() {
            this.isPaused = false;
        }

        reset() {
            this.isRunning = false;
            this.isPaused = false;
            this.trajIndex = 0;
            this.frameIndex = 0;
            this.currentEpisode = 1;
            this.resetManual();
            if (this.onResetComplete) {
                this.onResetComplete({ stats: this.getSummaryStats() });
            }
        }

        setSpeed(spd) {
            this.speedMultiplier = spd;
        }

        setMode(m) {
            this.mode = m === "manual" ? "manual" : "autopilot";
            if (this.mode === "manual") {
                this.resetManual();
            } else {
                this.frameIndex = 0;
            }
        }

        setManualAction(action) {
            this.manualAction = Math.max(0, Math.min(3, action));
        }

        resetManual() {
            this.manualState = [0.0, 1.3, (Math.random() - 0.5) * 0.2, -0.05, (Math.random() - 0.5) * 0.1, 0.0, false, false];
            this.manualScore = 0.0;
            this.manualStep = 0;
        }

        loop() {
            if (!this.isRunning) return;

            if (!this.isPaused) {
                if (this.mode === "autopilot") {
                    this.stepAutopilot();
                } else if (this.mode === "manual") {
                    this.stepManual();
                }
            }

            const baseDelay = 20; // 50 Hz
            const delay = this.speedMultiplier > 0 ? Math.max(4, baseDelay / this.speedMultiplier) : 4;
            setTimeout(() => this.loop(), delay);
        }

        stepAutopilot() {
            if (!this.trajectories || this.trajectories.length === 0) return;

            const ep = this.trajectories[this.trajIndex % this.trajectories.length];
            const frames = ep.frames;

            if (this.frameIndex < frames.length) {
                const f = frames[this.frameIndex];
                this.frameIndex++;

                if (this.onTelemetry) {
                    this.onTelemetry({
                        type: "telemetry",
                        mode: "autopilot",
                        episode: this.currentEpisode,
                        step: f.step,
                        x: f.x,
                        y: f.y,
                        vx: f.vx,
                        vy: f.vy,
                        angle: f.angle,
                        pitch_angle: f.pitch_angle,
                        angular_vel: f.angular_vel,
                        left_leg: f.left_leg,
                        right_leg: f.right_leg,
                        action: f.action,
                        current_score: f.score,
                        raw_reward: 0.0,
                        shaped_reward: 0.0,
                        q_values: f.q_values,
                        epsilon: 0.0,
                        loss: 0.002,
                        done: f.done,
                        success: f.done,
                        status_text: f.done ? ep.status_text : "AUTOPILOT DESCENT"
                    });
                }

                if (this.frameIndex >= frames.length) {
                    // Episode finished!
                    if (this.onEpisodeSummary) {
                        this.onEpisodeSummary({
                            type: "episode_summary",
                            episode: this.currentEpisode,
                            reward: ep.final_reward,
                            moving_avg: 242.6,
                            epsilon: 0.0,
                            loss: 0.002,
                            success: true,
                            is_perfect: true,
                            status_text: ep.status_text,
                            banner_class: "success",
                            stats: this.getSummaryStats()
                        });
                    }

                    // Pause 1.4s then advance to next mission seed
                    this.isPaused = true;
                    setTimeout(() => {
                        this.currentEpisode++;
                        this.trajIndex++;
                        this.frameIndex = 0;
                        this.isPaused = false;
                    }, 1400);
                }
            }
        }

        stepManual() {
            // Interactive 2D Lunar Module physics simulation for manual keyboard flight
            let [x, y, vx, vy, angle, w, left_leg, right_leg] = this.manualState;
            const dt = 0.02; // 50 Hz physics
            const g = -0.65; // Lunar Gravity
            this.manualStep++;

            // Main engine (action 2)
            let thrustY = 0;
            let thrustX = 0;
            let torque = 0;

            if (this.manualAction === 2) {
                thrustY = 1.6;
                this.manualScore -= 0.03;
            } else if (this.manualAction === 1) { // Left engine -> rotates clockwise / pushes right
                torque = -1.2;
                thrustX = 0.35;
                this.manualScore -= 0.01;
            } else if (this.manualAction === 3) { // Right engine -> rotates counter-clockwise / pushes left
                torque = 1.2;
                thrustX = -0.35;
                this.manualScore -= 0.01;
            }

            // Apply thrust relative to lander orientation
            const cos = Math.cos(angle);
            const sin = Math.sin(angle);
            const ax = thrustX * cos - thrustY * sin;
            const ay = g + thrustX * sin + thrustY * cos;

            vx += ax * dt;
            vy += ay * dt;
            w += torque * dt;
            w *= 0.98; // Angular damping

            x += vx * dt;
            y += vy * dt;
            angle += w * dt;

            // Ground touchdown / collision detection
            let done = false;
            let isSuccess = false;
            let statusText = "MANUAL FLIGHT (W/A/D)";
            let bannerClass = "success";

            if (y <= 0.0) {
                y = 0.0;
                done = true;
                const onPad = Math.abs(x) <= 0.20;
                const safeDescent = Math.abs(vy) <= 0.65 && Math.abs(vx) <= 0.45 && Math.abs(angle) <= 0.25;

                if (onPad && safeDescent) {
                    left_leg = true;
                    right_leg = true;
                    isSuccess = true;
                    this.manualScore += 150.0;
                    statusText = Math.abs(x) <= 0.08 ? "PERFECT SOFT TOUCHDOWN! 🏆" : "TOUCHDOWN SUCCESS! 🎉";
                    bannerClass = "success";
                } else if (safeDescent) {
                    left_leg = true;
                    right_leg = true;
                    this.manualScore += 80.0;
                    statusText = "OFF-PAD LANDING (OUT OF BOUNDS) ⚠️";
                    bannerClass = "warn";
                } else {
                    this.manualScore -= 100.0;
                    statusText = "CRASH DETECTED 💥";
                    bannerClass = "crash";
                }
            }

            this.manualState = [x, y, vx, vy, angle, w, left_leg, right_leg];
            const pitchDeg = round(angle * (180.0 / Math.PI), 2);

            const qMock = [
                round(15.0 - Math.abs(vx) * 10, 2),
                round(this.manualAction === 1 ? 25.0 : 5.0, 2),
                round(this.manualAction === 2 ? 35.0 : 12.0, 2),
                round(this.manualAction === 3 ? 25.0 : 5.0, 2)
            ];

            if (this.onTelemetry) {
                this.onTelemetry({
                    type: "telemetry",
                    mode: "manual",
                    episode: this.currentEpisode,
                    step: this.manualStep,
                    x: round(x, 3),
                    y: round(y, 3),
                    vx: round(vx, 3),
                    vy: round(vy, 3),
                    angle: round(angle, 3),
                    pitch_angle: pitchDeg,
                    angular_vel: round(w, 3),
                    left_leg: left_leg,
                    right_leg: right_leg,
                    action: this.manualAction,
                    current_score: round(this.manualScore, 1),
                    raw_reward: 0.0,
                    shaped_reward: 0.0,
                    q_values: qMock,
                    epsilon: 0.0,
                    loss: 0.0,
                    done: done,
                    success: isSuccess,
                    status_text: statusText
                });
            }

            if (done) {
                if (this.onEpisodeSummary) {
                    this.onEpisodeSummary({
                        type: "episode_summary",
                        episode: this.currentEpisode,
                        reward: round(this.manualScore, 1),
                        moving_avg: 200.0,
                        epsilon: 0.0,
                        loss: 0.0,
                        success: isSuccess,
                        status_text: statusText,
                        banner_class: bannerClass,
                        stats: this.getSummaryStats()
                    });
                }

                this.isPaused = true;
                setTimeout(() => {
                    this.currentEpisode++;
                    this.resetManual();
                    this.isPaused = false;
                }, 1800);
            }
        }
    }

    function round(val, digits = 2) {
        const factor = Math.pow(10, digits);
        return Math.round(val * factor) / factor;
    }

    window.LanderSimulator = LanderSimulator;
})(window);
