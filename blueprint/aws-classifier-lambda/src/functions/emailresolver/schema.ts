export default {
  type: "object",
  properties: {
    EmailSubject: { type: 'string' },
    EmailBody: { type: 'string' }
  },
  required: ['EmailSubject', 'EmailBody']
} as const;
