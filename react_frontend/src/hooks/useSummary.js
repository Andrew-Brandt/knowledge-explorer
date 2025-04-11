import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export const useSummary = (topic, level = 'basic', options = {}) =>
  useQuery({
    queryKey: ['summary', topic, level],
    queryFn: async () => {
      const { data } = await axios.get(`/summary/${topic}?level=${level}`);
      return data.summary;
    },
    enabled: !!topic,
    ...options,
  });

