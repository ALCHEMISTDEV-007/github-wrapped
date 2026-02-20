document.addEventListener("DOMContentLoaded", () => {
    // 1. Get Data from URL
    const urlParams = new URLSearchParams(window.location.search);
    const dataParam = urlParams.get('data');

    if (!dataParam) {
        document.body.innerHTML = "<h2 style='text-align:center; margin-top: 50vh;'>No data provided. Please start from the homepage.</h2>";
        return;
    }

    let userData;
    try {
        userData = JSON.parse(decodeURIComponent(dataParam));
    } catch (e) {
        console.error("Error parsing user data:", e);
        return;
    }

    // 2. Loading Animation
    const progressBar = document.querySelector('.progress-bar');
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress >= 100) {
            progress = 100;
            progressBar.style.width = `${progress}%`;
            clearInterval(interval);
            setTimeout(() => {
                document.getElementById('loading-screen').classList.add('hidden');
                document.getElementById('app').classList.remove('hidden');
                initApp(userData);
            }, 600);
        } else {
            progressBar.style.width = `${progress}%`;
        }
    }, 200);

    // 3. Slideshow Logic
    let currentSlide = 0;
    const numSlides = 5;
    let autoAdvanceTimer;

    function initApp(data) {
        // --- Populate Data ---

        // Welcome
        document.getElementById('user-avatar').src = data.avatar_url;
        document.getElementById('user-name').innerText = data.username;

        // Stats
        animateValue("total-commits", 0, data.wrapped.stats.total_commits, 1500);
        animateValue("active-days", 0, data.wrapped.stats.active_days, 1500);
        animateValue("longest-streak", 0, data.wrapped.stats.longest_streak, 1500);

        // Repos
        const reposList = document.getElementById('top-repos-list');
        reposList.innerHTML = '';
        if (data.wrapped.top_repos.length === 0) {
            reposList.innerHTML = '<p>No repositories found. Time to start building!</p>';
        } else {
            data.wrapped.top_repos.forEach((repo, index) => {
                const delay = index * 0.2;
                reposList.innerHTML += `
                    <div class="repo-item" style="animation-delay: ${delay}s">
                        <div class="repo-info">
                            <h3>${repo.name}</h3>
                            <p>${repo.language || 'Unknown'} · Popular repo</p>
                        </div>
                        <div class="repo-stats">
                            ⭐ ${repo.stars}
                        </div>
                    </div>
                `;
            });
        }

        // Languages
        const langs = data.wrapped.languages;
        const legendContainer = document.getElementById('lang-legend');
        const pieChart = document.getElementById('pie-chart');

        if (Object.keys(langs).length === 0) {
            pieChart.style.background = '#333';
            legendContainer.innerHTML = '<p>No languages detected.</p>';
            document.getElementById('lang-flavor-text').innerText = "A blank canvas. What will you create?";
        } else {
            const colors = ['var(--accent-1)', 'var(--accent-2)', 'var(--accent-3)', '#FFaa00', '#00ffaa'];
            let conicData = [];
            let currentTemp = 0;
            let i = 0;
            legendContainer.innerHTML = '';

            for (const [lang, perc] of Object.entries(langs)) {
                if (i >= 5) break;
                const color = colors[i % colors.length];
                conicData.push(`${color} ${currentTemp}% ${currentTemp + perc}%`);
                currentTemp += perc;

                legendContainer.innerHTML += `
                    <div class="legend-item">
                        <div class="legend-color" style="background: ${color}"></div>
                        <span><strong>${lang}</strong>: ${perc}%</span>
                    </div>
                `;
                i++;
            }
            pieChart.style.background = `conic-gradient(${conicData.join(', ')})`;

            // Flavor text
            const topLang = Object.keys(langs)[0];
            const flavorTexts = {
                "Python": "You followed the trend of ML... still never forgot your roots. 🐍",
                "JavaScript": "The web is your canvas. 🎨",
                "TypeScript": "A lover of types and order. 📐",
                "Java": "Write once, run anywhere. The classic enterprise builder. ☕",
                "C++": "Close to the metal. Maximum performance! 🏎️",
                "Rust": "Safety first, zero cost abstractions. 🦀",
                "Go": "Concurrency is the way. 🦦",
                "HTML": "The architect of the web. 🏗️",
                "CSS": "Making the web beautiful, one pixel at a time. ✨"
            };
            document.getElementById('lang-flavor-text').innerText = flavorTexts[topLang] || `A maestro of ${topLang}. Keep coding!`;
        }

        // Personality
        const pers = data.wrapped.personality;
        document.getElementById('personality-rarity').innerText = pers.rarity;
        document.getElementById('personality-title').innerText = pers.title;
        document.getElementById('personality-desc').innerText = pers.desc;

        const rarityColors = {
            "Common": "#A0A0B0",
            "Rare": "#00F0FF",
            "Epic": "#8A2BE2",
            "Legendary": "#FFaa00",
            "Mythic": "#FF3B7C"
        };
        document.getElementById('personality-rarity').style.backgroundColor = rarityColors[pers.rarity] || "var(--accent-2)";
        document.getElementById('personality-rarity').style.boxShadow = `0 0 15px ${rarityColors[pers.rarity] || "var(--accent-2)"}`;

        // Generate Random Image for Personality
        const imgElement = document.getElementById('personality-image');
        const loaderElement = document.getElementById('image-loader');

        // Using a random image service with a seed based on username and personality
        // to ensure the same user gets the same art for their specific wrapped
        const seed = `${data.username}-${pers.title.replace(/\s+/g, '')}`;
        const randomImageUrl = `https://picsum.photos/seed/${seed}/800/400?blur=2`;

        imgElement.onload = () => {
            loaderElement.classList.add('hidden');
            imgElement.classList.remove('hidden');
        };
        imgElement.onerror = () => {
            loaderElement.classList.add('hidden');
            // fallback color if image fails
            imgElement.parentElement.style.background = `linear-gradient(45deg, var(--bg-color-main), ${rarityColors[pers.rarity] || "var(--accent-2)"})`;
        };
        imgElement.src = randomImageUrl;


        // --- Slideshow Setup ---
        const indicatorsContainer = document.getElementById('progress-indicators');
        for (let i = 0; i < numSlides; i++) {
            indicatorsContainer.innerHTML += `<div class="progress-segment"><div class="fill"></div></div>`;
        }

        showSlide(0);

        document.getElementById('next-btn').addEventListener('click', () => changeSlide(1));
        document.getElementById('prev-btn').addEventListener('click', () => changeSlide(-1));
    }

    function showSlide(index) {
        if (index < 0 || index >= numSlides) return;

        currentSlide = index;

        // Update Slides UI
        document.querySelectorAll('.slide').forEach((slide, i) => {
            if (i === currentSlide) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });

        // Update Indicators UI
        const segments = document.querySelectorAll('.progress-segment');
        segments.forEach((seg, i) => {
            const fill = seg.querySelector('.fill');
            fill.style.transition = 'none'; // reset transition

            if (i < currentSlide) {
                seg.classList.add('completed');
                fill.style.width = '100%';
            } else if (i === currentSlide) {
                seg.classList.remove('completed');
                fill.style.width = '0%';

                // Start filling the current one
                setTimeout(() => {
                    fill.style.transition = 'width 6s linear';
                    fill.style.width = '100%';
                }, 50);

            } else {
                seg.classList.remove('completed');
                fill.style.width = '0%';
            }
        });

        // Auto advance
        clearTimeout(autoAdvanceTimer);
        if (currentSlide < numSlides - 1) {
            autoAdvanceTimer = setTimeout(() => {
                changeSlide(1);
            }, 6000);
        }
    }

    function changeSlide(direction) {
        let newIndex = currentSlide + direction;
        if (newIndex >= 0 && newIndex < numSlides) {
            showSlide(newIndex);
        }
    }

    // Number Counter Animation
    function animateValue(id, start, end, duration) {
        if (!end || end === 0) {
            document.getElementById(id).innerHTML = 0;
            return;
        }
        if (start === end) {
            document.getElementById(id).innerHTML = end;
            return;
        }
        let range = end - start;
        let current = start;
        let increment = Math.max(1, Math.floor(range / (duration / 30)));
        let obj = document.getElementById(id);

        let timer = setInterval(function () {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            obj.innerHTML = current;
        }, 30);
    }

    // Web Share API Implementation
    document.getElementById('btn-share')?.addEventListener('click', async () => {
        const shareData = {
            title: 'My GitHub Wrapped 2026',
            text: `I'm a ${userData.wrapped.personality.title}! I made ${userData.wrapped.stats.total_commits} commits across ${userData.wrapped.stats.active_days} active days this year. Generate your own GitHub Wrapped!`,
            url: window.location.origin
        };

        try {
            if (navigator.share && navigator.canShare(shareData)) {
                await navigator.share(shareData);
            } else {
                // Fallback to clipboard
                await navigator.clipboard.writeText(`${shareData.text} ${shareData.url}`);
                const btn = document.getElementById('btn-share');
                const originalText = btn.innerHTML;
                btn.innerHTML = 'Copied to clipboard! ✓';
                setTimeout(() => { btn.innerHTML = originalText; }, 2000);
            }
        } catch (err) {
            console.error('Error sharing:', err);
        }
    });

    // html2canvas Download Implementation
    document.getElementById('btn-download')?.addEventListener('click', () => {
        const cardElement = document.getElementById('personality-card');
        const btn = document.getElementById('btn-download');
        const originalText = btn.innerHTML;

        btn.innerHTML = 'Generating... ⏳';
        btn.disabled = true;

        // Temporarily adjust styles for better capture if needed
        const prevTransform = cardElement.style.transform;
        cardElement.style.transform = 'none';

        html2canvas(cardElement, {
            backgroundColor: '#0B0B0E', // Match theme background
            scale: 2, // High resolution
            useCORS: true, // Allow external images (like the generated art)
            logging: false
        }).then(canvas => {
            // Restore styles
            cardElement.style.transform = prevTransform;

            // Trigger download
            const image = canvas.toDataURL("image/png", 1.0);
            const link = document.createElement('a');
            link.download = `${userData.username}-github-wrapped-2026.png`;
            link.href = image;
            link.click();

            btn.innerHTML = 'Saved! ✓';
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 2000);
        }).catch(err => {
            console.error('Error generating card image:', err);
            btn.innerHTML = 'Error ❌';
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 2000);
        });
    });
});
