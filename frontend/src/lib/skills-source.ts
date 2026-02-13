export const normalizeRepoSourceUrl = (sourceUrl: string): string => {
  const trimmed = sourceUrl.trim().replace(/\/+$/, "");
  return trimmed.endsWith(".git") ? trimmed.slice(0, -4) : trimmed;
};

export const repoBaseFromSkillSourceUrl = (skillSourceUrl: string): string | null => {
  try {
    const parsed = new URL(skillSourceUrl);
    const marker = "/tree/";
    const markerIndex = parsed.pathname.indexOf(marker);
    if (markerIndex <= 0) return null;

    // Reject unexpected structures (e.g. multiple /tree/ markers).
    if (parsed.pathname.indexOf(marker, markerIndex + marker.length) !== -1) return null;

    const repoPath = parsed.pathname.slice(0, markerIndex);
    if (!repoPath || repoPath === "/") return null;
    if (repoPath.endsWith("/tree")) return null;

    return normalizeRepoSourceUrl(`${parsed.origin}${repoPath}`);
  } catch {
    return null;
  }
};

export const packUrlFromSkillSourceUrl = (skillSourceUrl: string): string => {
  const repoBase = repoBaseFromSkillSourceUrl(skillSourceUrl);
  return repoBase ?? skillSourceUrl;
};

export const packLabelFromUrl = (packUrl: string): string => {
  try {
    const parsed = new URL(packUrl);
    const segments = parsed.pathname.split("/").filter(Boolean);
    if (segments.length >= 2) {
      return `${segments[0]}/${segments[1]}`;
    }
    return parsed.host;
  } catch {
    return "Open pack";
  }
};

export const packsHrefFromPackUrl = (packUrl: string): string => {
  const params = new URLSearchParams({ source_url: packUrl });
  return `/skills/packs?${params.toString()}`;
};
