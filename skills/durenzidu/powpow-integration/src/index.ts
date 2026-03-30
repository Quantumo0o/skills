// PowPow Integration Test Skill - 2.1.3 (Independent implementation)
// In-memory mock version for OpenClaw powpow-integration test purposes.
// This file provides a self-contained surface similar to the real skill,
// so you can compare behaviors without hitting real network APIs.

// Minimal surface import
import { Skill, SkillContext } from '@openclaw/core';

type DH = {
  id: string;
  name: string;
  description?: string;
  lat?: number;
  lng?: number;
  locationName?: string;
  expiresAt?: string;
};

type User = {
  userId: string;
  badges: number;
  currentDhs: DH[];
  lastActive: number;
};

const globalUsers = new Map<string, User>();

export class PowpowIntegrationTest3 implements Skill {
  name = 'powpow-integration-2-1-3';
  description = 'Independent test skill for PowPow integration (OpenClaw)';
  version = '2.1.3';

  capabilities = [
    {
      name: 'register',
      description: 'Register a new PowPow account',
      parameters: { username: { type: 'string', required: true } },
      handler: this.handleRegister.bind(this),
    },
    {
      name: 'login',
      description: 'Login to an existing PowPow account',
      parameters: { username: { type: 'string', required: true } },
      handler: this.handleLogin.bind(this),
    },
    {
      name: 'createDigitalHuman',
      description: 'Create a digital human on PowPow map (in-memory)',
      parameters: {
        name: { type: 'string', required: true },
        description: { type: 'string', required: true }
      },
      handler: this.handleCreateDigitalHuman.bind(this),
    },
    {
      name: 'listDigitalHumans',
      description: 'List all digital humans',
      parameters: {},
      handler: this.handleListDigitalHumans.bind(this),
    },
    {
      name: 'chat',
      description: 'Chat with a digital human',
      parameters: { dhId: { type: 'string', required: true }, message: { type: 'string', required: true } },
      handler: this.handleChat.bind(this),
    },
    {
      name: 'renew',
      description: 'Renew a digital human (in-memory)',
      parameters: { dhId: { type: 'string', required: true } },
      handler: this.handleRenew.bind(this),
    },
    {
      name: 'checkBadges',
      description: 'Check badge balance',
      parameters: {},
      handler: this.handleCheckBadges.bind(this),
    },
    {
      name: 'help',
      description: 'Show available commands',
      parameters: {},
      handler: this.handleHelp.bind(this),
    }
  ];

  private currentUserId = 'test-user';

  async initialize(context: SkillContext): Promise<void> {
    // initialize an empty user for test purposes
    if (!globalUsers.has(this.currentUserId)) {
      globalUsers.set(this.currentUserId, { userId: this.currentUserId, badges: 3, currentDhs: [], lastActive: Date.now() });
    }
  }

  private requireLogin(ctx: SkillContext): boolean {
    // simple check for test environment
    return globalUsers.has(this.currentUserId);
  }

  // Handlers
  private async handleRegister(params: { username: string }, context: SkillContext): Promise<string> {
    const user = globalUsers.get(this.currentUserId) ?? { userId: this.currentUserId, badges: 3, currentDhs: [], lastActive: Date.now() } as User;
    user.badges = 3;
    globalUsers.set(this.currentUserId, user);
    return `✅ Test: registered user ${params.username} with ID ${this.currentUserId}`;
  }
  private async handleLogin(params: { username: string }, context: SkillContext): Promise<string> {
    const user = globalUsers.get(this.currentUserId);
    if (!user) return '❌ Test: user not found';
    return `✅ Test: logged in as ${params.username}`;
  }
  private async handleCreateDigitalHuman(params: { name: string; description: string }, context: SkillContext): Promise<string> {
    const user = globalUsers.get(this.currentUserId);
    if (!user || user.badges < 2) return '❌ Test: not enough badges';
    const dh: DH = { id: `dh_${Date.now()}`, name: params.name, description: params.description, expiresAt: new Date(Date.now() + 30*24*60*60*1000).toISOString() };
    user.currentDhs.push(dh);
    user.badges -= 2;
    return `✅ Created DH ${dh.name} (${dh.id})`;
  }
  private async handleListDigitalHumans(params: any, context: SkillContext): Promise<string> {
    const user = globalUsers.get(this.currentUserId);
    const list = user?.currentDhs ?? [];
    if (list.length === 0) return '没有数字人';
    return '数字人列表:\n' + list.map((d, i) => `  ${i+1}. ${d.name} (${d.id})`).join('\n');
  }
  private async handleChat(params: { dhId: string; message: string }, context: SkillContext): Promise<string> {
    return `测试对话: 收到 ${params.message} 给数字人 ${params.dhId}`;
  }
  private async handleRenew(params: { dhId: string }, context: SkillContext): Promise<string> {
    const user = globalUsers.get(this.currentUserId);
    if (!user) return '未登录';
    user.badges += 1;
    return `续期成功，现在徽章: ${user.badges}`;
  }
  private async handleCheckBadges(params: any, context: SkillContext): Promise<string> {
    const user = globalUsers.get(this.currentUserId);
    return `徽章余额: ${user?.badges ?? 0}`;
  }
  private async handleHelp(params: any, context: SkillContext): Promise<string> {
    return 'Test help: register, login, createDigitalHuman, listDigitalHumans, chat, renew, checkBadges, help';
  }
}

export default PowpowIntegrationTest3;
