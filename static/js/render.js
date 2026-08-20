/**
 * High-End Cybernetic Lunar Lander Canvas 2D Renderer
 * Renders spacecraft, jet propulsion flames, particle fx, lunar terrain, and HUD.
 */

class LanderRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Internal resolution for crisp rendering
        this.width = 800;
        this.height = 480;
        this.canvas.width = this.width;
        this.canvas.height = this.height;

        // Space Coordinates to Canvas Mapping
        // Gym LunarLander state:
        // x: approx [-1.0, 1.0] (0.0 is center)
        // y: approx [0.0, 1.4] (0.0 is ground level)
        this.scaleX = this.width / 2.2;
        this.scaleY = this.height / 1.5;
        this.originX = this.width / 2;
        this.originY = this.height * 0.82; // Ground baseline

        // Particle System
        this.particles = [];
        this.fireworks = [];
        this.trail = [];
        this.maxTrailLength = 40;

        // Background Stars
        this.stars = [];
        this.initStars(120);

        // State Cache
        this.landerState = {
            x: 0, y: 1.0, vx: 0, vy: 0,
            angle: 0, angular_vel: 0,
            left_leg: false, right_leg: false,
            action: 0, done: false, success: false
        };

        // Animation Loop
        this.isRunning = true;
        this.lastTime = performance.now();
        this.animate = this.animate.bind(this);
        requestAnimationFrame(this.animate);
    }

    initStars(count) {
        this.stars = [];
        for (let i = 0; i < count; i++) {
            this.stars.push({
                x: Math.random() * this.width,
                y: Math.random() * (this.originY - 20),
                radius: Math.random() * 1.5 + 0.5,
                alpha: Math.random(),
                speed: Math.random() * 0.02 + 0.005
            });
        }
    }

    updateState(telemetry) {
        if (!telemetry) return;
        this.landerState = { ...this.landerState, ...telemetry };

        // Convert coordinates to canvas
        const cx = this.originX + this.landerState.x * this.scaleX;
        const cy = this.originY - this.landerState.y * this.scaleY;

        // Record Trajectory Trail
        this.trail.push({ x: cx, y: cy, time: performance.now() });
        if (this.trail.length > this.maxTrailLength) {
            this.trail.shift();
        }

        // Spawn Jet Propulsion Particles
        this.spawnJetParticles(cx, cy, this.landerState.angle, this.landerState.action);

        // Success / Crash Particle Trigger
        if (this.landerState.done) {
            if (this.landerState.success) {
                this.spawnFireworks(cx, cy);
            } else if (this.landerState.y < 0.1 && (Math.abs(this.landerState.vx) > 0.5 || Math.abs(this.landerState.vy) > 0.6)) {
                this.spawnExplosion(cx, cy);
            }
        }
    }

    spawnJetParticles(cx, cy, angle, action) {
        // action: 0: None, 1: Left engine, 2: Main engine, 3: Right engine
        const cos = Math.cos(angle);
        const sin = Math.sin(angle);

        // Main Engine (fires downward relative to lander)
        if (action === 2) {
            const nozzleX = cx - sin * 18;
            const nozzleY = cy + cos * 18;
            for (let i = 0; i < 4; i++) {
                const spread = (Math.random() - 0.5) * 0.4;
                const speed = Math.random() * 6 + 4;
                this.particles.push({
                    x: nozzleX,
                    y: nozzleY,
                    vx: -sin * speed + (Math.random() - 0.5) * 2,
                    vy: cos * speed + (Math.random() - 0.5) * 2,
                    radius: Math.random() * 4 + 2,
                    color: Math.random() > 0.4 ? '#00f2fe' : (Math.random() > 0.5 ? '#f59e0b' : '#ffffff'),
                    life: 1.0,
                    decay: Math.random() * 0.05 + 0.03
                });
            }
        }

        // Left Engine (fires rightwards relative to lander)
        if (action === 1) {
            const nozzleX = cx + cos * 14 - sin * 4;
            const nozzleY = cy + sin * 14 + cos * 4;
            for (let i = 0; i < 2; i++) {
                this.particles.push({
                    x: nozzleX,
                    y: nozzleY,
                    vx: cos * 4 + Math.random() * 2,
                    vy: sin * 4 + (Math.random() - 0.5) * 2,
                    radius: Math.random() * 2.5 + 1.5,
                    color: '#38bdf8',
                    life: 1.0,
                    decay: 0.06
                });
            }
        }

        // Right Engine (fires leftwards relative to lander)
        if (action === 3) {
            const nozzleX = cx - cos * 14 - sin * 4;
            const nozzleY = cy - sin * 14 + cos * 4;
            for (let i = 0; i < 2; i++) {
                this.particles.push({
                    x: nozzleX,
                    y: nozzleY,
                    vx: -cos * 4 - Math.random() * 2,
                    vy: -sin * 4 + (Math.random() - 0.5) * 2,
                    radius: Math.random() * 2.5 + 1.5,
                    color: '#38bdf8',
                    life: 1.0,
                    decay: 0.06
                });
            }
        }
    }

    spawnFireworks(cx, cy) {
        const colors = ['#00f2fe', '#10b981', '#f59e0b', '#a855f7', '#ffffff'];
        for (let i = 0; i < 60; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 7 + 2;
            this.particles.push({
                x: cx,
                y: cy,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed - 2,
                radius: Math.random() * 3 + 2,
                color: colors[Math.floor(Math.random() * colors.length)],
                life: 1.0,
                decay: Math.random() * 0.02 + 0.015
            });
        }
    }

    spawnExplosion(cx, cy) {
        const colors = ['#ef4444', '#f97316', '#eab308', '#ffffff'];
        for (let i = 0; i < 40; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 5 + 1;
            this.particles.push({
                x: cx,
                y: cy,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: Math.random() * 4 + 2,
                color: colors[Math.floor(Math.random() * colors.length)],
                life: 1.0,
                decay: 0.03
            });
        }
    }

    resetTrail() {
        this.trail = [];
    }

    animate(timestamp) {
        const dt = (timestamp - this.lastTime) / 1000;
        this.lastTime = timestamp;

        this.render();
        requestAnimationFrame(this.animate);
    }

    render() {
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.width, this.height);

        // 1. Draw Space & Twinkling Stars
        this.drawBackground(ctx);

        // 2. Draw Lunar Surface & Landing Pad
        this.drawTerrain(ctx);

        // 3. Draw Trajectory Trail
        this.drawTrajectory(ctx);

        // 4. Draw Particles (Jet flames, fireworks)
        this.drawParticles(ctx);

        // 5. Draw Lander Spacecraft
        this.drawLander(ctx);

        // 6. Draw HUD Guidance & Vector
        this.drawHUD(ctx);
    }

    drawBackground(ctx) {
        // Space Gradient
        const grad = ctx.createLinearGradient(0, 0, 0, this.originY);
        grad.addColorStop(0, '#040711');
        grad.addColorStop(0.6, '#080f24');
        grad.addColorStop(1, '#0b1633');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, this.width, this.height);

        // Nebula Glow
        const nebula = ctx.createRadialGradient(this.width * 0.75, 100, 10, this.width * 0.75, 100, 250);
        nebula.addColorStop(0, 'rgba(168, 85, 247, 0.12)');
        nebula.addColorStop(0.5, 'rgba(56, 189, 248, 0.05)');
        nebula.addColorStop(1, 'transparent');
        ctx.fillStyle = nebula;
        ctx.fillRect(0, 0, this.width, this.height);

        // Stars
        for (let star of this.stars) {
            star.alpha += star.speed;
            const opacity = 0.3 + 0.7 * Math.abs(Math.sin(star.alpha));
            ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fill();
        }

        // Earth in distant background
        ctx.save();
        const earthGrad = ctx.createRadialGradient(90, 70, 5, 90, 70, 25);
        earthGrad.addColorStop(0, '#60a5fa');
        earthGrad.addColorStop(0.7, '#1e40af');
        earthGrad.addColorStop(1, '#0f172a');
        ctx.fillStyle = earthGrad;
        ctx.shadowColor = 'rgba(56, 189, 248, 0.6)';
        ctx.shadowBlur = 15;
        ctx.beginPath();
        ctx.arc(90, 70, 20, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    drawTerrain(ctx) {
        const gy = this.originY;

        // Lunar Ground Body
        ctx.fillStyle = '#1e293b';
        ctx.beginPath();
        ctx.moveTo(0, gy);
        // Stylized Moon Surface with subtle craters
        ctx.bezierCurveTo(this.width * 0.2, gy + 10, this.width * 0.3, gy - 8, this.originX - 70, gy);
        ctx.lineTo(this.originX + 70, gy);
        ctx.bezierCurveTo(this.width * 0.7, gy - 6, this.width * 0.85, gy + 12, this.width, gy);
        ctx.lineTo(this.width, this.height);
        ctx.lineTo(0, this.height);
        ctx.closePath();
        ctx.fill();

        // Terrain Edge Highlight
        ctx.strokeStyle = 'rgba(148, 163, 184, 0.4)';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Landing Pad Base (Centered between -0.2 and 0.2 in Gym coordinate, mapped to originX +/- 60)
        const padW = 100;
        const padX = this.originX - padW / 2;
        const padY = gy - 2;

        // Glowing Pad Surface
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(padX, padY, padW, 8);
        ctx.strokeStyle = '#00f2fe';
        ctx.lineWidth = 2;
        ctx.strokeRect(padX, padY, padW, 8);

        // Neon Yellow Hazard Stripes on Pad
        ctx.save();
        ctx.fillStyle = 'rgba(245, 158, 11, 0.7)';
        for (let i = 0; i < padW; i += 16) {
            ctx.beginPath();
            ctx.moveTo(padX + i, padY + 8);
            ctx.lineTo(padX + i + 8, padY);
            ctx.lineTo(padX + i + 12, padY);
            ctx.lineTo(padX + i + 4, padY + 8);
            ctx.closePath();
            ctx.fill();
        }
        ctx.restore();

        // Landing Zone Guide Beacon Flags
        this.drawBeacon(ctx, padX - 6, padY);
        this.drawBeacon(ctx, padX + padW + 6, padY);
    }

    drawBeacon(ctx, x, y) {
        ctx.save();
        // Flagpole
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y - 22);
        ctx.stroke();

        // Pulsing Neon Light on top
        const pulse = 0.5 + 0.5 * Math.sin(performance.now() * 0.006);
        ctx.fillStyle = '#00f2fe';
        ctx.shadowColor = '#00f2fe';
        ctx.shadowBlur = 10 * pulse;
        ctx.beginPath();
        ctx.arc(x, y - 22, 3.5, 0, Math.PI * 2);
        ctx.fill();

        // Neon Pennant Flag
        ctx.fillStyle = 'rgba(56, 189, 248, 0.8)';
        ctx.beginPath();
        ctx.moveTo(x, y - 20);
        ctx.lineTo(x + 12, y - 15);
        ctx.lineTo(x, y - 10);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }

    drawTrajectory(ctx) {
        if (this.trail.length < 2) return;

        ctx.save();
        ctx.lineWidth = 2.5;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        for (let i = 1; i < this.trail.length; i++) {
            const alpha = (i / this.trail.length) * 0.6;
            ctx.strokeStyle = `rgba(0, 242, 254, ${alpha})`;
            ctx.beginPath();
            ctx.moveTo(this.trail[i - 1].x, this.trail[i - 1].y);
            ctx.lineTo(this.trail[i].x, this.trail[i].y);
            ctx.stroke();
        }
        ctx.restore();
    }

    drawParticles(ctx) {
        ctx.save();
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;

            if (p.life <= 0) {
                this.particles.splice(i, 1);
                continue;
            }

            ctx.fillStyle = p.color;
            ctx.globalAlpha = Math.max(0, p.life);
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius * p.life, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.restore();
    }

    drawLander(ctx) {
        const { x, y, angle, left_leg, right_leg, action } = this.landerState;

        const cx = this.originX + x * this.scaleX;
        const cy = this.originY - y * this.scaleY;

        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(-angle); // Gymnasium angles: clockwise is negative in Box2D, standard canvas is opposite

        // ========================
        // 1. Landing Legs & Shock Absorbers
        // ========================
        // Left Leg
        ctx.strokeStyle = left_leg ? '#10b981' : '#94a3b8';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(-10, 10);
        ctx.lineTo(-20, 22);
        ctx.lineTo(-24, 22); // Footpad
        ctx.stroke();

        // Left Footpad Sensor Glow
        if (left_leg) {
            ctx.fillStyle = '#10b981';
            ctx.shadowColor = '#10b981';
            ctx.shadowBlur = 8;
            ctx.fillRect(-26, 21, 5, 3);
            ctx.shadowBlur = 0;
        }

        // Right Leg
        ctx.strokeStyle = right_leg ? '#10b981' : '#94a3b8';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(10, 10);
        ctx.lineTo(20, 22);
        ctx.lineTo(24, 22); // Footpad
        ctx.stroke();

        // Right Footpad Sensor Glow
        if (right_leg) {
            ctx.fillStyle = '#10b981';
            ctx.shadowColor = '#10b981';
            ctx.shadowBlur = 8;
            ctx.fillRect(21, 21, 5, 3);
            ctx.shadowBlur = 0;
        }

        // ========================
        // 2. Main Engine Thruster Nozzle
        // ========================
        ctx.fillStyle = '#475569';
        ctx.beginPath();
        ctx.moveTo(-6, 12);
        ctx.lineTo(6, 12);
        ctx.lineTo(8, 18);
        ctx.lineTo(-8, 18);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 1;
        ctx.stroke();

        // ========================
        // 3. Lower Stage Body (Gold Foil Thermal Shield)
        // ========================
        const goldGrad = ctx.createLinearGradient(-14, 0, 14, 12);
        goldGrad.addColorStop(0, '#f59e0b');
        goldGrad.addColorStop(0.5, '#fbbf24');
        goldGrad.addColorStop(1, '#b45309');
        ctx.fillStyle = goldGrad;
        ctx.beginPath();
        ctx.roundRect(-14, 0, 28, 12, 3);
        ctx.fill();
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 1;
        ctx.stroke();

        // ========================
        // 4. Upper Stage Command Module (Titanium Hex Capsule)
        // ========================
        const bodyGrad = ctx.createLinearGradient(-16, -18, 16, 0);
        bodyGrad.addColorStop(0, '#f8fafc');
        bodyGrad.addColorStop(0.6, '#cbd5e1');
        bodyGrad.addColorStop(1, '#94a3b8');
        ctx.fillStyle = bodyGrad;
        ctx.beginPath();
        ctx.moveTo(0, -18);
        ctx.lineTo(14, -6);
        ctx.lineTo(14, 2);
        ctx.lineTo(-14, 2);
        ctx.lineTo(-14, -6);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Blue Cybernetic Cockpit Visor
        ctx.fillStyle = '#0284c7';
        ctx.shadowColor = '#00f2fe';
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(0, -7, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        // Visor Glare
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(-1.5, -8.5, 1.8, 0, Math.PI * 2);
        ctx.fill();

        // ========================
        // 5. RCS Side Thruster Pods
        // ========================
        ctx.fillStyle = '#334155';
        ctx.fillRect(-17, -4, 3, 6);
        ctx.fillRect(14, -4, 3, 6);

        // ========================
        // 6. Thrust Flame Effects on Lander
        // ========================
        if (action === 2) {
            // Main Flame Core
            ctx.save();
            const flameGrad = ctx.createLinearGradient(0, 18, 0, 36);
            flameGrad.addColorStop(0, '#ffffff');
            flameGrad.addColorStop(0.3, '#00f2fe');
            flameGrad.addColorStop(0.7, '#f59e0b');
            flameGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = flameGrad;
            ctx.shadowColor = '#00f2fe';
            ctx.shadowBlur = 15;

            const flameLen = 18 + Math.random() * 8;
            ctx.beginPath();
            ctx.moveTo(-6, 18);
            ctx.lineTo(6, 18);
            ctx.lineTo(0, 18 + flameLen);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }

        ctx.restore();
    }

    drawHUD(ctx) {
        const { x, y, vx, vy, angle } = this.landerState;
        const cx = this.originX + x * this.scaleX;
        const cy = this.originY - y * this.scaleY;

        ctx.save();
        // Target Alignment Crosshair Line down to Pad
        if (y > 0.1) {
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
            ctx.setLineDash([4, 4]);
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(cx, cy + 25);
            ctx.lineTo(cx, this.originY);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // Velocity Vector Arrow
        if (Math.hypot(vx, vy) > 0.05) {
            ctx.strokeStyle = 'rgba(245, 158, 11, 0.8)';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + vx * 60, cy - vy * 60);
            ctx.stroke();

            // Arrow head
            const arrowAngle = Math.atan2(-vy, vx);
            const headLen = 6;
            ctx.fillStyle = 'rgba(245, 158, 11, 0.8)';
            ctx.beginPath();
            ctx.moveTo(cx + vx * 60, cy - vy * 60);
            ctx.lineTo(
                cx + vx * 60 - headLen * Math.cos(arrowAngle - Math.PI / 6),
                cy - vy * 60 - headLen * Math.sin(arrowAngle - Math.PI / 6)
            );
            ctx.lineTo(
                cx + vx * 60 - headLen * Math.cos(arrowAngle + Math.PI / 6),
                cy - vy * 60 - headLen * Math.sin(arrowAngle + Math.PI / 6)
            );
            ctx.closePath();
            ctx.fill();
        }

        ctx.restore();
    }
}

window.LanderRenderer = LanderRenderer;
