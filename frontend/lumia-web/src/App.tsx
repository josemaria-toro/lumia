import { useEffect, useState } from 'react';
import { fetchContent, type ContentItem, type ContentLoader } from './api';

interface AppProps {
  loadContent?: ContentLoader;
}

export function App({ loadContent = fetchContent }: AppProps) {
  const [items, setItems] = useState<ContentItem[] | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    loadContent(controller.signal)
      .then(setItems)
      .catch(() => {
        if (!controller.signal.aborted) setFailed(true);
      });
    return () => controller.abort();
  }, [loadContent]);

  return (
    <main>
      <h1>Lumia</h1>
      <section aria-labelledby="catalog-title">
        <h2 id="catalog-title">Catálogo</h2>
        {failed && <p role="alert">No se pudo cargar el catálogo.</p>}
        {!failed && items === null && <p role="status">Cargando…</p>}
        {items?.length === 0 && <p>No hay contenido disponible.</p>}
        {items && items.length > 0 && (
          <ul className="catalog">
            {items.map((item) => (
              <li key={item.id}>{item.title}</li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
