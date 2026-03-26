# Mode example — full

## User input
The user sends 3 campaign references and asks:

> 参考这 3 个活动页，先分析共性，再给我出一个新的 H5 活动方案，最后补一套 HTML + CSS + JS 的 starter 代码。走 full mode。

## Expected response shape

### Mode
full

## 1. Reference analysis
### Observed
- all references are mobile-first campaign pages
- each page uses a strong hero section near the top
- a reward promise appears before the detailed rules
- task completion is tied to a visible reward action
- popup-based feedback is strongly implied

### Inferred
- the campaign is designed for repeat daily participation
- the main business goal is likely short-term activation
- reward exposure is used as the primary motivation trigger

### Assumed
- exact microcopy and reward probabilities are not fully readable
- hidden states such as “already claimed” or “chance exhausted” are likely present but not fully visible

## 2. Gameplay abstraction
Shared pattern:
1. attract attention with hero and date range
2. expose reward value early
3. drive task completion
4. convert task progress into chances, points, or unlock states
5. reveal result feedback through popups

## 3. New campaign proposal
### Name
Spring Route Challenge

### Goal
Increase repeat visits and task completion during a short seasonal campaign window.

### Main idea
Instead of repeating a direct lucky-draw page, this proposal changes:
- the theme: from generic festive draw to route-based progress challenge
- the reward design: from flat prize display to staged checkpoint rewards plus a final draw
- the task structure: from independent tasks to daily progress tasks
- the main interaction: users unlock reward checkpoints before reaching the final action area

### Participation path
Enter page → complete daily tasks → unlock route checkpoints → claim checkpoint rewards → use final draw chances

### Anti-copy note
This proposal changes at least 2 required dimensions:
- reward mechanism
- task structure
- core interaction path

## 4. Page architecture
### Modules
1. hero banner
2. campaign meta bar
3. progress route strip
4. daily task list
5. checkpoint reward area
6. final draw area
7. reward pool
8. rules section
9. record entry

### Popups
- rule popup
- checkpoint unlocked popup
- reward result popup
- insufficient chance popup

### State flow
`init -> taskUpdated -> routeProgressed -> checkpointUnlocked -> chanceReady -> drawing -> resultShown`

### Tracking suggestions
- hero_cta_click
- task_action_click
- checkpoint_claim_click
- draw_start_click
- draw_result_view

## 5. Delivery schema
The schema should cover both campaign config and delivery structure.

### Suggested schema sections
- `campaignMeta`
- `hero`
- `progressRoute`
- `tasks`
- `checkpointRewards`
- `lottery`
- `modules`
- `popups`
- `stateMachine`
- `tracking`

## 6. Visual direction
- dominant palette: cherry red, amber gold, warm cream
- page mood: festive, busy, rewarding, glossy
- hero composition: large title art + highlight prize block + floating ornaments
- module treatment: decorated panels with stronger top headers and contrast separators
- CTA language: loud, central, badge-supported
- popup style: branded celebration layer instead of neutral modal

## 7. H5/Web high-fidelity draft files
### File structure
- `index.html`
- `styles.css`
- `main.js`
- `mock-data.js`

### index.html
```html
<div class="route-page">
  <div class="route-page-glow route-page-glow-top"></div>
  <main class="route-shell">
    <section id="hero" class="route-hero">
      <div class="route-hero-copy">
        <span class="hero-pill">春日限定玩法</span>
        <h1 class="route-title">春日闯关大道</h1>
        <p class="route-subtitle">完成每日任务点亮路标，开出阶段宝箱并冲刺终点大奖</p>
        <div class="route-meta">
          <span>活动时间 02.01 - 02.14</span>
          <span>累计完成越多，奖励越高</span>
        </div>
      </div>
      <aside class="hero-side-card">
        <p>终点大奖</p>
        <strong>锦鲤礼包 x 1</strong>
        <button class="hero-side-cta js-start-draw">冲刺终点</button>
      </aside>
    </section>

    <section id="progress-route" class="route-panel"></section>
    <section id="task-list" class="route-panel"></section>
    <section id="checkpoint-rewards" class="route-panel"></section>
    <section id="draw-zone" class="route-panel highlight-panel"></section>
    <section id="reward-pool" class="route-panel"></section>
    <section id="rules" class="route-panel"></section>
  </main>
</div>

<div id="popup-root"></div>
```

