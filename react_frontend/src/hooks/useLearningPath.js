import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export const useLearningPath = (topic, level = 'basic') =>
  useQuery({
    queryKey: ['learningPath', topic, level],
    queryFn: async () => {
      const { data } = await axios.get(`/learning-path/${topic}?level=${level}`);
      return {
        links: data.links || [],
        summary: data.summary || "No summary available.",
        topic: data.topic || topic,
      };
    },
    enabled: !!topic,
  });

