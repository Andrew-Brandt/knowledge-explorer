import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export const useSummary = (topic, level = 'basic', options = {}) =>
  useQuery({
    queryKey: ['summary', topic, level],
    queryFn: async () => {
      const { data } = await axios.get(`http://localhost:5000/summary/${topic}?level=${level}`);
      return data.summary;
    },
    enabled: !!topic,
    ...options,
  });
