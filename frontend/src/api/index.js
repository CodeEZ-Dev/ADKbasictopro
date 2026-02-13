import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const analysisAPI = {
  analyzeText: (content) => 
    api.post('/analyze/text', { content }, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  
  analyzeMarkdown: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/analyze/markdown', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  
  analyzePDF: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/analyze/pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  
  getAnalysis: (id) => api.get(`/analysis/${id}`),
  
  listAnalyses: (skip = 0, limit = 20) => 
    api.get('/analyses', { params: { skip, limit } }),
  
  deleteAnalysis: (id) => api.delete(`/analysis/${id}`),
};

export const templateAPI = {
  generateFromJIRA: (ticketId, userContext = '', useAPI = false) => {
    const formData = new FormData();
    formData.append('jira_ticket_id', ticketId);
    formData.append('user_context', userContext);
    formData.append('use_api', useAPI);
    return api.post('/templates/generate-from-jira', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  
  getTemplate: (id) => api.get(`/templates/${id}`),
  
  listTemplates: (skip = 0, limit = 20) => 
    api.get('/templates', { params: { skip, limit } }),
  
  updateTemplate: (id, content, status = 'draft') => {
    const formData = new FormData();
    formData.append('content', content);
    formData.append('status', status);
    return api.put(`/templates/${id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  
  deleteTemplate: (id) => api.delete(`/templates/${id}`),
};

export const jiraAPI = {
  getIssue: (issueKey) => api.get(`/jira/issues/${issueKey}`),
  
  listCachedIssues: (skip = 0, limit = 20) => 
    api.get('/jira/issues/cached', { params: { skip, limit } }),
  
  testConnection: () => api.post('/jira/test-connection'),
  
  checkConfig: () => api.get('/jira/config-status'),
};

export default api;
