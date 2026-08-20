/**
 * Lunar Lander Mission Control - 3-Column Cockpit App Controller
 * Manages WebSocket, Pitch Gyro Animation, 3-Tier Chart.js, HUD Telemetry, and Mode Buttons.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Canvas Renderer
    const renderer = new LanderRenderer('flightCanvas');

    // 2. State & WebSocket Variables
    let socket = null;
    let isConnected = false;
    let manualKeyActive = { up: false, left: false, right: false };

    // 3. UI Element References
    const connectionDot = document.getElementById('connectionDot');
    const connectionText = document.getElementById('connectionText');
    const hdrEpisode = document.getElementById('hdrEpisode');
    const hdrEpsilon = document.getElementById('hdrEpsilon');
    const hdrBestScore = document.getElementById('hdrBestScore');

    // Telemetry Elements
    const gyroGround = document.getElementById('gyroGround');
    const telePitch = document.getElementById('telePitch');
    const teleOmega = document.getElementById('teleOmega');
    const valVy = document.getElementById('valVy');
    const valVx = document.getElementById('valVx');
    const barVy = document.getElementById('barVy');
    const barVx = document.getElementById('barVx');
    const valAlt = document.getElementById('valAlt');
    const valOffset = document.getElementById('valOffset');
    const leftLegBox = document.getElementById('leftLegBox');
    const rightLegBox = document.getElementById('rightLegBox');
    const leftLegText = document.getElementById('leftLegText');
    const rightLegText = document.getElementById('rightLegText');

    // Q-Value Elements
    const qCards = [
        document.getElementById('qCard0'),
        document.getElementById('qCard1'),
        document.getElementById('qCard2'),
        document.getElementById('qCard3'),
    ];
    const qScores = [
        document.getElementById('qScore0'),
        document.getElementById('qScore1'),
        document.getElementById('qScore2'),
        document.getElementById('qScore3'),
    ];
    const qFills = [
        document.getElementById('qFill0'),
        document.getElementById('qFill1'),
        document.getElementById('qFill2'),
        document.getElementById('qFill3'),
    ];

    // Sim View Elements
    const simStatusBadge = document.getElementById('simStatusBadge');
    const simEpStep = document.getElementById('simEpStep');
    const simScoreText = document.getElementById('simScoreText');
    const touchdownBanner = document.getElementById('touchdownBanner');

    // Analytics Metrics
    const statCurScore = document.getElementById('statCurScore');
    const statSma = document.getElementById('statSma');
    const statSuccess = document.getElementById('statSuccess');
    const statLoss = document.getElementById('statLoss');

    // Control Buttons
    const btnStart = document.getElementById('btnStart');
    const btnPause = document.getElementById('btnPause');
    const btnReset = document.getElementById('btnReset');
    const btnLoadBest = document.getElementById('btnLoadBest');
    const modeButtons = document.querySelectorAll('.btn-mode');
    const speedButtons = document.querySelectorAll('.btn-speed');

    // =========================================================================
    // 4. Initialize 3-Tier Chart.js Instances
    // =========================================================================
    const commonChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        plugins: { legend: { display: false }, tooltip: { enabled: true } },
        scales: {
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 }, maxTicksLimit: 6 }
            },
            y: {
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 }, maxTicksLimit: 4 }
            }
        }
    };

    // Chart 1: Reward & 100-MA
    const rewardChart = new Chart(document.getElementById('rewardChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Score',
                    data: [],
                    borderColor: '#38bdf8',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.1,
                },
                {
                    label: 'SMA 100',
                    data: [],
                    borderColor: '#c084fc',
                    borderWidth: 2.5,
                    pointRadius: 0,
                    tension: 0.2,
                },
                {
                    label: 'Target (200)',
                    data: [],
                    borderColor: 'rgba(16, 185, 129, 0.5)',
                    borderWidth: 1.5,
                    borderDash: [4, 4],
                    pointRadius: 0,
                    fill: false,
                }
            ]
        },
        options: {
            ...commonChartOptions,
            scales: {
                ...commonChartOptions.scales,
                y: { ...commonChartOptions.scales.y, suggestedMin: -200, suggestedMax: 260 }
            }
        }
    });

    // Chart 2: Epsilon Decay
    const epsilonChart = new Chart(document.getElementById('epsilonChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Epsilon (%)',
                data: [],
                borderColor: '#fbbf24',
                backgroundColor: 'rgba(251, 191, 36, 0.07)',
                borderWidth: 2,
                pointRadius: 0,
                fill: true,
                tension: 0.1,
            }]
        },
        options: {
            ...commonChartOptions,
            scales: {
                ...commonChartOptions.scales,
                y: { ...commonChartOptions.scales.y, min: 0, max: 100 }
            }
        }
    });

    // Chart 3: MSE Loss Progression
    const lossChart = new Chart(document.getElementById('lossChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'MSE Loss',
                data: [],
                borderColor: '#f43f5e',
                backgroundColor: 'rgba(244, 63, 94, 0.07)',
                borderWidth: 2,
                pointRadius: 0,
                fill: true,
                tension: 0.1,
            }]
        },
        options: {
            ...commonChartOptions,
            scales: {
                ...commonChartOptions.scales,
                y: { ...commonChartOptions.scales.y, suggestedMin: 0, suggestedMax: 1.0 }
            }
        }
    });

    // =========================================================================
    // 5. WebSocket Communication
    // =========================================================================
    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;

        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            isConnected = true;
            connectionDot.style.background = 'var(--neon-green)';
            connectionText.textContent = 'GYM SIMULATION CONNECTED';
            console.log('[WebSocket] Connected.');
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleServerMessage(data);
        };

        socket.onclose = () => {
            isConnected = false;
            connectionDot.style.background = '#64748b';
            connectionText.textContent = 'RECONNECTING...';
            setTimeout(connectWebSocket, 2000);
        };

        socket.onerror = (err) => {
            console.error('[WebSocket] Error:', err);
        };
    }

    function sendCommand(cmd, payload = {}) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ command: cmd, ...payload }));
        }
    }

    // =========================================================================
    // 6. Message & Telemetry Handler
    // =========================================================================
    function handleServerMessage(msg) {
        if (msg.type === 'init') {
            updateStatsUI(msg.stats);
            if (msg.history) {
                populateChartsHistory(msg.history);
            }
        } else if (msg.type === 'telemetry') {
            handleTelemetry(msg);
        } else if (msg.type === 'episode_summary') {
            handleEpisodeSummary(msg);
        } else if (msg.type === 'showcase_complete' || msg.type === 'manual_complete') {
            handleFlightComplete(msg);
        } else if (msg.type === 'reset_complete') {
            resetCharts();
            updateStatsUI(msg.stats);
        } else if (msg.type === 'model_loaded') {
            showTouchdownBanner('BEST MODEL LOADED! 🌟', false);
            updateStatsUI(msg.stats);
        }
    }

    function handleTelemetry(t) {
        // Feed into Canvas Renderer
        renderer.updateState(t);

        // 1. Attitude & Pitch Gyro
        const pitchAngle = t.pitch_angle || (t.angle * (180 / Math.PI));
        telePitch.textContent = `${pitchAngle.toFixed(2)}°`;
        teleOmega.textContent = `${t.angular_vel.toFixed(2)} rad/s`;

        // Rotate Gyro Ground
        if (gyroGround) {
            gyroGround.style.transform = `rotate(${-pitchAngle}deg)`;
        }

        // 2. Velocity Vectors & Gauges
        valVy.textContent = `${(t.vy * 10).toFixed(2)} m/s`;
        valVx.textContent = `${(t.vx * 10).toFixed(2)} m/s`;

        const vyPct = Math.max(5, Math.min(100, ((-t.vy + 1.0) / 2.0) * 100));
        barVy.style.width = `${vyPct}%`;
        if (t.vy < -0.6) {
            barVy.className = 'gauge-bar danger';
        } else if (t.vy < -0.3) {
            barVy.className = 'gauge-bar warn';
        } else {
            barVy.className = 'gauge-bar';
        }

        const vxPct = Math.max(5, Math.min(100, ((Math.abs(t.vx)) / 1.0) * 100));
        barVx.style.width = `${vxPct}%`;

        // 3. Coordinates & Sensors
        valAlt.textContent = t.y.toFixed(3);
        valOffset.textContent = t.x.toFixed(3);

        if (t.left_leg) {
            leftLegBox.className = 'leg-box contact';
            leftLegText.textContent = 'CONTACT';
        } else {
            leftLegBox.className = 'leg-box';
            leftLegText.textContent = 'NO CONTACT';
        }

        if (t.right_leg) {
            rightLegBox.className = 'leg-box contact';
            rightLegText.textContent = 'CONTACT';
        } else {
            rightLegBox.className = 'leg-box';
            rightLegText.textContent = 'NO CONTACT';
        }

        // 4. DQN Action Q-Values
        if (t.q_values && t.q_values.length === 4) {
            const maxQ = Math.max(...t.q_values, 1.0);
            const minQ = Math.min(...t.q_values, 0.0);
            const range = Math.max(0.1, maxQ - minQ);

            for (let i = 0; i < 4; i++) {
                const q = t.q_values[i];
                qScores[i].textContent = q.toFixed(2);
                const pct = Math.max(5, Math.min(100, ((q - minQ) / range) * 100));
                qFills[i].style.width = `${pct}%`;

                if (i === t.action) {
                    qCards[i].classList.add('active');
                } else {
                    qCards[i].classList.remove('active');
                }
            }
        }

        // 5. Sim View Info
        simEpStep.textContent = `EP: ${t.episode} | STEP: ${t.step}`;
        simScoreText.textContent = `SCORE: ${t.current_score.toFixed(1)}`;
        simStatusBadge.textContent = t.status_text || 'IN FLIGHT';

        // 6. Right Side Quick Metrics
        statCurScore.textContent = t.current_score.toFixed(1);
        statLoss.textContent = t.loss.toFixed(3);
    }

    function handleEpisodeSummary(msg) {
        // Chart 1: Reward & 100-MA
        rewardChart.data.labels.push(msg.episode);
        rewardChart.data.datasets[0].data.push(msg.reward);
        rewardChart.data.datasets[1].data.push(msg.moving_avg);
        rewardChart.data.datasets[2].data.push(200);

        // Chart 2: Epsilon
        epsilonChart.data.labels.push(msg.episode);
        epsilonChart.data.datasets[0].data.push(msg.epsilon);

        // Chart 3: Loss
        lossChart.data.labels.push(msg.episode);
        lossChart.data.datasets[0].data.push(msg.loss);

        if (rewardChart.data.labels.length > 1000) {
            rewardChart.data.labels.shift();
            rewardChart.data.datasets[0].data.shift();
            rewardChart.data.datasets[1].data.shift();
            rewardChart.data.datasets[2].data.shift();

            epsilonChart.data.labels.shift();
            epsilonChart.data.datasets[0].data.shift();

            lossChart.data.labels.shift();
            lossChart.data.datasets[0].data.shift();
        }

        rewardChart.update('none');
        epsilonChart.update('none');
        lossChart.update('none');

        updateStatsUI(msg.stats);

        if (msg.success) {
            showTouchdownBanner('PERFECT LANDING! 🏆', false);
        }
    }

    function handleFlightComplete(msg) {
        if (msg.success) {
            showTouchdownBanner('TOUCHDOWN SUCCESS! 🎉', false);
        } else {
            showTouchdownBanner('MISSION FAILED 💥', true);
        }
    }

    function showTouchdownBanner(text, isCrash) {
        touchdownBanner.textContent = text;
        touchdownBanner.className = `touchdown-banner ${isCrash ? 'crash' : ''} show`;
        setTimeout(() => {
            touchdownBanner.classList.remove('show');
        }, 2200);
    }

    function updateStatsUI(stats) {
        if (!stats) return;

        // Top Header
        hdrEpisode.textContent = `${stats.current_episode} / ${stats.max_episodes}`;
        hdrEpsilon.textContent = `${(stats.epsilon * 100).toFixed(1)}%`;
        hdrBestScore.textContent = stats.best_reward;

        // Right Column Cards
        statCurScore.textContent = stats.current_score || 0.0;
        statSma.textContent = stats.moving_avg;
        statSuccess.textContent = `${stats.success_rate}%`;
        statLoss.textContent = stats.loss;

        // Button States
        if (stats.is_training && !stats.is_paused) {
            btnStart.style.opacity = '0.6';
            btnPause.style.opacity = '1';
        } else {
            btnStart.style.opacity = '1';
            btnPause.style.opacity = '0.6';
        }
    }

    function populateChartsHistory(hist) {
        const eps = hist.rewards.map((_, idx) => idx + 1);
        
        rewardChart.data.labels = eps;
        rewardChart.data.datasets[0].data = hist.rewards;
        rewardChart.data.datasets[1].data = hist.moving_avg;
        rewardChart.data.datasets[2].data = hist.rewards.map(() => 200);
        rewardChart.update();

        if (hist.epsilon) {
            epsilonChart.data.labels = eps;
            epsilonChart.data.datasets[0].data = hist.epsilon.map(e => e * 100);
            epsilonChart.update();
        }

        if (hist.loss) {
            lossChart.data.labels = eps;
            lossChart.data.datasets[0].data = hist.loss;
            lossChart.update();
        }
    }

    function resetCharts() {
        rewardChart.data.labels = [];
        rewardChart.data.datasets[0].data = [];
        rewardChart.data.datasets[1].data = [];
        rewardChart.data.datasets[2].data = [];
        rewardChart.update();

        epsilonChart.data.labels = [];
        epsilonChart.data.datasets[0].data = [];
        epsilonChart.update();

        lossChart.data.labels = [];
        lossChart.data.datasets[0].data = [];
        lossChart.update();

        renderer.resetTrail();
    }

    // =========================================================================
    // 7. Interactive Buttons & Mode Selectors
    // =========================================================================
    btnStart.addEventListener('click', () => {
        sendCommand('start');
    });

    btnPause.addEventListener('click', () => {
        sendCommand('pause');
    });

    btnReset.addEventListener('click', () => {
        if (confirm('Are you sure you want to reset all training metrics and neural network weights?')) {
            sendCommand('reset');
        }
    });

    if (btnLoadBest) {
        btnLoadBest.addEventListener('click', () => {
            sendCommand('load_best');
        });
    }

    // Mode Selector Buttons
    modeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            modeButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const mode = btn.dataset.mode;
            renderer.resetTrail();
            sendCommand('set_mode', { mode });
        });
    });

    // Speed Selector Buttons
    speedButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            speedButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const speed = parseFloat(btn.dataset.speed);
            sendCommand('set_speed', { speed });
        });
    });

    // =========================================================================
    // 8. Keyboard Controls for Manual Mode
    // =========================================================================
    window.addEventListener('keydown', (e) => {
        if (['ArrowUp', 'ArrowLeft', 'ArrowRight', 'KeyW', 'KeyA', 'KeyD', 'Space'].includes(e.code)) {
            e.preventDefault();
        }

        let action = 0;
        if (e.code === 'ArrowUp' || e.code === 'KeyW' || e.code === 'Space') {
            manualKeyActive.up = true;
            action = 2; // Main engine
        } else if (e.code === 'ArrowLeft' || e.code === 'KeyA') {
            manualKeyActive.left = true;
            action = 1; // Left engine
        } else if (e.code === 'ArrowRight' || e.code === 'KeyD') {
            manualKeyActive.right = true;
            action = 3; // Right engine
        }

        if (action !== 0) {
            sendCommand('manual_action', { action });
        }
    });

    window.addEventListener('keyup', (e) => {
        if (e.code === 'ArrowUp' || e.code === 'KeyW' || e.code === 'Space') {
            manualKeyActive.up = false;
        } else if (e.code === 'ArrowLeft' || e.code === 'KeyA') {
            manualKeyActive.left = false;
        } else if (e.code === 'ArrowRight' || e.code === 'KeyD') {
            manualKeyActive.right = false;
        }

        if (!manualKeyActive.up && !manualKeyActive.left && !manualKeyActive.right) {
            sendCommand('manual_action', { action: 0 });
        }
    });

    // Connect WebSocket on Load
    connectWebSocket();
});
