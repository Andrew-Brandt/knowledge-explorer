import {
    QueryClient,
  } from '@tanstack/react-query';
  import {
    persistQueryClient,
  } from '@tanstack/react-query-persist-client';
  import {
    createSyncStoragePersister,
  } from '@tanstack/query-sync-storage-persister';
  
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: 1,
        refetchOnWindowFocus: false,
        staleTime: 1000 * 60 * 60 * 24, // 24 hours
      },
    },
  });
  
  const localStoragePersister = createSyncStoragePersister({
    storage: window.localStorage,
  });
  
  persistQueryClient({
    queryClient,
    persister: localStoragePersister,
  });
  
  export default queryClient;
  