/**
 * AI律师团队协作全球标准技能包 - 统一入口文件
 * 提供统一的技能访问接口
 */

const StandardAssessmentSystem = require('./standard-assessment/evaluate.js');
const StandardImplementationNavigator = require('./standard-implementation/navigation.js');
const TrainingCourseGenerator = require('./training-generator/course-generator.js');
const ComplianceChecker = require('./compliance-checker/compliance-checker.js');
const ROICalculator = require('./roi-calculator/roi-calculator.js');

class StandardSkillsPackage {
    constructor() {
        this.version = 'v1.0.0';
        this.standardVersion = 'v1.8';
        this.assessmentSystem = new StandardAssessmentSystem();
        this.implementationNavigator = new StandardImplementationNavigator();
        this.trainingGenerator = new TrainingCourseGenerator();
        this.complianceChecker = new ComplianceChecker();
        this.roiCalculator = new ROICalculator();
    }

    /**
     * 评估用户的适配度
     */
    async assessUser(answers, userInfo) {
        try {
            const report = await this.assessmentSystem.generateReport(answers, userInfo);
            return {
                success: true,
                report: report
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 生成实施计划
     */
    generateImplementationPlan(userType, customizations) {
        try {
            const plan = this.implementationNavigator.generateImplementationPlan(
                userType,
                customizations
            );
            return {
                success: true,
                plan: plan
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 导出评估报告
     */
    exportReport(report, format = 'json') {
        switch (format.toLowerCase()) {
            case 'json':
                return this.assessmentSystem.exportToJSON(report);
            case 'markdown':
                return this.assessmentSystem.exportToMarkdown(report);
            default:
                return this.assessmentSystem.exportToJSON(report);
        }
    }

    /**
     * 导出实施计划
     */
    exportPlan(plan, format = 'json') {
        switch (format.toLowerCase()) {
            case 'json':
                return this.implementationNavigator.exportToJSON(plan);
            case 'markdown':
                return this.implementationNavigator.exportToMarkdown(plan);
            default:
                return this.implementationNavigator.exportToJSON(plan);
        }
    }

    /**
     * 快速评估（简化版）
     */
    async quickAssess(userInfo) {
        const simplifiedAnswers = {
            q1: userInfo.size || '<10人',
            q2: ['民事诉讼', '企业法务'],
            q3: '基础办公软件',
            q4: '未开始',
            q5: '了解基本概念',
            d1: '<100条',
            d2: '无标准化',
            d3: '从不',
            d4: ['案例分析统计'],
            d5: '偶尔需要',
            c1: '成本控制',
            c2: ['降低成本', '提升效率'],
            c3: '10-50万',
            c4: '3-6个月',
            c5: '支持'
        };

        return await this.assessUser(simplifiedAnswers, userInfo);
    }

    /**
     * 检查合规性
     */
    async checkCompliance(systemInfo, checkOptions) {
        try {
            const result = await this.complianceChecker.checkCompliance(systemInfo, checkOptions);
            return {
                success: true,
                result: result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 计算ROI
     */
    async calculateROI(userData, implementationCost, timeFrame) {
        try {
            const result = await this.roiCalculator.calculateROI(userData, implementationCost, timeFrame);
            return {
                success: true,
                result: result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 生成培训课程
     */
    generateTrainingCourse(assessmentResult, targetType) {
        try {
            const course = this.trainingGenerator.generateTrainingPackage(assessmentResult, targetType);
            return {
                success: true,
                course: course
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 获取技能包信息
     */
    getInfo() {
        return {
            version: this.version,
            standardVersion: this.standardVersion,
            skills: [
                {
                    name: '标准自动化评估系统',
                    version: '1.0.0',
                    status: '✅ 已开发',
                    file: 'skills/standard-assessment/evaluate.js',
                    features: [
                        '25个专业评估问题',
                        '5个评估维度',
                        '智能评分算法',
                        '优化建议',
                        '多格式输出'
                    ]
                },
                {
                    name: '标准实施导航系统',
                    version: '1.0.0',
                    status: '✅ 已开发',
                    file: 'skills/standard-implementation/navigation.js',
                    features: [
                        '3种组织类型支持',
                        '5个完整阶段',
                        '16-20个任务分解',
                        '风险管理',
                        '进度跟踪'
                    ]
                },
                {
                    name: '标准培训自动化生成器',
                    version: '1.0.0',
                    status: '✅ 已开发',
                    file: 'skills/training-generator/course-generator.js',
                    features: [
                        '3种培训课程',
                        'PPT大纲生成',
                        '练习题库',
                        '证书模板'
                    ]
                },
                {
                    name: '标准合规检查器',
                    version: '1.0.0',
                    status: '✅ 已开发',
                    file: 'skills/compliance-checker/compliance-checker.js',
                    features: [
                        '20+合规检查项',
                        '3个法律框架',
                        'GDPR支持',
                        '自动报告'
                    ]
                },
                {
                    name: '标准ROI计算器',
                    version: '1.0.0',
                    status: '✅ 已开发',
                    file: 'skills/roi-calculator/roi-calculator.js',
                    features: [
                        '3种律所基准',
                        'ROI计算',
                        '回本期分析',
                        '12个月预测',
                        '图表数据'
                    ]
                }
            ],
            totalSkills: 5,
            completedSkills: 5,
            pendingSkills: 0
        };
    }
}

// 导出技能包
module.exports = StandardSkillsPackage;

// 如果直接运行，显示技能包信息
if (require.main === module) {
    const skillsPackage = new StandardSkillsPackage();
    console.log('\n=== AI律师标准技能包 ===');
    console.log(JSON.stringify(skillsPackage.getInfo(), null, 2));
    console.log('\n快速测试：\n');
    skillsPackage.quickAssess({
        name: '测试律所',
        organization: 'XX律师事务所',
        industry: '法律服务',
        size: '小型律所（<10人）'
    }).then(result => {
        if (result.success) {
            console.log('\n评估结果：');
            console.log('综合评分：', result.report.assessment.overall.score + '分');
            console.log('适配等级：', result.report.assessment.overall.adaptationLevel.level);
        } else {
            console.error('评估失败：', result.error);
        }
    });
}
