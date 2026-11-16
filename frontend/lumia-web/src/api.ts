export interface ContentItem {
  id: string;
  title: string;
}

export type ContentLoader = (signal?: AbortSignal) => Promise<ContentItem[]>;

export const fetchContent: ContentLoader = async (signal) => {
  const response = await fetch('/api/v1/content', { signal });
  if (!response.ok) {
    throw new Error(`Unexpected status ${response.status}`);
  }
  return (await response.json()) as ContentItem[];
};