### styles.css
```css
:root {
  --route-bg: #9f1420;
  --route-bg-deep: #5d0912;
  --route-panel: linear-gradient(180deg, #fff7e4 0%, #ffe4a8 100%);
  --route-stroke: rgba(255, 242, 196, 0.9);
  --route-title: #74130f;
  --route-copy: #984021;
}

body {
  margin: 0;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  background:
    radial-gradient(circle at top, rgba(255, 218, 130, 0.28), transparent 26%),
    linear-gradient(180deg, var(--route-bg-deep) 0%, var(--route-bg) 42%, #db4b34 100%);
}

.route-shell {
  max-width: 750px;
  margin: 0 auto;
  padding: 18px 16px 34px;
}

.route-hero,
.route-panel {
  position: relative;
  overflow: hidden;
  border-radius: 28px;
  border: 1px solid var(--route-stroke);
  box-shadow: 0 18px 40px rgba(78, 10, 11, 0.22);
}

.route-hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
  padding: 24px;
  margin-bottom: 16px;
  color: #fff8eb;
  background:
    radial-gradient(circle at top right, rgba(255, 244, 199, 0.42), transparent 26%),
    linear-gradient(140deg, #8f0f17 0%, #d33730 52%, #ff8a47 100%);
}

.route-title {
  margin: 10px 0 8px;
  font-size: 40px;
  line-height: 1.05;
}

.hero-pill,
.route-meta span {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
}

.hero-pill {
  padding: 6px 12px;
  background: rgba(255, 248, 221, 0.18);
  border: 1px solid rgba(255, 248, 221, 0.34);
}

.route-meta span {
  margin: 12px 10px 0 0;
  padding: 6px 12px;
  background: rgba(94, 5, 0, 0.24);
}

.hero-side-card,
.route-panel {
  background: var(--route-panel);
  color: var(--route-title);
}

.hero-side-card {
  align-self: end;
  padding: 18px;
  border-radius: 22px;
}

.hero-side-cta {
  width: 100%;
  height: 48px;
  border: 0;
  border-radius: 999px;
  font-weight: 700;
  color: #7a180a;
  background: linear-gradient(180deg, #ffe082 0%, #ffb533 100%);
}

.route-panel {
  padding: 18px;
  margin-bottom: 14px;
}

.highlight-panel {
  background:
    radial-gradient(circle at top, rgba(255, 243, 189, 0.72), transparent 38%),
    linear-gradient(180deg, #fff3c4 0%, #ffd778 100%);
}
```

