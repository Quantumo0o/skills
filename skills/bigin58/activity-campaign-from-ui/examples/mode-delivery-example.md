# Mode example — delivery

## User input
The user sends one campaign reference and asks:

> 我只要前端 starter 代码，固定 H5 / Web，技术栈 HTML + CSS + JS。走 delivery mode。

## Expected response shape

### Mode
delivery

### Delivery notes
- keep the implementation H5/Web only
- use HTML + CSS + JavaScript only
- output a visual-first high-fidelity draft, not a bare wireframe
- do not claim pixel-perfect recovery from the screenshot
- summarize the likely visual language before code

### File structure
- `index.html`
- `styles.css`
- `main.js`
- `mock-data.js`

### Visual extraction summary
- warm festive palette with red, gold, and cream contrast
- tall hero with layered title art and floating reward ornaments
- modules feel like decorated panels, not plain white cards
- CTA area is loud and centered, with glow and badge support
- progress and reward zones use chips, medals, and framed items
- popup style should feel celebratory and branded

### index.html
```html
<div class="page-shell">
  <div class="page-bg-glow page-bg-glow-left"></div>
  <div class="page-bg-glow page-bg-glow-right"></div>

  <main class="festival-page">
    <section id="hero" class="hero-banner">
      <div class="hero-spark hero-spark-left"></div>
      <div class="hero-spark hero-spark-right"></div>
      <div class="hero-copy">
        <p class="hero-badge">限时挑战季</p>
        <h1 class="hero-title">福气冲榜赛</h1>
        <p class="hero-subtitle">做任务攒福气值，解锁阶梯好礼与终极抽奖机会</p>
        <div class="hero-meta">
          <span class="meta-pill">03.20 - 04.05</span>
          <span class="meta-pill">每日 10:00 刷新</span>
        </div>
      </div>
      <div class="hero-prize-card">
        <span class="prize-card-label">今日最高奖</span>
        <strong class="prize-card-value">188 元礼包</strong>
        <button class="hero-main-cta js-open-popup" data-popup="rewardResultPopup">立即冲榜</button>
      </div>
    </section>

    <section id="progress-strip" class="feature-panel progress-panel"></section>
    <section id="task-list" class="feature-panel task-panel"></section>
    <section id="reward-zone" class="feature-panel reward-panel"></section>
    <section id="reward-pool" class="feature-panel pool-panel"></section>
    <section id="rules" class="feature-panel rules-panel"></section>
  </main>
</div>

<div id="popup-root"></div>
```

### styles.css
```css
:root {
  --bg-top: #7d1018;
  --bg-bottom: #c63a2d;
  --panel-fill: linear-gradient(180deg, #fff7df 0%, #ffe8bb 100%);
  --panel-stroke: rgba(255, 245, 205, 0.8);
  --text-strong: #72140d;
  --text-soft: #9a3d22;
  --gold: #ffd46a;
  --gold-deep: #ffad2e;
  --shadow-panel: 0 18px 40px rgba(102, 12, 8, 0.22);
  --shadow-cta: 0 10px 24px rgba(171, 42, 0, 0.35);
  --radius-xl: 28px;
  --radius-lg: 22px;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  color: var(--text-strong);
  background:
    radial-gradient(circle at top, rgba(255, 226, 135, 0.28), transparent 28%),
    linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 42%, #f25c38 100%);
}

.page-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.festival-page {
  position: relative;
  z-index: 1;
  max-width: 750px;
  margin: 0 auto;
  padding: 20px 16px 36px;
}

.hero-banner,
.feature-panel {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-xl);
  border: 1px solid var(--panel-stroke);
  box-shadow: var(--shadow-panel);
}

.hero-banner {
  display: grid;
  grid-template-columns: 1.3fr 0.9fr;
  gap: 16px;
  padding: 26px 22px 22px;
  margin-bottom: 16px;
  background:
    radial-gradient(circle at top, rgba(255, 235, 159, 0.78), transparent 34%),
    linear-gradient(145deg, #a91516 0%, #d73e2f 46%, #ff874f 100%);
  color: #fff8ea;
}

.hero-title {
  margin: 8px 0;
  font-size: 42px;
  line-height: 1.05;
  letter-spacing: 2px;
}

.hero-badge,
.meta-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
}

.hero-badge {
  padding: 6px 14px;
  background: rgba(255, 243, 200, 0.18);
  border: 1px solid rgba(255, 244, 213, 0.36);
}

.meta-pill {
  margin: 10px 10px 0 0;
  padding: 6px 12px;
  background: rgba(93, 0, 0, 0.22);
}

.hero-prize-card,
.feature-panel {
  background: var(--panel-fill);
}

.hero-prize-card {
  align-self: end;
  padding: 18px;
  border-radius: var(--radius-lg);
  color: var(--text-strong);
}

.hero-main-cta {
  width: 100%;
  height: 48px;
  margin-top: 14px;
  border: 0;
  border-radius: 999px;
  font-size: 16px;
  font-weight: 700;
  color: #7c1a08;
  background: linear-gradient(180deg, #ffe59a 0%, #ffbc46 100%);
  box-shadow: var(--shadow-cta);
}

.feature-panel {
  padding: 18px;
  margin-bottom: 14px;
}

.popup-mask {
  position: fixed;
  inset: 0;
  display: none;
  place-items: center;
  padding: 24px;
  background: rgba(53, 6, 2, 0.62);
}

.popup-mask.is-open { display: grid; }
```

