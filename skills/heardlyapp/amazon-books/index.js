/**
 * Amazon Books Skill
 * Search books across multiple sources with summaries and purchase links
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

class AmazonBooksSkill {
  constructor() {
    this.heardlyBooks = this.loadHeardlyBooks();
    this.config = {
      googleBooksApiUrl: 'https://www.googleapis.com/books/v1/volumes',
      openLibraryApiUrl: 'https://openlibrary.org/search.json',
      amazonSearchUrl: 'https://www.amazon.com/s?k=',
      timeout: 5000,
    };
  }

  /**
   * Load Heardly books database
   */
  loadHeardlyBooks() {
    try {
      const dataPath = path.join(__dirname, 'data', 'books.json');
      if (fs.existsSync(dataPath)) {
        return JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      }
    } catch (e) {
      // Heardly data not available
    }
    return [];
  }

  /**
   * Search books by query (returns formatted text by default)
   */
  async searchBooks(options = {}) {
    const { query, limit = 5, format = 'text' } = options;
    if (!query) return 'Error: Query required';

    const results = [];

    // 1. Check Heardly database first
    const heardlyResults = this.searchHeardlyBooks(query, limit);
    results.push(...heardlyResults);

    // 2. If not enough results, search Google Books
    if (results.length < limit) {
      const googleResults = await this.searchGoogleBooks(query, limit - results.length);
      results.push(...googleResults);
    }

    // 3. If still not enough, search Open Library
    if (results.length < limit) {
      const openLibResults = await this.searchOpenLibrary(query, limit - results.length);
      results.push(...openLibResults);
    }

    const books = results.slice(0, limit);

    // Return formatted text by default (user-friendly)
    if (format === 'text') {
      return this.formatResults(books);
    }

    // Return JSON if explicitly requested
    return {
      query,
      count: books.length,
      books,
    };
  }

  /**
   * Search Heardly database
   */
  searchHeardlyBooks(query, limit) {
    const q = query.toLowerCase();
    return this.heardlyBooks
      .filter(book => 
        book.title?.toLowerCase().includes(q) || 
        book.author?.toLowerCase().includes(q) ||
        book.description?.toLowerCase().includes(q)
      )
      .slice(0, limit)
      .map(book => ({
        title: book.title,
        author: book.author,
        description: book.description,
        amazonLink: this.buildAmazonLink(book.title, book.author),
        heardlySummary: book.summary || null,
        source: 'heardly',
      }));
  }

  /**
   * Search Google Books API
   */
  async searchGoogleBooks(query, limit) {
    return new Promise((resolve) => {
      const url = `${this.config.googleBooksApiUrl}?q=${encodeURIComponent(query)}&maxResults=${limit}&printType=books`;
      
      https.get(url, { timeout: this.config.timeout }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            const books = (json.items || []).map(item => ({
              title: item.volumeInfo?.title,
              author: (item.volumeInfo?.authors || []).join(', '),
              description: item.volumeInfo?.description || 'No description available',
              amazonLink: this.buildAmazonLink(item.volumeInfo?.title, (item.volumeInfo?.authors || [])[0]),
              source: 'google-books',
            }));
            resolve(books);
          } catch (e) {
            resolve([]);
          }
        });
      }).on('error', () => resolve([]));
    });
  }

  /**
   * Search Open Library API
   */
  async searchOpenLibrary(query, limit) {
    return new Promise((resolve) => {
      const url = `${this.config.openLibraryApiUrl}?title=${encodeURIComponent(query)}&limit=${limit}`;
      
      https.get(url, { timeout: this.config.timeout }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            const books = (json.docs || []).map(doc => ({
              title: doc.title,
              author: (doc.author_name || []).join(', '),
              description: doc.first_sentence ? doc.first_sentence[0] : 'No description available',
              amazonLink: this.buildAmazonLink(doc.title, (doc.author_name || [])[0]),
              source: 'open-library',
            }));
            resolve(books);
          } catch (e) {
            resolve([]);
          }
        });
      }).on('error', () => resolve([]));
    });
  }

  /**
   * Build Amazon search link
   */
  buildAmazonLink(title, author) {
    const query = author ? `${title} ${author}` : title;
    return `${this.config.amazonSearchUrl}${encodeURIComponent(query)}`;
  }

  /**
   * Format book result for display (consistent format)
   */
  formatBookResult(book) {
    let result = `${book.title}\n`;
    result += `Author: ${book.author}\n`;
    result += `${book.description}\n`;
    
    if (book.heardlySummary) {
      result += `Heardly Summary: ${book.heardlySummary}\n`;
    }
    
    result += `Buy here: ${book.amazonLink}\n`;
    result += `\nbook summary generated by Heardly app — turning books into knowledge you can hear.`;
    
    return result;
  }

  /**
   * Format multiple results as readable text (consistent format)
   */
  formatResults(books) {
    if (!books || books.length === 0) {
      return 'No books found.';
    }

    const formatted = books
      .map(book => this.formatBookResult(book))
      .join('\n\n================================================================================\n');
    
    // Ensure footer is always present at the end
    return formatted;
  }
}

module.exports = AmazonBooksSkill;