### main.js
```javascript
document.addEventListener('DOMContentLoaded', function () {
  renderPage(window.campaignData);
  bindEvents();
});

function renderPage(data) {
  document.getElementById('progress-route').innerHTML = renderRoute(data.progressRoute);
  document.getElementById('task-list').innerHTML = renderTasks(data.tasks);
  document.getElementById('checkpoint-rewards').innerHTML = renderCheckpoints(data.checkpointRewards);
  document.getElementById('draw-zone').innerHTML = renderDrawZone(data.lottery);
  document.getElementById('reward-pool').innerHTML = renderRewardPool(data.rewardPool);
  document.getElementById('rules').innerHTML = renderRules(data.rules);
}

function renderRoute(route) {
  return '<div class="panel-title"><h2>闯关进度</h2><span>' + route.tip + '</span></div><div class="route-track">' +
    route.steps.map(function (item) {
      return '<div class="route-step' + (item.done ? ' is-done' : '') + '">' +
        '<b>' + item.label + '</b><span>' + item.note + '</span>' +
      '</div>';
    }).join('') +
  '</div>';
}

function renderTasks(tasks) {
  return tasks.map(function (task) {
    return '<article class="task-item">' +
      '<div><p class="task-type">' + task.type + '</p><h3>' + task.title + '</h3><p>' + task.benefit + '</p></div>' +
      '<button class="js-task-action" data-id="' + task.id + '">' + task.ctaText + '</button>' +
    '</article>';
  }).join('');
}

function renderCheckpoints(checkpoints) {
  return checkpoints.map(function (item) {
    return '<article class="checkpoint-card">' +
      '<span class="checkpoint-index">' + item.index + '</span>' +
      '<strong>' + item.title + '</strong>' +
      '<p>' + item.desc + '</p>' +
      '<span class="checkpoint-status">' + item.statusText + '</span>' +
    '</article>';
  }).join('');
}

function renderDrawZone(lottery) {
  return '<div class="panel-title"><h2>终点抽奖</h2><span>' + lottery.tip + '</span></div>' +
    '<div class="draw-stage"><strong>' + lottery.chanceText + '</strong><button class="draw-button js-start-draw">' + lottery.ctaText + '</button></div>';
}

function renderRewardPool(rewardPool) {
  return '<div class="panel-title"><h2>奖池展示</h2></div><div class="reward-pool-grid">' +
    rewardPool.map(function (item) {
      return '<div class="reward-pool-card"><span>' + item.tag + '</span><strong>' + item.name + '</strong></div>';
    }).join('') +
  '</div>';
}

function renderRules(rules) {
  return '<div class="panel-title"><h2>活动规则</h2></div><ol class="rule-list">' +
    rules.map(function (rule) {
      return '<li>' + rule + '</li>';
    }).join('') +
  '</ol>';
}

function bindEvents() {
  document.getElementById('draw-zone').addEventListener('click', function (event) {
    if (!event.target.closest('.js-start-draw')) {
      return;
    }

    openPopup('rewardResultPopup');
  });
}

function openPopup(id) {
  var popup = window.campaignData.popups.filter(function (item) {
    return item.id === id;
  })[0];

  document.getElementById('popup-root').innerHTML =
    '<div class="popup-mask is-open"><div class="route-popup"><p>' + popup.kicker + '</p><h3>' +
    popup.title + '</h3><span>' + popup.desc + '</span></div></div>';
}
```

### mock-data.js
```javascript
window.campaignData = {
  progressRoute: {
    tip: '再完成 1 个任务即可点亮下一路标',
    steps: [
      { id: 'step-1', label: '签到站', note: '已完成', done: true },
      { id: 'step-2', label: '助力站', note: '进行中', done: true },
      { id: 'step-3', label: '终点站', note: '待点亮', done: false }
    ]
  },
  tasks: [
    { id: 'daily-checkin', type: '每日任务', title: '每日签到', benefit: '完成后获得 10 点路程值', ctaText: '立即签到' },
    { id: 'share-campaign', type: '加速任务', title: '邀请好友助力', benefit: '完成后额外获得 20 点路程值', ctaText: '去邀请' }
  ],
  checkpointRewards: [
    { index: '01', title: '启程礼盒', desc: '解锁即得通用优惠券包', statusText: '已解锁' },
    { index: '02', title: '冲刺加速卡', desc: '终极抽奖次数 +1', statusText: '即将解锁' }
  ],
  lottery: {
    tip: '终点点亮后可参与 1 次',
    chanceText: '当前抽奖机会 1 次',
    ctaText: '立即抽奖'
  },
  rewardPool: [
    { tag: '终点大奖', name: '锦鲤礼包' },
    { tag: '惊喜奖', name: '品牌周边' },
    { tag: '加码奖', name: '满减券包' }
  ],
  rules: [
    '每日任务每天限完成一次，次日 00:00 刷新。',
    '终点大奖数量有限，先到先得。'
  ],
  popups: [
    {
      id: 'rewardResultPopup',
      kicker: '恭喜到站',
      title: '你抽中了终点加码礼',
      desc: '奖励已发放至账户，请前往“我的奖品”查看。'
    }
  ]
};
```

## What this mode should not do
- do not switch to other frameworks
- do not claim backend APIs that were never provided
- do not pretend the screenshot guarantees exact text, sizes, or hidden states
- do not reduce the delivery to empty containers and generic white cards
