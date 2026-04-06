/**
 * UI/UX 设计模块 v2.5.0
 * 
 * 生成设计系统 tokens
 */

const fs = require('fs');
const path = require('path');

class DesignModule {
  /**
   * 执行 UI/UX 设计
   */
  async execute(options) {
    console.log('\n🎨 执行技能：UI/UX 设计');
    
    const { dataBus, qualityGate, outputDir } = options;
    
    // 读取 PRD
    const prdRecord = dataBus.read('prd');
    if (!prdRecord) {
      throw new Error('PRD 不存在，请先执行 PRD 生成');
    }
    
    const prd = prdRecord.data;
    
    // 调用 ui-ux-pro-max 生成设计系统
    console.log('   调用 ui-ux-pro-max 生成设计系统...');
    const designResult = await this.generateDesignSystem(prd, outputDir);
    
    // 质量验证
    const quality = this.validateDesign(designResult);
    
    // 写入数据总线
    const filepath = dataBus.write('design', designResult, quality, {
      fromPRD: 'prd.json'
    });
    
    // 门禁检查
    if (qualityGate) {
      await qualityGate.pass('gate6_design', designResult);
    }
    
    return {
      ...designResult,
      quality: quality,
      outputPath: filepath
    };
  }
  
  /**
   * 调用 ui-ux-pro-max 生成设计系统（v2.6.3 修复）
   */
  async generateDesignSystem(prd, outputDir) {
    const { execSync } = require('child_process');
    const fs = require('fs');
    const path = require('path');
    
    // ui-ux-pro-max 脚本路径
    const designSystemPath = path.join(__dirname, '../../skills/ui-ux-pro-max/scripts/design_system.py');
    
    // 检查脚本是否存在
    if (!fs.existsSync(designSystemPath)) {
      console.warn('⚠️  ui-ux-pro-max 脚本不存在，使用备用方案');
      return this.generateFallbackDesign(prd);
    }
    
    // 从 PRD 提取产品类型
    const content = prd.content || '';
    const productType = this.extractProductType(content);
    const projectName = this.extractProductName(content);
    
    console.log(`   调用 ui-ux-pro-max：产品类型="${productType}", 项目="${projectName}"`);
    
    try {
      // 调用 design_system.py（支持 ascii/markdown 格式）
      const designDir = path.join(outputDir, 'design-system');
      if (!fs.existsSync(designDir)) {
        fs.mkdirSync(designDir, { recursive: true });
      }

      // 使用 markdown 格式，然后解析
      const result = execSync(
        `python3 "${designSystemPath}" "${productType}" --project-name "${projectName}" --format markdown`,
        { encoding: 'utf8', stdio: 'pipe' }
      );

      // 解析 markdown 输出，提取设计系统信息
      const designResult = this.parseMarkdownOutput(result);

      console.log('   ✅ 设计系统生成成功');
      return designResult;
      
    } catch (error) {
      console.warn('⚠️  ui-ux-pro-max 调用失败，使用备用方案');
      console.warn('   错误:', error.message);
      return this.generateFallbackDesign(prd);
    }
  }
  
  /**
   * 备用设计系统生成（当 ui-ux-pro-max 不可用时）
   */
  generateFallbackDesign(prd) {
    const content = prd.content || '';

    let primaryColor = '#1890FF';
    if (content.includes('金融') || content.includes('养老')) {
      primaryColor = '#1677FF';
    } else if (content.includes('电商')) {
      primaryColor = '#FF6B35';
    }

    return {
      colors: {
        primary: primaryColor,
        success: '#52C41A',
        warning: '#FAAD14',
        error: '#F5222D',
        neutral: ['#000000', '#595959', '#8C8C8C', '#BFBFBF', '#D9D9D9', '#F0F0F0', '#FAFAFA']
      },
      typography: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial',
        fontSizes: [12, 14, 16, 18, 20, 24, 30, 36, 48],
        lineHeights: [1.5, 1.6, 1.8]
      },
      spacing: {
        unit: 8,
        scale: [0, 4, 8, 12, 16, 24, 32, 48, 64, 80, 96]
      },
      components: {
        button: {
          height: 32,
          padding: '0 16px',
          borderRadius: 4
        },
        input: {
          height: 32,
          padding: '4px 11px',
          borderRadius: 4
        }
      }
    };
  }

  /**
   * 解析 markdown 输出（ui-ux-pro-max 输出格式）
   */
  parseMarkdownOutput(markdown) {
    // 简化实现：从 markdown 中提取设计系统信息
    const colors = {
      primary: '#1890FF',
      success: '#52C41A',
      warning: '#FAAD14',
      error: '#F5222D'
    };

    // 尝试提取颜色
    const colorMatch = markdown.match(/#[0-9A-Fa-f]{6}/g);
    if (colorMatch && colorMatch.length > 0) {
      colors.primary = colorMatch[0];
    }

    return {
      colors: colors,
      typography: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        fontSizes: [12, 14, 16, 18, 20, 24, 30, 36]
      },
      spacing: {
        unit: 8,
        scale: [0, 4, 8, 12, 16, 24, 32, 48]
      },
      raw: markdown.substring(0, 500)
    };
  }

  /**
   * 从 PRD 提取产品类型
   */
  extractProductType(content) {
    if (content.includes('金融') || content.includes('养老') || content.includes('理财')) {
      return 'financial';
    }
    if (content.includes('电商') || content.includes('购物')) {
      return 'ecommerce';
    }
    if (content.includes('社交') || content.includes('社区')) {
      return 'social';
    }
    return 'default';
  }

  /**
   * 从 PRD 提取产品名称
   */
  extractProductName(content) {
    const match = content.match(/^#\s+(.+)$/m);
    if (match) {
      return match[1].trim();
    }
    return '产品';
  }

  /**
   * 验证设计系统
   */
  async validateDesign(designResult) {
    const errors = [];
    
    // 检查颜色
    if (!designResult.colors || !designResult.colors.primary) {
      errors.push('缺少主色调');
    }
    
    // 检查字体
    if (!designResult.typography || !designResult.typography.fontFamily) {
      errors.push('缺少字体配置');
    }
    
    // 检查间距
    if (!designResult.spacing || !designResult.spacing.unit) {
      errors.push('缺少间距单位');
    }
    
    return {
      passed: errors.length === 0,
      errors: errors,
      tokensComplete: errors.length === 0
    };
  }
}

module.exports = DesignModule;
