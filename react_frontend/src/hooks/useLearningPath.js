import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export const useLearningPath = (topic, level = 'basic') =>
  useQuery({
    queryKey: ['learningPath', topic, level],
    queryFn: async () => {
      const { data } = await axios.get(`http://localhost:5000/learning-path/${topic}?level=${level}`);
      

      return {
        links: data.links || [],
        summary: data.summary || "No summary available.",
        topic: data.topic || topic, // fallback to original search if topic is missing
      };
    },
    enabled: !!topic,
  });
