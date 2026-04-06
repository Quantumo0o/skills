/**
 * HTML 原型模块 v4.0.0
 *
 * 多页面原型生成系统：
 * - Phase 1: 页面树推断（从 PRD 提取）
 * - Phase 2: 导航组件生成（侧边栏 + 底部 Tab）
 * - Phase 3: AI 内容填充（调用 OpenClaw AI）
 * - Phase 4: 路由注入（页面间跳转）
 * - Phase 5: 截图生成（桌面端 + 移动端）
 *
 * v4.0.0: 完整重构，支持多页面原型
 * v2.8.9: 使用 AIDiagramExtractor.generatePrototypeConfig
 */

const fs = require('fs');
const path = require('path');
const { AIDiagramExtractor } = require('../ai_diagram_extractor');

class PrototypeModule {
  constructor() {
    this.extractor = new AIDiagramExtractor();
    this.version = '4.0.0';

    // 页面类型映射
    this.pageTypes = {
      'list': '列表页',
      'form': '表单页',
      'dashboard': '仪表盘',
      'detail': '详情页',
      'login': '登录页',
      'landing': '落地页',
      'checkout': '支付页',
      'custom': '自定义页'
    };

    // 截图尺寸配置
    this.screenshotSizes = {
      desktop: { width: 1440, height: 900 },
      mobile: { width: 375, height: 667 }
    };
  }

  /**
   * 执行原型生成
   */
  async execute(options) {
    console.log('\n🎨 执行技能：HTML 原型生成 v4.0.0');
    console.log('   多页面原型系统启动...');

    const { dataBus, qualityGate, outputDir } = options;

    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }
    const prd = prdRecord.data;

    // 读取设计系统
    const designRecord = dataBus.read('design');
    const designTokens = designRecord?.data || this.getDefaultDesignTokens();

    // 读取需求拆解结果
    const decompositionRecord = dataBus.read('decomposition');
    const decomposition = decompositionRecord?.data || null;

    // ========== Phase 1: 页面树推断 ==========
    console.log('\n   📋 Phase 1: 页面树推断...');
    const sitemap = this.extractPageTree(prd, decomposition);
    console.log(`      ✅ 提取 ${sitemap.pages.length} 个页面`);
    sitemap.pages.forEach(p => {
      const parent = p.parent ? ` (父: ${p.parent})` : '';
      console.log(`         - ${p.name} [${this.pageTypes[p.type] || p.type}]${parent}`);
    });

    // ========== Phase 2: 导航组件生成 ==========
    console.log('\n   🧭 Phase 2: 导航组件生成...');
    const navigation = this.generateNavigation(sitemap, designTokens);
    console.log(`      ✅ 侧边栏: ${navigation.sidebar.items.length} 个菜单项`);
    console.log(`      ✅ 底部Tab: ${navigation.tabbar.items.length} 个Tab项`);

    // ========== Phase 3: 页面内容生成 ==========
    console.log('\n   📄 Phase 3: 页面内容生成...');
    const pages = await this.generatePages(sitemap, prd, designTokens, outputDir);
    console.log(`      ✅ 生成 ${pages.length} 个页面文件`);

    // ========== Phase 4: 路由注入 ==========
    console.log('\n   🔗 Phase 4: 路由注入...');
    const routes = this.generateRoutes(sitemap);
    await this.injectRoutes(pages, routes, navigation, outputDir);
    console.log(`      ✅ 注入 ${routes.length} 条路由`);

    // ========== Phase 5: 截图生成 ==========
    console.log('\n   📸 Phase 5: 截图生成...');
    const screenshots = await this.generateScreenshots(pages, outputDir);
    const desktopCount = screenshots.desktop?.length || 0;
    const mobileCount = screenshots.mobile?.length || 0;
    console.log(`      ✅ 桌面端截图: ${desktopCount} 张`);
    console.log(`      ✅ 移动端截图: ${mobileCount} 张`);

    // ========== 构建结果 ==========
    const result = {
      sitemap,
      pages,
      routes,
      navigation,
      screenshots,
      prototypeConfig: {
        designTokens,
        pageTypesGenerated: sitemap.pages.map(p => p.type)
      }
    };

    // 质量验证
    const quality = {
      passed: pages.length > 0,
      pagesGenerated: pages.length,
      routesGenerated: routes.length,
      screenshotsGenerated: desktopCount + mobileCount
    };

