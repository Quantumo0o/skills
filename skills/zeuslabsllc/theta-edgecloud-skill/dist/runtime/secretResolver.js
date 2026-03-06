export async function resolveThetaOnDemandToken(ctx, baseToken) {
    const env = ctx.env ?? {};
    if (ctx.getSecret) {
        try {
            const secret = await ctx.getSecret('THETA_ONDEMAND_API_TOKEN');
            if (secret && secret.trim())
                return secret.trim();
        }
        catch {
            // Intentionally swallow provider errors; continue chain.
        }
    }
    const envToken = env.THETA_ONDEMAND_API_TOKEN;
    if (envToken && envToken.trim())
        return envToken.trim();
    if (baseToken && baseToken.trim())
        return baseToken.trim();
    return undefined;
}