### main.js
```javascript
document.addEventListener('DOMContentLoaded', function () {
  renderPage(window.campaignData);
  bindEvents();
});

function renderPage(data) {
  document.getElementById('progress-strip').innerHTML = renderProgress(data.progress);
  document.getElementById('task-list').innerHTML = renderTasks(data.tasks);
  document.getElementById('reward-zone').innerHTML = renderRewards(data.featuredRewards);
  document.getElementById('reward-pool').innerHTML = renderPrizePool(data.prizePool);
  document.getElementById('rules').innerHTML = renderRules(data.rules);
}

function renderProgress(progress) {
  return [
    '<div class="panel-head"><h2>福气进度</h2><span>已积累 ' + progress.total + ' 点</span></div>',
    '<div class="progress-track">',
    progress.nodes.map(function (item) {
      return '<div class="progress-node' + (item.active ? ' is-active' : '') + '">' +
        '<span class="progress-node-value">' + item.value + '</span>' +
        '<span class="progress-node-label">' + item.label + '</span>' +
      '</div>';
    }).join(''),
    '</div>'
  ].join('');
}

function renderTasks(tasks) {
  return tasks.map(function (task) {
    return '<article class="task-card">' +
      '<div><p class="task-tag">' + task.tag + '</p><h3>' + task.title + '</h3><p>' + task.desc + '</p></div>' +
      '<button class="task-cta">' + task.ctaText + '</button>' +
    '</article>';
  }).join('');
}

function renderRewards(rewards) {
  return rewards.map(function (reward) {
    return '<article class="reward-card">' +
      '<span class="reward-card-top">' + reward.badge + '</span>' +
      '<strong>' + reward.title + '</strong>' +
      '<p>' + reward.desc + '</p>' +
    '</article>';
  }).join('');
}

function renderPrizePool(prizePool) {
  return '<div class="panel-head"><h2>奖池一览</h2><span>' + prizePool.tip + '</span></div>' +
    '<div class="prize-grid">' + prizePool.items.map(function (item) {
      return '<div class="prize-chip"><span>' + item.name + '</span><b>' + item.stock + '</b></div>';
    }).join('') + '</div>';
}

function renderRules(rules) {
  return '<div class="panel-head"><h2>活动说明</h2></div><ol class="rules-list">' +
    rules.map(function (rule) {
      return '<li>' + rule + '</li>';
    }).join('') +
  '</ol>';
}

function bindEvents() {
  document.querySelector('.festival-page').addEventListener('click', function (event) {
    var trigger = event.target.closest('.js-open-popup');
    if (!trigger) {
      return;
    }

    openPopup(trigger.getAttribute('data-popup'));
  });
}

function openPopup(id) {
  var popup = window.campaignData.popups.filter(function (item) {
    return item.id === id;
  })[0];

  document.getElementById('popup-root').innerHTML =
    '<div class="popup-mask is-open">' +
      '<div class="reward-popup">' +
        '<p class="popup-kicker">' + popup.kicker + '</p>' +
        '<h3>' + popup.title + '</h3>' +
        '<p>' + popup.desc + '</p>' +
      '</div>' +
    '</div>';
}
```

### mock-data.js
```javascript
window.campaignData = {
  progress: {
    total: 68,
    nodes: [
      { value: '20', label: '解锁红包雨', active: true },
      { value: '50', label: '解锁大奖池', active: true },
      { value: '88', label: '解锁终极抽奖', active: false }
    ]
  },
  tasks: [
    { tag: '每日任务', title: '浏览主会场 30 秒', desc: '完成后可获得 12 点福气值', ctaText: '去完成' },
    { tag: '加速任务', title: '邀请好友助力 1 次', desc: '完成后可额外获得 20 点福气值', ctaText: '去邀请' }
  ],
  featuredRewards: [
    { badge: '阶梯礼 01', title: '品牌券包', desc: '满 99 可用的组合优惠券' },
    { badge: '阶梯礼 02', title: '抽奖加码卡', desc: '终极抽奖额外 +1 次机会' }
  ],
  prizePool: {
    tip: '每晚 20:00 更新剩余库存',
    items: [
      { name: '188 元礼包', stock: 'x12' },
      { name: '免单券', stock: 'x48' },
      { name: '加速卡', stock: 'x188' }
    ]
  },
  rules: [
    '活动期间每日任务可重复完成一次，奖励次日刷新。',
    '阶段奖励达到对应福气值后可领取，过期不补发。'
  ],
  popups: [
    {
      id: 'rewardResultPopup',
      kicker: '恭喜解锁',
      title: '你获得 1 次终极抽奖加码机会',
      desc: '继续完成任务，点亮全部进度节点。'
    }
  ]
};
```

## What this mode should not do
- do not switch to Vue, React, or Uni-app
- do not add backend integration claims
- do not collapse into neutral white-card scaffolding
- do not generate a full new campaign strategy unless requested elsewhere
