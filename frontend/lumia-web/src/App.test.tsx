import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { App } from './App';
import { fetchContent } from './api';

describe('App', () => {
  it('renders the catalog', async () => {
    render(<App loadContent={() => Promise.resolve([{ id: '1', title: 'Movie' }])} />);
    expect(await screen.findByText('Movie')).toBeInTheDocument();
  });

  it('renders an empty state', async () => {
    render(<App loadContent={() => Promise.resolve([])} />);
    expect(await screen.findByText('No hay contenido disponible.')).toBeInTheDocument();
  });

  it('renders an accessible error', async () => {
    render(<App loadContent={() => Promise.reject(new Error('boom'))} />);
    expect(await screen.findByRole('alert')).toHaveTextContent('No se pudo cargar');
  });
});

describe('fetchContent', () => {
  it('returns the parsed items', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue({ ok: true, json: () => Promise.resolve([{ id: '1', title: 'A' }]) }),
    );
    await expect(fetchContent()).resolves.toEqual([{ id: '1', title: 'A' }]);
  });

  it('throws on a failed response', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 500 }));
    await expect(fetchContent()).rejects.toThrow('Unexpected status 500');
  });
});