    // 写入数据总线
    const filepath = dataBus.write('prototype', result, quality, {
      fromPRD: 'prd.json',
      fromDesign: 'design.json'
    });

    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate7_prototype', result);
    }

    console.log(`\n   ✅ 原型生成完成：${pages.length} 个页面，${routes.length} 条路由`);

    return {
      ...result,
      quality: quality,
      outputPath: filepath
    };
  }

  // ==================== Phase 1: 页面树推断 ====================

  /**
   * 从 PRD 提取页面树
   */
  extractPageTree(prd, decomposition) {
    const content = prd.content || '';
    const features = decomposition?.features || prd.features || [];

    // 提取产品信息
    const titleMatch = content.match(/^# (.+)$/m);
    const productName = titleMatch ? titleMatch[1].replace(/\s*PRD.*/i, '').trim() : '产品';
    const productType = this.extractor.inferProductType(content);

    // 页面列表
    const pages = [];

    // 1. 首页/落地页
    pages.push({
      id: 'home',
      name: '首页',
      type: 'landing',
      description: `${productName} 首页`,
      features: []
    });

    // 2. 从功能列表推断页面
    const featurePages = this.inferPagesFromFeatures(features, content);
    featurePages.forEach((page, index) => {
      // 避免重复
      if (!pages.find(p => p.id === page.id)) {
        pages.push(page);
      }
    });

    // 3. 补充必要的页面
    // 如果有列表页，添加详情页
    const hasList = pages.find(p => p.type === 'list');
    if (hasList && !pages.find(p => p.type === 'detail')) {
      pages.push({
        id: `${hasList.id}-detail`,
        name: `${hasList.name}详情`,
        type: 'detail',
        parent: hasList.id,
        description: `${hasList.name}的详细信息`,
        features: []
      });
    }

    // 4. 推断路由关系
    this.inferPageRelations(pages);

    return {
      productName,
      productType,
      pages
    };
  }

  /**
   * 从功能列表推断页面
   */
  inferPagesFromFeatures(features, content) {
    const pages = [];

    features.forEach((feature, index) => {
      const name = feature.name || `功能${index + 1}`;
      const pageType = this.inferPageType(feature, content);
      const pageId = this.generatePageId(name, index);

      pages.push({
        id: pageId,
        name: name,
        type: pageType,
        description: feature.description || `${name}页面`,
        features: [feature],
        priority: feature.priority || 'P0'
      });

      // 如果是表单类型，可能需要结果页
      if (pageType === 'form' && feature.outputs && feature.outputs.length > 0) {
        pages.push({
          id: `${pageId}-result`,
          name: `${name}结果`,
          type: 'detail',
          parent: pageId,
          description: `${name}的结果展示`,
          features: [feature]
        });
      }
    });

    return pages;
  }

  /**
   * 推断单个功能的页面类型
   */
  inferPageType(feature, content) {
    const name = (feature.name || '').toLowerCase();
    const inputs = feature.inputs || [];
    const outputs = feature.outputs || [];

    // 规则匹配
    if (name.includes('登录') || name.includes('注册') || name.includes('认证')) {
      return 'login';
    }
    if (name.includes('统计') || name.includes('分析') || name.includes('看板') || name.includes('概览')) {
      return 'dashboard';
    }
    if (name.includes('提交') || name.includes('申请') || name.includes('填写') || inputs.length > 3) {
      return 'form';
    }
    if (name.includes('详情') || name.includes('查看')) {
      return 'detail';
    }
    if (name.includes('支付') || name.includes('结算') || name.includes('收银')) {
      return 'checkout';
    }
    if (name.includes('列表') || outputs.length > 3) {
      return 'list';
    }

    // 默认列表页
    return 'list';
  }

  /**
   * 生成页面 ID
   */
  generatePageId(name, index) {
    const slug = name
      .toLowerCase()
      .replace(/[^\u4e00-\u9fa5a-z0-9]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
      .substring(0, 20);
    return `page-${slug || index}`;
  }

  /**
   * 推断页面关系
   */
  inferPageRelations(pages) {
    // 自动设置父页面关系
    const listPages = pages.filter(p => p.type === 'list');
    const detailPages = pages.filter(p => p.type === 'detail' && !p.parent);

    // 为详情页关联列表页
    detailPages.forEach(detail => {
      const matchingList = listPages.find(list =>
        detail.name.includes(list.name) || list.name.includes(detail.name.replace('详情', ''))
      );
      if (matchingList) {
        detail.parent = matchingList.id;
      }
    });
  }

  // ==================== Phase 2: 导航组件生成 ====================

  /**
   * 生成导航组件配置
   */
  generateNavigation(sitemap, designTokens) {
    const { pages, productName } = sitemap;
    const colors = designTokens?.colors || {};

    // 顶部页面（无 parent）作为菜单项
    const topLevelPages = pages.filter(p => !p.parent);

    // 侧边栏配置
    const sidebar = {
      brand: productName,
      items: topLevelPages.map(page => ({
        id: page.id,
        name: page.name,
        href: `${page.id}.html`,
        icon: this.getIconForPageType(page.type),
        children: pages.filter(p => p.parent === page.id).map(child => ({
          id: child.id,
          name: child.name,
          href: `${child.id}.html`
        }))
      })),
      style: {
        backgroundColor: colors.background || '#FFFFFF',
        textColor: colors.text || '#1E293B',
        activeColor: colors.primary || '#1890FF'
      }
    };

    // 底部 Tab 配置（最多 5 个）
    const tabItems = topLevelPages.slice(0, 5);
    const tabbar = {
      items: tabItems.map(page => ({
        id: page.id,
        name: page.name,
        href: `${page.id}.html`,
        icon: this.getIconForPageType(page.type)
      })),
      style: {
        backgroundColor: colors.background || '#FFFFFF',
        textColor: colors.muted || '#6B7280',
        activeColor: colors.primary || '#1890FF'
      }
    };

    // 顶部导航栏
    const header = {
      brand: productName,
      items: topLevelPages.slice(0, 6).map(page => ({
        id: page.id,
        name: page.name,
        href: `${page.id}.html`
      })),
      style: {
        backgroundColor: colors.primary || '#1890FF',
        textColor: '#FFFFFF'
      }
    };

    return { sidebar, tabbar, header };
  }

  /**
   * 根据页面类型获取图标
   */
  getIconForPageType(type) {
    const icons = {
      'landing': 'home',
      'list': 'list',
      'form': 'edit',
      'dashboard': 'dashboard',
      'detail': 'file-text',
      'login': 'user',
      'checkout': 'shopping-cart',
      'custom': 'file'
    };
    return icons[type] || 'file';
  }

  // ==================== Phase 3: 页面内容生成 ====================

  /**
   * 生成所有页面
   */
  async generatePages(sitemap, prd, designTokens, outputDir) {
    const pages = [];
    const htmlPrototypePath = path.join(__dirname, '../../skills/htmlPrototype/main.py');

    // 确保输出目录存在
    const pagesDir = path.join(outputDir, 'pages');
    if (!fs.existsSync(pagesDir)) {
      fs.mkdirSync(pagesDir, { recursive: true });
    }

    // 保存设计系统文件
    const tokensPath = path.join(outputDir, 'design-tokens.json');
    fs.writeFileSync(tokensPath, JSON.stringify(designTokens, null, 2), 'utf8');

    // 为每个页面生成 HTML
    for (const page of sitemap.pages) {
      console.log(`      生成: ${page.name}...`);

      const pageData = await this.generatePageContent(page, prd, designTokens);
      const htmlContent = this.renderPageTemplate(page, pageData, designTokens, sitemap);

      const htmlPath = path.join(pagesDir, `${page.id}.html`);
      fs.writeFileSync(htmlPath, htmlContent, 'utf8');

      pages.push({
        id: page.id,
        name: page.name,
        type: page.type,
        htmlPath: `pages/${page.id}.html`,
        absolutePath: htmlPath
      });
    }

    // 生成入口文件 index.html
    this.generateIndexPage(sitemap, designTokens, outputDir);

    return pages;
  }

  /**
   * 生成单个页面内容
   */
  async generatePageContent(page, prd, designTokens) {
    // 从 PRD 提取页面相关内容
    const content = prd.content || '';
    const feature = page.features?.[0] || {};

    // 表单字段
    const formFields = (feature.inputs || []).map(input => ({
      label: input.field,
      type: this.mapInputType(input.type),
      required: input.required,
      placeholder: `请输入${input.field}`,
      validation: input.validation
    }));

    // 表格列
    const tableColumns = (feature.outputs || []).map(output => ({
      field: output.field,
      label: output.description || output.field,
      type: output.type
    }));

    // 示例数据
    const sampleData = this.generateSampleData(feature.outputs, page.name);

    return {
      title: page.name,
      description: page.description,
      formFields,
      tableColumns,
      sampleData
    };
  }

  /**
   * 渲染页面模板
   */
  renderPageTemplate(page, pageData, designTokens, sitemap) {
    const colors = designTokens?.colors || {};
    const typography = designTokens?.typography || {};

    // 根据页面类型选择模板
    switch (page.type) {
      case 'list':
        return this.renderListPage(page, pageData, designTokens, sitemap);
      case 'form':
        return this.renderFormPage(page, pageData, designTokens, sitemap);
      case 'dashboard':
        return this.renderDashboardPage(page, pageData, designTokens, sitemap);
      case 'detail':
        return this.renderDetailPage(page, pageData, designTokens, sitemap);
      case 'login':
        return this.renderLoginPage(page, pageData, designTokens, sitemap);
      case 'landing':
        return this.renderLandingPage(page, pageData, designTokens, sitemap);
      default:
        return this.renderListPage(page, pageData, designTokens, sitemap);
    }
  }

  /**
   * 渲染列表页
   */
  renderListPage(page, pageData, designTokens, sitemap) {
    const colors = designTokens?.colors || {};
    const navigation = this.generateNavigation(sitemap, designTokens);
    const columns = pageData.tableColumns.length > 0 ? pageData.tableColumns : [
      { field: 'name', label: '名称' },
      { field: 'status', label: '状态' },
      { field: 'createTime', label: '创建时间' },
      { field: 'actions', label: '操作' }
    ];
    const sampleData = pageData.sampleData.length > 0 ? pageData.sampleData : [
      ['示例数据1', '正常', '2026-04-01', '查看'],
      ['示例数据2', '正常', '2026-04-02', '查看'],
      ['示例数据3', '正常', '2026-04-03', '查看']
    ];

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${page.name} - ${sitemap.productName}</title>
    <style>
        ${this.getBaseStyles(designTokens)}
        ${this.getNavigationStyles(designTokens)}
    </style>
</head>
<body>
    ${this.renderSidebar(navigation.sidebar, page.id)}
    <div class="main-content">
        <div class="page-header">
            <h1 class="page-title">${page.name}</h1>
            <div class="page-actions">
                <button class="btn btn-primary">+ 新建</button>
                <button class="btn btn-secondary">导出</button>
            </div>
        </div>

        <div class="filter-section">
            <div class="filter-row">
                <input type="text" class="filter-input" placeholder="搜索关键词...">
                <select class="filter-select"><option>全部状态</option></select>
                <button class="btn btn-secondary">筛选</button>
            </div>
        </div>

        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        ${columns.map(col => `<th>${col.label}</th>`).join('\n                        ')}
                    </tr>
                </thead>
                <tbody>
                    ${sampleData.map(row => `
                    <tr>
                        ${row.map((cell, i) => i === row.length - 1
                          ? `<td><a href="${page.id}-detail.html" class="action-link">${cell}</a></td>`
                          : `<td>${cell}</td>`
                        ).join('\n                        ')}
                    </tr>`).join('')}
                </tbody>
            </table>
        </div>

        <div class="pagination">
            <button class="page-btn">上一页</button>
            <button class="page-btn active">1</button>
            <button class="page-btn">2</button>
            <button class="page-btn">下一页</button>
        </div>
    </div>

    ${this.renderTabbar(navigation.tabbar, page.id)}
</body>
</html>`;
  }

  /**
   * 渲染表单页
   */
  renderFormPage(page, pageData, designTokens, sitemap) {
    const colors = designTokens?.colors || {};
    const navigation = this.generateNavigation(sitemap, designTokens);
    const fields = pageData.formFields.length > 0 ? pageData.formFields : [
      { label: '名称', type: 'text', required: true },
      { label: '描述', type: 'textarea', required: false }
    ];

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${page.name} - ${sitemap.productName}</title>
    <style>
        ${this.getBaseStyles(designTokens)}
        ${this.getNavigationStyles(designTokens)}
    </style>
</head>
<body>
    ${this.renderSidebar(navigation.sidebar, page.id)}
    <div class="main-content">
        <div class="page-header">
            <h1 class="page-title">${page.name}</h1>
        </div>

        <div class="form-container">
            <form class="form-section">
                ${fields.map(field => `
                <div class="form-group">
                    <label class="form-label">
                        ${field.label}${field.required ? ' <span class="required">*</span>' : ''}
                    </label>
                    ${field.type === 'textarea'
                      ? `<textarea class="form-input form-textarea" placeholder="${field.placeholder || '请输入' + field.label}"></textarea>`
                      : `<input type="${field.type}" class="form-input" placeholder="${field.placeholder || '请输入' + field.label}">`
                    }
                </div>`).join('')}

                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">提交</button>
                    <button type="button" class="btn btn-secondary">取消</button>
                </div>
            </form>
        </div>
    </div>

    ${this.renderTabbar(navigation.tabbar, page.id)}
</body>
</html>`;
  }

  /**
   * 渲染仪表盘页
   */
  renderDashboardPage(page, pageData, designTokens, sitemap) {
    const navigation = this.generateNavigation(sitemap, designTokens);
    const colors = designTokens?.colors || {};

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${page.name} - ${sitemap.productName}</title>
    <style>
        ${this.getBaseStyles(designTokens)}
        ${this.getNavigationStyles(designTokens)}
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 24px; }
        .stat-card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .stat-value { font-size: 28px; font-weight: 700; color: ${colors.primary || '#1890FF'}; }
        .stat-label { color: #666; margin-top: 8px; }
        .chart-placeholder { background: #f5f5f5; height: 300px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #999; }
    </style>
</head>
<body>
    ${this.renderSidebar(navigation.sidebar, page.id)}
    <div class="main-content">
        <div class="page-header">
            <h1 class="page-title">${page.name}</h1>
        </div>

        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-value">1,234</div>
                <div class="stat-label">总数据量</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">567</div>
                <div class="stat-label">本月新增</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">89%</div>
                <div class="stat-label">完成率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">¥12.3万</div>
                <div class="stat-label">总金额</div>
            </div>
        </div>

        <div class="chart-placeholder">
            图表区域（需要图表库支持）
        </div>
    </div>

    ${this.renderTabbar(navigation.tabbar, page.id)}
</body>
</html>`;
  }

  /**
   * 渲染详情页
   */
  renderDetailPage(page, pageData, designTokens, sitemap) {
    const navigation = this.generateNavigation(sitemap, designTokens);
    const colors = designTokens?.colors || {};
    const parentPage = sitemap.pages.find(p => p.id === page.parent);

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${page.name} - ${sitemap.productName}</title>
    <style>
        ${this.getBaseStyles(designTokens)}
        ${this.getNavigationStyles(designTokens)}
        .detail-card { background: white; border-radius: 8px; padding: 24px; margin-bottom: 20px; }
        .detail-row { display: flex; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
        .detail-label { width: 120px; color: #666; }
        .detail-value { flex: 1; color: #333; }
    </style>
</head>
<body>
    ${this.renderSidebar(navigation.sidebar, page.id)}
    <div class="main-content">
        <div class="page-header">
            <a href="${parentPage ? parentPage.id : 'home'}.html" class="back-link">← 返回列表</a>
            <h1 class="page-title">${page.name}</h1>
        </div>

        <div class="detail-card">
            <h3>基本信息</h3>
            <div class="detail-row">
                <div class="detail-label">名称</div>
                <div class="detail-value">示例数据</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">状态</div>
                <div class="detail-value">正常</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">创建时间</div>
                <div class="detail-value">2026-04-05</div>
            </div>
        </div>

        <div class="form-actions">
            <button class="btn btn-primary">编辑</button>
            <button class="btn btn-secondary">删除</button>
        </div>
    </div>

    ${this.renderTabbar(navigation.tabbar, page.id)}
</body>
</html>`;
  }

  /**
   * 渲染登录页
   */
  renderLoginPage(page, pageData, designTokens, sitemap) {
    const colors = designTokens?.colors || {};

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - ${sitemap.productName}</title>
    <style>
        ${this.getBaseStyles(designTokens)}
        body { background: linear-gradient(135deg, ${colors.primary || '#1890FF'} 0%, ${colors.secondary || '#1890FF'} 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-card { background: white; border-radius: 12px; padding: 40px; width: 100%; max-width: 400px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .login-logo { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 32px; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="login-logo">${sitemap.productName}</div>
        <form>
            <div class="form-group">
                <label class="form-label">用户名</label>
                <input type="text" class="form-input" placeholder="请输入用户名">
            </div>
            <div class="form-group">
                <label class="form-label">密码</label>
                <input type="password" class="form-input" placeholder="请输入密码">
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">登录</button>
        </form>
    </div>
</body>
</html>`;
  }

  /**
   * 渲染落地页/首页
   */
  renderLandingPage(page, pageData, designTokens, sitemap) {
    const colors = designTokens?.colors || {};
    const navigation = this.generateNavigation(sitemap, designTokens);

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${sitemap.productName} - 首页</title>
    <style>
        ${this.getBaseStyles(designTokens)}
        .hero { padding: 80px 32px; text-align: center; background: linear-gradient(180deg, #f8f9ff 0%, #fff 100%); }
        .hero h1 { font-size: 42px; font-weight: 700; margin-bottom: 16px; }
        .hero p { font-size: 18px; color: #666; margin-bottom: 32px; }
        .hero-buttons { display: flex; gap: 16px; justify-content: center; }
        .features { padding: 60px 32px; background: #f8f9fa; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; max-width: 1200px; margin: 0 auto; }
        .feature-card { background: white; padding: 32px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .feature-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
        .feature-desc { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    ${this.renderHeader(navigation.header, 'home')}

    <section class="hero">
        <h1>${sitemap.productName}</h1>
        <p>一站式解决方案，助力您的业务增长</p>
        <div class="hero-buttons">
            <a href="${sitemap.pages[1]?.id || 'home'}.html" class="btn btn-primary">立即体验</a>
            <button class="btn btn-secondary">了解更多</button>
        </div>
    </section>

    <section class="features">
        <div class="features-grid">
            ${sitemap.pages.filter(p => p.type !== 'landing' && p.type !== 'login').slice(0, 6).map(p => `
            <a href="${p.id}.html" class="feature-card">
                <div class="feature-title">${p.name}</div>
                <div class="feature-desc">${p.description || '功能模块'}</div>
            </a>
            `).join('')}
        </div>
    </section>

    ${this.renderTabbar(navigation.tabbar, 'home')}
</body>
</html>`;
  }

  /**
   * 生成入口页面
   */
  generateIndexPage(sitemap, designTokens, outputDir) {
    // 默认跳转到首页
    const indexContent = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=pages/home.html">
    <title>${sitemap.productName}</title>
</head>
<body>
    <p>正在跳转... <a href="pages/home.html">点击这里</a></p>
</body>
</html>`;

    fs.writeFileSync(path.join(outputDir, 'index.html'), indexContent, 'utf8');
  }

  // ==================== Phase 4: 路由注入 ====================

  /**
   * 生成路由表
   */
  generateRoutes(sitemap) {
    const routes = [];

    sitemap.pages.forEach(page => {
      // 列表页 → 详情页
      if (page.type === 'list') {
        const detailPage = sitemap.pages.find(p => p.parent === page.id && p.type === 'detail');
        if (detailPage) {
          routes.push({
            from: page.id,
            to: detailPage.id,
            trigger: '点击详情',
            type: 'link'
          });
        }
      }

      // 表单页 → 结果页
      if (page.type === 'form') {
        const resultPage = sitemap.pages.find(p => p.parent === page.id && p.name.includes('结果'));
        if (resultPage) {
          routes.push({
            from: page.id,
            to: resultPage.id,
            trigger: '提交成功',
            type: 'auto'
          });
        }
      }

      // 首页 → 功能页
      if (page.type === 'landing') {
        sitemap.pages.filter(p => p.type !== 'landing' && p.type !== 'login' && !p.parent).forEach(targetPage => {
          routes.push({
            from: page.id,
            to: targetPage.id,
            trigger: `点击${targetPage.name}`,
            type: 'link'
          });
        });
      }
    });

    return routes;
  }

  /**
   * 注入路由到页面
   */
  async injectRoutes(pages, routes, navigation, outputDir) {
    // 路由已通过模板中的 href 注入
    // 这里可以保存路由配置文件供后续使用
    const routesPath = path.join(outputDir, 'routes.json');
    fs.writeFileSync(routesPath, JSON.stringify({
      routes,
      navigation: {
        sidebar: navigation.sidebar.items.map(i => ({ id: i.id, name: i.name, href: i.href })),
        tabbar: navigation.tabbar.items.map(i => ({ id: i.id, name: i.name, href: i.href }))
      }
    }, null, 2), 'utf8');
  }

  // ==================== Phase 5: 截图生成 ====================

  /**
   * 生成多端截图
   */
  async generateScreenshots(pages, outputDir) {
    const screenshots = {
      desktop: [],
      mobile: []
    };

    const screenshotsDir = path.join(outputDir, 'screensshots');
    const desktopDir = path.join(screenshotsDir, 'desktop');
    const mobileDir = path.join(screenshotsDir, 'mobile');

    if (!fs.existsSync(desktopDir)) {
      fs.mkdirSync(desktopDir, { recursive: true });
    }
    if (!fs.existsSync(mobileDir)) {
      fs.mkdirSync(mobileDir, { recursive: true });
    }

    // 检测截图工具
    const hasPlaywright = this.checkPlaywright();
    const hasSafari = this.checkSafari();

    if (!hasPlaywright && !hasSafari) {
      console.log('      ⚠️  未检测到截图工具，跳过截图生成');
      console.log('      💡 安装 Playwright: npm install -g playwright');
      return screenshots;
    }

    // 为每个页面生成截图
    for (const page of pages) {
      const htmlPath = page.absolutePath;
      if (!fs.existsSync(htmlPath)) continue;

      // 桌面端截图
      const desktopPath = path.join(desktopDir, `${page.id}.png`);
      try {
        await this.captureScreenshot(htmlPath, desktopPath, this.screenshotSizes.desktop);
        screenshots.desktop.push({
          pageId: page.id,
          path: `screensshots/desktop/${page.id}.png`,
          ...this.screenshotSizes.desktop
        });
      } catch (e) {
        console.log(`      ⚠️  桌面端截图失败: ${page.id}`);
      }

      // 移动端截图
      const mobilePath = path.join(mobileDir, `${page.id}.png`);
      try {
        await this.captureScreenshot(htmlPath, mobilePath, this.screenshotSizes.mobile);
        screenshots.mobile.push({
          pageId: page.id,
          path: `screensshots/mobile/${page.id}.png`,
          ...this.screenshotSizes.mobile
        });
      } catch (e) {
        console.log(`      ⚠️  移动端截图失败: ${page.id}`);
      }
    }

    return screenshots;
  }

  /**
   * 截图
   */
  async captureScreenshot(htmlPath, outputPath, size) {
    const { execSync } = require('child_process');

    // 尝试 Playwright
    try {
      const script = `
        const { chromium } = require('playwright');
        (async () => {
          const browser = await chromium.launch();
          const page = await browser.newPage({ viewport: { width: ${size.width}, height: ${size.height} } });
          await page.goto('file://${htmlPath}');
          await page.screenshot({ path: '${outputPath}', fullPage: false });
          await browser.close();
        })();
      `;
      const tempScript = outputPath.replace('.png', '.js');
      fs.writeFileSync(tempScript, script, 'utf8');
      execSync(`node "${tempScript}"`, { stdio: 'pipe', timeout: 30000 });
      fs.unlinkSync(tempScript);
      return true;
    } catch (e) {
      // Playwright 失败，创建占位符
      this.createPlaceholderScreenshot(outputPath);
      return false;
    }
  }

  /**
   * 检测 Playwright
   */
  checkPlaywright() {
    try {
      const { execSync } = require('child_process');
      execSync('playwright --version', { stdio: 'pipe' });
      return true;
    } catch (e) {
      return false;
    }
  }

  /**
   * 检测 Safari
   */
  checkSafari() {
    return fs.existsSync('/Applications/Safari.app');
  }

  /**
   * 创建占位符截图
   */
  createPlaceholderScreenshot(outputPath) {
    const pngHeader = Buffer.from([
      0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
      0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
      0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
      0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
      0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
      0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
      0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
      0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
      0x42, 0x60, 0x82
    ]);
    fs.writeFileSync(outputPath, pngHeader);
  }

  // ==================== 辅助方法 ====================

  /**
   * 获取基础样式
   */
  getBaseStyles(designTokens) {
    const colors = designTokens?.colors || {};
    const typography = designTokens?.typography || {};

    return `
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: ${typography.fontFamily || 'system-ui, -apple-system, sans-serif'}; background: #f5f5f5; color: ${colors.text || '#333'}; }
        a { color: ${colors.primary || '#1890FF'}; text-decoration: none; }

        .btn { display: inline-block; padding: 10px 20px; border-radius: 6px; font-size: 14px; cursor: pointer; border: none; transition: all 200ms; font-weight: 500; }
        .btn-primary { background: ${colors.primary || '#1890FF'}; color: white; }
        .btn-primary:hover { opacity: 0.9; }
        .btn-secondary { background: white; color: #666; border: 1px solid #ddd; }
        .btn-secondary:hover { background: #f5f5f5; }

        .form-group { margin-bottom: 20px; }
        .form-label { display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500; }
        .form-label .required { color: #F5222D; }
        .form-input { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: border-color 200ms; }
        .form-input:focus { outline: none; border-color: ${colors.primary || '#1890FF'}; }
        .form-textarea { min-height: 100px; resize: vertical; }
        .form-actions { display: flex; gap: 12px; margin-top: 24px; }

        .table-container { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
        .data-table { width: 100%; border-collapse: collapse; }
        .data-table th { background: #f8f9fa; padding: 14px 16px; text-align: left; font-weight: 600; font-size: 13px; color: #666; border-bottom: 1px solid #eee; }
        .data-table td { padding: 14px 16px; font-size: 14px; border-bottom: 1px solid #f0f0f0; }
        .data-table tr:hover { background: #fafafa; }
        .action-link { color: ${colors.primary || '#1890FF'}; cursor: pointer; }

        .pagination { display: flex; gap: 8px; margin-top: 20px; justify-content: center; }
        .page-btn { padding: 8px 12px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
        .page-btn.active { background: ${colors.primary || '#1890FF'}; color: white; border-color: ${colors.primary || '#1890FF'}; }

        .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        .page-title { font-size: 24px; font-weight: 600; }
        .back-link { color: #666; margin-right: 16px; }

        .filter-section { background: white; padding: 16px; border-radius: 8px; margin-bottom: 16px; }
        .filter-row { display: flex; gap: 12px; flex-wrap: wrap; }
        .filter-input { padding: 10px 12px; border: 1px solid #ddd; border-radius: 6px; min-width: 200px; }
        .filter-select { padding: 10px 12px; border: 1px solid #ddd; border-radius: 6px; background: white; }

        .form-container { max-width: 800px; }
        .form-section { background: white; padding: 32px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }

        @media (max-width: 768px) {
            .sidebar { display: none; }
            .tabbar { display: flex; }
            .filter-row { flex-direction: column; }
            .filter-input { width: 100%; }
            .page-header { flex-direction: column; align-items: flex-start; gap: 12px; }
        }
    `;
  }

  /**
   * 获取导航样式
   */
  getNavigationStyles(designTokens) {
    return `
        .app-container { display: flex; min-height: 100vh; }
        .sidebar { width: 220px; background: white; box-shadow: 1px 0 8px rgba(0,0,0,0.05); position: fixed; left: 0; top: 0; bottom: 0; z-index: 100; }
        .sidebar-brand { padding: 20px; font-size: 18px; font-weight: 600; border-bottom: 1px solid #f0f0f0; }
        .sidebar-menu { list-style: none; padding: 12px 0; }
        .sidebar-item { display: block; padding: 12px 20px; color: #333; transition: all 200ms; }
        .sidebar-item:hover { background: #f5f5f5; }
        .sidebar-item.active { background: #e6f4ff; color: ${designTokens?.colors?.primary || '#1890FF'}; border-left: 3px solid ${designTokens?.colors?.primary || '#1890FF'}; }
        .sidebar-submenu { padding-left: 20px; }

        .main-content { flex: 1; margin-left: 220px; padding: 24px; min-height: 100vh; }

        .tabbar { display: none; position: fixed; bottom: 0; left: 0; right: 0; background: white; box-shadow: 0 -2px 8px rgba(0,0,0,0.05); z-index: 100; }
        .tabbar-item { flex: 1; text-align: center; padding: 12px 0; color: #666; font-size: 12px; }
        .tabbar-item.active { color: ${designTokens?.colors?.primary || '#1890FF'}; }

        .header-nav { background: ${designTokens?.colors?.primary || '#1890FF'}; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
        .header-brand { color: white; font-size: 18px; font-weight: 600; }
        .header-links { display: flex; gap: 24px; }
        .header-link { color: rgba(255,255,255,0.8); }
        .header-link:hover { color: white; }
    `;
  }

  /**
   * 渲染侧边栏
   */
  renderSidebar(sidebar, activeId) {
    return `
    <nav class="sidebar">
        <div class="sidebar-brand">${sidebar.brand}</div>
        <ul class="sidebar-menu">
            ${sidebar.items.map(item => `
            <li>
                <a href="../pages/${item.href}" class="sidebar-item ${item.id === activeId ? 'active' : ''}">
                    ${item.name}
                </a>
                ${item.children && item.children.length > 0 ? `
                <ul class="sidebar-submenu">
                    ${item.children.map(child => `
                    <li>
                        <a href="../pages/${child.href}" class="sidebar-item ${child.id === activeId ? 'active' : ''}">
                            ${child.name}
                        </a>
                    </li>
                    `).join('')}
                </ul>
                ` : ''}
            </li>
            `).join('')}
        </ul>
    </nav>`;
  }

  /**
   * 渲染底部 Tab
   */
  renderTabbar(tabbar, activeId) {
    return `
    <nav class="tabbar">
        ${tabbar.items.map(item => `
        <a href="../pages/${item.href}" class="tabbar-item ${item.id === activeId ? 'active' : ''}">
            ${item.name}
        </a>
        `).join('')}
    </nav>`;
  }

  /**
   * 渲染顶部导航
   */
  renderHeader(header, activeId) {
    return `
    <header class="header-nav">
        <div class="header-brand">${header.brand}</div>
        <nav class="header-links">
            ${header.items.map(item => `
            <a href="pages/${item.href}" class="header-link ${item.id === activeId ? 'active' : ''}">
                ${item.name}
            </a>
            `).join('')}
        </nav>
    </header>`;
  }

  /**
   * 映射输入类型
   */
  mapInputType(inputType) {
    const typeMap = {
      '整数': 'number',
      '数字': 'number',
      '数字 (2位小数)': 'number',
      '字符串': 'text',
      '文本': 'textarea',
      '日期': 'date',
      '日期时间': 'datetime-local',
      '百分比': 'number',
      '下拉选择': 'select',
      '布尔': 'checkbox'
    };
    return typeMap[inputType] || 'text';
  }

  /**
   * 生成示例数据
   */
  generateSampleData(outputs, featureName) {
    if (!outputs || outputs.length === 0) {
      return [
        ['示例数据1', '正常', '2026-04-01', '查看'],
        ['示例数据2', '正常', '2026-04-02', '查看'],
        ['示例数据3', '正常', '2026-04-03', '查看']
      ];
    }

    const columns = outputs.slice(0, 4).map(o => o.example || '-');
    return [
      [...columns.slice(0, 3), '查看'],
      [...columns.slice(0, 3).map(c => c + '2'), '查看'],
      [...columns.slice(0, 3).map(c => c + '3'), '查看']
    ];
  }

  /**
   * 默认设计系统
   */
  getDefaultDesignTokens() {
    return {
      colors: {
        primary: '#1890FF',
        secondary: '#1890FF',
        cta: '#F97316',
        background: '#FFFFFF',
        text: '#1E293B',
        success: '#52C41A',
        warning: '#FAAD14',
        error: '#F5222D',
        muted: '#6B7280'
      },
      typography: {
        fontFamily: 'system-ui, -apple-system, sans-serif',
        fontSize: 14
      },
      spacing: {
        unit: 8,
        scale: [0, 4, 8, 12, 16, 24, 32, 48, 64]
      }
    };
  }
}

module.exports = PrototypeModule;