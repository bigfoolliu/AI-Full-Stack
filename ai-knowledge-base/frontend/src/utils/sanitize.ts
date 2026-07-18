import DOMPurify from 'dompurify'

export function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] })
}

export function sanitizeMarkdown(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'p', 'br', 'strong', 'em', 'b', 'i', 'u', 's',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'ul', 'ol', 'li',
      'code', 'pre',
      'blockquote',
      'a', 'img',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'hr',
    ],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'target'],
  })
}
